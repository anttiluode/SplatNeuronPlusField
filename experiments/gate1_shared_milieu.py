"""Gate 1: does shared metric history buy something matched private history does not?

This is a controlled synthetic instrument, not a physiological tissue model.

The task is a two-event temporal-context problem.  A cue occurs at one unit,
then after a delay a distinct probe unit is queried.  The target says whether
cue and probe belong to the same latent context.  In the aligned regime,
context membership is spatially local.  In the scrambled regime, the same
latent grouping is permuted across physical positions.

The receiver is intentionally local: it sees only the slow state at the probe
unit immediately before the probe arrives.  Positive trials never reuse the
same unit for cue and probe, so independent per-unit adaptation cannot solve the
task merely by self-memory.

The important attackers are:

* private/local adaptation with the same number of state variables;
* a private diagonal system with the same multiset of decay rates as the
  shared field;
* a generic shared system with exactly the same decay spectrum as the metric
  field but random eigenvectors.

Run one seed/regime:
    python experiments/gate1_shared_milieu.py --seed 18101 --regime aligned

Run the frozen five-seed holdout suite:
    python experiments/gate1_shared_milieu.py --suite
"""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
import json
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from splatneuronplusfield.core import metric_laplacian


@dataclass(frozen=True)
class Protocol:
    n_units: int = 48
    n_contexts: int = 8
    train_trials: int = 6000
    test_trials: int = 6000
    length_scale: float = 0.07
    diffusion: float = 0.70
    clearance: float = 0.25
    delay: float = 1.50
    ridge: float = 1e-8


@dataclass(frozen=True)
class TrialSet:
    cue: np.ndarray
    probe: np.ndarray
    label: np.ndarray


def _positions(n: int) -> np.ndarray:
    return np.linspace(0.0, 1.0, n)


