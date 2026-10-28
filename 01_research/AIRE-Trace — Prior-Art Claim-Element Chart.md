# AIRE-Trace — Prior-Art Claim-Element Chart

**Subject:** Level-B mechanism for *intervention-conditioned future-capability preservation*
**Date:** 2026-09-04
**Analyst status:** prior-art gate only. No implementation performed. No filing decision made.
**Evidence level:** LEVEL 1 for every cell below (each is read directly from the cited publication page in this session). Absence of a feature is recorded as NOT DISCLOSED **on the pages read**, which is not the same as proof of non-existence anywhere in the reference.

---

## 0. Verdict

**KILL** — as a patent candidate.

Exactly one element of the ten survives the chart as not disclosed by any reference: **Element 5, estimation of future task-completion capability conditioned on an intervention-transformed state, without executing the intervention.** Every other element is disclosed, and several references disclose multiple elements *in combination*. Element 5 fails the inventive-step test as an obvious substitution across four references that are each already doing the neighbouring step (Section 4).

The research and final-year value of AIRE-Trace is unaffected and is addressed in Section 6.

---

## 1. Reference set (all verified to exist)

| Short name | Full title | ID | Date | Notes |
|---|---|---|---|---|
| **EvoUndo** | Recoverability-Constrained Self-Evolution for LLM Agent Harnesses | [arXiv:2608.28363](https://arxiv.org/html/2608.28363v1) | 28 Aug 2026 | CC BY 4.0. Sah, Sah, Jain, Sah |
| **AgentRewind** | Recoverable Execution for Long-Horizon LLM Agents | [arXiv:2608.14380](https://arxiv.org/html/2608.14380v1) | 14 Aug 2026 | |
| **AgentTether** | Graph-Guided Diagnosis and Runtime Intervention for Reliable LLM Agent Operation | [arXiv:2607.06273](https://arxiv.org/abs/2607.06273) | 7 Jul 2026 | Zhao et al., incl. Microsoft authors |
| **StateFork / Waypoint** | Toward Systems Foundations for Agentic Exploration; Waypoint checkpoint/restore | [arXiv:2510.05556](https://arxiv.org/abs/2510.05556); [DAPLab Waypoint](https://daplab.cs.columbia.edu/projects/waypoint/) | 7 Oct 2025; page posted 1 Jun 2026 | Columbia DAPLab |
| **2602.03338** | Accurate Failure Prediction in Agents Does Not Imply Effective Intervention | [arXiv:2602.03338](https://arxiv.org/html/2602.03338v1) | Feb 2026 | disruption–recovery tradeoff |
| **DreamGuard** | Efficient Runtime Guardrail for LLM Agents via Risk-Aware World Model | [arXiv:2608.05695](https://arxiv.org/html/2608.05695v1) | 6 Aug 2026 | |
| **CORA** | Conformal Risk-Controlled Agents for Safeguarded Mobile GUI Agents | [arXiv:2604.09155](https://arxiv.org/html/2604.09155v1) | Apr 2026 | |
| **ToolChain-CRC** | Conformal Risk Control for Agentic AI Under Retrieval and Tool-Use Drift | [arXiv:2606.18467](https://arxiv.org/html/2606.18467) | 16 Jun 2026 | |
| **FailFast-RestartSmart** | Fail-Fast, Restart-Smart: Early Failure Prediction and Restart for SWE Agentic Tasks | [arXiv:2608.03222](https://arxiv.org/html/2608.03222v1) | 4 Aug 2026 | |
| **ERR** | Recoverability Has a Law: The ERR Measure for Tool-Augmented Agents | [arXiv:2601.22352](https://arxiv.org/html/2601.22352v1) | Jan 2026 | |
| **RTDR** | Real-Time Detection and Repair of LLM Agent Failures | [arXiv:2608.02464](https://arxiv.org/html/2608.02464v1) | 3 Aug 2026 | |
| **PAINT / tacit** | When to Ask for Help: Proactive Interventions in Autonomous RL; Tracking Capabilities for Safer Agents | [alphaXiv 2603.00991](https://www.alphaxiv.org/abs/2603.00991) | 2026 | reversibility / capability typing |
| **Agentic Abstention** | Do Agents Know When to Stop Instead of Act? | [arXiv:2606.28733](https://arxiv.org/abs/2606.28733) | 27 Jun 2026 | |

Note on nomenclature: "RAIL" resolves to responsible-AI guardrail work ([RAIL Guard, arXiv:2607.16215](https://huggingface.co/papers/2607.16215)) that does not touch capability preservation; it is not material and is excluded from the chart.

---

## 2. Claim-element chart

Legend: **D** = disclosed, **P** = partial, **N** = not disclosed.

| # | Element | Our proposed Level-B mechanism | EvoUndo | AgentRewind | AgentTether | StateFork/Waypoint | 2602.03338 | DreamGuard | CORA / ToolChain-CRC | FailFast-RestartSmart | ERR | RTDR |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | **State acquisition** | prefix events from recorded trajectories, plus live checkpoint at decision boundary | **D** — witness capture `w:S→W`; `E(m,s)=SnapshotDiff ∪ ExecutionTraceEffects`; SHA-256 canonicalisation | **D** — aligned checkpoints `d_t=(c_t,s_t)` at LLM/tool hooks | **P** — runs abstracted into Transition Units; mechanism unstated | **D** — CRIU process checkpoint + OverlayFS filesystem deltas; 6 snapshot/restore mechanisms benchmarked | **D** — paired matched runs from identical initial conditions | **P** — pre-action hook, `x_t=(e,H_t,a_t)` | **D** — per-step screenshot, UI tree, action, episode id, frozen goal | **D** — replays bash commands, `git diff HEAD` snapshots per command | **P** — states `s_t`, perturbations `δ_t∼F(s_t,a_t)` | **D** — per-step telemetry `x_t=[e_t;u_t;m_t]`, 674 µs/step median; committed JSONL traces + seed |
| 2 | **Context / environment / tool / task representation** | `Z_t=(C_t,E_t,T_t,P_t,G)` | **D** — config, prompts, routing, tool registry, middleware, listeners, files, resources; objective `J` | **D** — agent context `c_t` + controlled environment `s_t`, tool calls and results | **P** — Critical Transition Graph; components not enumerated | **P** — files, sockets, cloud APIs | **P** — task, step budget, intervention budget | **D** — instruction `e`, observations `o_t`, action `a_t`, prefix `H_t`, latent `s_t=(h_t,z_t)`; Qwen3-4B layer-31, 2560-d, latent 1024/32×32 | **D** — `(g,o_t,h_t,â_t)` incl. frozen user goal | **D** — value/F2P/P2P heads over trajectory prefix | **P** — `π_θ(a_t|s_t)`, tool-call outcomes | **P** — 32-d char-3-gram embedding, surprisal aggregates, 8 behavioural + 9 grounding dims |
| 3 | **Intervention transformation** | `I : Z_t → T_I(Z_t)` for RESET / REWIND_δ / BRANCH / MODIFY_ACTION | **D** — forward mutation `m:S→S'`; recovery program `u`; candidate `ξ=(m,w,u,C_e)` | **D** — rewind to checkpoint `k`, restore `s_k` and `c_k`, inject rewind memory, `backtrack_candidates` / `backtrack_commit` | **P** — guarded runtime intervention during re-execution | **P** — branch, backtrack, fork semantics | **D** — ROLLBACK and APPEND | **P** — PASS / HOLD / BLOCK only; explicitly not replacement actions | **P** — Execute / Abstain; Abort, Confirm, Reflect, takeover | **D** — overlay `Δ` from cumulative git diff, applicable or removable via `git apply` | **N** | **D** — rollback + re-run rungs: resample, located, generic, specific, recompute, adaptive |
| 4 | **Counterfactual / transformed state** | construct `T_I(Z_t)` and reason over it | **D** — round trip `s→z→s'→ŝ`; 10 dev + 40 hidden counterfactual states (20 IID, 20 OOD); 100-state holdout suite | **P** — restores state and replays retained prefix from log without re-firing side effects | **P** — correction re-applied during re-execution | **P** — branching across execution paths | **D** — obtained by paired live re-execution from identical initial conditions | **D — without execution** — predicted successor latent `ŝ_{t+1}=(h_{t+1},ẑ_{t+1})` via learned dynamics predictor | **N** | **P** — overlay available in fresh rollout, explicitly unverified | **N** | **D** — rollback to same checkpoint, re-execute, paired on identical prefix and task |
| 5 | **Future capability estimation conditioned on the transformed state, without executing** | `Ĉ_π(T_I(Z_t),G)` | **N** — capability judged by executing `J_t(m(S))` | **N** | **N** | **N** | **N** — aggregate `r`, `d` measured by execution, not predicted per state | **N** — estimates hazard `p_t^haz` and prefix risk `p_t^pre`, **not** task completion | **N** — Guardian estimates harm risk of the proposed action only | **N** — predicts failure of the *current* trajectory, not of the intervened branch | **P** — analytic law `ERR ≤ (1−ES)/(1−γ)` and the statement that a controller "can estimate whether a plan lies in a recoverable regime before executing it"; no per-state candidate-intervention predictor | **N** — anomaly score, not completion probability |
| 6 | **Compare intervention vs baseline** | per-state `ΔC_π(I,z_t,g)` by estimation | **P** — paired task-level contrasts `D₁L₀ vs D₀L₀` etc.; aggregate rescue rates 0/197, 38/197, 180/197, 167/197 | **N** | **P** — repair rate vs initially failed tasks | **N** | **D — aggregate** — `ΔSuccess = p·r − (1−p)·d`; recovery = baseline fails/intervention succeeds; disruption = baseline succeeds/intervention fails | **N** | **P** — aggregate: GAR 89.69% vs 72.22%, IF1 85.29% vs 39.56% | **D — aggregate** — vanilla vs cold restart vs overlay; ΔRes. +5.2 pp at 25% FPR | **N** | **D — per-state paired** — same checkpoint, identical prefix and task, vs untouched and vs resampling control |
| 7 | **Preservation criterion** | `ΔC_π ≥ −ε` | **D** — admission requires `ΔJ>0`, `(w,u)∈L`, `E(m,s)⊆C_e`, `ŝ≃_{C_e}s`, 10/10 dev states, and `LCB_0.95(k,n) ≥ τ_R = 0.85` over 40 hidden counterfactuals, fail-closed | **N** | **N** | **N** | **D** — deploy only if `p > d/(r+d)`; avoid steps 0–1; `min_step ≥ 2`; if `d/r>1` prefer post-hoc selection | **D** — `BLOCK if p^haz ≥ λ_block; HOLD if S_t ≥ λ_hold; else PASS`, thresholds by split-conformal quantile `λ_hold = M_(k)`, `k=min(⌈(n+1)(1−α)⌉,n)` | **D** — CRC: `τ̂ = sup{τ : (Σ L(Z_i;τ)+1)/(n+1) ≤ α}`, `L(Z_t;τ)=ℓ(Z_t)1{s_t≤τ}`, target `E[L]≤α`, α=0.01; ToolChain-CRC same form on trajectory risk | **P** — operating point by grid search maximising recall subject to target FPR | **P** — recovery-aware gating discussed, no threshold given | **N** — detection threshold `θ=Q_{1−β}(max_t s_t)` only |
| 8 | **Per-state accept/reject, pre-execution** | admit/block/select candidate `I` by estimate | **P** — per-state verification **by execution**, not estimation; only a syntactic language gate is pre-execution | **N** — agent-initiated rewind after observing being stuck | **N** | **N** | **N** — decision is population-level go/no-go | **D — by estimation** — PASS/HOLD/BLOCK before every tool invocation, no trial execution | **D — by estimation** — `e_t(τ̂)=1{s_t ≤ τ̂}` per proposed action, learned scalar risk head, no trial execution | **P** — per-step abort vote, Count-M / Sustained-K, `φ_min=20` steps | **N** | **P** — per-step alarm `τ̂=min{t: s_t>θ}`, then repair |
| 9 | **Technical execution mechanism** | AIRE-Trace prefix harness + capability estimator + gate | **D** — locked `m₀`, witness store + recovery AST, 393.6 B mean storage vs 1165.0 B full snapshot | **D** — LLM-call and tool-call hooks, ~150–300 LOC per harness, 3 harnesses | **P** — offline diagnostic or online repair layer, no agent/env modification | **D** — CRIU + OverlayFS, named checkpoints, CLI, backend for StateFork | **D** — Qwen3-0.6B LoRA r16 critic, τ=0.6, temperature scaling, 15-step budget, 3 interventions/episode | **D** — recurrent risk-aware world model, frozen Qwen3-4B, split-conformal calibration | **D** — post-policy pre-action shield, VLM backbone + risk head `s_t=σ(Wz_t+b)`, base policy unmodified | **D** — Qwen3-0.6B LoRA, 3 heads, Platt scaling, meta-score `p_fail=σ(wᵀ[v,ĝ_f,φ]+b)` | **D** — analytic law + Monte Carlo rollout validation | **D** — runtime adapter, 674 µs/step, per-episode JSONL + manifest with checksum |
| 10 | **Demonstrated technical effect** | not demonstrated | **D** — 197 capability-positive but non-recoverable mutations of 600; 0/197 → 180/197 rescued | **D** — reported recovery gains | **D** — 261 tau-bench tasks; Banking repairs 59.04% (49/83) Qwen3.7-max, 65.12% (56/86) GPT-5.4 | **P** — Pass@20 in under 10 min; CRIU/container commits "not fast enough" | **D** — quantified disruption vs recovery on ALFWorld, 50-task pilot | **D** — SR/F1/FPR/latency, PHIR, MAS; 100-case online set, 48 unsafe / 52 benign | **D** — GAR 89.69%, HR 2.19%, OIR 9.83%, calibration n=1075 | **D** — resolve rate 66.6% → 71.8% | **P** — law validated against observed ERR | **D** — 55 episodes: located repair 45% vs resample 16%; over 120 episodes success 52% → 73%, 25 failures recovered, **zero correct runs broken** |

---

## 3. Which elements are already known, and where they are combined

- **Elements 1–4, 6, 7, 9, 10 are all individually disclosed.** No single element of the candidate is new.
- **Elements 3+4+7+8 combined in one reference: EvoUndo.** It defines interventions as state transformations, constructs counterfactual states, applies a statistical preservation criterion with a Wilson lower confidence bound at 0.85 over 40 hidden states, and gates admission of the change. It differs only in *how* the criterion is evaluated: by executing the recovery round trip, not by estimating an unexecuted outcome.
- **Elements 7+8 by estimation, combined: CORA and DreamGuard.** Both make a per-state, pre-execution accept/reject decision from a learned estimate with a conformal threshold and no trial execution. CORA gives distribution-free control of the accepted-risk rate.
- **Elements 3+4+6 at per-state paired granularity: RTDR.** It rolls back to the same checkpoint and re-runs paired on the identical prefix and task, and reports that its located-repair policy broke zero correct runs — i.e. it already measures the capability-destruction quantity empirically.
- **Element 6 formalised as the exact tradeoff our candidate targets: 2602.03338.** `ΔSuccess = p·r − (1−p)·d` with recovery and disruption defined from paired matched runs.
- **Element 4 without execution: DreamGuard.** A learned world model produces the successor latent state for a proposed action and scores it before execution.

**Collateral finding.** FailFast-RestartSmart selects its operating point by "maximise recall subject to a target FPR" — the same threshold procedure as the AIRE-Trace frozen protocol (maximise Recall subject to FAR ≤ 5%). The threshold procedure itself therefore carries no novelty.

---

## 4. The one uncovered element, and why it does not survive inventive step

**Uncovered:** Element 5 — a mechanism that, given state `Z_t` and candidate intervention `I`, estimates `Ĉ_π(T_I(Z_t),G)`, the probability of eventual task completion from the intervention-transformed state, *without executing the intervention*, and gates on `ΔC_π ≥ −ε`.

Nothing read discloses this. The nearest approaches each stop one step short: DreamGuard predicts a successor state without executing but scores harm rather than completion; FailFast predicts eventual failure of the current branch, not the intervened branch; EvoUndo evaluates preservation but by execution; ERR predicts recovery regret at policy level from observed efficiency, and only gestures at ex-ante regime checking.

**Why this is an obvious combination rather than an inventive step:**

1. The transformation `T_I` is supplied ready-made by AgentRewind, RestartSmart, and Waypoint.
2. The supervision label is supplied ready-made by 2602.03338 and RTDR: a disruption is exactly "baseline succeeds, intervention fails" on paired runs from the same state.
3. The pre-execution estimator architecture is supplied ready-made by DreamGuard, which already predicts an unexecuted successor state and scores it, and by FailFast, which already trains a small LoRA head on eventual-outcome labels.
4. The gate is supplied ready-made by CORA and ToolChain-CRC as conformal risk control with a distribution-free bound on the accepted-loss rate.

Reaching Element 5 requires only substituting the training label in a known estimator (hazard → eventual completion), pointing it at a known transformed state, and reusing a known thresholding procedure. Each component is used for its established purpose with a reasonable expectation of success. Under Indian practice this compounds with **Section 3(k)**: with no technical effect beyond a better prediction and a better decision rule, the claim reads as an algorithm and a computer program per se.

**Additional blockers independent of the legal analysis:**

- **No supervision data, and no feasible route to it.** Training the estimator needs paired live re-runs of Terminal-Bench tasks under each candidate intervention. The comparable studies used 50 ALFWorld tasks and 55 episodes × 3 repeats. The project has 636 recorded episodes with no intervention arm and no checkpoint state.
- **The infrastructure route is also blocked as an invention.** Waypoint's own benchmark of six snapshot/restore mechanisms reports that CRIU and container commits "are not fast enough even in isolated testbeds" and "crumble entirely in real deployments." Controlled replay is therefore both published and hard.
- **State sufficiency is still unproven, and the project's own evidence is discouraging.** Gate X measured M1 AUROC 0.6399 and showed M4 behaving as a static difficulty prior. There is no evidence the current representation supports estimating a *harder* quantity than the one it already estimates poorly.

---

## 5. Answers to the five questions posed

1. **What each reference discloses** — Section 2.
2. **Which elements are already known** — all except Element 5.
3. **Which elements are combined in the same reference** — Section 3; EvoUndo, CORA, DreamGuard and RTDR each carry multi-element combinations.
4. **What remains uncovered** — Element 5 only.
5. **Is it new or an obvious combination** — obvious combination; Section 4.
6. **Does it produce a concrete technical effect** — not demonstrated, and not demonstrable with the data the project holds.

**Level A** (the conceptual question "will intervention preserve future capability?") is fully occupied by 2602.03338, EvoUndo and RTDR. **Level B** (a distinctive computational mechanism) does not survive.

---

## 6. What this does not kill

The following remain intact and are the honest basis for the final-year deliverable:

- The leakage-controlled, prefix-only, episode-aware **evaluation protocol** is unaffected. None of the references above evaluates warning methods prospectively at prefix level under a frozen calibration-only threshold with episode-cluster bootstrap.
- The Gate X negative results are now **externally corroborated**: 2602.03338 independently establishes that prediction accuracy does not imply intervention value, which strengthens rather than weakens the project's own finding that M4 is a static difficulty prior.
- There is a defensible research contribution in **evaluating the disruption–recovery question prospectively**: 2602.03338 estimates `r` and `d` as aggregate post-hoc rates; no reference read here provides a prefix-level, leakage-controlled, episode-aware evaluation protocol for *when* intervention gating is admissible. That is an evaluation contribution, not a patent.
- Public disclosure has not occurred, so nothing has been forfeited by this decision.

---

## 7. Recorded limitations of this chart

- Coverage is limited to the publications listed in Section 1, read via their public pages in one session. No patent-database search was performed against IPO, USPTO, EPO, or WIPO full-text; a KILL verdict does not require it, but a SURVIVES verdict would have.
- Element-level absences are "not disclosed on the page read," not proof of absence.
- This is not legal advice. Any filing decision, and any Section 3(k) conclusion, requires a qualified Indian patent professional.


## RAIL (Recoverability-Aware Intervention Learning) Candidates
| Reference                      | What It Discloses                                                             | Candidate Killed       |
| ------------------------------ | ----------------------------------------------------------------------------- | ---------------------- |
| EvoUndo (arXiv:2608.28363)     | Round-trip recoverability verification (mutate → recover → check equivalence) | Candidate 1            |
| AgentRewind (arXiv:2608.14380) | Checkpoint/restore for agent recovery                                         | Candidate 1            |
| PAINT (ICML 2022)              | Reversibility estimation + proactive intervention                             | Candidate 2            |
| Doyle 1979 (TMS)               | Justification-based belief revision                                           | Candidate 4            |
| de Kleer 1986 (ATMS)           | Assumption-based truth maintenance                                            | Candidate 4            |
| BLIP (arXiv:2608.25210)        | Minimal verifiable provenance for black-box LLM                               | Candidate 5            |
| Gupta/Mumick 1993 (IVM)        | Incremental view maintenance                                                  | Candidate 6            |
| RAIL (arXiv:2608.05080)        | Recoverability-aware intervention learning                                    | Counterfactual revival |

FailFast (arXiv:2608.03222) — baseline for comparison


## Additional Validation & Early-Alerting Candidates
| Reference                      | What It Discloses                                                             | Candidate Killed       |
| ------------------------------ | ----------------------------------------------------------------------------- | ---------------------- |
| Verified Tool Calls (2608.02645)| Postcondition verification for non-atomic tool failures                       | TBD                    |
| PlanFence (arXiv:2609.03340)   | Dependency-scoped validation for distributed memory to prevent stale plans    | TBD                    |
| FreshCtx                       | Runtime freshness boundary to verify evidence before action execution         | TBD                    |
| Sparse-Evidence Alerting       | Attention-based early failure alerting using sparse signals                   | TBD                    |
| ACRFence                       | Semantic rollback attacks from regenerated tool calls                         | TBD                    |
| E-valuator                     | False alarm rate control via sequential hypothesis testing (e-processes)      | TBD                    |
| Silent Semantic Violations     | Identification of failures that break semantic guarantees without loud errors | TBD                    |


## Capability and Verification Candidates

| Candidate                          | Mechanism Investigated                                   | Directly Verified References                             | Exact Collision                                       | Remaining Uncertainty          | Status     |
| ---------------------------------- | -------------------------------------------------------- | -------------------------------------------------------- | ----------------------------------------------------- | ------------------------------ | ---------- |
| 1. Intervention-conditioned future-capability preservation | Estimate Ĉ_π(T_I(Z_t),G) without executing intervention | EvoUndo (2608.25210), AgentRewind, DreamGuard, CORA/ToolChain-CRC | Joint elements disclose all components except unexecuted estimation; that gap is obvious mechanical substitution (swap training label, reuse known estimator/gate) | None significant | ❌ KILLED |
| 2. Recovery-Option Preservation / Recovery Frontier | Preserve future recovery/control options; safety boundary crossing | Viability kernels, reachability-based safety, control-barrier functions (classical control theory); PAINT | Structurally identical to decades-old control-theory primitive | None significant | ❌ KILLED |
| 3. Capability-Gap Diagnosis | Diagnose specific capability deficit causing failure | — | No ground-truth deficit labels exist in dataset (unfalsifiable); live-execution testing required is out of project scope | Feasibility, not prior art | ❌ KILLED |
| 4. Decision-Support Integrity / selective revalidation | Justification/dependency graph, invalidate only affected subgraph | Doyle (1979) TMS, de Kleer (1986) ATMS | Identical computational pattern to classical Truth Maintenance Systems | None significant | ❌ KILLED |
| 5. Minimal observable support / provenance | Minimal sufficient subset of evidence supporting an LLM output/action | Database why-provenance/witness theory; BLIP (2608.25210, verified) | BLIP discloses minimal-subset-for-black-box-LLM-output as its core contribution | None significant | ❌ KILLED |
| 6. Action-Admissibility Invariance | Minimal recomputation needed after state change | Gupta/Mumick/Subrahmanian (1993) Incremental View Maintenance | Identical delta-recomputation objective | None significant | ❌ KILLED |
| 7. Semantic Execution Checkpointing / state minimization | Determine necessary/reconstructable/disposable agent state | Crab, StateFork/Waypoint, EvoUndo, 2025 "Semantic Checkpointing Mechanisms for Stateless LLM Agents", HORMA, PABU | Crab: 87% checkpoint-traffic reduction via semantics-aware selection; semantic checkpointing literature already stores task-relevant meaning; HORMA/PABU already do minimal-sufficient-context retention | None significant | ❌ KILLED |
| 8. Post-restore action divergence prediction | Predict whether regenerated action diverges from checkpoint-time action before restoration | ACRFence | ACRFence already performs reactive replay-or-fork detection of exactly this divergence; predictive framing is an obvious timing shift | None significant | ❌ KILLED |
| 9. dyn_comp as generic mechanism / residual-risk decomposition | Static-vs-dynamic model subtraction + threshold | Biostatistics landmarking/dynamic-prediction literature; general residual-anomaly-scoring patent (video anomaly detection); RAIL (2608.05080, verified — different domain, not direct collision); Weakly Supervised Early Failure Alerting; "Monitoring Web Agents Without Internal Signals" (Sept 2026); AgentTrajectorySentinel; DECIDER (model disagreement); DA-LCE (difficulty conditioning); US20110161048A1 (2011, threshold-violation-from-baseline-deviation, granted patent) | Individual components (partial-prefix prediction, difficulty conditioning, residual/deviation scoring, FAR-constrained thresholding) each independently disclosed across multiple recent and older references; obviousness-by-combination risk is substantial even though no single reference discloses the exact combination verbatim | Exact combination not found disclosed verbatim; formal legal obviousness determination not made | NARROW CANDIDATE — SUBSTANTIAL RISK, NOT KILLED, NOT CONFIRMED |


### Note on Additional Axes

Additional axes also searched and killed during the same investigation: calibration/statistical-integrity mechanisms, environment-staleness/dependency-freshness, multi-agent concurrency/contention, benchmark/evaluation-protocol construction, terminal/CLI shell-execution semantics — collision references include CoAgent, DPBench, Semantic Consensus/SCF, E-valuator (verified Level 1), and the "silent semantic violations" systems-research lineage (Lou et al., OSDI '22/'25) plus TOCTOU/idempotency-key literature as foundational background.


## Candidate 9 (dyn_comp) Patent Search Results

The following patents were searched and evaluated against the specific mechanism of 'trajectory-dependent risk decomposition / isolating trajectory risk from task-difficulty risk'.

| Patent | Title | Key Difference from Target Mechanism |
|---|---|---|
| US12441366B2 (Nvidia, 2025) | Task-relevant failure detection for trajectory prediction in machines | Detects failures in trajectory predictors using cost probability distributions; does not isolate trajectory risk from task-difficulty risk. |
| US12202518B2 (Nvidia, 2025) | Safety decomposition architecture for autonomous machine applications | Uses 'safety decomposition' for ASIL compliance in trajectory selection, not failure risk decomposition for warning systems. |
| US20230192139A1 | Method and system for addressing failure in an autonomous agent | Covers failure detection and response in autonomous vehicles, but not trajectory-dependent risk decomposition. |
| US #63/841,017 (pending) | System and Method for Predictive Failure Detection in AI Agent Workflows | Covers predictive failure detection for AI agents, but focuses on cross-user contamination analysis, not trajectory-dependent decomposition. |
| US20200174481A1 (Waymo, 2020) | Probabilistic risk assessment for trajectory evaluation | Evaluates trajectory risk using heat maps and overlap probabilities for autonomous vehicles; no task-difficulty decomposition. |
| US12450494B1 (2025) | Validating autonomous artificial intelligence (AI) agents using generative AI | Maps actions to risk categories based on task sensitivity, but doesn't separate trajectory-dependent from task-difficulty risk. |
| US12296849B2 (2024) | Method and system for feasibility-based operation of an autonomous agent | Scores policies based on feasibility for agents in environment; focuses on intention estimation, not risk isolation. |
| WO1994029983A1 (1994) | Performance monitoring and failure isolation in communications networks | Isolates equipment failures in networks through error distribution analysis; unrelated to trajectory or task-difficulty risk. |
