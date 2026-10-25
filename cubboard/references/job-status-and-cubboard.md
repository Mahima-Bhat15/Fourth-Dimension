# Job status labels, the jobs workbook and Cubboard sync

Read this for every request about the student's job applications ("my applications", "job applications",
"summary of my jobs", "application status", "check my Gmail for jobs"). It adds three things to every such
answer: a status for each job, the jobs workbook, and the Cubboard link.

## Status labels

Use the latest hiring stage from the reconciled ledger (`pipeline.py brief` / `export`, after the Gmail scan),
never a guess. Map it exactly:

| Ledger status | Show the student | In the workbook |
| --- | --- | --- |
| `applied` (or only notes / follow-ups since) | Applied | Applied |
| `assessment` | Online assessment | Online assessment |
| `interview` | Interview stage | Interview stage |
| `offer` | Offer | Offer |
| `rejected` | Leave the job out entirely | Leave the row out |
| `withdrawn` | Leave the job out entirely | Leave the row out |

Rejected and withdrawn jobs are skipped "for now": keep them in the private ledger, but do not list, count or
mention them in the answer or the workbook. Apply this by exact company + role (+ requisition when known); a
rejection for one role never hides a different role at the same company. "Online assessment" is the label for
any assessment stage, including take-home tests. A completed assessment with no newer stage stays "Online
assessment" until new mail moves it on. Never upgrade a status without evidence (an invitation to schedule is
"Interview stage"; do not call it a scheduled interview in the text unless a time is confirmed).

## The jobs workbook (every application answer)

Attach a real `.xlsx` with every answer about applications, including the first one in a conversation. Name it
`cubboard-jobs-YYYY-MM-DD.xlsx` using the student's local date; Cubboard looks for this name. Sheets, in order:

1. `Applications`: Company name | Role applied | Status | Date applied
2. `LinkedIn Connections`: Company name | Contact name | LinkedIn profile link | Short outreach message
3. `Assessments`: Company name | Assessment | Deadline (local time and time zone) | Add to Google Calendar link

Keep these sheet names and header texts exactly, with the header in row 1; Cubboard reads them by name.
Status uses only the four labels above. "Date applied" is an ISO date (`2026-10-12`) when verified, otherwise
the text `Not verified`. One row per non-rejected, non-withdrawn application; deduplicate. The other sheets
follow SKILL.md Section 6. Save it under `~/.config/cubbridge/reports/`, inspect it, then attach it with Cubbie's
file-sharing ability in this iMessage conversation. Never claim it was attached without confirmation.

## Cubboard link and sync

End every application answer with this exact line:

`Cubboard: http://127.0.0.1:8787/#student`

It opens the student's Cubboard dashboard on the Mac where Cubboard runs (`pnpm live`); it does not open on a
phone. Syncing happens through the workbook: Cubboard reads new `cubboard-jobs-*.xlsx` files that Cubbie sends
in this conversation and updates its Job hunt board, skipping rejected rows.

- Do **not** send HTTP requests to `127.0.0.1`, `localhost` or any dashboard address. From Cubbie's sandbox,
  `127.0.0.1` is the sandbox itself, not the student's Mac, so a request there cannot reach Cubboard.
- Do not claim the dashboard was updated; Cubbie cannot see it. Say "Cubboard updates from this workbook when
  it's open on your Mac" once, the first time in a conversation.
- If the workbook could not be attached, say so in one line; the dashboard will not update until it arrives.