def _groups(
    n: int,
    k: int,
    regime: str,
    rng: np.random.Generator,
) -> np.ndarray:
    if n % k != 0:
        raise ValueError("n_units must be divisible by n_contexts")

    contiguous = np.repeat(np.arange(k), n // k)
    if regime == "aligned":
        # Relabel contexts without changing their spatial contiguity.
        labels = rng.permutation(k)
        return labels[contiguous]
    if regime == "scrambled":
        return contiguous[rng.permutation(n)]
    raise ValueError("regime must be 'aligned' or 'scrambled'")


def _make_trials(
    groups: np.ndarray,
    rng: np.random.Generator,
    n_trials: int,
) -> TrialSet:
    k = int(groups.max()) + 1
    members = [np.flatnonzero(groups == g) for g in range(k)]

    label = rng.integers(0, 2, size=n_trials, dtype=np.int64)
    cue = np.empty(n_trials, dtype=np.int64)
    probe = np.empty(n_trials, dtype=np.int64)

    for row, same_context in enumerate(label):
        cue_context = int(rng.integers(k))
        cue_unit = int(rng.choice(members[cue_context]))

        if same_context:
            # Exclude exact self-memory.  The task requires history to become
            # available at a *different* receiver.
            candidates = members[cue_context]
            candidates = candidates[candidates != cue_unit]
            probe_unit = int(rng.choice(candidates))
        else:
            other_contexts = np.delete(np.arange(k), cue_context)
            probe_context = int(rng.choice(other_contexts))
            probe_unit = int(rng.choice(members[probe_context]))

        cue[row] = cue_unit
        probe[row] = probe_unit

    return TrialSet(cue=cue, probe=probe, label=label)


def _propagator(rate: np.ndarray, delay: float) -> tuple[np.ndarray, np.ndarray]:
    """Exact exp(-rate * delay) for a real symmetric positive rate matrix."""

    evals, evecs = np.linalg.eigh(np.asarray(rate, dtype=float))
    if float(evals.min()) < -1e-10:
        raise ValueError("rate matrix must be positive semidefinite")
    decay = np.exp(-evals * delay)
    transition = (evecs * decay[None, :]) @ evecs.T
    return transition, evals


def _feature(transition: np.ndarray, trials: TrialSet) -> np.ndarray:
    # A unit pulse at cue followed by delay.  The local receiver at probe reads
    # only the state that arrived at its own coordinate.
    return transition[trials.probe, trials.cue]


def _fit_scalar_ridge(feature: np.ndarray, label: np.ndarray, ridge: float) -> np.ndarray:
    x = np.column_stack([feature, np.ones(len(feature))])
    y = 2.0 * label.astype(float) - 1.0
    reg = np.diag([ridge, 0.0])
    return np.linalg.solve(x.T @ x + reg, x.T @ y)


def _accuracy(weights: np.ndarray, feature: np.ndarray, label: np.ndarray) -> float:
    x = np.column_stack([feature, np.ones(len(feature))])
    pred = (x @ weights >= 0.0).astype(np.int64)
    return float(np.mean(pred == label))


def _evaluate(
    transition: np.ndarray,
    train: TrialSet,
    test: TrialSet,
    ridge: float,
) -> tuple[dict[str, float], np.ndarray]:
    f_train = _feature(transition, train)
    f_test = _feature(transition, test)
    weights = _fit_scalar_ridge(f_train, train.label, ridge)
    result = {
        "accuracy": _accuracy(weights, f_test, test.label),
        "positive_mean": float(np.mean(f_test[test.label == 1])),
        "negative_mean": float(np.mean(f_test[test.label == 0])),
    }
    return result, weights


def run(seed: int, regime: str, protocol: Protocol = Protocol()) -> dict[str, object]:
    rng = np.random.default_rng(seed)
    n = protocol.n_units
    k = protocol.n_contexts
    positions = _positions(n)
    groups = _groups(n, k, regime, rng)

    train = _make_trials(groups, rng, protocol.train_trials)
    test = _make_trials(groups, rng, protocol.test_trials)

    lap = metric_laplacian(positions, length_scale=protocol.length_scale)
    metric_rate = protocol.clearance * np.eye(n) + protocol.diffusion * lap
    metric_transition, metric_rates = _propagator(metric_rate, protocol.delay)

    # Same N state variables and same local release/clearance, but no sharing.
    local_transition = np.exp(-protocol.clearance * protocol.delay) * np.eye(n)

    # Stronger private attacker: keep exactly N private states and give them the
    # same multiset of decay rates as the metric field.  What is removed is the
    # shared eigenvector geometry, not the temporal spectrum.
    private_rates = rng.permutation(metric_rates)
    private_matched_transition = np.diag(np.exp(-private_rates * protocol.delay))

    # Stronger shared attacker: preserve N, every decay eigenvalue, Frobenius
    # norm and symmetry, but replace the metric eigenvectors with a random
    # orthogonal basis.
    q, _ = np.linalg.qr(rng.normal(size=(n, n)))
    random_shared_transition = (
        q * np.exp(-metric_rates * protocol.delay)[None, :]
    ) @ q.T

    transitions = {
        "A_no_slow_state": np.zeros((n, n)),
        "B_private_same_clearance": local_transition,
        "C_shared_metric_diffusion": metric_transition,
        "D_shared_no_diffusion": local_transition,
        "F_private_matched_decay_spectrum": private_matched_transition,
        "G_shared_random_matched_spectrum": random_shared_transition,
    }

    conditions: dict[str, dict[str, float]] = {}
    weights: dict[str, np.ndarray] = {}
    for name, transition in transitions.items():
        conditions[name], weights[name] = _evaluate(
            transition,
            train,
            test,
            protocol.ridge,
        )

    # Test-time intervention only: move unit identities to different physical
    # coordinates, while preserving latent groups and the already-fitted C
    # readout.  No retraining is allowed.
    shuffled_positions = positions[rng.permutation(n)]
    shuffled_lap = metric_laplacian(
        shuffled_positions,
        length_scale=protocol.length_scale,
    )
    shuffled_rate = protocol.clearance * np.eye(n) + protocol.diffusion * shuffled_lap
    shuffled_transition, shuffled_rates = _propagator(shuffled_rate, protocol.delay)
    shuffled_feature = _feature(shuffled_transition, test)
    geometry_shuffle_accuracy = _accuracy(
        weights["C_shared_metric_diffusion"],
        shuffled_feature,
        test.label,
    )

    # Exact matched-spectrum check for the random shared attacker.
    metric_decay = np.sort(np.exp(-metric_rates * protocol.delay))
    random_decay = np.sort(np.linalg.eigvalsh(random_shared_transition))

    return {
        "seed": seed,
        "regime": regime,
        "protocol": asdict(protocol),
        "conditions": conditions,
        "interventions": {
            "E_metric_geometry_shuffle_test_only": geometry_shuffle_accuracy,
        },
        "checks": {
            "positive_trials_have_distinct_cue_probe": bool(
                np.all(train.cue[train.label == 1] != train.probe[train.label == 1])
                and np.all(test.cue[test.label == 1] != test.probe[test.label == 1])
            ),
            "B_equals_D_max_abs": float(
                np.max(np.abs(transitions["B_private_same_clearance"] - transitions["D_shared_no_diffusion"]))
            ),
            "metric_vs_random_decay_spectrum_max_abs": float(
                np.max(np.abs(metric_decay - random_decay))
            ),
            "geometry_shuffle_decay_spectrum_max_abs": float(
                np.max(
                    np.abs(
                        np.sort(np.exp(-metric_rates * protocol.delay))
                        - np.sort(np.exp(-shuffled_rates * protocol.delay))
                    )
                )
            ),
        },
    }


def _suite() -> dict[str, object]:
    seeds = [18101, 18102, 18103, 18104, 18105]
    runs = [run(seed, regime) for regime in ("aligned", "scrambled") for seed in seeds]

    def mean_accuracy(regime: str, condition: str) -> float:
        vals = [
            item["conditions"][condition]["accuracy"]
            for item in runs
            if item["regime"] == regime
        ]
        return float(np.mean(vals))

    def mean_intervention(regime: str) -> float:
        vals = [
            item["interventions"]["E_metric_geometry_shuffle_test_only"]
            for item in runs
            if item["regime"] == regime
        ]
        return float(np.mean(vals))

    aligned_metric = mean_accuracy("aligned", "C_shared_metric_diffusion")
    aligned_private = mean_accuracy("aligned", "B_private_same_clearance")
    aligned_private_spectrum = mean_accuracy("aligned", "F_private_matched_decay_spectrum")
    aligned_random = mean_accuracy("aligned", "G_shared_random_matched_spectrum")
    scrambled_metric = mean_accuracy("scrambled", "C_shared_metric_diffusion")
    aligned_shuffle = mean_intervention("aligned")

    summary = {
        "aligned": {
            name: mean_accuracy("aligned", name)
            for name in runs[0]["conditions"].keys()
        },
        "scrambled": {
            name: mean_accuracy("scrambled", name)
            for name in runs[0]["conditions"].keys()
        },
        "aligned_geometry_shuffle_test_only": aligned_shuffle,
    }
    summary["frozen_checks"] = {
        "aligned_metric_above_0p75": bool(aligned_metric >= 0.75),
        "aligned_metric_beats_private_by_0p20": bool(aligned_metric >= aligned_private + 0.20),
        "aligned_metric_beats_private_spectrum_by_0p20": bool(
            aligned_metric >= aligned_private_spectrum + 0.20
        ),
        "aligned_metric_beats_random_shared_by_0p20": bool(aligned_metric >= aligned_random + 0.20),
        "scrambled_metric_below_0p60": bool(scrambled_metric <= 0.60),
        "geometry_shuffle_below_0p60": bool(aligned_shuffle <= 0.60),
    }

    return {
        "suite": "gate1_shared_milieu_holdout",
        "seeds": seeds,
        "runs": runs,
        "summary": summary,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=18101)
    parser.add_argument("--regime", choices=["aligned", "scrambled"], default="aligned")
    parser.add_argument("--suite", action="store_true")
    parser.add_argument("--json", type=Path, default=None)
    args = parser.parse_args()

    result = _suite() if args.suite else run(args.seed, args.regime)
    text = json.dumps(result, indent=2, sort_keys=True)
    print(text)
    if args.json is not None:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(text + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
