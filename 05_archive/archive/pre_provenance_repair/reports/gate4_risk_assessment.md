# Gate 4: Risk Assessment

## Technical Risks
- **Hardware Limitations (VRAM):** The RTX 2050 possesses only 4GB VRAM. Implementing the Sequence (S) model risks Out-Of-Memory (OOM) errors during backpropagation if sequence length $K$ or batch sizes are too large. **Mitigation:** Strict batch-size tuning, utilizing lightweight architectures (GRU/1D-CNN), and treating the Semantic (L) model as strictly optional.
- **Compute Accounting Overhead:** Measuring memory and latency inside the inference loop may inadvertently impact the application's actual throughput. **Mitigation:** Profile methods using a dedicated timing/memory wrapper outside the core evaluation path.

## Scientific Risks
- **Overfitting to TerminalBench:** A highly parameterized Sequence model may achieve excellent Mode A performance but suffer severe representation transfer collapse on τ²-Bench (Mode B). **Mitigation:** Protocol Rule 9 enforces cross-dataset feature compatibility; regularization will be employed in the sequence architecture.
- **Insufficient Warning Opportunity:** A majority of failures may only manifest near $T_i$, truncating the actual pre-onset warning window. **Mitigation:** Rely on episode-adaptive checkpoints rather than fixed $K=30$, and isolate Lead Time explicitly.

## Protocol Risks
- **Violation of Rule 8 (Post-Onset Masking):** The Sequence model must learn temporal trajectories, which historically creates code paths that accidentally feed post-onset failure data into the optimizer. **Mitigation:** Explicit temporal masking inside `trainer.py` validated by integration tests.
- **Violation of Rule 11 (Episode-Balanced Weights):** Frameworks like PyTorch do not natively balance variable-length episode histories when extracting minibatches. **Mitigation:** Custom PyTorch `DataLoader` / loss mask implementation that enforces $1/n_i$ scaling for each valid prefix.

## Implementation Risks
- **Signature Mismatch:** Forcing Sequence models to accept flattened $t$-dimensional vectors (like Classical ML models) destroys the temporal ordering. **Mitigation:** Implement flexible `AbstractMonitor` signatures supporting both flat (H, M) and padded tensor (S) representations.
- **Threshold Leakage:** Accidentally sweeping thresholds on the TEST set during final model comparison. **Mitigation:** API separation in `inference.py` ensuring the calibration threshold is returned from a dedicated `calibrate()` function operating only on CALIBRATION.

## Reproducibility Risks
- **Non-Deterministic GPU Operations:** PyTorch RNN/CNN implementations can yield non-deterministic results across runs. **Mitigation:** Force deterministic cuDNN algorithms and fix random seeds globally.
- **Inconsistent Bootstrapping:** Mixing random states between the baseline bootstrapping and the new Sequence model bootstrapping. **Mitigation:** Reuse the exact same $B=100$ random state generation sequences from the Gate 3 artifacts.
