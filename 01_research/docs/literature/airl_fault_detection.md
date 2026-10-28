# Label-Free Industrial Fault Detection via Adversarial IRL (July 2026)

**Category:** Anomaly Detection / One-Class Methods
**arXiv:** [2607.22987](https://arxiv.org/abs/2607.22987)
**Published:** July 2026
**Code:** https://github.com/dhirajneupane/AIRL-MFD-DN
**Ref ID:** [A3]

---

## What the Paper Is

Proposes an **Adversarial Inverse Reinforcement Learning (AIRL)** framework for **label-free machinery fault detection (MFD)** — treating fault detection as an offline IRL problem that recovers an intrinsic "health reward" from observational state transitions, requiring neither manual reward engineering nor fault labels.

### Key Technical Approach
- Treats MFD as **offline IRL**: recovers intrinsic health reward from state transitions
- Unlike static classification approaches, explicitly models **temporal state transitions** (not just contextual bandits)
- Avoids reconstruction-based approaches' static error margins
- Learns from observational data only — no fault labels required

### Results (HUMS2023, IMS, XJTU-SY benchmarks)
- **Only method achieving non-saturated post-detection consistency** across all three datasets
- CB (contextual bandit) baselines **fail to detect gradual degradation**
- Reconstruction models **collapse into always-anomalous states**
- Achieves meaningful PDC (**68–90%**) across three industrial datasets

## What It Solves

- Label-free fault detection by learning from healthy operational data only
- Proper temporal modeling (vs. static contextual bandit reduction)
- Avoids reconstruction model collapse via adversarial formulation

## What It Lacks

- Industrial machinery domain — not LLM agent trajectories
- Run-to-failure benchmarks have continuous degradation; agent failures can be sudden
- AIRL training is computationally expensive
- No evaluation on agent benchmarks

## Relevance to AIRE-TRACE

- **PDC (Post-Detection Consistency) metric** — 68–90% across datasets — is exactly the metric our protocol uses (Section 8: PDC must always be reported with coverage figure)
- The AIRL framework's health reward learning from state transitions parallels our echo-state-network's learning of healthy trajectory dynamics
- **Label-free from healthy data only** aligns with our Rule 8: train only on successful prefixes
- The finding that contextual bandit approaches (ignoring temporal dynamics) fail to detect gradual degradation directly supports our choice of echo-state-network (which has memory) over memoryless baselines
- AIRL's adversarial formulation could be a future architectural enhancement for AIRE-TRACE monitors
- PDC coverage reporting connection: this paper demonstrates the value of PDC in industrial settings — validates our use of PDC for agent trajectory monitoring

---

## Key Terms
`adversarial IRL` · `label-free` · `PDC` · `temporal state transitions` · `health reward` · `industrial fault detection`
