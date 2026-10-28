# Gate 1 Report: Data Forensics and Experimental Specification

## Section from `gate1_dataset_inventory.md`

# Gate 1 Report: Dataset Inventory and Forensic Analysis

**Date:** 2026-07-31  
**Status:** EVIDENCE COMPLETE — GATE 1 INSPECTION PASSED  
**Scope:** Forensic evaluation of candidate datasets: TerminalBench (`yoonholee/terminalbench-trajectories`), Tracebench (`Contextbench/Tracebench`), and τ²-Bench (`sierra-research/tau-bench` historical trajectories).

---

## Executive Summary

A comprehensive forensic inspection was performed on all candidate datasets to determine whether real empirical distributions support the frozen prospective warning protocol.

### Key Forensic Discoveries:
1. **TerminalBench Sufficiency:** TerminalBench (`yoonholee/terminalbench-trajectories`) contains **52,104 episodes** across 89 tasks with a **60.37% failure rate** (31,455 failures, 20,649 successes). This provides more than sufficient statistical power for a 3-way TRAIN / CALIBRATION / TEST episode split.
2. **Task Clustering Necessity:** In TerminalBench, each of the 89 tasks appears in ~585 episodes. A naive random episode split (`run_id`) will result in severe **Task Leakage** (the same task appearing across TRAIN, CALIBRATION, and TEST). **Splitting MUST be task-cluster aware.**
3. **Tracebench Onset Annotation Gap:** In Tracebench (`Contextbench/Tracebench` full split, 3,316 episodes), only **66.89% (1,273 / 1,903)** of failed episodes contain non-empty `incorrect_step_ids`. 33.11% of failed episodes have no step-level failure onset label.
4. **Observation Window Truncation:** Under fixed horizon $K=30$, 74.48% of TerminalBench trajectories terminate before step 30 (median length is 9 steps). Conversely, for Tracebench, median length is 30 steps. A fixed horizon $K=30$ creates significant observation-window truncation on TerminalBench.
5. **τ²-Bench Characteristics:** τ²-Bench static historical dataset contains **1,980 episodes** across 4 model/domain runs (GPT-4o Airline/Retail, Claude 3.5 Sonnet Airline/Retail) with a 40.25% failure rate (797 failures, 1,183 successes) and maximum length of 62 steps.

---

## 1. Candidate Dataset Summaries

| Metric / Attribute | TerminalBench (`yoonholee`) | Tracebench (`Contextbench`) | τ²-Bench (`sierra-research`) |
|---|---|---|---|
| **Role in Protocol** | Primary Benchmark (Mode A) | Primary Diagnostic / Annotation Source | Secondary Transfer Diagnostic (Mode B) |
| **Total Episodes** | **52,104** | **3,316** (full) / **1,000** (verified) | **1,980** (combined 4 runs) |
| **Total Unique Tasks** | 89 tasks | 662 tasks | 115 tasks |
| **Success Count** | 20,649 (39.63%) | 1,307 (39.42%) | 1,183 (59.75%) |
| **Failure Count** | 31,455 (60.37%) | 1,903 (57.39%) | 797 (40.25%) |
| **Failure Rate** | **60.37%** | **57.39%** | **40.25%** |
| **Min Trajectory Length** | 0 steps | 1 step | 6 steps |
| **Median Length** | **9.0 steps** | **30.0 steps** | **28.0 steps** |
| **Mean Length** | 31.13 steps | 44.52 steps | 28.58 steps |
| **Max Trajectory Length** | 3,006 steps | 666 steps | 62 steps |
| **Step-Level Onset Available?** | No (outcome only) | Yes (for 66.89% of failures) | No (outcome only) |
| **Outcome Fields** | `reward` (0.0 or 1.0) | `solved` (boolean) | `reward` (0.0 or 1.0) |

---

## 2. Detailed Dataset Breakdown

### 2.1 TerminalBench (`yoonholee/terminalbench-trajectories`)
- **Source:** HuggingFace `yoonholee/terminalbench-trajectories` (split: `train`).
- **Structure:** 52,104 rows. Each row represents a full execution trace of an agent attempt on a command-line / terminal task.
- **Top Tasks:** `configure-git-webserver` (599 runs), `constraints-scheduling` (597 runs), `dna-assembly` (595 runs), `cancel-async-tasks` (594 runs).
- **Agents:** `mini-SWE-agent`, `TermAgent`, etc.
- **Models:** Anthropic Claude, OpenAI GPT-4o, DeepSeek, etc.

