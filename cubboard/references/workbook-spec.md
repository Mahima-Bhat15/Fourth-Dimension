# Cubbridge Excel workbook contract

Deliver a real Excel `.xlsx` attachment for each completed career report/update. Cubbie
creates the workbook with its document abilities; the ledger script supplies JSON and
never claims to generate Excel, research profiles or call Google Calendar itself.

Suggested filename: `Cubbridge_Applications_YYYY-MM-DD_HHMM.xlsx`, using the student's
local time. Save privately outside the replaceable Skill folder. Keep filters, a frozen
header row, readable widths, wrapped message drafts and clearly labeled source links.
Store imported names, email excerpts and drafts as literal text, including text beginning
with `=`, `+`, `-` or `@`; never evaluate it as a spreadsheet formula. No macros.

## Applications — one row per application_key

Required columns:
- Application key
- Company
- Official website
- Company description / industry
- Company research source
- Role applied for
- Requisition ID (if verified)
- Job location (if verified)
- Application date
- Application date evidence / source
- Confirmation received (local date/time, separately labeled)
- Current hiring stage
- Last communication (local date/time)
- Assessment summary
- Next action
- Application evidence link(s)
- Research / verification notes

Actual application dates require explicit source evidence or student confirmation.
Unknown dates are `Unknown — needs confirmation`, not the confirmation-email date.
Conflicting dates remain unknown with the candidates and evidence in notes. Dates with
only a verified day stay date-only. Source timestamps are displayed in the student's
zone. Do not infer job location from employer headquarters. Missing company details
remain `Unavailable`, with a research status.

## LinkedIn Connections — one row per application/contact pair

Required columns:
- Application key, company, role applied for
- Contact name
- Category: Alumni / Recruiter / Alumni and recruiter
- Current title and employer
- Shared school and evidence (for alumni)
- Verified LinkedIn profile URL
- Employment evidence URL
- School / recruiting-role evidence URL
- Verification status and checked-at time
- Personalized connection note
- Personalized follow-up draft
- Outreach status (default `Draft — not sent`)

Verify current employer and shared school/recruiting role independently. A common
school is not a personal relationship. Deduplicate the same person within an application;
reuse the contact for another actual role only with a tailored draft. Record a company
coverage row with blank identity/message fields when research finds no verified match.
Label partial research, blocked pages and absent school information honestly.

Example draft structure (fill only with verified facts):
“Hi <name>, I'm a <school> student and applied for <role> at <company>. I'd appreciate
connecting and learning about your experience there.”
For recruiters, use the actual role/application context and omit unverified shared-school
claims. These are reviewable drafts, not sent messages or automatically issued requests.

## Assessments — one row per assessment source message

Required columns:
- Application key, company, role
- Assessment source ID and description
- Assessment status: Pending / Deadline unconfirmed / Past due — verify / Completed /
  Application closed — review
- Original deadline wording
- Confirmed deadline (local date/time)
- IANA time zone
- Evidence link
- Calendar/reminder status
- Calendar ID and event ID (only real returned IDs)
- Event link (only real returned links)
- Verified reminder lead times
- Calendar last verified at
- Follow-up / approval notes

Map ledger states carefully:
- `not_recorded`: no verified event saved; use the actual pending approval/connection state.
- `recorded`: saved evidence of an event with configured reminders; recheck before claiming
  it still exists. `recorded_at` is the last stored verification, not proof of a current read.
- `event_only`: event saved, reminder settings not confirmed. Never label this a reminder set.
- `deadline_changed_review`: recorded deadline differs; needs approved update and verification.
- `review_existing_event`: completed/closed application with a saved event; review cancellation.

New Calendar actions require approval. Reporting a pending action does not create it.
Separate assessments survive later hiring-stage updates until completed or closed; an
interview invitation alone does not establish assessment completion.

## Report Notes — coverage and unresolved items

Include report date/time, student time zone, school, approved scan range, searched accounts,
search pagination/coverage, failed sources, unresolved application/deadline dates, contact
research coverage, Calendar failures/pending approvals and next steps. Mark `Sample —
fictional data` prominently for demos. No verified applications: retain headers and explain
what was searched; do not populate fake live rows. Unknown school: still deliver available
application/recruiter results and label alumni research pending.

## Before delivery

Inspect the saved artifact for valid `.xlsx` structure and all four sheets; confirm the
application count equals unique application keys, contact rows have supporting sources,
no closed/completed assessments are scheduled silently, and event status matches actual
Google results. Check paths, links and local time conversions. Attach the file; a command,
JSON payload, local path or text table alone does not satisfy the report request.
