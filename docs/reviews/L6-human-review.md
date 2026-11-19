# L6 V1.0 Integration, Deployment and Deep Review

**L6: ACCEPT_LOOP. Human decision: ACCEPT_LOOP, declared by the project author on 19 November 2026 (Asia/Shanghai, UTC+08:00). L7: NOT_STARTED / HELD_BY_AUTHOR. Main merge/tag/V1.0 release: NOT_AUTHORISED.**

Current acceptance applies to preceding delivered candidate [5c1e3ff92168b34397e2bee2ace85431ae4d124e](https://github.com/Ray-Yan-Rui-14793817/cp5401-outdoor-workshop-booking-waitlist-management-system/commit/5c1e3ff92168b34397e2bee2ace85431ae4d124e). The technical execution sections preserve their 18 November evidence and pre-acceptance gates; the [current human acceptance](#current-human-acceptance) records the subsequent 19 November author decision. No historical L0-L5 checkmark is transferred to L6.

## Intake and accepted base

Client date: 18 November 2026 (UTC+08:00). Accepted L5 branch head: 8a5c9723afe6a81bbafc634acc09b65dac436ee4. Initial L6 review base: fc964bb7bde9476e98aaabfee85ff8ab15156300. Revised source: [cb9b1f6bc9883c3e3162a98209b4b0de6b4193df](https://github.com/Ray-Yan-Rui-14793817/cp5401-outdoor-workshop-booking-waitlist-management-system/commit/cb9b1f6bc9883c3e3162a98209b4b0de6b4193df). Preserve original accepted L0-L5 reviews, L3 HF-02, L4-F08 and all five actual L5 feedback items in [L5 history](L5-human-review.md#current-human-acceptance). No old human checkmark transfers to L6.

The author authorises this technical review, bounded repairs, GitHub/local ZIP updates and retained services. After the actual cloud mismatch is identified, they specifically permit necessary PyArrow pin/hash correction with existing tools, no fabricated hashes or unrelated upgrades. They require an open deployment finding if revised environment/function proof fails. Neither instruction is personal validation, ACCEPT_LOOP, main merge, ACCEPT_RELEASE, tag, GitHub Release or L7/CR-01 authority.

## Intended and preserved behaviour

V1.0 implements FR-01-FR-07. Preserve all 39 canonical FR/BR/QR/risk rows and 51 scenario rows; integer capacity 1-30; creation strictly >24h; C=S-24h; new Book/effective confirmed Cancel only t<C; valid canonical actor/actual stored ownership; no active duplicate; CANCELLED history/new-ID pre-C rebooking; owned cancelled-repeat ALREADY_CANCELLED even after C/S; exact input/counter integrity. Full Book does not waitlist. No policy, data model, persistence, authentication, shared concurrency, notification, new framework or waitlist feature is added.

app.py retains UI/session responsibilities and adds a bounded read-only deployment identity log. booking.py retains accepted L5 bytes, independent role/target ownership and pure complete-State operations. test_booking.py retains all 308 intake cases/116 test ASTs/decorators plus seven helpers and appends nine cases in three functions. requirements.in and both locks change only the authorised existing Arrow pin/hash; requirements-dev.in, pyproject.toml and the entire single-job workflow remain unchanged. All 33 runtime/70 development unrelated pin/hash blocks are identical. Six current English documents change; no delivery file is added. Delivery remains 23 files/12 Markdown documents.

## Independent findings and dispositions

| ID | Actual observation, correction/evidence and status |
|---|---|
| L6-F01 (initial) | Initial generated insertion interrupted an old test. Focused failures/Ruff caught it; restore accepted source and append properly. Historical test-placement correction, not a product defect. |
| L6-F02 (initial) | Add two real-control serial Create -> Browse -> Book -> Cancel -> Rebook -> History/Roster journeys. Retained, including two role permutations and exact IDs/full-State expectations. |
| L6-F03 (initial) | Deployment form defaulted to Python 3.14; select 3.12. Managed Python is 3.12.16. Initial job patch aligned from local 3.12.14 to 3.12.16. Exact source/runtime proof is strengthened by F10/F11 below. |
| L6-F04 | Green tests/AI role-play alone did not establish useful user policy; human validation was pending at the technical stage. On 19 November, the author supplies VAL-01 PASS 9/9, VAL-02 PASS 10/10 and actual policy/session/outdoor-safety rationale: BASELINE_ACCEPTABLE_WITHIN_SCOPE. V1.1 R-08 and formal release remain separate pending gates. |
| L6-F05 (initial) | Manager detects requirements.txt and tool-only pyproject.toml, but explicitly selects root requirements.txt with uv. Keep necessary configuration; no evidence of wrong dependency input. DISMISSED_WITH_EVIDENCE. |
| L6-F06 (initial) | Browser radio-input automation and stale canvas cells gave unreliable intermediate evidence. Use visible semantic labels and a fresh painted state/screenshot. Verification-method correction, not a manufactured product defect. |
| L6-F07 (initial) | Full-plus-duplicate tests refusal precedence, not isolated B09. Exact-C disabled controls are not stale-submit I10. Correct mapping; keep spare-capacity duplicate and fresh-time tests unchanged. |
| L6-F08 | A private Create counter mutation before final DemoState construction, undone on ordinary success, passes all 308 intake cases (53.97s). Add Create domain/UI final-construction failure checks; two new tests reject it. Genuine creation was correct. ORACLE_GAP_CORRECTED. |
| L6-F09 | Equivalent private Book mutation passes all 308 old cases (53.58s). Add Book domain/UI final-construction checks; two new tests reject it. Genuine booking was correct. ORACLE_GAP_CORRECTED. |
| L6-F10 | Initial deployment record only established branch/head-at-launch, not independently observed remote SHA/package parity. Add read-only root Git/source/Python/runtime-package log and five metadata tests. Resolved by actual revised hosted observation in the controlled-restart section: CLOSED_TECHNICAL_FOR_TESTED_TARGET. |
| L6-F11 | Real build installs locked Arrow 26.0.1 then replaces it with 24.0.0. Initial lock/runtime parity claim was incomplete. Author permits targeted correction; pip-tools regenerates consistent 24.0.0 locks with 50 generated Arrow hashes each and no unrelated pin/hash change. Installed Streamlit permits 24.0.0. The authorised restart installs 24.0.0 directly and actual runtime metadata matches all 34 locked pins: CLOSED_TECHNICAL_FOR_TESTED_TARGET. CI alone is not the closure evidence. |
| L6-F12 | Initial reset disclosure lacked an actual process-restart observation. Isolated revised-lock 8520 stop/start plus native reconnect/rerun confirms factory reset 4/2 -> 4/3, original registration-2 CONFIRMED. Existing 8518/cloud preserved. VERIFIED_RESET_SEMANTICS, not data recovery. |
| L6-F13 / further review | README's unqualified Actual restart row could suggest only the local 8520 restart had occurred after the separate cloud reboot. Relabel the local row as historical and add an explicit subsequent cloud-restart row. The original events/history are preserved. CORRECTED_DOCUMENTATION_CHRONOLOGY. |
| L6-F14 / further review | A current branch head and an actual deployed checkout need separate identities. New cloud metadata reports 2cad4b5; intake is 78cdce5. GitHub proves exactly six Markdown-only changes and unchanged runtime/test/lock/workflow blobs. Record checkout equality as false and executable/lock parity as true; do not silently substitute the later head. DOCUMENTATION_ONLY_DELTA_RECORDED; no runtime drift found. |

The fault copies exist only in private evidence. No genuine late mutation was found in booking.py; improving test oracles is the actual repair. No original assertion/function/parameter is weakened. New tests isolate valid actors/open clocks/capacity, inject only final State failure, assert exact original records/list identity/counters and check the UI retains actor/submitted fields with no false success. The four creation/booking paths supplement retained late cancellation/multiple-attendee/clicked-target tests. Coverage alone had not revealed these gaps.

## Verification results

| Check | Actual result/executor/limit |
|---|---|
| Fresh local full suite | AI; Python 3.12.14, PyArrow 24.0.0: 317 passed in 76.81s, no failures/errors/skips. All 317 review-intake case identities and 126 top-level test/helper definitions/decorators remain unchanged; the earlier 308-case intake is historical. |
| Original-environment comparison | AI; Python 3.12.14/PyArrow 26.0.1: 317 passed in 81.34s. Not revised-environment proof. Original running 8518 is deliberately not modified. |
| Local quality/security | Ruff/format/Bandit/pip check PASS. Strict runtime/development pip-audit covers all 34/71 locked packages, no known vulnerabilities/skips/omissions at execution. Platform extras are outside this audit. |
| Coverage | 99% booking diagnostic; 200 statements/one missing, 70 branches/one partial. Existing demo-fixture guard remains unexecuted. No grade/completeness claim. |
| Private independent boundary matrix | 16 passing literal decisions: active Create/Book/Cancel x C-1/C/C+1/S plus separately owned-CANCELLED repeats at four instants. Check exact State/history/counters/input, active refusals and no-op identity. Separate from pytest count. |
| Current source CI | Accepted-candidate CI: [run 44284607153](https://github.com/Ray-Yan-Rui-14793817/cp5401-outdoor-workshop-booking-waitlist-management-system/actions/runs/44284607153) tests 5c1e3ff92168b34397e2bee2ace85431ae4d124e; job 134733904416, Python 3.12.16, 317 passed in 55.10s, zero failures/errors/skips, one job/all 18 steps successful. Runtime/development audits cover all 34/71 pins without known vulnerabilities or omissions. Artifact 14418996361 (quality-checks-44284607153-1) was independently checked for digest/CRC, exact tested SHA, all 317 case identities, quality reports and all 34 installed runtime versions. This accepted candidate and subsequent acceptance-record heads have unchanged executable/test/lock/workflow files relative to the observed cloud checkout. The records-only acceptance commit receives a separate exact-head Actions/artifact check; this run is not relabelled as that later result. |
| Revised hosted browser | PASS in a new AI-operated CUA Chrome session: eligible Xingjian receives FULL on seeded Photography; Alex submits a new workshop with capacity 0 and otherwise valid fields, receives only the capacity error and retains all eight inputs. Rui has blank title/no Alex error; switching back restores Alex's exact invalid zero and all other values. Correction to capacity 2 creates workshop-5 under Alex and resets only his form. Sam receives registration-5; a repeat while one place remains returns DUPLICATE_ACTIVE. Xingjian receives registration-6, then cancels only that second attendee. Sam registration-5 remains CONFIRMED in Alex's actual roster. Xingjian rebooks as registration-7; own History keeps CANCELLED registration-6 and unrelated 1/3 remain confirmed. Final Alex roster contains exactly confirmed 5/Sam and 7/Xingjian; Rui's choices exclude Alex workshop-5. These are fresh technical observations, not genuine human validation or direct inspection of all internal State. |
| Actual isolated restart | Verified target PID/path/start-time and unhealthy -> healthy transition for 8520 only. Native cancellation before restart is lost after reconnect/rerun; factory 4 workshops/3 confirmations and registration-2 CONFIRMED return. Sam selection can survive; main view/data reset. Existing 8518 stays healthy, cloud not stopped. |
| Protection/delivery | Compare all 23 local/source-tree/archive raw bytes and CRC; preserve 139 earlier files/archives, six historical reviews and 39/51 canonical rows. Source ZIP remains local, private tools/evidence outside repository. Final head Actions and parity are checked after records update. |

Historical intake evidence, not this patch's result: run 44244879029/job 134601303777 at fc964bb, Python 3.12.16, 308 passed in 71.14s/all 18 steps. Artifact 14400843523 was independently downloaded, CRC/digest/tested SHA/JUnit308 checked; digest cff4bc890a66defa31d6778359bf1dc0653a0886c7d008d0a8ac8049f83b6603. Earlier aligned source 1c952ee and run 44244177092 also belong to initial L6. An empty legacy commit-status collection is not a failed Actions run; actual jobs/artifacts are authoritative here.

## Dependency revision record

| Item | Actual evidence |
|---|---|
| Original input | Runtime and development locks pin PyArrow 26.0.1. Cloud Python 3.12.16/Streamlit 1.67.0 log installs it, then reports replacement with pyarrow<25 and installs 24.0.0. |
| Reason/constraint | Align this provider's observed functioning version and test a reproducible project environment. Installed Streamlit requires pyarrow!=25.0.0,<27,>=12.0.0; 24.0.0 satisfies it. No 26.0.1 application crash was reproduced. |
| Upstream interpretation | [Arrow issue 50471](https://github.com/apache/arrow/issues/50471) concerns 25.0.0/mimalloc and is closed; it reports 24 as a workaround. Do not generalise that issue into proof that 26.0.1 is broken or 24 is the only compatible version. |
| Authority | Author's explicit targeted pin/hash permission. It is not permission for unrelated upgrades or release. |
| Tool/method | Existing pip-tools 7.7.0, official PyPI, existing inputs/locks, --generate-hashes --reuse-hashes --allow-unsafe --resolver=backtracking --upgrade-package=pyarrow. Add direct pyarrow==24.0.0 constraint to requirements.in, compile requirements.txt then development lock constrained by runtime. No handwritten hashes. |
| Actual difference | Only version 26.0.1 -> 24.0.0; 50 tool-generated Arrow hashes in each lock, related via/input explanation. Runtime 34/development 71 package sets unchanged; all other 33/70 pin/hash blocks identical. requirements-dev.in unchanged. |
| Rejected private draft | Initial private compile omitted --allow-unsafe and failed retained-pin checking. Corrected before application/publication. The extras-aware audit parser matches the unchanged workflow; pip/setuptools and every other pin remain included. |
| Verification | Fresh isolated install --require-hashes from revised development lock, 317 full tests/static checks and complete strict audits. CI/runtime-only install and real cloud evidence must independently agree. |

## Deployment record

| Field | Observed value/status |
|---|---|
| Hosted candidate | [https://cp5401-outdoor-workshops-v1.streamlit.app/](https://cp5401-outdoor-workshops-v1.streamlit.app/), branch codex/l6-v1-integration, root app.py/requirements.txt. |
| Managed Python | 3.12.16 observed in actual build logs. Workflow remains pinned to 3.12.16; local compatibility environment is 3.12.14. |
| Revised local human preview | http://127.0.0.1:8520, isolated hash-installed Arrow 24.0.0. Kept running. |
| Original preview | http://127.0.0.1:8518 kept running with earlier Arrow 26.0.1; explicitly not current-lock environment proof. |
| Source/runtime proof | REVERIFIED at 18 November 2026 18:07:04 UTC+08:00 from a newly generated cloud runtime record. Actual checkout SHA is 2cad4b53899f5827c0d51cfb298c49f704d77b6b; review intake HEAD is 78cdce5ce906ea0f42aad03cb346e21ccf0c0c16. They are NOT the same Git commit. GitHub comparison establishes that the intake is one commit ahead with exactly six modified Markdown files; all runtime/test/dependency/configuration/workflow blobs are unchanged. Cloud SHA256 of app.py, booking.py and requirements.txt exactly matches the current L6 branch, Python is 3.12.16, Streamlit is 1.67.0, and all 34 installed runtime pins match requirements.txt, including PyArrow 24.0.0, with zero missing/version differences. F10/F11 remain technically closed for the verified executable/lock target; literal checkout-versus-documentation-HEAD equality is explicitly not claimed. No new server reboot is performed in this review. Later evidence-only heads are checked for the same non-runtime delta and have their own CI. At this 18 November technical stage, human validation and ACCEPT_LOOP were still pending. The author supplied UI/H01-H07 completion, VAL-01/02 results and ACCEPT_LOOP on 19 November; the current human acceptance record supersedes that gate. Merge/tag/release remain NOT_AUTHORISED. |
| Log scope | Once per Streamlit session: root Git SHA or explicit None, SHA256 of app.py/booking.py/requirements.txt, Python and installed runtime pin versions. Read-only; no user/session business data, arbitrary environment values or secrets. New/fresh session is required after a source update. |
| Platform boundary | Provider installs logging/installer extras beyond project lock. Project pin parity is not a claim of bit-identical OS/Python patch across local/cloud or full platform vulnerability certification. |
| Release state | APPLICATION_AND_RUNTIME_LOCK_PARITY_VERIFIED; DOCUMENTATION_ONLY_CHECKOUT_DELTA_EXPLICIT. F10/F11 remain closed for the verified executable target, without claiming that the actual cloud checkout equals a later documentation HEAD. L6: ACCEPT_LOOP by the author on 19 November 2026; UI/H01-H07 complete, VAL-01 9/9 and VAL-02 10/10 accepted within classroom scope. R-08 baseline timing/session suitability is ACCEPTABLE_WITHIN_SCOPE; V1.1 waiting/promotion validation remains pending. L7: NOT_STARTED / HELD_BY_AUTHOR. Main merge, tag and V1.0 release: NOT_AUTHORISED; ACCEPT_LOOP is not ACCEPT_RELEASE. Human acceptance/validation and release remain separate. |

Community Cloud follows the review branch; verify a fresh runtime identity after each candidate/update. If the exact source, revised pins or real controls cannot be established, leave F10/F11 OPEN and deployment condition NOT_MET. Do not silently substitute historical CI/local smoke or claim source proof from a branch label alone. Code/config rollback requires a reviewed source revision and new CI/smoke; it does not recover temporary bookings. The actual isolated restart demonstrates reinitialisation only.

## Integration, architecture and review depth

FR-01 identity/menu reset; FR-02 complete information/time/counts; FR-03 Book; FR-04 own Cancel; FR-05 own current/history; FR-06 valid Create; FR-07 actual-owner roster are integrated. The two serial journeys use an empty valid State and literal expected IDs/counters/records across the real UI controls. Retained multi-attendee tests check that only the target row changes; distinct active deadline/no-op fixtures prevent false deadline evidence. Capacity/full/duplicate/role/owner/unknown target checks keep valid isolated preconditions.

The UI takes fresh trusted time at actual submission; hidden/disabled controls are additional usability checks, not sole authority. Domain permission uses canonical actor and actual looked-up ownership. Original input is never modified by genuine success/refusal/no-op/failure, and UI adopts only explicit OK. There is no database transaction or shared-user race guarantee. All relevant F05/F08 regressions remain unchanged; L3 HF-02 is historical, not a current shared-draft contract.

No extra application layer, generic recovery abstraction, speculative persistence or duplicated rule validation is added. Only deployment provenance has a bounded metadata helper; missing metadata becomes unknown rather than inventing a SHA or mutating state. Existing unknown-target/invalid-clock/explicit-OK checks defend actual interfaces and rejected-candidate tests, not arbitrary state repair. Actual observed risk motivates the dependency fix. Review depth is AI-proposed Medium for this bounded environment/evidence patch; student judgement and allocation/permission scrutiny remain required.

## Risk/control and test mapping

| Risk | Implemented/executed control | Remaining acceptance/limit |
|---|---|---|
| R-01 | Capacity 1-30, CONFIRMED counts, duplicates, latest-state serial allocation and one-place cancellation/rebooking; retained B04/B07-B09/I01-I02. | No shared concurrency claim; human checks actual UI/results. |
| R-02 | V1.0 no waitlist/FIFO implementation. Full Book remains FULL. | W/I03/I04/I07 and CR-01 stay future. |
| R-03 | Role menus plus business canonical-actor/actual owner; B01/B02/B10/B12-B14/I08. F08 isolates accidental draft mixing. | Freely selectable fictional identities are not authentication; author-declared H05/H07 complete and this limitation accepted for the classroom model. |
| R-04 | Pure complete-State adoption/full input/counter snapshots; new Create/Book late-failure checks plus retained cancellation I05; independent initialisation and actual reset evidence I09. | No durable recovery; old preview environment differs; author accepts temporary data only for the declared single-session demonstration. |
| R-05 | Aware instants, trusted fresh clock, strict C/S and separate active/no-op fixtures, stale-submit I10; independent 16-decision audit. | Author accepts cutoff preparation rationale within classroom scope; late cancellation remains closed, with no emergency override or guaranteed attendance. |
| R-06 | Bounded author scope, actual code/dependency differences, generated-hash provenance, rejected-tool assumptions and AI ledger. | Author supplies UI/H01-H07 completion, substantive rationale and ACCEPT_LOOP; AI records rather than supplies the decision. |
| R-07 | All 308 old cases retained, nine independent review cases, private faults and current-SHA CI/artifacts/audits; no reduced assertions. | 99% coverage/317 cases do not prove completeness; full platform extras are outside audit. |
| R-08 | Information, status/deadline/preparation disclosures and concrete VAL-01/VAL-02 tasks. | Actual VAL-01/02 feedback accepts baseline timing/session/safety suitability within classroom scope; V1.1 near-C awareness/feasibility VAL-03A-03E remains VALIDATION_PENDING. |

I05 now tests late construction for all V1.0 mutations, not future promotion rollback. I06 combines automated preservation and separately labelled AI browser observations with the subsequent author-declared personal lifecycle check and judgement. I08 separates role/owner/adoption correctness from genuine human comprehension. I09 tests independent factory/session State and actual reset, not storage restoration. I10 has actual stale Create/Book/confirmed Cancel clock seams; waiting/promotion/withdrawal variants remain V1.1.

## Course and HD alignment

Original Assessment 3, three transcript PDFs and Week3-9 archive were re-extracted; source hashes match and 22 teaching decks were inspected as relevant. The rubric weights requirements/planning 15%, functioning app/deployment 15%, V&V/testing 20%, change/regression/release 20%, GitHub CI 15% and presentation/defence 15%. This technical review supports scoped/testable/traceable requirements, a genuine browser candidate, independent tests and documented human control; it cannot confer a grade.

The lecture permits explained adaptation of the three Demo core files and requires student understanding/ownership of AI/code/tests/acceptance. Verification versus actual user validation, risk-based tool findings, independent oracles, regression and justified human decisions are kept distinct. The assessed later CR-01 issue/impact/branch/PR/review/merge/V1.1 release, final document/PPTX/URLs and defence remain incomplete future work. A dependency alignment fix is not substituted for the assessed waitlist change. Earlier accepted reviews remain byte-identical. No rigid file count, test count or coverage percentage is represented as an HD requirement.

## Controlled restart resolution

### Authority, execution and lifecycle

The author's next instruction explicitly authorises one controlled reboot to resolve F10/F11, retaining the same candidate URL/branch and all services afterward. It does not approve human acceptance, main merge, a tag or V1.0 release. AI submitted the native existing-app Reboot confirmation once; no second manual reboot, app deletion/recreation, alternate deployment, source/dependency edit or GitHub permission expansion was used.

| Observed event | Actual cloud UTC time / result |
|---|---|
| Existing session before reboot | 5 workshops / 4 confirmations from the preceding AI walkthrough. |
| Disconnect | 18 November 2026 09:42:02 UTC (17:42:02 UTC+08:00). |
| Same repository/branch/entrypoint build | 09:42:07 UTC, codex/l6-v1-integration, root app.py. |
| Dependencies processed | 09:42:19 UTC; requirements.txt selected with uv. |
| Server started | 09:42:21 UTC; meaningful app becomes available at the original URL. |
| Runtime identity independently compared | 18 November 2026 17:42:47 UTC+08:00; all checks below MATCH. |
| Session after reboot | Factory 4 workshops / 3 confirmations, no selected identity. Earlier session data is not recovered. |

Earlier 05:09 UTC logs remain in the manager alongside the new build. They are historical evidence, not the revised installation result. The 09:42 build directly installs pyarrow==24.0.0; its post-build runtime metadata independently confirms 24.0.0 and no new Arrow override. The requirements.txt versus tool-only pyproject.toml warning remains, but the actual selected input is explicitly requirements.txt. Platform logging/installer additions are outside the 34 project runtime pins.

### Actual source and Python identity

Observed Git SHA: [2cad4b53899f5827c0d51cfb298c49f704d77b6b](https://github.com/Ray-Yan-Rui-14793817/cp5401-outdoor-workshop-booking-waitlist-management-system/commit/2cad4b53899f5827c0d51cfb298c49f704d77b6b), exactly the L6 branch HEAD at execution. Python 3.12.16 matches the unchanged single-job CI target; Streamlit 1.67.0 and PyArrow 24.0.0 match the lock. These values come from the executing cloud process's read-only metadata log, not the configured branch label or localhost.

| File | Actual cloud SHA256, identical to local/GitHub | Comparison |
|---|---|---|
| app.py | `4578d6365fe6ca06499dee379b87a02c907d6ed03a604af896c3aba3b1d68b2b` | MATCH |
| booking.py | `63711b39a2e21f04913ef0d9aa6b6b29a9eec5ee7c44f336aaa6d04963e79b91` | MATCH |
| requirements.txt | `3c7ed09982005eafbdd15bad51cf8effb854a631d6b02f59712bd5f9ebf48e62` | MATCH |

If a following commit contains only this evidence, record its GitHub HEAD separately and compare its unchanged application/lock blobs with these actual deployed digests. Never replace the observed deployment SHA with a later documentation SHA without a new runtime observation. No additional manual reboot is authorised by this record.

### All 34 installed project runtime dependencies

The exact expected/observed package-name sets both contain 34 entries. Missing packages: zero; version mismatches: zero. The identical 34 pinned values were independently rechecked from a new execution record at 18 November 2026 18:07:04 UTC+08:00; this table is not a claim of literal checkout-HEAD equality. These are installed distribution versions reported after managed setup; they do not certify unlisted platform/OS packages.

| Package | requirements.txt | Actual cloud version | Result |
|---|---|---|---|
| altair | 6.3.0 | 6.3.0 | MATCH |
| anyio | 4.16.0 | 4.16.0 | MATCH |
| attrs | 26.1.0 | 26.1.0 | MATCH |
| certifi | 2026.10.23 | 2026.10.23 | MATCH |
| charset-normalizer | 3.5.2 | 3.5.2 | MATCH |
| click | 8.5.1 | 8.5.1 | MATCH |
| h11 | 0.16.0 | 0.16.0 | MATCH |
| idna | 3.20 | 3.20 | MATCH |
| itsdangerous | 2.2.0 | 2.2.0 | MATCH |
| jinja2 | 3.1.6 | 3.1.6 | MATCH |
| jsonschema | 4.26.0 | 4.26.0 | MATCH |
| jsonschema-specifications | 2025.9.1 | 2025.9.1 | MATCH |
| markupsafe | 3.0.4 | 3.0.4 | MATCH |
| narwhals | 2.28.0 | 2.28.0 | MATCH |
| numpy | 2.5.5 | 2.5.5 | MATCH |
| packaging | 26.3 | 26.3 | MATCH |
| pandas | 3.1.1 | 3.1.1 | MATCH |
| pillow | 13.0.0 | 13.0.0 | MATCH |
| protobuf | 7.36.2 | 7.36.2 | MATCH |
| pyarrow | 24.0.0 | 24.0.0 | MATCH |
| pydeck | 0.9.3 | 0.9.3 | MATCH |
| python-dateutil | 4.0.0 | 4.0.0 | MATCH |
| python-multipart | 0.0.34 | 0.0.34 | MATCH |
| referencing | 0.37.0 | 0.37.0 | MATCH |
| requests | 2.34.2 | 2.34.2 | MATCH |
| rpds-py | 2026.9.1 | 2026.9.1 | MATCH |
| starlette | 1.10.0 | 1.10.0 | MATCH |
| streamlit | 1.67.0 | 1.67.0 | MATCH |
| typing-extensions | 4.16.0 | 4.16.0 | MATCH |
| tzdata | 2026.6 | 2026.6 | MATCH |
| urllib3 | 2.8.0 | 2.8.0 | MATCH |
| uvicorn | 0.54.0 | 0.54.0 | MATCH |
| watchdog | 7.1.0 | 7.1.0 | MATCH |
| websockets | 17.4 | 17.4 | MATCH |

### Post-reboot native business verification

| Step | Actual observation and independent check |
|---|---|
| Eligible FULL refusal | Xingjian attempts the seeded full Photography workshop before C and receives FULL; no waiter/success. The next valid new registration is still registration-5. |
| Invalid Create / organiser isolation | Missing meeting point rejects creation. All eight visible values match their pre-submit snapshot. Alex has a blank title/no Rui error; returning Rui restores all eight values/errors. |
| Correct / success reset | Correction creates exactly workshop-5 owned by Rui, capacity 2, >24h away. Title/meeting point/notes reset empty and capacity resets to 10. The first failed attempt consumed no workshop ID. |
| First Book / isolated duplicate | Xingjian gets registration-5. A repeat with one free place returns DUPLICATE_ACTIVE, isolating duplication from fullness. |
| Second participant | Sam gets registration-6; the new workshop has two confirmations and total confirmations rise to 5. |
| Target-only cancellation | Xingjian cancels registration-5, total falls 5->4; the freshly painted actual owner's roster still contains Sam registration-6 CONFIRMED. |
| Rebook / History | Xingjian receives new registration-7; registration-5 remains CANCELLED in own History, unrelated registrations 1/3 stay confirmed, and the closed Trail Safety cancellation remains disabled. |
| Final own roster | Rui's workshop-5 roster contains exactly registration-6/participant-2/Sam and registration-7/participant-1/Xingjian, both CONFIRMED; total 5 workshops/5 confirmations. |
| Other organiser | Alex's actual workshop choices contain only Past Nature Walk/workshop-4 and Photography/workshop-2, excluding Rui's workshop-5. |
| Refresh and independent public session | Native Refresh view keeps 5 workshops/5 confirmations and the two-person roster. A separate public/no-owner IAB session has factory 4/3, no Manage app control and meaningful app content. No cross-session sharing is claimed. |
| Browser health | Fresh Chrome and public IAB URL/title match the target; meaningful app/no framework overlay and empty error/warning collections. Desktop/narrow-desktop only; no mobile-specific run or genuine user validation is inferred. |

This is AI technical verification through actual controls/painted tables. Complete internal input/Counter assertions and C-1/C/C+1/S/failure oracles remain in the unchanged 317-case suite; the browser is not used to invent internal State visibility. Fresh session checks and final CI/delivery receipts are verified before handoff. The actual human H01-H07/VAL-01/02 observations were pending at this historical technical stage; the 19 November record below supplies the later declaration.

### Findings and release boundary

L6-F10 and L6-F11 are CLOSED_TECHNICAL_FOR_TESTED_TARGET for the actually observed source/runtime and exercised workflows. Earlier open-stage findings and their causes remain in history. At this 18 November technical stage, human validation/acceptance and explicit release approval had not been supplied. The subsequent 19 November author record supplies baseline validation and ACCEPT_LOOP only. R-08 V1.1 validation and release remain pending; no main merge/tag/Release occurs and L7 stays NOT_STARTED.

## Further L6 deep review

### Intake, fresh execution and findings

The author's next instruction requests this new review while keeping human acceptance and all release decisions pending. Intake is [78cdce5ce906ea0f42aad03cb346e21ccf0c0c16](https://github.com/Ray-Yan-Rui-14793817/cp5401-outdoor-workshop-booking-waitlist-management-system/commit/78cdce5ce906ea0f42aad03cb346e21ccf0c0c16); all 23 local blobs match that GitHub tree before edits. Current source/tests/configuration/locks are byte-identical to the actually deployed application target. The review makes no additional manual server restart; the earlier authorised one remains a separate historical event.

| Review area | Actual conclusion/evidence |
|---|---|
| Architecture and redundancy | app.py handles views/session adoption, booking.py uses pure complete-State operations, and tests remain in test_booking.py. No extra framework/layer/guard or duplicated policy validation is needed. Actual-target role/ownership, invalid clock and explicit-OK adoption checks protect real tested interfaces. |
| Business/state integration | Existing FR-01-FR-07, strict C/creation lead, capacity 1-30, active uniqueness, target-only cancellation, history/new IDs and own roster remain intact. No code or business-rule repair is justified by this review. |
| Test quality | Keep every 317 case/119 test function and all helper/decorator/parameter/assertion bytes. Review independent preconditions, complete expected snapshots, active versus no-op clocks, multiple attendees and final-State construction failures; no weaker test replaces a retained oracle. |
| Fresh local execution | 317 passed in 76.81s; Python 3.12.14/PyArrow 24.0.0, with all 34 installed runtime versions matching the lock. Ruff/format/Bandit/pip check PASS; diagnostic booking coverage unchanged at 99%. Local patch is compatibility evidence; CI/cloud target remains 3.12.16. |
| Independent time/state audit | 16 fresh decisions pass: active Create/Book/Cancel at C-1 second/C/C+1 second/S, plus four distinct owned-CANCELLED repeats. Literal expected outcomes/full results/input, histories and counters are asserted. Separate private audit, not additional pytest count or shared-concurrency proof. |
| F13 repair | Distinguish historical isolated 8520 reset from the later one authorised cloud reboot in README. Neither is persisted recovery; this review performs zero manual server restarts. |
| F14 repair | Explicitly separate actual checkout SHA, review-intake SHA and any following evidence-only head. Literal commit equality is false for the current documentation delta; raw executable/lock and installed-pin parity is independently true. |

### New cloud identity observation

Observed at 18 November 2026 18:07:04 UTC+08:00. A new cloud session increases visible metadata records from six to seven; this is a newly generated execution record, not a reused initial log. Actual checkout: [2cad4b53899f5827c0d51cfb298c49f704d77b6b](https://github.com/Ray-Yan-Rui-14793817/cp5401-outdoor-workshop-booking-waitlist-management-system/commit/2cad4b53899f5827c0d51cfb298c49f704d77b6b). Review-intake branch HEAD: [78cdce5ce906ea0f42aad03cb346e21ccf0c0c16](https://github.com/Ray-Yan-Rui-14793817/cp5401-outdoor-workshop-booking-waitlist-management-system/commit/78cdce5ce906ea0f42aad03cb346e21ccf0c0c16). GitHub comparison establishes one descendant commit and exactly six modified Markdown files. No code/test/lock/workflow/configuration change exists between those identities.

| Assertion | Fresh result |
|---|---|
| Actual checkout SHA equals intake HEAD | NO: 2cad4b5 versus 78cdce5; disclosed documentation-only delta. |
| app.py, booking.py, requirements.txt raw SHA256 equal current branch/local | YES: all three equal the digest table above. |
| Actual Python equals cloud/CI target | YES: 3.12.16. |
| Actual Arrow / Streamlit | 24.0.0 / 1.67.0, matching unchanged requirements.txt. |
| Installed package-name set and all 34 versions | Exact match to the 34-row table above; zero missing entries or version differences. |
| Additional manual server restarts in this review | Zero. Existing cloud/local services are retained. |

F10/F11 remain closed for the verified executable/lock target. This is not a claim that the complete Git checkout equals every later Markdown-only evidence head. If literal final-head equality is separately required, do not mark it passed merely because the application files match. Preserve the actual observed SHA and verify any following commit's complete diff/current CI rather than inventing a deployment identity. Project pin parity does not certify platform-added/OS packages or real authentication.

### Fresh hosted business permutation

| Native step | Actual result |
|---|---|
| Eligible full target | Xingjian's pre-C Photography request returns FULL; no waiter/success is created. |
| Isolated invalid capacity | Alex submits capacity 0 with valid title/location/dates/notes. The capacity error appears, all eight exact values are retained and current workshop count stays 4. |
| Organiser isolation | Rui has blank title/no Alex error; Alex restores all eight values including invalid zero. This directly complements F05/F08 regressions. |
| Correction | Capacity 2 creates workshop-5 under Alex. Title/location/notes clear, capacity resets to 10 and default dates/times return. |
| Two attendees / duplicate | Sam gets registration-5. A repeat with one place free is DUPLICATE_ACTIVE. Xingjian gets registration-6. |
| Cancel second attendee | Xingjian cancels registration-6; total confirmations 5->4. Alex's actual roster still contains registration-5/participant-2/Sam CONFIRMED. |
| New-ID rebooking / history | Xingjian gets registration-7, own History keeps registration-6 CANCELLED, and unrelated confirmed 1/3 stay intact. Closed Trail Safety cancellation remains disabled. |
| Actual final roster | Alex's workshop-5 lists exactly confirmed 5/Sam and 7/Xingjian; total workshop/confirmation metrics are 5/5. Rui's choices contain only owned workshops 3/1 and exclude Alex's new workshop. |
| Refresh and independent public access | Native Refresh retains 5 workshops/5 confirmations and the two-person roster. A separate public/no-owner IAB session starts with 4/3 and no Manage app control. Both pages have the expected URL/title and meaningful app content. |
| Console/render health | Fresh Chrome and public IAB error/warning collections are empty; no framework overlay is observed. Desktop/narrow-desktop only; no mobile-specific or genuine human validation claim. |

Browser-visible ID/count/table observations complement the stronger internal State/Counter assertions in unchanged automated tests; they are not direct access to arbitrary internal state. Actual refresh/public-session/console and final-head CI/delivery receipts are checked before handoff. These are AI technical checks, not H01-H07 completion or genuine VAL-01/02 policy feedback. No new user risk decision is invented.

### Pre-acceptance human gate (historical technical stage)

At the 18 November technical-review handoff all seven personal items were unchecked and baseline suitability awaited actual author evidence. The author subsequently declares those checks complete, supplies genuine validation feedback and ACCEPT_LOOP on 19 November as recorded below. This supersedes the earlier human loop gate, without authorising main merge, tag, GitHub Release, V1.0 publication or L7 work.

## Validation record

Verification asks whether specified behaviour works; validation asks whether the intended user task/policy is useful. Record actual author role-play honestly or identify real external testers; never invent either.

| Task | Personal task/acceptance question | Actual human evidence/decision |
|---|---|---|
| VAL-01 / participant | In a fresh session find suitable workshop; explain S/C/location/preparation/full versus locked; cancel Sam's Photography registration-2 before C, retain history; book as Xingjian (registration-5), inspect own records and next action. Explain post-C restriction and temporary/selectable identity limits. Is this coherent/useful for the declared task? | AUTHOR_REPORTED_PASS 9/9 submitted participant scenarios; ACCEPTABLE_WITHIN_SCOPE. Project author, declaration 19 November 2026 (Asia/Shanghai, UTC+08:00), accepted candidate 5c1e3ff92168b34397e2bee2ace85431ae4d124e. Booking/cancellation/history meet requirements; cutoff supports preparation but restricts late cancellation and must be clear. Aggregate feedback L6-HF-02/07 below; individual scenario logs/timestamps were not supplied. |
| VAL-02 / organiser | Create capacity-1 workshop >24h away, intentionally omit meeting point, inspect all eight retained values/errors/no consumed ID, correct/reset, book as participant and inspect creating/other organiser rosters. Does the 24h freeze support preparation; is closed confirmed cancellation acceptable? | AUTHOR_REPORTED_PASS 10/10 submitted organiser scenarios; ACCEPTABLE_WITHIN_SCOPE. Same author/date/candidate. Stable rosters support equipment/activity preparation; temporary Session State is acceptable for one-session teaching demonstration, not reliable real-world operations. Actual feedback L6-HF-03/07 below; no external testers are claimed. |
| Manual I06/I08/I09 | Exercise identity/menu reset, owner/private lists, Refresh view/ordinary rerun, independent session and actual reload/new-session semantics. Explain possible factory reset and lack of secure login/sharing/recovery. | COMPLETE by explicit author UI/H01-H07 declaration. Feedback L6-HF-05 accepts role/draft/rerun behaviour within the demo model and acknowledges independent-session/restart lack of shared/durable records. Exact personal command or per-step logs were not supplied. No service restart is needed for this records-only update. |
| R-08 / later waiting | VAL-03A-E: unconfirmed waiting/no notification, latest useful discovery, promotion just before C discovered after C, preparation/arrival and post-C waiting withdrawal. No promotion at/after C under accepted policy. | VALIDATION_PENDING / DEFERRED_TO_V1.1. Neither 24h rule nor AI browser success closes feasibility/awareness concerns. |

## Human acceptance checklist

The author explicitly declares UI/H01-H07 complete on 19 November 2026 (Asia/Shanghai, UTC+08:00) for delivered candidate 5c1e3ff92168b34397e2bee2ace85431ae4d124e. All seven checkmarks below record that declaration, not an AI inference or a new AI execution. The original task wording is retained for traceability; exact personal command/time logs were not supplied.

- [x] **H01 - Candidate/evidence.** Verify current L6 GitHub HEAD, its actual Actions/job/artifact, source candidate SHA, deployed identity/version comparison and 23-file local ZIP parity. Explain preserved booking.py/308 old cases/single job, nine new cases and only the authorised Arrow pin/hash correction. Review F01-F14 and AI contribution.
- [x] **H02 - VAL-01 participant.** Perform the participant task above, check exact cancellation/history/replacement IDs/counts and explain full versus deadline closure. Record actual comprehension, next action and cancellation-policy judgement.
- [x] **H03 - VAL-02 organiser.** Perform invalid -> corrected creation/reset and participant booking/owned-roster task. Check >24h/capacity 1-30, eight failed fields, no invalid ID advance, current identity ownership and other organiser isolation; record preparation-policy feedback.
- [x] **H04 - Independent oracle review.** Inspect active C-1/C/C+1/S versus separate owned-CANCELLED repeats; spare-capacity duplicate versus eligible FULL; multiple-attendee/clicked-target cancellation; old-input/counters/history and late Create/Book/Cancel failure tests; F05/F08 regressions. Explain why high coverage or capacity-1 journeys could miss the private faults.
- [x] **H05 - Identity/session lifecycle.** Personally check role-specific menus plus business permission evidence, same-organiser failure restore/other-organiser isolation, Refresh/rerun, another session and reload. Explain no secure authentication/shared allocation/durable recovery; use fictional data only. Prefer aligned 8520 for revised local checks; 8518 is preserved with older Arrow.
- [x] **H06 - Actual deployment/validation.** Open the hosted candidate and inspect Participant/Organiser native workflows; compare observed SHA/source/package evidence and declared Python patches. Record genuine VAL-01/02 observations/rationale and any unresolved environment or suitability issue; preserve R-08/V1.1 questions. AI screenshots are not personal execution.
- [x] **H07 - Human decision/release boundary.** Explain AI/Demo contributions and test expectations; record actual findings/edits/rejected suggestions, residual-risk reasoning, reviewer/date/candidate and ACCEPT_LOOP or CHANGES_REQUIRED. ACCEPT_LOOP does not imply READY_TO_MERGE or ACCEPT_RELEASE. Do not start L7/CR-01 automatically.

| Human record | Current value |
|---|---|
| Reviewer/date/candidate | Project author; declaration 19 November 2026 (Asia/Shanghai, UTC+08:00); delivered candidate 5c1e3ff92168b34397e2bee2ace85431ae4d124e. Exact execution time not supplied. |
| Personal UI/commands/observations | UI/H01-H07 explicitly declared COMPLETE; actual aggregate observations transcribed below. No personal commands/times or detailed scenario logs supplied; AI/Actions executions remain separately attributed. |
| VAL-01/VAL-02 decision/rationale | PASS 9/9 participant and 10/10 organiser scenarios; ACCEPTABLE_WITHIN_SCOPE for classroom preparation/cutoff/session model. See HF-02/03/07 and limitations. |
| Actual feedback/edits/rejected suggestions/risk judgement | Six original feedback items plus later actual supplemental HF-07 below. Scoped timing/session/safety rationale supplied; no personal edits, rejected suggestions or new numerical risk ratings supplied. |
| L6 loop decision | ACCEPT_LOOP by explicit project-author declaration; acceptance-record changes only. |
| Main merge | NOT_AUTHORISED/PENDING; separate reviewed-main evidence and decision. |
| Formal v1.0 tag/GitHub Release | NOT_AUTHORISED/PENDING; separate ACCEPT_RELEASE required. |
| L7 | NOT_STARTED / HELD_BY_AUTHOR; no new-loop authority. |

## Current human acceptance

Reviewer: project author. Declaration received on 19 November 2026 (Asia/Shanghai, UTC+08:00); this date is the receipt date, not an invented exact execution timestamp. Accepted candidate: [5c1e3ff92168b34397e2bee2ace85431ae4d124e](https://github.com/Ray-Yan-Rui-14793817/cp5401-outdoor-workshop-booking-waitlist-management-system/commit/5c1e3ff92168b34397e2bee2ace85431ae4d124e), the preceding delivered L6 branch target and local ZIP. The subsequent commit records acceptance and changes documentation only. Its own HEAD/CI/artifact and archive-byte checks are reported in the delivery receipt; this record does not substitute that future SHA for the candidate the author actually inspected.

The author explicitly states completion of L6 UI, H01-H07 and VAL-01/02 and supplies ACCEPT_LOOP. All nine submitted participant and all ten submitted organiser scenarios passed according to that actual declaration. This is author-reported personal validation, distinct from automated tests and AI-operated browser observations. No individual scenario execution log, external-tester identity, exact personal command/time, personal code edit or rejected suggestion was supplied; none is inferred.

The original acceptance message contains six substantive feedback items and an empty numbered item 7. That blank is preserved as a disclosure, not fabricated feedback and not an incomplete H07. A subsequent message supplies the genuine supplemental L6-HF-07 below. Verbatim feedback follows; wording is retained, including the sixth item's absent terminal full stop.

### L6-HF-01

> The L6 candidate is consistent with the accepted L1–L5 baseline. All 317 tests passed, and the delivery ZIP matches the current GitHub branch. The cloud application and runtime dependencies match the reviewed executable target. The later documentation-only commits are correctly disclosed.

### L6-HF-02

> All nine submitted participant validation scenarios passed. Booking, cancellation and history management are consistent with the requirements. The 24-hour cutoff is acceptable for the classroom prototype, although it restricts late cancellations and must be clearly explained to participants.

### L6-HF-03

> All ten submitted organiser validation scenarios passed. The 24-hour roster freeze helps organisers prepare equipment and activities with a stable participant list. Temporary Session State is acceptable for the single-session demonstration, but not for reliable real-world operations.

### L6-HF-04

> The boundary tests and independent test oracles are appropriate. They distinguish active cancellation from repeated no-op requests, and full capacity from duplicate bookings. The new failure-injection tests strengthen state-integrity verification without weakening existing regression cases.

### L6-HF-05

> Role-based navigation, business permissions and organiser-specific draft isolation work within the declared demo model. Ordinary reruns preserve session data. A separate session and process restart do not provide shared or durable records. These limitations are documented.

### L6-HF-06

> The hosted application has recorded source, dependency and functional verification evidence. Findings L6-F10 and L6-F11 are technically closed for the verified target. The cloud checkout differs from the latest documentation HEAD, but the executable files and dependency locks are unchanged

### L6-HF-07 (subsequent human feedback)

Human Feedback - 24-Hour Cutoff and Outdoor Activity Risks

> The 24-hour cutoff supports preparation for both organisers and participants. It helps organisers finalise equipment and activity arrangements. It also gives participants a clear deadline to plan transportation and review safety instructions.
> Unexpected personal circumstances should be respected. Organisers are not responsible for participants' private emergencies, although unexpected absences may affect actual attendance.
> A confirmed booking does not guarantee attendance or require participants to take part when it is unsafe. The system manages booking records rather than actual attendance.
> Decision: ACCEPTABLE_WITHIN_SCOPE.

### Feedback dispositions and scoped risk decision

| Feedback | Recorded decision/implication |
|---|---|
| L6-HF-01 | Author accepts candidate traceability, baseline/317-test/ZIP consistency, reviewed cloud executable/lock parity and disclosure of later documentation-only commits. The documentation head is not labelled as the observed deployed checkout. |
| L6-HF-02 | VAL-01 PASS 9/9, ACCEPTABLE_WITHIN_SCOPE. Retain the strict 24h policy; clearly disclose late-cancellation restrictions. |
| L6-HF-03 | VAL-02 PASS 10/10, ACCEPTABLE_WITHIN_SCOPE. Stable rosters support equipment/activity preparation; single-session memory is accepted only for the classroom demonstration. |
| L6-HF-04 | Independent active/no-op and full/duplicate oracles and added final-State failure checks are substantively reviewed; no regression assertion is weakened and no human scenario is added to pytest counts. |
| L6-HF-05 | Role menus/business permissions, organiser draft isolation and reruns accepted in the declared selectable-identity model. Independent sessions/restart do not provide shared/durable records or real authentication. |
| L6-HF-06 | F10/F11 technical closure accepted for observed cloud 2cad4b53899f5827c0d51cfb298c49f704d77b6b, Python 3.12.16, Arrow 24.0.0 and all 34 runtime pins. Later documentation-only HEAD differences remain explicit. |
| L6-HF-07 | Additional actual human decision ACCEPTABLE_WITHIN_SCOPE for preparation, transport and safety needs. Unexpected personal circumstances are respected; bookings manage records, not guaranteed attendance or unsafe participation. No cancellation override, attendance feature, new requirement or risk-free real-world claim is introduced. |

R-08 baseline timing/information/session suitability is ACCEPTABLE_WITHIN_SCOPE for the classroom prototype, based on actual author feedback and declared task completion. The retained 24h policy restricts late confirmed cancellation; absences can still occur. V1.1 delayed promotion awareness, preparation/arrival feasibility and waiting withdrawal/comprehension (VAL-03A-03E) remain VALIDATION_PENDING / DEFERRED_TO_V1.1. This is a scoped human judgement, not blanket closure of R-08 or a newly invented numerical residual-risk rating.

**Decision: L6 ACCEPT_LOOP. L7 NOT_STARTED / HELD_BY_AUTHOR. Main merge, formal v1.0 tag, GitHub Release and V1.0 publication NOT_AUTHORISED. ACCEPT_LOOP does not represent ACCEPT_RELEASE.** Keep the existing local and hosted services available. The author retains separate next-loop, merge and release decisions.

## Current technical candidate and gate

APPLICATION_AND_RUNTIME_LOCK_PARITY_VERIFIED; DOCUMENTATION_ONLY_CHECKOUT_DELTA_EXPLICIT. F10/F11 remain closed for the verified executable target, without claiming that the actual cloud checkout equals a later documentation HEAD. L6: ACCEPT_LOOP by the author on 19 November 2026; UI/H01-H07 complete, VAL-01 9/9 and VAL-02 10/10 accepted within classroom scope. R-08 baseline timing/session suitability is ACCEPTABLE_WITHIN_SCOPE; V1.1 waiting/promotion validation remains pending. L7: NOT_STARTED / HELD_BY_AUTHOR. Main merge, tag and V1.0 release: NOT_AUTHORISED; ACCEPT_LOOP is not ACCEPT_RELEASE.

Accepted-candidate CI: [run 44284607153](https://github.com/Ray-Yan-Rui-14793817/cp5401-outdoor-workshop-booking-waitlist-management-system/actions/runs/44284607153) tests 5c1e3ff92168b34397e2bee2ace85431ae4d124e; job 134733904416, Python 3.12.16, 317 passed in 55.10s, zero failures/errors/skips, one job/all 18 steps successful. Runtime/development audits cover all 34/71 pins without known vulnerabilities or omissions. Artifact 14418996361 (quality-checks-44284607153-1) was independently checked for digest/CRC, exact tested SHA, all 317 case identities, quality reports and all 34 installed runtime versions. This accepted candidate and subsequent acceptance-record heads have unchanged executable/test/lock/workflow files relative to the observed cloud checkout. The records-only acceptance commit receives a separate exact-head Actions/artifact check; this run is not relabelled as that later result.

REVERIFIED at 18 November 2026 18:07:04 UTC+08:00 from a newly generated cloud runtime record. Actual checkout SHA is 2cad4b53899f5827c0d51cfb298c49f704d77b6b; review intake HEAD is 78cdce5ce906ea0f42aad03cb346e21ccf0c0c16. They are NOT the same Git commit. GitHub comparison establishes that the intake is one commit ahead with exactly six modified Markdown files; all runtime/test/dependency/configuration/workflow blobs are unchanged. Cloud SHA256 of app.py, booking.py and requirements.txt exactly matches the current L6 branch, Python is 3.12.16, Streamlit is 1.67.0, and all 34 installed runtime pins match requirements.txt, including PyArrow 24.0.0, with zero missing/version differences. F10/F11 remain technically closed for the verified executable/lock target; literal checkout-versus-documentation-HEAD equality is explicitly not claimed. No new server reboot is performed in this review. Later evidence-only heads are checked for the same non-runtime delta and have their own CI. At this 18 November technical stage, human validation and ACCEPT_LOOP were still pending. The author supplied UI/H01-H07 completion, VAL-01/02 results and ACCEPT_LOOP on 19 November; the current human acceptance record supersedes that gate. Merge/tag/release remain NOT_AUTHORISED.

The author supplies H01-H07 completion, actual VAL-01/02 feedback, scoped risk reasoning and ACCEPT_LOOP as recorded above. This accepts L6, not a formal V1.0 release. Retain existing local/cloud services and the aligned preview; keep ZIP personal/local. Technical verification, human acceptance, merge approval and release approval remain four distinct evidence/decision boundaries.

## Exit and release preparation

Stop at L6. Do not merge main, create v1.0, publish a Release or enter L7/CR-01. Resolve any material technical finding and genuine validation issue before a later human release decision; verify reviewed-main CI/deployment if explicitly authorised then. Preserve a released V1.0 baseline before the assessed change.

Prepared release scope, not a publication: fixed fictional roles, valid outdoor workshop creation/browsing, serial booking/own cancellation/history/new-ID replacement and owned rosters, strict creation/C policy and capacity 1-30. Disclose temporary unshared state, no authentication/notifications/waitlist and managed environment limits. The author retains the release decision.