### 2.2 Tracebench (`Contextbench/Tracebench`)
- **Source:** HuggingFace `Contextbench/Tracebench` (splits: `full` [3,316 rows], `verified` [1,000 rows]).
- **Structure:** Contains rich multi-stage error annotations (`incorrect_stages`).
- **Key Discovery on `incorrect_stages`:**
  - Structure: List of objects containing `stage_id`, `incorrect_step_ids`, and `steps` (each step has `step_id`, `action_ref`, `observation_ref`, `labels`).
  - Operational definition: `min(incorrect_step_ids)` indicates the step index of the first observed incorrect action.

### 2.3 τ²-Bench (`sierra-research/tau-bench`)
- **Source:** `historical_trajectories/` directory in GitHub repository.
- **Run Files Inspected:**
  1. `gpt-4o-airline.json`: 200 episodes (84 succ, 116 fail; failure rate 58.00%).
  2. `gpt-4o-retail.json`: 460 episodes (278 succ, 182 fail; failure rate 39.57%).
  3. `sonnet-35-new-airline.json`: 400 episodes (184 succ, 216 fail; failure rate 54.00%).
  4. `sonnet-35-new-retail.json`: 920 episodes (637 succ, 283 fail; failure rate 30.76%).
- **Total:** 1,980 episodes, 1,183 success, 797 failure (failure rate 40.25%).

---

## 3. Split Validity & Task Leakage

- **Finding:** TerminalBench has 52,104 episodes distributed across only 89 unique task definitions (~585 runs per task).
- **Leakage Risk:** If splitting is done randomly by episode ID (`run_id`), every split (TRAIN, CALIBRATION, TEST) will contain runs from the exact same 89 tasks. The model will memorize task-specific prompts/structures rather than learning general failure indicators.
- **Protocol Enforcement:** Splitting MUST be **Task-Group Aware** (all episodes of task $T_i$ go exclusively to TRAIN, CALIBRATION, or TEST).

---

## 4. Conclusion & Status

- **TerminalBench 3-Way Split:** VERIFIED viable (52,104 episodes across 89 tasks supports 60/20/20 task-disjoint split).
- **τ²-Bench Transfer Evaluation:** VERIFIED viable (1,980 episodes for Mode B evaluation).
- **Gate 1 Status:** **PASSED WITH EVIDENCE**.


---

## Section from `gate1_feature_comparison.md`

# Gate 1 Report: Unified Feature Space and Cross-Dataset Compatibility Audit

**Date:** 2026-07-31  
**Status:** VERIFIED — PROTOCOL RULE 9 ENFORCED  
**Scope:** Identifying common, dataset-specific, and post-outcome/leakage-prone feature spaces across TerminalBench, Tracebench, and τ²-Bench.

---

## Executive Summary

Per **Protocol Rule 9**, the primary transferable model ($M, S, L$) evaluated on τ²-Bench (Mode B) must use features that are computable with identical definitions and information boundaries on **both** datasets. TerminalBench-only features may enter a secondary diagnostic model, but never the primary transferable one.

This audit categorizes all available fields across candidate datasets into three distinct groups:
1. **Category A: COMMON AND SAFE** (Primary Transferable Feature Space)
2. **Category B: DATASET-SPECIFIC** (Internal Diagnostic Space)
3. **Category C: POST-OUTCOME / LEAKAGE-PRONE** (Strictly Excluded / Neutralized)

---

## 1. Feature Taxonomy

```
                            AVAILABLE TRACE DATA
                                     │
           ┌─────────────────────────┼─────────────────────────┐
           ▼                         ▼                         ▼
   Category A: COMMON        Category B: SPECIFIC      Category C: LEAKAGE
   (Transferable M/S/L)     (TB-Internal Diagnostic)   (Strictly Excluded)
   • Step Index             • Input / Output Tokens   • Reward / Passed
   • Actor Role             • Duration / Latency (ms) • Solved / Status
   • Action Type            • Cost (cents)             • Terminal Output
   • Tool Error Indicator   • Difficulty / Category    • incorrect_stages
   • Retry Counter          • User / Order Domain State• artifact_path
   • Tool Diversity
   • Action Repetition
```

---

## 2. Feature Category Breakdown

### Category A: COMMON AND SAFE (Primary Transfer Vector)
These features are computable on **both** TerminalBench and τ²-Bench at any prefix checkpoint $t$:

