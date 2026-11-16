# L0 Human Acceptance Record

**Accepted design: L0 revision 3. Decision: ACCEPT_LOOP. Decision date: 16 November 2026. L1: NOT_STARTED.**

## Actual decision

| Field | Recorded fact |
|---|---|
| Decision-maker | Project author, identified by the chat role; personal name not supplied. |
| Source | Explicit author message in the project conversation. |
| Local decision date | 16 November 2026, Asia/Singapore. |
| Accepted edition | L0 revision 3. |
| Decision | ACCEPT_LOOP. |
| Recorded meaning in English | "L0 revision 3 is accepted (ACCEPT_LOOP)." This is an English translation, not a verbatim English statement by the author. |
| Current direction | Prepare English GitHub task/design files as the design baseline; omit auxiliary L0 checking tools and focus on L0 and human-in-the-loop development. |
| Individual checklist observations | Seven L0 self-review checks were recorded by the project author on 16 November 2026 (Asia/Singapore). See the L0 Human Self-Review Checklist below. These checks represent author self-review, not independent approval or application testing. |
| Additional written rationale | PROVIDED. The author supplied a written justification following the explicit ACCEPT_LOOP decision. See Decision Rationale below. |

AI transcribed this record. The acceptance decision belongs to the author and was not inferred from the AI review. It is author self-review, not independent external approval.

## Accepted scope

The controlled documents are indexed in the [README](../../README.md#design-baseline-documents). They define the overview and two roles, V1.0/V1.1 boundaries, simple Streamlit/Python in-memory architecture, FR-01-FR-11, BR-01-BR-16, QR-01-QR-04, R-01-R-08, Demo reuse, test mappings and the human-controlled workflow.

Key policy decisions retained by this package:

- A workshop can be created only with more than 24 hours of lead time; exactly 24 hours is rejected.
- At C = S - 24 hours, Book, effective confirmed cancellation, Join and Promotion close.
- During C<=t<S, an owner may still withdraw a WAITLISTED record. Confirmed records remain unchanged and no promotion occurs.
- At S, all effective registration mutations close; reads and owned cancelled no-op repeats remain.
- Fictional actor selection and independent/resettable session memory are explicit prototype limits.

Packaging consolidates existing records and removes ancillary checking files. It does not introduce a new functional policy or create application V1.0.
## L0 Human Self-Review Checklist

**Review Date:** 16 November 2026 (Asia/Singapore)
**Reviewer:** Project Author
**Reviewed Edition:** L0 Revision 3

- [x] C01 — Confirmed that L0 Revision 3 is the reviewed design edition.
- [x] C02 — Reviewed FR, BR, QR and the project scope.
- [x] C03 — Reviewed R-01 to R-08 and their planned risk controls.
- [x] C04 — Checked the mapping between the Test Plan and Traceability.
- [x] C05 — Reviewed the limitations of Session State and fictional demo identities.
- [x] C06 — Recorded the actual human decision, date and written rationale.
- [ ] C07 — Verified consistent L0/L1 status across README, Requirements, Workflow and AI-use.

**Review Outcome:** The design is suitable for progression to L1 within the declared teaching-prototype scope. Application implementation and R-08 user validation remain pending.

## Human Decision Rationale

**Decision:** ACCEPT_LOOP  
**Accepted Edition:** L0 Revision 3  
**Decision Date:** 16 November 2026  
**Decision-maker:** Project Author

I reviewed the L0 requirements, business rules, risks, test plan and development workflow. I accept the simplified Streamlit and Python architecture for a single-session teaching prototype.

The capacity, timing and FIFO requirements are sufficiently defined for implementation and testing. The limitations of demo identity selection and temporary session data are documented.

R-08 remains pending user validation in later stages.

**Decision Outcome:** L0 Revision 3 is accepted. The design baseline is approved for progression to L1. This decision does not constitute application testing, deployment approval or release acceptance.

## Human and AI responsibilities

At L0, the author supplied scope/policy directions, requested review and made the actual ACCEPT_LOOP decision. AI drafted/reviewed the specification, proposed evidence and organised the English baseline. The [AI-use record](../ai-use.md) distinguishes those contributions and summarises the design findings.

Later loops must record what the author actually checked, understood, changed or rejected, alongside what AI generated and executed. The [workflow](../development-workflow.md#record-for-each-loop) defines each loop's AI task, personal acceptance, outputs and exit condition. AI must wait for the relevant human decision before advancing.

## Remaining obligations and next step

| Item | Status after this decision |
|---|---|
| L0 design gate | SATISFIED by the explicit ACCEPT_LOOP. No repeat L0 acceptance is required. |
| L1 entry | Eligible under the accepted plan; NOT_STARTED. This request packages L0 only. |
| Working V1.0, CR-01 and V1.1 | PLANNED; require actual implementation and separate acceptance. |
| Application tests and GitHub Actions | NOT_EXECUTED. Planned scenarios and checks are not passing evidence. |
| R-08 user suitability | VALIDATION_PENDING under VAL-01, VAL-02 and VAL-03A-VAL-03E. Design acceptance does not close this risk. |
| GitHub publication | L0 publication evidence is provided by the repository's actual commit history. The README was committed separately before this document upload. Documentation commits do not constitute application testing or release evidence. |
| Merge, deployment and release approval | NOT_GRANTED by this design decision. READY_TO_MERGE and ACCEPT_RELEASE are separate. |

The next implementation task is L1 when the author requests it. New material design changes require an explicit reason, impact assessment and human decision; they must not silently overwrite the accepted baseline.

