# AI Use and Development Record

Accepted design: L0 revision 3. L1 foundation implemented; human decision PENDING. L2 NOT_STARTED. The L0 sections below retain their historical scope; current execution is recorded in the L1 section.

## Human direction and actual contributions

The project author selected Outdoor Workshop Booking and Waitlist Management, the teacher's simple file/state approach and the timing policy. Creation requires more than 24 hours of lead time. At C, confirmed bookings freeze and joining/promotion close; owner waitlist withdrawal remains available until S.

The author requested source-based design review, English GitHub deliverables and a human acceptance gate before each implementation loop. The author explicitly accepted L0 revision 3 with ACCEPT_LOOP and then requested a lean design baseline focused on L0 and human oversight. Bilingual chat supports understanding; repository documents are English.

| Contributor or activity | Actual scope at L0 |
|---|---|
| Human | Topic, architecture and policy choices; review directions; explicit overall L0 ACCEPT_LOOP in chat on 16 November 2026; direction to exclude auxiliary L0 checking tools from the delivery. |
| AI | Codex assistant drafted and refined requirements, rules, risks, reuse decisions, test scenarios, mappings, workflow, source references and review findings. AI organised this package and transcribed the human decision into English. No unverified model version is recorded. |
| Source inspection | Supplied assessment sections, relevant transcript/deck sections and the pinned Demo's eight files/five test definitions. See [Sources](sources.md) and [Demo reuse](demo-reuse.md). |
| Document review | AI-assisted consistency review of language, links, requirement/rule IDs, test mappings and selected policy boundaries. This is design verification, not application execution or proof of user suitability. |
| Not performed for the application | Application implementation, automated application tests, executable GitHub Actions, deployment, external-user validation and releases. Documentation commits do not constitute application test evidence. |

Inputs were supplied course/design materials, screenshots and the public Demo. No production booking records or deployment credentials were introduced. The author recorded a seven-item L0 self-review checklist and a written decision rationale in the [L0 Human Acceptance Record](reviews/L0-human-acceptance.md). These records document author self-review, not independent approval or executed application tests.

## Design history

| Edition | Meaning |
|---|---|
| L0 revision 1 | Initial unaccepted draft with a more complex architecture and full freeze. |
| L0 revision 2 | User-selected simple session model, fictional actors, final-24h withdrawal and re-scoped I09/I10. |
| L0 revision 3 | Source-based review, English delivery, stronger independent test oracles, derived queue positions, demonstration readiness and explicit human evidence requirements. Accepted by the author. |

This packaging retains revision 3's functional design. Design editions are separate from working application V1.0/V1.1 releases. Auxiliary document-checking scripts, generated reports and duplicate packaging documents are outside the GitHub baseline; their removal does not remove the design obligations.

## L0 review findings

The review used S01-S10 and S13-S14 as applicable. Findings concern specifications and planned evidence, not observed runtime defects. The AI review preceded the author's separate acceptance.

| ID | Finding and revision 3 response | Status |
|---|---|---|
| L0-F01 | Reusing a withdrawn record could test a no-op instead of start-time rejection. W12/I10 now require a fresh active fixture for each boundary and separate repeat cases. | ADDRESSED_IN_SPECIFICATION |
| L0-F02 | Negative tests could fail for an unrelated reason. Require valid unrelated preconditions and independent outcomes from this project's FR/BR, including separate Book/Join behaviour. | ADDRESSED_IN_SPECIFICATION |
| L0-F03 | Queue sequence gaps could produce misleading displayed positions. Define position from current active waiters; cover withdrawal and ordered rosters in W13/W14. | ADDRESSED_IN_SPECIFICATION |
| L0-F04 | Tests needed explicit outcomes and complete-state assertions. Define result reasons and unchanged input/counter snapshots on success, rejection, no-op and failure. | ADDRESSED_IN_SPECIFICATION |
| L0-F05 | Fixed dated examples could become unusable live seeds. Separate controlled-clock tests from once-per-session, relatively dated demonstration fixtures. | ADDRESSED_IN_SPECIFICATION |
| L0-F06 | Human oversight needed concrete records. Define bounded AI tasks, personal checks, executor/evidence/code identities, finding dispositions and distinct loop/merge/release decisions. | ADDRESSED_IN_SPECIFICATION |
| L0-F07 | Comprehension alone does not establish policy suitability. Define validation decisions and keep R-08 pending actual task feedback, including near-C promotion and delayed awareness. | PLAN_REFINED; VALIDATION_PENDING |
| L0-F08 | Earlier bilingual documents did not match the requested GitHub language. Deliver the baseline in English and keep bilingual explanation in chat. | ADDRESSED_IN_DELIVERY |