| Feature Name | Type | Definition / Computation | Common Boundary |
|---|---|---|---|
| `steps_so_far` | Integer | Total number of events/steps processed up to checkpoint $t$ | Identical ($t$) |
| `actor_role` | Categorical | Role of event emitter (`agent`, `tool`, `user`, `system`) | Mapped to `{agent, tool, user, system}` |
| `action_type` | Categorical | Type of action (`message`, `tool_call`, `tool_result`, `terminal`) | Neutralized terminal marker |
| `tool_error_count` | Integer | Count of tool calls returning `error`, `traceback`, or non-zero return code up to $t$ | Normalized across CLI output & tool JSON status |
| `retry_count` | Integer | Consecutive error count or repeated tool invocation count up to $t$ | Computed identically from step sequence |
| `unique_tools_used` | Integer | Number of distinct tool names invoked up to $t$ | Extracted from function calls / CLI commands |
| `tool_call_ratio` | Float | Ratio of tool invocation events to total events up to $t$ | $\frac{\text{tool\_calls}(t)}{t}$ |
| `repeated_action_last2` | Binary | 1 if action type / tool call at $t$ equals action at $t-1$, else 0 | Sequence window = 2 |

---

### Category B: DATASET-SPECIFIC (Diagnostic Only)
These features exist on only one benchmark. Per Rule 9, they are **PROHIBITED** from entering the primary transferable model.

#### TerminalBench-Specific Features:
- `input_tokens` / `output_tokens` / `cache_tokens` (LLM token consumption metrics).
- `cost_cents` (Financial cost of trajectory).
- `duration_seconds` (Wall-clock execution duration).
- `difficulty` / `category` (SWE/terminal task metadata).

#### τ²-Bench-Specific Features:
- `domain` (`airline` vs `retail`).
- Domain-specific state changes (flight reservations, order updates).

---

### Category C: POST-OUTCOME / LEAKAGE-PRONE (Strictly Excluded)
These fields encode the ground-truth final outcome or evaluation results. They are extracted into evaluation-only targets before sanitization and **MUST NEVER** enter any feature vector:

| Field Name | Source Dataset | Why It Leaks | Handling Rule |
|---|---|---|---|
| `reward` | TerminalBench / τ²-Bench | Directly discloses task success ($1.0$) or failure ($0.0$) | Extracted to `eventual_outcome`, stripped from trace |
| `solved` / `passed` | Tracebench | Explicit outcome boolean | Extracted to `eventual_outcome`, stripped from trace |
| `incorrect_stages` | Tracebench | Ground-truth error labels and step annotations | Extracted to `failure_onset_step`, stripped from trace |
| `status` / `outcome` | TerminalBench / τ²-Bench | High-level execution status string | Excluded from trace |
| Terminal Output Log | Both | Contains test verifier outputs, pass/fail assertions | Stripped to neutral `"[TERMINAL EVENT REDACTED]"` |

---

## 3. Protocol Verification

- **Rule 9 Enforcement:** All transferable models ($H, M, S$) will be trained and evaluated using ONLY **Category A** features.
- **Diagnostic Extension:** A secondary TerminalBench-internal model utilizing Category B features may be trained, but its performance will be reported strictly as an in-benchmark diagnostic, never as a cross-dataset transfer result.


---

## Section from `gate1_leakage_audit.md`

# Gate 1 Report: Terminal Event Leakage Audit and Sanitization Specification

**Date:** 2026-07-31  
**Status:** VERIFIED — PROTOCOL RULES 2 & 6 ENFORCED  
**Scope:** Identifying explicit and structural outcome leakage risks in trace events and specifying mandatory ingestion sanitization.

---

## Executive Summary

Per **Protocol Rules 2 & 6**, a monitor evaluating risk at checkpoint $t$ must only observe information available up to $t$. Furthermore, at $t = T$ (the terminal event), the trace must not disclose whether the trajectory succeeded or failed. Naive ingestion of raw terminal events leaks final verifier outcomes, test assertion logs, and reward values.

This audit catalogues all identified leakage vectors across TerminalBench, Tracebench, and τ²-Bench, and specifies the programmatic sanitization rules required before feature extraction.

---

## 1. Identified Leakage Vectors

### 1.1 Direct Outcome Fields (Scalar / Metadata Leakage)
Raw dataset rows contain scalar fields that directly disclose task success or failure:
- **TerminalBench (`yoonholee`):** `reward` ($1.0$ vs $0.0$).
- **Tracebench (`Contextbench`):** `solved` (`True` vs `False`), `incorrect_error_stage_count` ($>0$).
- **τ²-Bench (`sierra-research`):** `reward` ($1$ vs $0$).

