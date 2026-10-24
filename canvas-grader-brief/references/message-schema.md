# Input contract

The input JSON is an object containing `messages`, a list of at most 2,000 normalized
messages (file under 5 MB). Each record has these fields:

| Field | Meaning |
| --- | --- |
| message_id | Actual stable Gmail message ID, or a clearly identified user-supplied evidence ID |
| application_key | Stable key for one actual application; preserve across scans |
| company, role | Evidence-backed nonempty strings |
| status | applied, assessment, interview, offer, rejected, withdrawn, follow_up_sent, or note |
| received_at | ISO timestamp with explicit offset; for sent follow-ups use actual sent time |
| evidence | Short source quote (max 1,000 characters); never full message body |
| source_url | Optional verified HTTPS link to the email; omit rather than invent |
| deadline_text | Optional exact deadline quote; may remain ambiguous |
| deadline_at | Optional verified absolute ISO timestamp with UTC offset |
| relative_hours | Alternative to deadline_at, only when anchored explicitly to email receipt |
| deadline_confirmed | Boolean true required for either calculated deadline form |

Required strings except evidence have a 200-character limit. Source links allow 2,000.
Only documented fields are accepted. Both absolute and relative deadlines cannot coexist.
A deadline with text alone becomes a clarification action. `deadline_confirmed` means the
interpretation is unambiguous in the source or explicitly confirmed by the student; it
never means permission to create reminders or send email.

```json
{"messages":[{"message_id":"example-message-1","application_key":"exampleco-swe-req123",
"company":"ExampleCo","role":"Software Intern","status":"assessment",
"received_at":"2026-10-23T10:00:00-07:00","evidence":"Complete within 72 hours of this email.",
"deadline_text":"within 72 hours of this email","relative_hours":72,"deadline_confirmed":true}]}
```

The script performs date arithmetic and ranking, not raw-email classification. Cubbie
reads the real mail and supplies structured evidence. `note` and `follow_up_sent` do not
change the hiring stage, but update the latest communication time. A new hiring-stage
message replaces the prior stage's pending action. Import events in either order; received
time determines the latest stage. Conflicting stages with identical timestamps should
be clarified before import, rather than relying on message-ID ordering.

There is no network client, remote sync, separate OAuth or PostgreSQL dependency in the
Skill. Its SQLite ledger is per student's HOME. Secure permissions limit local access;
this is not a claim of application-level encrypted ledger storage.
