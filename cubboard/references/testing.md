# Real Cubbie acceptance

Local tests cannot prove the following. Text Cubbie the public GitHub folder link;
approve installation, then use these checks with your own account:

1. “Scan my applications from the last 30 days.” Confirm scope; verify the company,
   role and source evidence against actual Gmail. No connected Gmail: verify the
   connect/manual-message fallback. An incomplete search must be reported.
2. Rescan the same range; verify no duplicate applications or messages. Check two
   distinct roles at one company remain separate. Import an older message later;
   verify it cannot regress an offer/interview into applied.
3. Test a real explicit deadline, a receipt-anchored relative deadline, and an
   ambiguous deadline. Verify exact local times and that ambiguity triggers a question.
4. Request a reminder. Verify no event before approval and no duplicate after retry.
   Mark an assessment complete; verify its action clears without inventing a new stage.
5. “Give me my top three career tasks today.” Check the ranking and source links.
6. Ask for a networking draft. Verify every recipient fact against a cited source,
   no invented relationship, and no email sent before exact-message approval.
7. Decline sending; verify no send. Edit a draft; verify a new approval is required.
8. Opt into a scheduled check-in and verify its real delivery. Cancel it and verify
   cancellation. Do not imply this was tested until it actually runs.
9. Reinstall the newest Skill and verify saved tracking survives. Request export,
   then deletion; verify deletion waits for yes and does not delete Gmail messages.
10. On another student's Cubbie, verify there is no access to your saved ledger.

Optional demo: show the “You applied. Now what?” moment, the real top-three briefing,
a verified assessment deadline and an outreach draft awaiting approval. Use fictional
mail for public recording or redact private details. Label sample-mode footage as a demo.

## Excel, LinkedIn and Calendar acceptance

11. “Use Cubbridge to make an Excel tracker of my applications from the last 30 days.
    My school is <your school>. Include alumni, recruiters and LinkedIn message drafts.”
    Verify an actual `.xlsx` attachment opens with Applications, LinkedIn Connections,
    Assessments and Report Notes sheets. A text table or local file path does not pass.
12. Check each company/role, application date and source. Confirm unknown application
    dates stay unknown, email confirmation times are separate, different jobs remain
    separate rows, and conflicting dates are flagged.
13. Verify each included alumnus attended the stated school and currently works for the
    company; verify recruiter employment/role. Open the LinkedIn and evidence URLs. A
    company with no verified match must show a coverage note, not fabricated people.
14. Read each draft: company, applied role, shared school and background must be supported.
    Confirm no LinkedIn request or message was sent. Confirm the workbook treats email
    text beginning with '=' as literal text, not an executable formula.
15. For a pending assessment with a confirmed deadline, inspect the proposed Google
    Calendar event and reminder offsets. Before approval: workbook says pending. After
    approval: verify the real event at the correct local deadline, no attendees, actual
    reminder settings and a working event link in the updated workbook.
16. Repeat the request; verify only one event for that assessment. Change a verified
    deadline; confirm an update is proposed for the same event, not a duplicate. If
    Calendar fails/disconnects or reminders cannot be configured, verify that exact status
    in the workbook. Do not accept a simulated event ID as live acceptance.
17. Supply a later interview email and check that an unfinished assessment stays tracked.
    Mark it completed; confirm completion in the workbook and review any existing event.
18. Run the offline demo: the workbook must be labeled fictional, contain no invented real
    LinkedIn profiles, and create no actual Calendar events. Test no matches and missing
    school: deliver available data with explicit coverage gaps, not invented rows.

These are real Cubbie acceptance checks. Local Python tests validate date/state behavior;
they do not establish Excel attachment delivery, live LinkedIn verification or Calendar
creation/reminder delivery.
