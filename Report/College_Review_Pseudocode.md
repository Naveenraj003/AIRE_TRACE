# AIRE-Trace Phase-I Review: Methodology & Pseudocode

The methodology relies on decomposing the trajectory risk. The core novelty of the AIRE-Trace `dyn_comp` module is mathematically isolating execution-dependent risk from the static prior task difficulty.

### Algorithm 1: Trajectory Risk Decomposition (`dyn_comp`)

This pseudocode faithfully represents the logical calculations implemented in the `dyn_comp` evaluation module.

**Input**: 
- $e_{1:t}$: A trajectory prefix up to checkpoint step $t$
- $\mathcal{T}$: The static task definition/instruction
- $M_{1}$: A trained feature-based risk model (e.g., Logistic Regression)
- $M_{static}$: A trained static task-prior risk model (e.g., M4-category-only baseline)

**Output**: 
- $s_{dyn\_comp}(t)$: The dynamic execution anomaly score at checkpoint $t$

**Procedure**:
1. Extract dynamic structural features $X_t$ exclusively from the observable prefix $e_{1:t}$.
2. Compute the dynamic prefix posterior: 
   $P(M_{1} \mid e_{1:t}) \leftarrow M_{1}.\text{predict\_proba}(X_t)$
3. Compute the static task-prior probability without observing the trajectory: 
   $P(M_{static} \mid \mathcal{T}) \leftarrow M_{static}.\text{predict\_proba}(\mathcal{T})$
4. Calculate the decomposed dynamic execution risk score by subtracting the static prior from the prefix posterior:
   $s_{dyn\_comp}(t) \leftarrow P(M_{1} \mid e_{1:t}) - P(M_{static} \mid \mathcal{T})$
5. **Return** $s_{dyn\_comp}(t)$

---

### Algorithm 2: AIRE-Trace Prospective Evaluation Protocol & Calibration

The overall AIRE-Trace evaluation protocol guarantees information visibility boundaries and strict false-alarm rate bounding across the test splits.

**Input**: 
- $D_{train}, D_{calib}, D_{test}$: Task-disjoint dataset splits of trajectory prefixes
- $\text{target\_far}$: Maximum allowable false alarm rate (e.g., 0.05 / 5%)
- $K$: Maximum Checkpoint horizon limit (e.g., 30)

**Output**: 
- $\tau^*$: Frozen operating threshold
- Prospective $\text{Recall@FAR}$ and operational $\text{FAR}$ on the Test split

**Procedure**:

// Phase 1: Training
1. Train $M_{1}$ and $M_{static}$ on the prefixes bounded by horizon $K$ in $D_{train}$.

// Phase 2: Calibration (Threshold Selection)
2. For each episode in $D_{calib}$:
   a. Compute $s_{dyn\_comp}(t)$ for all observable checkpoints $t \le K$.
3. Gather $S_{succ}$: Maximum prefix scores for successful episodes in $D_{calib}$.
4. Gather $S_{fail}$: Maximum valid pre-onset prefix scores for failed episodes in $D_{calib}$.
5. Find optimal frozen threshold $\tau^*$:
   a. Initialize $\text{best\_recall} = -1.0, \text{best\_far} = 1.0, \tau^* = 0.5$
   b. For candidate threshold $\tau \in \text{CandidateRange}$:
      i. $\text{FAR}(\tau) \leftarrow \text{fraction of } S_{succ} \ge \tau$
      ii. $\text{Recall}(\tau) \leftarrow \text{fraction of } S_{fail} \ge \tau$
      iii. If $\text{FAR}(\tau) \le \text{target\_far}$:
          If $\text{Recall}(\tau) > \text{best\_recall}$ OR ($\text{Recall}(\tau) == \text{best\_recall}$ AND $\text{FAR}(\tau) < \text{best\_far}$):
              $\tau^* \leftarrow \tau, \text{best\_recall} \leftarrow \text{Recall}(\tau), \text{best\_far} \leftarrow \text{FAR}(\tau)$

// Phase 3: Prospective Testing
6. **Freeze** $\tau^*$ indefinitely.
7. For each episode in $D_{test}$:
   a. Compute $s_{dyn\_comp}(t)$ for all checkpoints $t \le K$.
8. Compute episode-level test $\text{FAR}$ and prospective test $\text{Recall@FAR}$ on $D_{test}$ using the frozen $\tau^*$.
9. Perform episode-cluster bootstrapping on the test distribution to verify statistical significance (e.g., Holm-Bonferroni correction).
10. **Return** $\tau^*$, Test Recall, Test FAR.

---
**Implementation-to-Pseudocode Verification Note:**
- The algorithmic mapping was verified against `p:/Projects/AIRE-TRACE/02_experiments/src/evaluation/warning_decomposition.py`.
- **Algorithm 1** accurately mirrors the model-loading, prefix-scoring, and simple subtraction formulation from `main()` (lines 92-99).
- **Algorithm 2** mirrors `custom_select_calibration_threshold()` (lines 16-61) ensuring post-onset filters in CALIBRATION and independent application of the frozen threshold on the TEST split via `compute_episode_far_and_recall()` (lines 124-128).
