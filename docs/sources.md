# Sources and Design Decisions

L0 revision 3. Course originals, transcripts and screenshots are not copied into this repository. Identify supplied materials by title, date and location; pin public code references. Teaching examples are evidence of methods, not automatic project behaviour.

## Course and user sources

| ID | Source | Support |
|---|---|---|
| **S01** | CP5401_Assessment3.pdf, 13 pages; scope pp.3-5, presentation pp.6-7, AI/submission p.8, rubric pp.9-13 | Minimum functionality/roles, quality/risk, V&V, baseline/change, tests, review, decisions, GitHub, deployment and defence. |
| **S02** | Supplied lecture transcript, 16 November 2026 09:40, also supplied as 10:45; English p.2 and review discussion pp.8-10 | Permission to adapt the simple three-file Demo to a different realistic scenario, disclose AI and retain human oversight. Duplicated transcription is not independent corroboration. |
| **S03** | Supplied lecture transcript, 16 November 2026 10:46; English pp.2-4 and 6-7 | Risk-based review/escalation, precise disclosure, change/test/decision artefacts, static/security/dependency checks and process understanding. |
| **S04** | Week3 SQA and Project Plan supplementary deck, risk/stage-exit/small-project sections | Risk ownership and monitoring, explicit stage exits and proportionate planning. |
| **S05** | Week6 AI Generated Code supplementary deck, slides 11, 14, 17 and 20 | Intent, preserved behaviour, assumptions, prompt-to-diff traceability, human verification and justified risk. |
| **S06** | Week7 AI Generated Tests and Security Review supplementary deck, slides 7, 12 and 14 | Strong assertions, regression safeguards and tests that establish the intended property. |
| **S07** | Week8 Tool Assisted Review supplementary deck, quality gates and merge sections | Automated checks, findings dispositions, evidence-based gates and no tool approval. |
| **S08** | Week9 Team Workflow and Governance supplementary deck, author ownership, focused PRs, disclosure, audit and student-project sections | Human ownership before PR, bounded changes, escalation, auditability and professional judgement. |
| **S09** | [Pinned CampusConnect tree](https://github.com/Georgegiri/CampusConnect-Demo/tree/12e8ea17f068b019e33ee37ed4b82e579d1993b2) and [Demo reuse record](demo-reuse.md) | Exact eight-file source inspection, functions and five test definitions. |
| **S10** | Latest user instructions and supplied architecture/policy screenshots, 16 November 2026 | Simple app.py/booking.py/dataclass-list architecture; creation lead and final-24h waiting-withdrawal policy. These are user choices, not rubric mandates. |
| **S13** | Week4 Verification and Validation supplementary deck, slides 4, 18 and 22 | Lifecycle evaluation, auditable design findings and requirement-evidence-decision traceability. |
| **S14** | Week5 Software Testing supplementary deck, slides 4, 9-10, 12-13 and 16 | Test levels, requirement-driven oracles, Arrange/Act/Assert and retained regression. |

Transcripts are automatic text records, not independently checked original audio. Tool names such as Ruff and Bandit are interpreted using the corresponding teaching decks.

The review uses relevant supplied decks and transcripts rather than claiming inspection of every video in the course archive.

## Technical references

| ID | Source | Support |
|---|---|---|
| **S11** | [GitHub workflow security](https://docs.github.com/en/actions/reference/security/secure-use), [PR reviews](https://docs.github.com/en/pull-requests/how-tos/review-pull-requests/reviewing-proposed-changes-in-a-pull-request), [PR event](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#pull_request) | Least privilege, pinned actions, own PRs and tested/head code identities. |
| **S12** | [Streamlit Session State](https://docs.streamlit.io/develop/api-reference/caching-and-state/st.session_state), [state concepts](https://docs.streamlit.io/develop/concepts/architecture/session-state), [deployment](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy) | Rerun state, independent/resettable sessions and branch-based deployment, not durable/shared booking storage. |

## Requirements versus selected design

The brief requires at least three meaningful functional requirements, two roles, important rules/data, at least two quality requirements, risk control, V&V, a working V1.0, a later controlled change, automated/regression checks, Actions, deployment and defence evidence.

The listed minima do not mandate a database or password login. The design must nevertheless work reliably within its declared scope and provide convincing quality evidence.

Capacity 1-30, Asia/Singapore, demo identities, the C/S policy, session memory and ten development loops are project choices. Lecture examples of overlap rejection or automatic full-session waitlisting are not this project's oracle: Book remains FULL and Join is separate.

No arbitrary coverage percentage, commit count, prompt count or AI-code ratio guarantees HD. Application behaviour, test rationale, reviewed findings, justified decisions and the author's understanding determine the quality of the evidence.
