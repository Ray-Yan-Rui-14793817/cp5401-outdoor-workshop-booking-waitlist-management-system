# AI Use and L0 Review Record

L0 revision 3. Human decision: ACCEPT_LOOP, 16 November 2026. L1: NOT_STARTED.

## Human direction and actual contributions

The project author selected Outdoor Workshop Booking and Waitlist Management, the teacher's simple file/state approach and the timing policy. Creation requires more than 24 hours of lead time. At C, confirmed bookings freeze and joining/promotion close; owner waitlist withdrawal remains available until S.

The author requested source-based design review, English GitHub deliverables and a human acceptance gate before each implementation loop. The author explicitly accepted L0 revision 3 with ACCEPT_LOOP and then requested a lean design baseline focused on L0 and human oversight. Bilingual chat supports understanding; repository documents are English.

| Contributor or activity | Actual scope |
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

The [acceptance record](reviews/L0-human-acceptance.md) records the actual ACCEPT_LOOP. L0 is accepted; L1 remains unstarted. R-08 validation and all implementation, merge and release decisions require their own evidence.
