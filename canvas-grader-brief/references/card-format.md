# Rendering workflow

## Setup for visual cards

Use Python 3.10+ and install the pinned drawing dependency once:

```bash
python3 -m venv ~/.local/share/venvs/canvas-grader-brief
~/.local/share/venvs/canvas-grader-brief/bin/pip install Pillow==12.0.0
```

From this Skill's folder, try the offline renderer:

```bash
~/.local/share/venvs/canvas-grader-brief/bin/python scripts/render_card.py --sample
```

This reads assets/sample-card.json and creates a separately named fictional sample image. Never present it as real Canvas data. No student state is changed. If setup fails, explain the failure and offer a concise text or document brief rather than claiming an image was sent.

## Visual cards

Default to a PNG image card plus a short plain-text caption for assignment/grading briefs. If the user asks for text only, honor that. This is a generated image attachment, not a native interactive iMessage extension or guaranteed rich-link preview. Use the current conversation's supported file/image delivery ability. If PNG delivery is unavailable, offer a document or plain-text fallback and explain that no image was delivered.

1. Fetch verified data first using the preceding access and scope rules. The script cannot call Cubbie's Canvas, browser, or memory abilities. Never use the bundled fictional example to fill gaps in a real report. A polished card does not prove a sync or permission issue was resolved.
2. Include assignment title, course, student submission deadline in the user's time zone, points possible (assignment's maximum marks), and available needs-grading count. Do not display an individual student's grade. If the user means earned marks, ask whose results and clarify the separate scope. Label assignment-group weight separately; a group worth 10% does not prove an assignment has 10 possible points or individually counts for 10% of the course.
3. Use a submission progress bar only for a verified distinct-student submission count and matching eligible-student denominator, with the same scope and units. A pie chart is inappropriate without a verified whole and disjoint categories. Leave student counts null for group-only statistics, unknown totals, or ambiguous graded/ungraded buckets. No progress chart is drawn for unavailable or zero denominators. Zero verified submissions with a positive denominator shows a genuine 0% bar.
4. Use the JSON schema below. Write only aggregate verified fields to a JSON file under ~/.config/canvas-grader-brief/; keep raw student records and credentials out. Supply source, actual checked-at timestamp with offset, user's IANA time zone, a concise scope/coverage note, and sorted assignments. For multiple deadlines, set due_status to multiple and explain section dates in the accompanying caption or document. Do not generate an urgent/overdue badge based on a student deadline and imply a grading deadline has passed.
5. Run from this Skill's folder:

```bash
~/.local/share/venvs/canvas-grader-brief/bin/python scripts/render_card.py --input ~/.config/canvas-grader-brief/brief.json
```

6. Read the printed image paths and send the actual generated files to this user. Do not send a local filesystem path as if it were an accessible attachment. There are at most three assignment blocks per image, with additional images numbered automatically. For long reports, offer a document instead of flooding the thread. Rendered titles/source notes may be shortened to fit; preserve full assignment names, section variants, links, and material coverage limits in the caption or document. Links printed inside an image are not tappable; send original authorized Canvas links separately on their own lines.
7. On exit code 1, report the validation/rendering error and correct the source fields or provide a text fallback. Never replace unknown counts with zeros to make rendering succeed. Sample mode is only for an explicitly requested demonstration and is prominently labeled fictional.

## Text fallback example

Example format only; the following numbers are fictional:

CS 201 — Lab 4
Due: Nov 6, 11:59 pm MST
Students submitted: 38 of 45
Needs grading: 12

# Visual card input

Run scripts/render_card.py from the Skill folder. Python 3.10+ and Pillow==12.0.0 are required. The renderer reads local JSON, draws PNGs, and prints a JSON list of absolute image paths. It makes no requests, reads no credentials, and never fetches Canvas itself.

## Required report fields

- `source`: truthful source label, such as `Canvas browser - CSE 579, Section A` or `User-provided snapshot`. Do not label synced or supplied data live unless it was read live.
- `checked_at`: actual check timestamp in ISO format with offset or Z. For a supplied snapshot, this is when it was inspected, not a claim its data was refreshed then; describe snapshot freshness in the coverage note.
- `time_zone`: user's IANA time zone, for example `America/Phoenix`.
- `assignments`: array of 0-30 records. Sort before passing to the renderer. Three records are drawn per image. More than 30 requires a separate report or document.
- Optional `range_label` and `coverage_note`: short strings displayed in the header/footer. Keep important warnings in the caption too, since long strings are shortened to fit.

## Assignment fields

| Field | Meaning |
|---|---|
| `course`, `name` | Required course and assignment names |
| `due_at` | ISO timestamp with UTC offset/Z, or null when unknown/unset |
| `due_status` | `unavailable` (default), `no_due_date` (explicitly unset), or `multiple` (section/student variants; takes precedence over due_at) |
| `grading_due_at` | Optional explicit staff deadline, ISO timestamp with offset/Z; otherwise not specified |
| `points_possible` | Verified assignment maximum points, or null; never a grade earned |
| `assignment_group_weight_pct` | Verified parent group weight, 0-100, or null; not assignment weight or points |
| `students_submitted` | Verified distinct students who actually submitted, or null |
| `eligible_students` | Verified matching assignment/section student denominator, or null |
| `needs_grading` | Source-labeled number needing grading, or null; explain unit/scope in caption |

Counts must be nonnegative whole numbers. Missing counts stay null. Students submitted cannot exceed the denominator. A bar is drawn only with both verified counts and a positive denominator. Group-only counts must not populate student count fields. Do not sum graded/ungraded categories to fabricate actual submissions.

See assets/sample-card.json for a **fictional** example. It is deliberately not real CSE 579 data, despite illustrating that course name. The sample is never a fallback for a real account lookup.

## Commands and output

```bash
~/.local/share/venvs/canvas-grader-brief/bin/python scripts/render_card.py --sample
~/.local/share/venvs/canvas-grader-brief/bin/python scripts/render_card.py --input ~/.config/canvas-grader-brief/brief.json
```

Default real output: `~/.config/canvas-grader-brief/cards/brief.png`. Sample output: `~/.config/canvas-grader-brief/cards/sample.png`. Additional pages have a numeric suffix. Use `--output /absolute/path/report.png` to choose another location. Parent directories are created. Explicit output files may be replaced; do not choose an input path or a path containing unrelated work.

Exit 0 prints `{"images": ["/absolute/path/brief.png"], "sample": false}`. Exit 1 reports a data/file/rendering error. Argument errors use exit 2. No user state except the requested image artifacts is saved. Dates are converted before drawing, using the supplied time zone rather than the sandbox clock.

## To Do text example

Example reply format using fictional data:

CS 201 — Lab 4
To Do: Grade 12 submissions
Student submissions due: Nov 1, 2026, 11:59 pm MST
Grading deadline: Not specified

