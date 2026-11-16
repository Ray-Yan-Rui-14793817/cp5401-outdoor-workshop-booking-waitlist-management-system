# cp5401 Outdoor Workshop Booking and Waitlist Management System

A small, single-session prototype for one outdoor workshop provider. Participants reserve limited places and manage their own selected-demo-user records. Organisers create workshops and inspect their own rosters. Release V1.1 adds an explicit FIFO waitlist and automatic promotion before registration closes.

**Design baseline: L0 revision 3. Human decision: ACCEPT_LOOP, 16 November 2026. L1: NOT_STARTED.**

This English-language package records the author's accepted design and the human-controlled development plan. It was reviewed against the supplied assessment, lecture transcripts and relevant teaching decks. Application tests, GitHub Actions runs, deployment, validation and releases remain planned. Packaging does not change the accepted functional design.

## Design baseline documents

The baseline consists of this README and the ten documents below. The two root Git configuration files support normal repository use; no L0 document-checking tool or generated report is required.

| Document | Purpose |
|---|---|
| [Requirements](requirements.md) | Problem, users, scope, releases, functional and quality requirements, architecture |
| [Business rules](docs/business-rules.md) | Sixteen rules, operation outcomes and the C/S timing matrix |
| [Risk register](docs/risks.md) | Risks, controls, planned acceptance and residual limitations |
| [Demo reuse](docs/demo-reuse.md) | Pinned source, file/function decisions and attribution |
| [Test plan](docs/test-plan.md) | B/W/I scenarios, independent test oracles and validation |
| [Traceability](docs/traceability.md) | Requirements, rules, risks, tests and development loops |
| [Development workflow](docs/development-workflow.md) | AI tasks, personal checks, outputs, progression gates and CI |
| [Human acceptance](docs/reviews/L0-human-acceptance.md) | The author's actual chat acceptance; individual checklist observations are not separately recorded |
| [AI use and L0 review](docs/ai-use.md) | Actual assistance, design-review findings, human direction/acceptance and evidence limits |
| [Sources](docs/sources.md) | Assessment, lecture and technical references |

## Architecture and limits

    app.py -> booking.py -> dataclasses and in-memory lists
                 |
          test_booking.py -> pytest -> GitHub Actions

Use the teacher's simple file-based development approach. Streamlit owns views, fictional actor selection and session state; booking.py owns independently testable rules.

Within one preserved browser session, switching fictional participants and organisers uses the same state. Independent browser sessions do not share bookings. Browser reload, session recreation or server restart can reset data. In-app Refresh means a normal rerun, not browser reload.

Actor selection is not authentication. Visitors can select another fictional identity. Role/ownership checks are evaluated within that declared demo model; use fictional data only. This prototype makes no production identity, durability or shared-concurrency claim.

## Releases

| Release | Scope |
|---|---|
| V1.0 | Demo actors, creation/browsing, booking/cancellation, own history, organiser rosters, 24-hour policy, session state and quality checks. No waitlist. |
| V1.1 | CR-01 adds Join/Withdraw, FIFO, promotion and waitlist display while preserving baseline timing, roles, capacity and history contracts. |

Establish and accept an actual working V1.0 before implementing CR-01. A full Book request remains rejected in both releases; Join Waitlist is a separate V1.1 action.

## Timing policy

S is the workshop start, C = S - 24 elapsed hours, and t is trusted server decision time.

| Operation | t < C | C <= t < S | t >= S |
|---|---|---|---|
| Create the proposed workshop | Allow if otherwise valid | Reject | Reject |
| Book | Apply booking rules | Reject | Reject |
| Cancel CONFIRMED | Owner may cancel | Reject | Reject |
| Join waitlist | Apply V1.1 rules | Reject | Reject |
| Withdraw WAITLISTED | Owner may withdraw | Owner may still withdraw | Reject effective withdrawal |
| Promote | With effective confirmed cancellation | Prohibited | Prohibited |
| Read or repeat an owned CANCELLED record | Role/ownership rules | Same | Same |

Creation requires strictly more than 24 hours of lead time. In the final 24 hours, freeze the confirmed roster and close joining/promotion, but allow the waitlist to shrink through owner withdrawal. Withdrawal never changes confirmed places or triggers promotion.

## Current gate and evidence

The project author explicitly accepted L0 revision 3 with ACCEPT_LOOP on 16 November 2026. The [acceptance record](docs/reviews/L0-human-acceptance.md) distinguishes that overall decision from checklist observations not individually supplied. It is a human decision separate from the AI design review.

The L0 gate is satisfied. This task prepares the GitHub design baseline; L1 has not started. ACCEPT_LOOP does not approve a merge, application deployment or release. This documentation baseline must not be tagged as application v1.0.

Demo inspection and planned reuse are recorded directly in [Demo reuse](docs/demo-reuse.md). L0 findings and actual AI/human contributions are in [AI use](docs/ai-use.md). Future loops record the AI task, actual checks, human judgement and progression decision using the compact format in the [workflow](docs/development-workflow.md#record-for-each-loop).

R-08 user suitability remains pending the planned validation activities. Design acceptance is not evidence that the unimplemented controls work or that intended users accept the policy.

## Initial GitHub baseline

Upload the existing files with their relative paths preserved. Suggested initial commit: `docs: establish accepted L0 design baseline`. Retain the resulting real repository URL and commit SHA. No remote is configured and no upload or commit is claimed by this package.

Keep supplied course PDFs, recordings, ZIPs, screenshots, private chat exports, local analysis and old drafts outside the repository. Their relevant references are recorded in Sources. Add application files, executable Actions, test results and later loop records only when that work actually occurs.

The next implementation step is L1, under a new bounded task from the author. No second L0 acceptance is needed. Later design changes require a recorded reason, impact assessment and human decision rather than silently changing this baseline.

