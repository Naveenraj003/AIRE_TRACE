# Trajectory Guard (Jan 2026)

**Key Technical Feature:** Siamese Recurrent Autoencoder, hybrid contrastive+reconstruction loss, 32ms latency
**Status:** Published
**Link:** [arxiv](https://arxiv.org/abs/2601.00516)

## Detailed Report

Autonomous LLM agents generate multi-step action plans that can fail due to contextual misalignment or structural incoherence. Existing anomaly detection methods are ill-suited for this challenge: mean-pooling embeddings dilutes anomalous steps, while contrastive-only approaches ignore sequential structure. Standard unsupervised methods on pre-trained embeddings achieve F1-scores no higher than 0.69. We introduce Trajectory Guard, a Siamese Recurrent Autoencoder with a hybrid loss function that jointly learns task-trajectory alignment via contrastive learning and sequential validity via reconstruction. This dual objective enables unified detection of both "wrong plan for this task" and "malformed plan structure." On benchmarks spanning synthetic perturbations and real-world failures from security audits (RAS-Eval) and multi-agent systems (Who\&When), we achieve F1-scores of 0.88-0.94 on balanced sets and recall of 0.86-0.92 on imbalanced external benchmarks. At 32 ms inference latency, our approach runs 17-27$\times$ faster than LLM Judge baselines, enabling real-time safety verification in production deployments.
