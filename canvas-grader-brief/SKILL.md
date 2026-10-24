---
name: canvas-grader-brief
description: Reports Canvas assignments, deadlines, and available submission counts for courses where the user is a TA, grader, or IA. Use for requests such as "what needs grading", "how many students submitted", "TA course overview", or "assignment deadlines for the courses I grade". This Skill reports workload; it does not evaluate student work or change grades.
---

# Canvas Grader Brief

Help a student who also works as a TA, grader, or instructional assistant check their grading workload from a text conversation. Use Cubbie's Canvas and browser abilities in plain language. No scripts, packages, keys, or team backend are required.

## Scope

Read only the courses and sections the user's own Canvas account can access. A Skill does not grant staff permissions. Staff statistics through Cubbie's connected Canvas ability are not guaranteed: establish availability from actual results before claiming they work.

Report course, assignment, deadline, and number of students who submitted when that number is available. Keep submission counts separate from numbers awaiting grading. Do not open student work, assign scores, post comments, change deadlines, or submit anything as part of this workflow. For requests to grade work, explain this Skill's scope and ask the user to define a separate workflow.

## Find the course and time range

1. Read the user's accessible Canvas courses through the connected Canvas ability. Use the course and date range the user named. Otherwise, look for assignments due in the next seven days in their staff courses and state that range. A "needs grading" request instead calls for assignments awaiting grading, including past deadlines; do not exclude overdue grading work just because it falls outside the next seven days.
2. Use staff enrollment information if returned. Do not assume every course is a staff course: the user may be a student in other courses. If the role is absent or ambiguous, ask which course they grade. Disambiguate duplicate names with term or section.
3. Use the user's local date and time and show the time zone. Ask if the time zone is unavailable; do not derive it from the sandbox clock. Translate dates such as "tomorrow" into an explicit date when confirming the range.

## Access and sign-in

1. Prefer the account already connected to Cubbie. Read assignments and any staff submission summaries actually exposed by that connection. Assignment metadata alone does not establish access to staff counts.
2. If Canvas is disconnected, offer to connect it. If the connection does not expose staff courses or counts, explain that limitation and offer to open Canvas in Cubbie's browser using the user's existing TA account.
3. For the browser route, use a verified Canvas link returned by the connection, or ask for the school's Canvas HTTPS address. Ask the user to sign in through the secure login page or take over the browser for school SSO and MFA. Never collect a password or code in the text thread. Confirm the visible course and staff view belong to the intended account.
4. Navigate to the requested course's Assignments, Grades, or assignment summary view and read the available aggregate statistics. School interfaces and permissions differ. If the browser cannot expose the count, say it is unavailable and offer to summarize an authorized assignment-summary export the user provides. Do not imply browser access bypasses Canvas permissions.
5. When running outside Cubbie without Canvas or browser access, ask for an authorized export or pasted aggregate assignment data. Explain that the report describes the supplied snapshot rather than live Canvas.

## Read assignments and counts

1. Retrieve all relevant pages of assignments or visible summaries for the selected courses. Follow pagination before saying a list or count is complete. If some courses or pages fail, identify the gap and report only verified results.
2. For each assignment, retain its course, title, source link, relevant deadline or deadline variants, section scope, and source-reported counts. Show "No due date" for an explicitly unset date; use "Deadline unavailable" for a date that was not retrieved. Do not substitute the user's personal due date for a course-wide deadline.
3. If sections or students have different deadlines, label the variants or say "Multiple deadlines" and give the assignment link. Do not collapse overrides into one misleading deadline. Keep unpublished assignments labeled if the staff view includes them.
4. Prefer an explicit count of distinct students with submissions. A number of upload attempts, files, groups, graded records, or submissions awaiting grading is not automatically that number. Do not add graded and ungraded counts and call the result students submitted unless the source establishes that definition for this assignment. Manual grades can exist without a submission.
5. Preserve the source's labels when only "graded", "ungraded", "not submitted", or "needs grading" counts are available. For example, report "Needs grading: 12; total students submitted unavailable" rather than substituting 12 for the total submitted. Count a student once if working from complete submission records with an actual submitted state or submission timestamp.
6. Label group counts as groups, not students. Label section-only totals as that section; do not extrapolate them to the course. For external-tool, paper, or no-submission assignments, report only what Canvas actually tracks. An inaccessible count is "Unavailable", never zero. An explicit, verified zero is zero.
7. Include a denominator only if a matching eligible-student total is available for the same assignment and scope. Do not use a general course roster total as a denominator for an assignment with restricted visibility. Exclude student names, identifiers, grades, and submission contents from this aggregate brief.

## Replies

Use short, plain text lines, one assignment per small block, with links on their own lines. Lead with the requested answer. Sort a deadline brief by earliest deadline; put assignments without a due date at the end. For a grading brief, lead with verified pending grading work. For more than five assignments, text a short summary and offer a document or sheet with the rest. Include when the information was checked and whether it came from live Canvas or an export.

Example format only; the following numbers are fictional:

CS 201 — Lab 4
Due: Nov 6, 11:59 pm MST
Students submitted: 38 of 45
Needs grading: 12

Use this format only for fields actually verified. If no count is accessible, keep the assignment and deadline and say "Submission count unavailable with this connection."

## Follow-ups and failures

- Missing staff course: ask the user to confirm the course and Canvas account; do not infer a course has no assignments from an access failure.
- Permission denied: say "This account cannot read submission statistics for that course. Check your Canvas course permissions." Stop that retrieval rather than retrying with other accounts or guessing.
- Nothing matches: name the checked courses and range, and offer a wider range. Distinguish an empty result from a failed lookup.
- Session expired: ask the user to reconnect or sign in securely, then retry the requested read.
- User requests recurring briefs: propose the course scope, fields, local time, and frequency. Create the scheduled check-in only after they agree. Each scheduled instruction names this Skill and those settings, fetches fresh data, and reports access failures without inventing counts.
