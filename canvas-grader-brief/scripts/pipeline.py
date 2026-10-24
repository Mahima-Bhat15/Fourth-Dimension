#!/usr/bin/env python3
"""Private per-student application ledger. No network or provider credentials."""

import argparse
import json
import os
import sqlite3
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import urlsplit

STATUSES = {
    "applied",
    "assessment",
    "interview",
    "offer",
    "rejected",
    "withdrawn",
    "follow_up_sent",
    "note",
}
CLOSED = {"rejected", "withdrawn"}


def timestamp(value):
    if not isinstance(value, str):
        raise ValueError("Timestamps must be ISO 8601 strings with a UTC offset")
    try:
        result = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        raise ValueError("Invalid ISO 8601 timestamp") from None
    if result.tzinfo is None:
        raise ValueError("Timestamps need a UTC offset; confirm the student time zone")
    return result.astimezone(timezone.utc)


def text(record, key, required=True, maximum=1000):
    value = record.get(key)
    if value is None and not required:
        return None
    if not isinstance(value, str) or not value.strip() or len(value) > maximum:
        raise ValueError(f"{key} must be nonempty text, at most {maximum} characters")
    return value.strip()


def validate(record):
    if not isinstance(record, dict):
        raise ValueError("Each message must be an object")
    allowed = {
        "message_id",
        "application_key",
        "company",
        "role",
        "status",
        "received_at",
        "source_url",
        "evidence",
        "deadline_at",
        "deadline_text",
        "relative_hours",
        "deadline_confirmed",
    }
    if set(record) - allowed:
        raise ValueError("Unknown message fields; use the documented schema")
    result = {
        key: text(record, key, maximum=200 if key != "evidence" else 1000)
        for key in ("message_id", "application_key", "company", "role", "status", "evidence")
    }
    if result["status"] not in STATUSES:
        raise ValueError("Unsupported application status")
    result["received_at"] = timestamp(record.get("received_at")).isoformat()
    source = text(record, "source_url", required=False, maximum=2000)
    if source:
        url = urlsplit(source)
        if url.scheme != "https" or not url.hostname or url.username or url.password:
            raise ValueError("source_url must be an HTTPS evidence link")
    result["source_url"] = source
    result["deadline_text"] = text(record, "deadline_text", required=False)
    result["deadline_at"] = None
    explicit = record.get("deadline_at")
    hours = record.get("relative_hours")
    if explicit is not None and hours is not None:
        raise ValueError("Use deadline_at or relative_hours, not both")
    if "deadline_confirmed" in record and not isinstance(record["deadline_confirmed"], bool):
        raise ValueError("deadline_confirmed must be a boolean")
    if explicit is not None or hours is not None:
        if not result["deadline_text"] or record.get("deadline_confirmed") is not True:
            raise ValueError(
                "A calculated deadline needs quoted evidence and confirmed interpretation"
            )
        if explicit is not None:
            due = timestamp(explicit)
        else:
            if (
                isinstance(hours, bool)
                or not isinstance(hours, (int, float))
                or not 0 < hours <= 8760
            ):
                raise ValueError("relative_hours must be greater than zero and at most 8760")
            due = timestamp(result["received_at"]) + timedelta(hours=hours)
        result["deadline_at"] = due.isoformat()
    return result


def connect(path):
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    # Exclusive creation avoids replacing an existing ledger or changing unrelated directories.
    try:
        fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError:
        pass
    else:
        os.close(fd)
    os.chmod(path, 0o600)
    db = sqlite3.connect(path, timeout=30)
    db.execute(
        "CREATE TABLE IF NOT EXISTS messages "
        "(id TEXT PRIMARY KEY, application_key TEXT NOT NULL, payload TEXT NOT NULL, "
        "completed INTEGER NOT NULL DEFAULT 0)"
    )
    db.execute(
        "CREATE TABLE IF NOT EXISTS resolutions "
        "(message_id TEXT PRIMARY KEY, deadline_at TEXT NOT NULL, deadline_text TEXT NOT NULL)"
    )
    return db


