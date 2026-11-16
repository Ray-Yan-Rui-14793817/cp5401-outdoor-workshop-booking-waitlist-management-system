# Project Requirements

L0 revision 3. Human design decision: ACCEPT_LOOP, 16 November 2026. L1 foundation implemented; human loop decision PENDING. Requirement acceptance targets below are unchanged and are not claimed complete by L1. [L1 review](docs/reviews/L1-human-review.md) | [Rules](docs/business-rules.md) | [Tests](docs/test-plan.md) | [Sources](docs/sources.md)

## Problem and purpose

Outdoor workshops have limited places. Duplicate registrations, incorrect cancellation and unclear timing can undermine allocation. Full sessions need a fair queue and a way to reallocate places released before the booking cutoff.

The application demonstrates correct management of capacity, selected demo identities, registration state and time within one session. Its engineering purpose is to provide requirements, verification, validation, tests, tool findings and human decisions that can be traced through a baseline and a controlled change.

## Users and scope

| Role | Meaningful operations |
|---|---|
| Participant | Browse; book/cancel own confirmed records before C; withdraw own waiting records before S; view own history. |
| Organiser | Create workshops more than 24 hours ahead; inspect owned confirmed rosters and, in V1.1, ordered waitlists. |

Use predefined fictional DemoUser records with stable IDs and fixed roles. Display names are not keys. Business functions reject unknown actors, role mismatch and non-owner actions. Selection does not authenticate a real person and cannot prevent a visitor selecting another demo identity.

Workshop details include title, aware start/end instants, location, capacity and optional preparation notes. Capacity is an integer from 1 to 30. Display Asia/Singapore, the start and the registration cutoff separately.

Workshops, My Bookings and Organiser may be views within app.py. No separate login system is required.

### Boundaries

Included: one provider, one-session state, serial rule operations, two meaningful roles, full dates, stable records, cancelled history and the selected C/S policy.

Excluded: real authentication/passwords, shared or durable storage, multi-user concurrency guarantees, payments, weather/map integrations, email/push, self-registration, whole-workshop cancellation, cross-workshop conflict checks, editing created workshop details/capacity and confirmed-roster overrides.

Organisers make weather and on-site safety decisions outside the application. Explain meeting/preparation information and the limits of a demonstration reservation.

## Release boundaries

| Release | Requirements |
|---|---|
| V1.0 | FR-01 through FR-07, applicable baseline BRs and QR-01 through QR-04. Includes strict creation lead, confirmed-roster closure and temporary session state. No waitlist implementation. |
| V1.1 | CR-01 adds FR-08 through FR-11 and extends cancellation/display. Preserve V1.0 actor, time, full-booking rejection, capacity, history and repeated-request contracts. |

V1.1 does not change C or reopen confirmed cancellation. Withdrawal until S applies to the newly introduced waitlist. Baseline tests with no waiters keep their original preconditions.

## Functional requirements

| ID | Release | Acceptance target |
|---|---|---|
| **FR-01** | V1.0 | A valid selected fictional actor resolves to its fixed ID/role. Unknown or inconsistent selection performs no restricted action. Switching/clearing selection preserves session business state. State explicitly that selection is not secure login. |
| **FR-02** | V1.0 | Show start, end, C, time zone, location, preparation, capacity and confirmed/remaining counts. Distinguish confirmed-roster closure from permitted waiting withdrawal and workshop start. Spare capacity does not reopen closed booking. |
| **FR-03** | V1.0 | Before C, a valid participant with no active registration can book an available place, receiving one CONFIRMED record/ID. Rejection leaves the entire input state unchanged. |
| **FR-04** | V1.0; extended V1.1 | An owner cancels a CONFIRMED record only before C, retaining history. Repetition allocates nothing further. V1.1 cancellation/promotion produces one complete state change. |
| **FR-05** | V1.0; extended V1.1 | Filter records/history by selected actor ID. Switching actors does not reset data. Filtering is not a real confidentiality boundary against identity selection. |
| **FR-06** | V1.0 | Organisers create valid workshops with S-t>24h, end>S and integer capacity 1-30. Assign IDs/ownership in the application. Invalid creation produces no record or counter advance. |
| **FR-07** | V1.0; extended V1.1 | Selected organisers read only owned rosters/counts. V1.1 adds ordered waiting records and operation-specific closure information. |
| **FR-08** | V1.1 | Explicitly join only when full, before C and without active duplication. Assign an increasing workshop-specific sequence; consume no confirmed place. |
| **FR-09** | V1.1 | Owner withdrawal is allowed while t<S, including C<=t<S. Change only that waiting registration; confirmed IDs/states/counts remain unchanged, and no promotion occurs. At/after S reject effective withdrawal. |
| **FR-10** | V1.1 | One effective confirmed cancellation before C promotes at most the earliest active waiter. Cancellation and promotion return together; no partial input mutation. No promotion at/after C. |
| **FR-11** | V1.1 | In-app refresh shows own state and current position. During C<=t<S explain that joining/promotion are closed but withdrawal remains allowed; after S show historical outcomes. Browser reload is not a state-preserving refresh. |

