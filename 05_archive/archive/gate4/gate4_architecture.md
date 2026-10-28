# Gate 4: AIRE-Trace Architecture & Interface Contract

## High-Level Architecture
The AIRE-Trace framework acts as a rigid evaluation wrapper around pluggable failure warning methods. It ensures that every method is trained, calibrated, and evaluated under strictly identical constraints. The core architecture is separated into three tiers:
1. **Data & Preprocessing**: Handled by the legacy canonical extraction pipeline. It provides static Parquet manifests containing sequences of numerical feature vectors per episode.
2. **Method Families (`src/aire_trace`)**: The unified modeling interface implementing Heuristic (H), Classical ML (M), and Sequence (S) models. These components expose identical APIs regardless of internal complexity.
3. **Evaluation Harness**: The calibration, statistical bootstrapping, and PDC analysis layers that consume method predictions to produce canonical result artifacts.

## Module Responsibilities (`src/aire_trace/`)

- `registry.py`: Central registration and factory instantiation of all method families (H, M, S, L).
- `encoder.py`: Handles feature normalization, scaling, and sequence padding (for S models) or flattening (for M models).
- `temporal_model.py`: Core sequence modeling layer (S). Implements a lightweight GRU or 1D-CNN designed to process ordered feature sequences.
- `feature_fusion.py`: Optional module to fuse structured temporal features with dense semantic embeddings (reserved for L model integrations).
- `prediction_head.py`: Maps the final hidden states or flattened vectors to a scalar risk probability (0 to 1).
- `confidence.py`: Analyzes internal prediction confidence, enabling threshold calibration and ECE calculation.
- `trainer.py`: Implements the fit loop for trainable models (M, S), enforcing Rule 8 (post-onset exclusion) and Rule 11 (episode-balanced sample weights).
- `inference.py`: Orchestrates checkpoint-by-checkpoint prediction, enforcing Rule 2 (feature leakage guards) during model execution.
- `utils.py`: Logging, metric mapping, model serialization, and hardware tracking (peak memory, latency).

## Information Flow & Component Interactions
1. **Training Flow**: 
   - TRAIN Parquet records $\to$ `encoder.py` (fit scaler) $\to$ `trainer.py` $\to$ `temporal_model.py` / `prediction_head.py` $\to$ parameter updates.
   - Post-onset prefix filtering and episode-balanced sample weights are injected at `trainer.py`.
2. **Calibration Flow**:
   - CALIBRATION Parquet records $\to$ `inference.py` $\to$ `confidence.py`.
   - The evaluation harness selects the optimal risk threshold achieving the target FAR.
3. **Inference Flow (Evaluation)**:
   - TEST (Mode A) / τ²-Bench (Mode B) records $\to$ `encoder.py` (transform) $\to$ `inference.py` $\to$ predicted risks.
   - The frozen calibration threshold maps risks to binary alerts.

## Pipeline Lifecycle

### Training Pipeline
1. Load TRAIN dataset manifest.
2. Exclude all post-onset prefixes ($t > t_{\text{onset}}$) for failed episodes (Rule 8).
3. Compute sample weights $w_{i,t} = 1 / \min(T_i, K)$ to balance long and short episodes.
4. Fit the feature encoder (standardization/scaling).
5. Pass processed batches to `trainer.py`.
6. Invoke `fit()` on the underlying model architecture.
7. Save optimized parameters via `save()`.

### Inference Pipeline
1. Load frozen model parameters via `load()`.
2. For each episode in TEST / τ²-Bench:
   - Sequentially present prefixes up to checkpoint $t$.
   - Extract current feature state.
   - `predict_proba()` to generate failure risk.
   - Apply frozen threshold to yield binary alert.
   - Record inference latency and peak memory usage.

## Interface Contract

All method families MUST implement the following `AbstractMonitor` base class contract:

```python
class AbstractMonitor(ABC):
    
    @abstractmethod
    def fit(self, X: np.ndarray, y: np.ndarray, weights: np.ndarray = None) -> None:
        """
        Trains the monitor on the pre-onset training data.
        - X: Feature matrices (flattened for H/M, padded sequences for S).
        - y: Binary labels (0=Success, 1=Failure).
        - weights: Episode-balanced sample weights.
        - Note: Heuristic (H) models will implement this as a no-op.
        """
        pass

    @abstractmethod
    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        """
        Returns the continuous probability of eventual failure [0, 1].
        - X: Feature matrix for the given prefixes.
        """
        pass

    def predict(self, X: np.ndarray, threshold: float) -> np.ndarray:
        """
        Returns binary alerts based on the provided threshold.
        """
        probs = self.predict_proba(X)
        return (probs >= threshold).astype(int)

    @abstractmethod
    def save(self, filepath: str) -> None:
        """
        Serializes the model architecture, weights, and fitted encoders to disk.
        """
        pass

    @abstractmethod
    def load(self, filepath: str) -> None:
        """
        Loads the model from disk.
        """
        pass

    def evaluate(self, X: np.ndarray, y: np.ndarray, threshold: float) -> dict:
        """
        Convenience function for internal metrics generation. Returns basic 
        discrimination and calibration metrics for a single dataset split.
        """
        pass
```
