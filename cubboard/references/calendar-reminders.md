# Google Calendar reminders for grading work

Use this workflow when the user says "remind me" about an assignment, grading task, or deadline in the Canvas Grader Brief conversation. This behavior is scoped to the grader Skill; it does not change the separate Cubbridge career workflow or other Cubbie Skills. A request for a card or a deadline lookup alone does not authorize any Calendar write.

## Resolve what and when

1. Identify the assignment and course from the user's message or the immediately preceding verified card. If several assignments could match, ask which one. Distinguish "remind me to grade" from "remind me of the student submission deadline". Never infer that the student due date is the TA's grading due date.
2. Resolve the reminder's exact local date, time, and IANA time zone. Reuse the user's verified America/Phoenix preference when applicable; otherwise ask. Use the user's current local date/time rather than the sandbox clock. Resolve "tomorrow" or "Friday" into an explicit date. If only "remind me" or a date is supplied, ask for the missing time; suggest one concrete option, such as "Tomorrow at 9 am Arizona time?" and wait for a reply. Do not silently choose a time or a past date.
3. For "two hours before the deadline", first verify the relevant student or staff deadline and calculate the reminder time in the user's zone. If it has passed, say so and ask for a future reminder time rather than silently moving it. If a course has multiple section deadlines, identify the applicable section or ask which deadline.
4. Show the exact event details and wait for confirmation when resolving missing or ambiguous information, proposing a time, choosing among ambiguous calendars, or expanding to an unrequested batch/recurrence. An explicit request that already specifies the assignment and exact reminder time authorizes that event; proceed without asking the same permission again. No events are created merely by installing or updating this Skill.

## Create using connected Google Calendar

1. Use Cubbie's connected Google Calendar ability in plain words. If Google is disconnected, ask the user to connect the intended Google account, then resume only after the connection is confirmed. The hackathon sign-in and Canvas sign-in do not establish a Google Calendar connection. Never collect passwords, tokens, or verification codes in the chat.
2. Use the user's saved Calendar choice. Otherwise use the verified primary writable calendar of the connected Google account. If the account/calendar is ambiguous or no writable calendar is available, ask rather than guessing. Do not create on a shared course calendar by default.
3. Create a short 15-minute personal event starting at the requested reminder time, titled "Grade <assignment> - <course>" for grading requests, or "<assignment> deadline reminder - <course>" for submission-deadline requests. In its description, include the authorized Canvas assignment link when available, relevant deadline type and verified deadline, and a stable marker derived from the assignment identity, reminder purpose, and requested start time. Do not copy student names, individual grades, or submission contents. Add no attendees or invitations.
4. Configure an explicit Google Calendar popup notification at event start (0 minutes), unless the user requested another offset. The event is at the reminder time, so do not apply "two hours before" a second time as an extra event offset. Do not claim that an event alone guarantees a notification on the user's phone; Google Calendar and device settings also affect delivery.
5. Before writing, search the intended calendar for the marker and matching assignment/purpose/start time. Reuse an existing identical event and confirm it, rather than duplicating it. For a changed reminder, identify the existing event and update only the reminder the user meant. After a timeout or uncertain create response, search for the event before retrying. If the user explicitly requests another separate reminder time, create a separately marked event.
6. Read back the actual event and verify the calendar, local start date/time/zone, and notification configuration. Return the provider's actual event link when available. Say "Added to Google Calendar: Grade Assignment 2 - Nov 1, 9 am MST" only after verification. If the event exists but notification settings could not be configured/verified, say the event was added and notification setup remains unverified. If creation fails, say it was not added; never substitute a generated link or a local note and claim success.
7. If direct Calendar creation is unavailable, explain that limitation and offer an Add to Google Calendar link containing the verified title, local-zone-correct start/end times and assignment link. Opening that link still requires the user to save the event; creating a link does not create an event or configure notifications.

## Recurrence and cancellation

Only create recurring reminders or a batch when the user requests/approves the exact course/task scope, times, zone, frequency, and any end condition. Scheduled instructions explicitly name this Skill. For cancellation, identify the exact event and any recurring scope (one occurrence or the series) before removing it; deleting a local file or the Skill does not cancel Calendar events. Do not create a separate Cubbie reminder in addition to the Calendar event unless the user asks for both.

## Example conversations

- User: "Remind me to grade Assignment 2 tomorrow at 9 am Arizona time." With one unambiguous assignment and calendar, create the personal event with a 0-minute notification and confirm the resolved date after reading it back.
- User: "Remind me about this." Ask one question with a proposed exact time; create nothing until the user answers.
- User: "Remind me two hours before Assignment 2 is due." Verify which deadline applies and its time. Create the event at that offset once authorized; a student due date is not a staff grading deadline.
- User repeats the same request after an uncertain response. Search the intended calendar first; do not create a duplicate.