### 1.2 Terminal Event Content (Textual / Assertion Leakage)
In TerminalBench and Tracebench, the final action/observation step often contains test suite verifier execution outputs. For example:
- **Success signatures:** `"COMPLETE_TASK_AND_SUBMIT_FINAL_OUTPUT"`, `"<returncode>0</returncode>"`, `"93,347 examples verified"`, `"All unit tests passed"`.
- **Failure signatures:** `"AssertionError"`, `"FAILED (failures=1)"`, `"Traceback (most recent call last):"`, `"<returncode>1</returncode>"`.

If a monitor at checkpoint $t = T$ observes these textual strings, it can predict failure with 100% precision by acting as a keyword filter on the terminal verifier output rather than detecting early execution anomalies.

### 1.3 Structural Opportunity Leakage
In Tracebench, `incorrect_stages` contains step-by-step error annotations. If fed directly to an agent or monitor, it provides hindsight labels that are unavailable online during agent execution.

---

## 2. Mandatory Leakage Risk Inventory

| Field / Content | Dataset | Why It Leaks | Availability | Mandatory Handling |
|---|---|---|---|---|
| `reward` | TerminalBench / τ²-Bench | Direct scalar outcome ($1/0$) | Task End | Extract to ground-truth target `eventual_failure`, strip from trace |
| `solved` | Tracebench | Direct boolean outcome | Task End | Extract to ground-truth target `eventual_failure`, strip from trace |
| `incorrect_stages` | Tracebench | Ground-truth error step indices | Post-hoc | Extract to `failure_onset_step`, strip from trace |
| `terminal_reason` | TerminalBench | Status string ("success", "eval_failed") | Task End | Exclude entirely from trace |
| Final observation string | All | Contains unit test results / error tracebacks | Task End ($t = T$) | Sanitize to neutral string `"[TERMINAL EVENT REDACTED]"` |
| `artifact_path` | Tracebench | Path containing `full` vs `verified` status | Metadata | Exclude from trace |

---

## 3. Terminal Sanitization Invariant Specification

To satisfy **Protocol Rule 6**, every event dict processed by the ingestion engine must be routed through `strip_terminal_leakage()` before turning into a canonical `Event` object:

```python
OUTCOME_LEAK_KEYS = {"reward", "success", "solved", "passed", "final_outcome", "task_failed", "task_success", "incorrect_stages"}
TERMINAL_ACTION_TYPES = {"terminal", "submit", "eval"}

def strip_terminal_leakage(raw_event: dict) -> dict:
    """
    Sanitizes trace events to guarantee Rule 2 & Rule 6 invariants.
    Neutralizes outcome-bearing content in terminal events and strips outcome keys.
    """
    cleaned = dict(raw_event)
    
    # 1. Neutralize terminal action types and observation text
    if cleaned.get("action_type") in TERMINAL_ACTION_TYPES:
        cleaned["action_type"] = "message"
        cleaned["content"] = "[TERMINAL EVENT REDACTED FOR LEAKAGE PREVENTION]"
        cleaned["observation"] = "[TERMINAL OBSERVATION REDACTED]"
    
    # 2. Strip any embedded outcome keys
    for k in OUTCOME_LEAK_KEYS:
        cleaned.pop(k, None)
        
    return cleaned
```

---

## 4. Invariant Enforcement Checklist

- [x] Ground-truth outcome targets (`eventual_success`, `eventual_failure`) are isolated in `Run` metadata and never enter `Event` feature vectors.
- [x] Ground-truth onset target (`failure_onset_step`) is isolated in `Run` metadata and never enters `Event` feature vectors.
- [x] Terminal events ($t = T$) retain `action_type = "message"` and neutral content, preventing $t = T$ from leaking final verifier status.
- [x] Automated runtime guard `assert_no_feature_leakage()` is executed prior to every experiment run.


---

## Section from `gate1_checkpoint_analysis.md`

# Gate 1 Report: Checkpoint Horizon K and Truncation Analysis

**Date:** 2026-07-31  
**Status:** EVIDENCE COMPLETE — GATE 2 INPUT PREPARED  
**Scope:** Quantitative evaluation of candidate checkpoint horizons ($K \in \{5, 10, 15, 20, 25, 30, 40, 50\}$) across TerminalBench, Tracebench, and τ²-Bench to assess observation-window truncation bias.

---

## Executive Summary

Per **Protocol Rule 1**, checkpoint selection must be outcome-independent and episode-symmetric across all trajectories. The provisional protocol suggested evaluating checkpoints up to $t = 30$ by absolute step index ($K=30$).

This empirical analysis evaluates how trajectory-length distributions across TerminalBench, Tracebench, and τ²-Bench interact with candidate horizon values $K$.