## Quality requirements

Every applicable critical scenario must be executed and pass before the relevant release. Planned scenarios and skipped checks are not passing evidence.

| ID | Measurable acceptance target | Planned evidence |
|---|---|---|
| **QR-01** | Selected valid, invalid, boundary and repeated serial actions preserve capacity, active uniqueness and the C/S matrix; V1.1 also preserves FIFO. Record zero invariant violations in those executed cases, without claiming shared-concurrency correctness. | B03-B09, B15; W03-W12; I01-I04, I10 |
| **QR-02** | Successful mutating functions return a complete new state without changing input. Rejection, no-op and injected failure preserve all original records and ID/queue counters. Repeats create no extra place allocation. | B16; W10/W16; I04/I05 |
| **QR-03** | Selected valid-actor role/owner violations are denied without mutation or mixed-record display. Use fictional data and disclose identity-selection limits; do not claim authentication or impersonation resistance. | B01/B02/B10/B12-B14; W13/W14; I08 |
| **QR-04** | Ordinary reruns and actor changes preserve the same-session state. Independent initialisations share no mutable collections. Explain browser reload/new-session/restart reset and verify that lifecycle rather than promising recovery. | I06/I07/I09; VAL-01/VAL-02/VAL-03 |

Coverage is diagnostic evidence, not an arbitrary HD threshold or proof of untested behaviour.

## Simple architecture

    app.py -> booking.py -> dataclasses and in-memory lists
                 |
          test_booking.py -> pytest and GitHub Actions

app.py handles views, demo actor selection and st.session_state. booking.py has no Streamlit dependency. Rule operations receive current state, selected actor and fresh trusted time and return an explicit outcome with candidate state. The UI assigns complete successful results only; it never adopts a partial failure.

Keep the core files simple. A small result record or constants can represent observable outcomes without introducing a framework, repository layer or external service.

| Data | Purpose |
|---|---|
| DemoUser | Predefined stable user_id, display_name and fixed role; not an authenticated account. |
| Workshop | ID, owner, title, aware start/end, location, capacity and notes. Derive C from S. |
| Registration | ID, workshop/user IDs, state and timestamps. Preserve cancelled history; rebooking uses a new ID. V1.1 adds queue_seq. |
| Demo state | Workshop/registration lists and necessary ID/queue counters, authoritative only within the current session. |

Switch fictional actors within one preserved browser session to demonstrate the workflow. Do not use mutable global booking state shared across independent sessions.

### Fixture and demonstration readiness

Use a controlled clock for automated tests. The dated examples in the rules are test examples, not a permanent live schedule.

At first demo-session initialisation, create bookable example workshops relative to current time with enough margin, such as at least 48 hours ahead. If closed/start-boundary examples are seeded, represent legitimate historical creation and registrations before C rather than allowing illegal late creation. Initialise once per session; do not regenerate timestamps on every rerun.

I07 checks representative baseline fixtures under V1.1 rules. It does not promise live-session upgrade, serialization or durable migration.

Target Python 3.12, Streamlit and pytest. Lock actual application and quality-tool versions in L1, aligned with deployment.
