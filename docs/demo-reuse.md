# Demo Reuse Record

L0 revision 3 source and reuse decisions retained. Source inspection completed. L1 architecture/state-pattern adaptation is implemented; business-operation adoption remains PLANNED. No application code was imported during L0.

Source: [Georgegiri/CampusConnect-Demo](https://github.com/Georgegiri/CampusConnect-Demo).
Pinned v1.0 reference commit: 12e8ea17f068b019e33ee37ed4b82e579d1993b2.

Eight text files were inspected at that commit: README.md, BASELINE_REQUIREMENTS.md, TEACHING_DEMO.md, app.py, booking.py, test_booking.py, requirements.txt and .github/workflows/quality-checks.yml. The record below preserves the relevant provenance without requiring a generated inventory file.

Five source test functions were identified, not executed:

- test_first_booking_is_accepted
- test_overlapping_booking_is_rejected
- test_non_overlapping_booking_is_accepted
- test_capacity_is_enforced
- test_cancellation_releases_booking

Historical passing tests and releases belong to the source project. These definitions are reference material, not this project's executed test evidence.

## Planned file and function reuse

| Source | Treatment and rationale | Project mapping |
|---|---|---|
| [app.py](https://github.com/Georgegiri/CampusConnect-Demo/blob/12e8ea17f068b019e33ee37ed4b82e579d1993b2/app.py) views | Adapt cards, Book, own records and cancellation to outdoor details, organiser views and S/C/withdrawal messages. | FR-02-FR-07/FR-11; B06-B17/W13/W14 |
| Name input and filtering | Replace free-name identity keys with predefined fictional actors and fixed IDs/roles. Keep the demonstration limitation rather than claiming login. | FR-01/FR-05/FR-07; B01/B02/B10/B12/B13 |
| Session state | Retain same-session memory, initialising once and sharing state across actor switches within that session. Disclose independent/resettable browsers. | QR-04; I06/I09 |
| [booking.py Session/Booking](https://github.com/Georgegiri/CampusConnect-Demo/blob/12e8ea17f068b019e33ee37ed4b82e579d1993b2/booking.py) | Retain dataclasses/lists. Add aware dates, location, owner, registration IDs/states and cancelled history. | FR-03-FR-10; B05/B17/I07 |
| booking_count | Count CONFIRMED records only; retained CANCELLED and WAITLISTED records do not consume places. | BR-04; B06/B11/W06-W08 |
| can_book / add_booking | Adapt validate-then-return-new-state logic with selected actors, IDs, C, active uniqueness and unchanged input. | BR-01-BR-08/BR-13/BR-15/BR-16; B07-B09/I01/I02/I05/I10 |
| overlaps / overlap branch | Retire cross-workshop overlap rejection. This project enforces per-workshop rules only. | Scope; B09 positive control; R-07 |
| cancel_booking | Replace history deletion/name-session matching with registration ID, selected ownership, operation deadline, retained state and complete V1.1 promotion. | FR-04/FR-09/FR-10; B11-B17/W06-W12/I04/I05 |
| [test_booking.py](https://github.com/Georgegiri/CampusConnect-Demo/blob/12e8ea17f068b019e33ee37ed4b82e579d1993b2/test_booking.py) | Adapt first/full/cancellation ideas to actual project entry points. Retire overlap expectations; add role, C/S, history, failures and waitlist cases. | B/W/I plan |
| [quality-checks.yml](https://github.com/Georgegiri/CampusConnect-Demo/blob/12e8ea17f068b019e33ee37ed4b82e579d1993b2/.github/workflows/quality-checks.yml) | Retain the simple checkout/setup/install/pytest idea. Add static/security/dependency checks, reports and a human-governed quality gate in L1. | CI; R-06/R-07 |
| [requirements.txt](https://github.com/Georgegiri/CampusConnect-Demo/blob/12e8ea17f068b019e33ee37ed4b82e579d1993b2/requirements.txt) | Keep dependencies small, but lock actual project/tool versions instead of treating source ranges as completed dependency control. | L1 |
| README / BASELINE_REQUIREMENTS / TEACHING_DEMO | Source context, not the student's engineering history. The classroom instruction to deliberately break overlaps is not an L0 task. | S02/S09 |

## Waitlist provenance

The pinned v1.0 contains no waitlist. Implement CR-01 only after this project's actual V1.0. If later Demo versions inform implementation, record exact SHAs, functions, modifications and verification. Disclose the reference rather than claiming independent authorship.

## Implementation record

### L1 foundation adaptation

| Destination | Actual use and change | Verification |
|---|---|---|
| app.py main | Adapted the Demo's Streamlit/separate-booking-module/initialise-once session pattern. Added a preview navigation shell and session counts. No free-name booking input, source cards or source booking actions are adopted yet. | FND-07 AppTest smoke, rerun and isolation checks. |
| booking.py models/create_demo_state | Adapted frozen dataclasses and list-based memory to Workshop, Registration, DemoUser and independent DemoState collections. Added aware instants, structural validation and the derived C value. Source add/cancel/overlap algorithms are not adopted in L1. | FND-01-FND-06. |
| test_booking.py | Used the three-file pytest approach. Foundation cases were written for this design; the Demo's five tests were not represented as this project's executed tests. | 40 collected local foundation cases, including four timestamp-order regression cases; see the L1 record. |
| quality-checks.yml | Adapted checkout/setup/install/pytest structure. Added SHA pins, hash installation, static/security/dependency checks, reports and the aggregate gate. | Local tool results and actual hosted runs are distinguished in the L1 record. |

AI drafted and verified this adaptation under the author's L1 task. Human L1 review remains pending. The [L1 record](reviews/L1-human-review.md) identifies actual evidence and code identity; source provenance remains pinned to the commit above.

When adoption occurs, add the destination file/function, source location, actual change, commit SHA, AI/human contribution and linked tests. PLANNED must not become ADOPTED or TESTED until those actions occur.

The pinned tree has no standalone LICENSE file. Do not invent a licence label or infer broader rights beyond the recorded course-adaptation context in [Sources](sources.md).