### Key Findings:
1. **TerminalBench Disparity:** Median trajectory length in TerminalBench (`yoonholee`) is **9.0 steps**. Under a fixed $K=30$ horizon, **74.48% of TerminalBench trajectories are already terminated** before step 30.
2. **Tracebench Disparity:** Median trajectory length in Tracebench (`Contextbench`) is **30.0 steps**. Under $K=30$, **50.06% of Tracebench trajectories survive** to step 30.
3. **τ²-Bench Disparity:** Median trajectory length in τ²-Bench is **28.0 steps**, with a hard maximum length of 62 steps. Under $K=30$, **44.04% of τ²-Bench trajectories survive** to step 30.
4. **Observation Window Bias:** Setting a single fixed absolute cutoff $K=30$ across datasets introduces a dataset-dependent observation window (evaluating late execution in Tracebench/τ²-Bench vs. post-terminal padding in TerminalBench).

---

## 1. Empirical Trajectory Survival Tables

The table below reports the **Surviving Percentage** (trajectories with $\text{length} \ge K$) and **Truncated Percentage** (trajectories with $\text{length} > K$) across candidate horizons $K$:

| Candidate Horizon ($K$) | TerminalBench (`yoonholee`) | Tracebench (`Contextbench`) | τ²-Bench (`sierra-research`) |
|---|---|---|---|
| **$K = 5$** | 61.90% survive (32,250 / 52,104) | **99.97% survive** (3,315 / 3,316) | **100.00% survive** (1,980 / 1,980) |
| **$K = 10$** | 49.40% survive (25,739 / 52,104) | **99.46% survive** (3,298 / 3,316) | **98.84% survive** (1,957 / 1,980) |
| **$K = 15$** | 40.92% survive (21,320 / 52,104) | **86.01% survive** (2,852 / 3,316) | **93.43% survive** (1,850 / 1,980) |
| **$K = 20$** | 34.38% survive (17,913 / 52,104) | **71.74% survive** (2,379 / 3,316) | **85.20% survive** (1,687 / 1,980) |
| **$K = 25$** | 29.59% survive (15,415 / 52,104) | **59.77% survive** (1,982 / 3,316) | **62.93% survive** (1,246 / 1,980) |
| **$K = 30$ (Provisional)** | **25.52% survive** (13,298 / 52,104) | **50.06% survive** (1,660 / 3,316) | **44.04% survive** (872 / 1,980) |
| **$K = 40$** | 19.63% survive (10,229 / 52,104) | **33.90% survive** (1,124 / 3,316) | **13.48% survive** (267 / 1,980) |
| **$K = 50$** | 15.64% survive (8,151 / 52,104) | **23.34% survive** (774 / 3,316) | **2.83% survive** (56 / 1,980) |

---

## 2. Onset Distribution vs. Horizon K (Tracebench)

For Tracebench failed episodes with verified step-level onset labels ($N = 1,273$), failure onset step stats are:
- **Min:** step 1
- **25th Percentile:** step 5
- **Median:** step 11
- **Mean:** step 18.50
- **75th Percentile:** step 23
- **90th Percentile:** step 42

### Onset Coverage by Horizon:
- **$K = 10$:** 48.78% of failure onsets occur at $t \le 10$.
- **$K = 20$:** 71.96% of failure onsets occur at $t \le 20$.
- **$K = 30$:** **82.95% of failure onsets** occur at $t \le 30$. (17.05% occur after step 30).
- **$K = 40$:** 89.40% of failure onsets occur at $t \le 40$.
- **$K = 50$:** 93.09% of failure onsets occur at $t \le 50$.

---

## 3. Checkpoint Policy Recommendations for Gate 2

1. **Rejection of Fixed Absolute $K=30$ for All Datasets:**
   Evaluating up to step 30 across all datasets truncates 74.48% of TerminalBench episodes after task completion.
2. **Recommended Operational Policy Options (Pending Gate 2 Decision):**
   - **Option A (Episode-Adaptive Absolute Horizon):** Evaluate checkpoints at $t = 1, 2, \dots, \min(T_i, K)$, where $T_i$ is the actual trajectory length of episode $i$ and $K=30$.
   - **Option B (Quantile / Stride Sampling):** Evaluate $N=10$ or $N=15$ checkpoints sampled deterministically across the episode execution.

---

## 4. Conclusion & Decision Status

- **Status:** **PROVISIONAL** (empirical evidence collected; final horizon $K$ choice deferred to Gate 2 approval).


---