The plan addresses requirements/quality planning, meaningful roles, V&V, baseline/change separation, regression, CI, deployment and human judgement. Later implementation and evidence are still necessary. This review is not lecturer approval, independent human review or an HD grade.

## Human control in later loops

Use the [workflow record](development-workflow.md#record-for-each-loop) when each actual loop occurs. Record significant AI tasks, constraints, assumptions, affected functions/tests, human edits or rejected suggestions, actual results and the author's decision.

The author's contribution must become visible through independently chosen expected cases, code understanding, personal checks, assessment of findings and justified decisions. AI can draft records and run checks; it cannot invent personal execution, user feedback or human approval. A human review of an AI result must be labelled as review rather than personal test execution.

The [acceptance record](reviews/L0-human-acceptance.md) preserves the actual L0 ACCEPT_LOOP and subsequent author self-review. The author has now requested L1; its distinct work and pending human decision are recorded below. R-08 validation and later merge/release decisions require their own evidence.

## L1 assistance and contribution

**Author task, summarised in English:** Start L1 from the accepted L0 and GitHub repository, retain the CampusConnect-Demo three-file approach, establish app.py/booking.py/test_booking.py, foundation tests and Actions, keep deliverables English, explain work bilingually in chat, record AI assistance and provide a personal checklist. Stop at L1 for ACCEPT_LOOP before L2.

| Activity | Actual AI contribution | Human responsibility/status |
|---|---|---|
| Baseline intake | Located the project repository and accepted main commit 822710b238bb14b8eba17cf2ab9a76ab2753bdb2; preserved the author's seven L0 checks/rationale. | L0 accepted; new L1 request supplied by the author. |
| Scope | Kept L1 to foundations; no actor selection, restricted business operations, creation/booking/cancellation or waitlist implementation. | Confirm this bounded delivery before accepting. |
| Code | Drafted the preview, dataclasses, independent state factory, structural checks and cutoff property. | Personally inspect separation, model/service distinction and state lifecycle. |
| Tests and correction | Derived examples from BR-02/BR-03 and the state model. Initially ran 36 cases. Further review reproduced incorrect repeated-clock timestamp ordering; four new regression cases failed before a UTC-comparison correction. All 40 cases then passed locally. | Assess the actual finding, independently predict selected outcomes and record personal observations. |
| Quality | Resolved and hash-locked dependencies; created SHA-pinned Actions and executed local checks. Detected incomplete initial audit coverage, corrected audit mode and verified all 34 runtime/71 development pins; added a CI reconciliation check. | Review the finding/correction, actual hosted CI and remaining limits. |
| GitHub delivery | Used existing Git configuration to commit/push the L1 branch and inspected hosted job logs/artifacts. Corrected implementation run 43868519549 passed 40 cases and all four jobs. Main remains the accepted L0; no PR, merge or release was performed. | A Git author identity is not evidence of personal test execution. Perform the required author review before a PR or next loop. |
| Review records | Recorded actual AI results, partial mappings, assumptions and an unchecked human checklist. | Supply the decision/rationale. No L1 approval has been supplied or inferred. |

AI used Codex, local Python/tooling, GitHub tools and official technical references. No unverified model version, human test execution or external reviewer is invented. Actual results and source/code identities are in the [L1 work/review record](reviews/L1-human-review.md).

Constructor validation is structural, so legitimate historical records can be represented. The future creation service must enforce role and fresh-time S-t>24h. AppTest state insertion is a test fixture, not a released booking operation. The author must assess these assumptions and any findings rather than treating passing checks as approval.

Human L1 edits, personal execution, finding dispositions and ACCEPT_LOOP remain pending. L2 is NOT_STARTED. No merge, deployment, application release or R-08 validation is approved by AI checks.
