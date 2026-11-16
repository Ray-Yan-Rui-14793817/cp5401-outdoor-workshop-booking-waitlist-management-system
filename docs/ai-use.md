# AI Use and Human Contributions

Tool: Codex assistant with local Python and Git/GitHub tools. No unverified model version is claimed. Inputs were supplied course/design materials and public Demo code; fictional data is used in the prototype.

## Significant tasks

| Task | Author direction and substantive AI output |
|---|---|
| L0 design and review | The author selected the outdoor domain, simple session architecture and timing policy. AI drafted/refined the English requirements, rules, risks, reuse and test plan. The author accepted revision 3 and later recorded seven checks and a written rationale. |
| L1 foundation | The author requested app.py, booking.py, test_booking.py, real tests, locks and Actions, with a stop before L2. AI generated these files and ran the checks. |
| L1 deep review | The author requested assessment/lecture/Demo comparison. AI corrected a CI pipeline failure path, strengthened state/count assertions, checked runtime isolation and recorded explicit risk recommendations. |
| L1 simplification | The author requested fewer repeated documents, one CI job, retained dependency locks/effective tests, English deliverables and unchanged business rules/L0. AI consolidated five documents, removed optional slots settings, retained all 40 cases and four dependency files, and replaced four jobs with one. At that stage, verification was local only. |
| Simplified L1 deep review | The author requested checks against accepted L0, Assessment 3/HD criteria, transcripts, slides, tests, Actions and human oversight, with fixes and a stop at L1. AI rechecked the original documents, identified a cutoff-test gap, added two boundary cases within the existing test function, challenged them using a private faulty copy, clarified partial stage exits, and verified the single-job workflow on codex/l1-simplified-review. Actual results and substantive findings are in the L1 review. |

## Current contribution boundary

| Contributor | Actual responsibility or work |
|---|---|
| Author | Topic, requirements and policy choices, actual L0 acceptance, and instructions to simplify and review L1. L1 personal observations and acceptance have not been supplied. |
| AI | Code/configuration/document drafting and revisions, source comparison, automated/local verification and technical findings. These executions are not described as the author's personal checks. |
| GitHub Actions | Automated execution against its recorded commit. CI is evidence, not human approval. |

The simplification changes documentation layout and CI organisation. All original 40 cases remain; the deep review adds two cutoff cases, bringing the total to 42. app.py and booking.py are unchanged by this deep review. The earlier simplification removed only optional slots=True settings from booking.py; its fields, validation, state and time contracts remain. Dependency inputs/locks, business-rule definitions and L0_develop are preserved. The L1 copy of the L0 acceptance record has one navigation target updated; its human decision, checks and rationale remain intact.

## L0 review findings

The L0 review clarified isolated test preconditions, derived queue positions, observable result/state contracts, demonstration dates and validation decisions. R-08 user suitability remains pending actual task feedback. The original records and author decision remain available in the [accepted baseline](https://github.com/Ray-Yan-Rui-14793817/cp5401-outdoor-workshop-booking-waitlist-management-system/tree/822710b238bb14b8eba17cf2ab9a76ab2753bdb2) and [L0 acceptance](reviews/L0-human-acceptance.md).

## Evidence and acceptance

The [L1 review](reviews/L1-human-review.md) is the sole current record of verification results, prior findings, risk assessment and the personal checklist. [Demo reuse](demo-reuse.md) records provenance; [README](../README.md#development-workflow) defines the gates. Significant tasks above summarise the interactions that materially affected the work; unrelated chat is not retained.

The author must understand the changed code, evaluate independent expected outcomes and assess AI assumptions/findings. Actual human edits, rejected suggestions, observations, risk judgement and a reasoned ACCEPT_LOOP belong in the review record. They are not inferred from this request or automated results. L1 decision: PENDING. L2: NOT_STARTED.