def ingest(db, records):
    if not isinstance(records, list) or len(records) > 2000:
        raise ValueError("messages must be a list with at most 2000 entries")
    # Validate the entire batch before writing anything.
    items = [validate(record) for record in records]
    added = 0
    with db:
        db.execute("BEGIN IMMEDIATE")
        for item in items:
            payload = json.dumps(item, sort_keys=True)
            existing = db.execute(
                "SELECT payload FROM messages WHERE id=?", (item["message_id"],)
            ).fetchone()
            if existing:
                if existing[0] != payload:
                    raise ValueError(
                        "Conflicting message ID; review evidence instead of overwriting"
                    )
                continue
            db.execute(
                "INSERT INTO messages(id,application_key,payload) VALUES (?,?,?)",
                (item["message_id"], item["application_key"], payload),
            )
            added += 1
    return added


def briefing(db, now, follow_up_days=7):
    groups = {}
    resolutions = {
        r[0]: r[1:]
        for r in db.execute("SELECT message_id, deadline_at, deadline_text FROM resolutions")
    }
    for payload, completed in db.execute("SELECT payload,completed FROM messages"):
        event = json.loads(payload)
        event["completed"] = bool(completed)
        if event["message_id"] in resolutions:
            event["deadline_at"], event["deadline_text"] = resolutions[event["message_id"]]
        groups.setdefault(event["application_key"], []).append(event)
    applications, actions = [], []
    for key, events in groups.items():
        events.sort(key=lambda e: (timestamp(e["received_at"]), e["message_id"]))
        stages = [e for e in events if e["status"] not in {"note", "follow_up_sent"}]
        latest = stages[-1] if stages else events[-1]
        last_contact = max(timestamp(e["received_at"]) for e in events)
        application = {
            "application_key": key,
            "company": latest["company"],
            "role": latest["role"],
            "status": latest["status"],
            "last_contact_at": last_contact.isoformat(),
            "evidence": [
                {k: e[k] for k in ("message_id", "source_url", "evidence", "received_at", "status")}
                for e in events
            ],
        }
        applications.append(application)
        if latest["status"] in CLOSED or latest["completed"]:
            continue
        action = None
        due = timestamp(latest["deadline_at"]) if latest["deadline_at"] else None
        ambiguous = latest["deadline_text"] and due is None
        if ambiguous:
            action = (0, "confirm_deadline", "Confirm the deadline before scheduling")
        elif due:
            hours = (due - now).total_seconds() / 3600
            if hours < 0:
                action = (0, "verify_overdue", "Deadline passed; verify availability before acting")
            else:
                action = (1 if hours <= 72 else 3, "deadline", "Complete the requested hiring step")
        elif latest["status"] == "interview":
            action = (2, "reply_interview", "Review the interview invitation and prepare a reply")
        elif latest["status"] == "assessment":
            action = (
                2,
                "review_assessment",
                "Review the assessment instructions and confirm its deadline",
            )
        elif latest["status"] == "offer":
            action = (2, "review_offer", "Review the offer and confirm any response deadline")
        elif latest["status"] == "applied" and now - last_contact >= timedelta(days=follow_up_days):
            action = (
                4,
                "consider_follow_up",
                "Consider a follow-up draft; silence is not a rejection",
            )
        if action:
            priority, kind, instruction = action
            actions.append(
                {
                    "application_key": key,
                    "company": latest["company"],
                    "role": latest["role"],
                    "priority": priority,
                    "kind": kind,
                    "instruction": instruction,
                    "deadline_at": latest["deadline_at"],
                    "deadline_text": latest["deadline_text"],
                    "message_id": latest["message_id"],
                    "source_url": latest["source_url"],
                }
            )
    actions.sort(key=lambda a: (a["priority"], a["deadline_at"] or "9999", a["application_key"]))
    applications.sort(key=lambda a: a["application_key"])
    return {
        "as_of": now.isoformat(),
        "tracked": len(applications),
        "applications": applications,
        "actions": actions,
        "top_three": actions[:3],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "command", choices=["scan", "brief", "complete", "resolve", "export", "delete"]
    )
    parser.add_argument("--input", type=Path)
    parser.add_argument("--now", required=True, help="Student current ISO timestamp with offset")
    parser.add_argument("--follow-up-days", type=int, default=7)
    parser.add_argument("--message-id")
    parser.add_argument("--deadline-at")
    parser.add_argument("--deadline-text")
    parser.add_argument(
        "--sample", action="store_true", help="In-memory demo; never reads saved state"
    )
    parser.add_argument(
        "--yes", action="store_true", help="Confirm deletion of this student ledger"
    )
    args = parser.parse_args()
    db = None
    try:
        now = timestamp(args.now)
        if not 1 <= args.follow_up_days <= 365:
            raise ValueError("follow-up-days must be between 1 and 365")
        if args.sample:
            db = sqlite3.connect(":memory:")
            db.execute(
                "CREATE TABLE messages (id TEXT PRIMARY KEY, application_key TEXT, "
                "payload TEXT, completed INTEGER DEFAULT 0)"
            )
            db.execute(
                "CREATE TABLE resolutions (message_id TEXT PRIMARY KEY, "
                "deadline_at TEXT NOT NULL, deadline_text TEXT NOT NULL)"
            )
            fixture = Path(__file__).resolve().parents[1] / "assets/sample-messages.json"
            ingest(db, json.loads(fixture.read_text())["messages"])
        else:
            path = Path.home() / ".config/cubbridge/pipeline.sqlite3"
            db = connect(path)
        if args.command == "scan":
            if not args.sample:
                if args.input is None or args.input.stat().st_size > 5_000_000:
                    raise ValueError("scan requires --input with a JSON file under 5 MB")
                data = json.loads(args.input.read_text())
                added = ingest(db, data["messages"])
            else:
                added = 0
            output = briefing(db, now, args.follow_up_days)
            output["added"] = added
        elif args.command == "resolve":
            due = timestamp(args.deadline_at).isoformat()
            quote = text({"deadline_text": args.deadline_text}, "deadline_text")
            with db:
                if not db.execute(
                    "SELECT 1 FROM messages WHERE id=?", (args.message_id,)
                ).fetchone():
                    raise ValueError("Message not found")
                db.execute(
                    "INSERT INTO resolutions VALUES (?,?,?) "
                    "ON CONFLICT(message_id) DO UPDATE SET "
                    "deadline_at=excluded.deadline_at, deadline_text=excluded.deadline_text",
                    (args.message_id, due, quote),
                )
            output = {"resolved": args.message_id, "deadline_at": due}
        elif args.command == "complete":
            if not args.message_id:
                raise ValueError("complete needs --message-id after student confirmation")
            with db:
                result = db.execute(
                    "UPDATE messages SET completed=1 WHERE id=?", (args.message_id,)
                )
                if result.rowcount != 1:
                    raise ValueError("Message not found")
            output = {"completed": args.message_id}
        elif args.command == "delete":
            if not args.yes:
                raise ValueError("Show the student what will be deleted and obtain yes first")
            with db:
                db.execute("PRAGMA secure_delete=ON")
                db.execute("DELETE FROM resolutions")
                db.execute("DELETE FROM messages")
            db.execute("VACUUM")
            output = {"deleted": True}
        else:
            output = briefing(db, now, args.follow_up_days)
            if args.command == "export":
                output["records"] = [
                    {"message": json.loads(payload), "completed": bool(completed)}
                    for payload, completed in db.execute("SELECT payload,completed FROM messages")
                ]
                output["deadline_confirmations"] = [
                    {"message_id": mid, "deadline_at": due, "deadline_text": quote}
                    for mid, due, quote in db.execute("SELECT * FROM resolutions")
                ]
        print(json.dumps(output, ensure_ascii=False))
        return 0
    except (ValueError, TypeError, KeyError, OSError, sqlite3.Error, OverflowError):
        # Input may contain private mail. Do not echo payloads or file paths in errors.
        print(
            json.dumps(
                {
                    "error": "Could not process the ledger. Check schema, dates, "
                    "message IDs and command flags; saved records were not replaced."
                }
            ),
            file=sys.stderr,
        )
        return 2
    finally:
        if db is not None:
            db.close()


if __name__ == "__main__":
    sys.exit(main())
