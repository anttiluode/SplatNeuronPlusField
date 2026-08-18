"""Gate 1b: can an addressed learned transition recover the Gate-1 task?

This attacker deliberately does not use physical positions.  It learns a low-rank
pairwise relation from the same cue/probe labels used by Gate 1, then turns that
relation into an addressed transition.  A cue at i produces local receiver
state at j according to T[j, i].

The purpose is to attack *capability*, not to settle resource cost.  If this
wins in both aligned and scrambled worlds, Gate 1 becomes an inductive-bias /
installation-cost result rather than a unique field-computation result.

Run:
    python experiments/gate1b_addressed_attacker.py --suite
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from experiments.gate1_shared_milieu import Protocol, _groups, _make_trials


def fit_addressed_factor(
    cue: np.ndarray,
    probe: np.ndarray,
    label: np.ndarray,
    *,
    n_units: int,
    rank: int,
) -> tuple[np.ndarray, float, dict[str, float]]:
    """Fit a symmetric low-rank addressed relation from observed pair labels.

    Pair labels are converted to +/-1, averaged for each observed unordered
    pair, and stored in a symmetric empirical relation matrix.  Unknown pairs
    are neutral (0).  The top positive eigendirections define a rank-limited
    factor U with transition T = U U^T.

    The scalar decision threshold is selected on training data only.
    """

    sums = np.zeros((n_units, n_units), dtype=float)
    counts = np.zeros((n_units, n_units), dtype=float)
    signed = 2.0 * np.asarray(label, dtype=float) - 1.0

    for i, j, y in zip(cue, probe, signed, strict=True):
        sums[i, j] += y
        counts[i, j] += 1.0
        sums[j, i] += y
        counts[j, i] += 1.0

    relation = np.zeros_like(sums)
    seen = counts > 0
    relation[seen] = sums[seen] / counts[seen]
    np.fill_diagonal(relation, 1.0)

    evals, evecs = np.linalg.eigh(relation)
    order = np.argsort(evals)[::-1][:rank]
    positive = np.maximum(evals[order], 0.0)
    factor = evecs[:, order] * np.sqrt(positive)[None, :]

    train_score = np.sum(factor[cue] * factor[probe], axis=1)
    # Training-only threshold search.  Quantiles keep this deterministic and
    # avoid using the holdout labels for any selection.
    candidates = np.unique(
        np.concatenate(
            [
                np.quantile(train_score, np.linspace(0.01, 0.99, 199)),
                np.array([float(train_score.min()) - 1e-12, float(train_score.max()) + 1e-12]),
            ]
        )
    )
    train_acc = np.array(
        [np.mean((train_score >= threshold) == label) for threshold in candidates]
    )
    best = int(np.argmax(train_acc))
    threshold = float(candidates[best])

    observed_fraction = float(np.mean(seen[np.triu_indices(n_units, k=1)]))
    return factor, threshold, {
        "training_accuracy": float(train_acc[best]),
        "observed_unordered_pair_fraction": observed_fraction,
        "float32_factor_bytes": float(n_units * rank * 4),
        "free_pairwise_matrix_float32_bytes": float(n_units * n_units * 4),
    }


def accuracy(
    factor: np.ndarray,
    threshold: float,
    cue: np.ndarray,
    probe: np.ndarray,
    label: np.ndarray,
) -> float:
    score = np.sum(factor[cue] * factor[probe], axis=1)
    return float(np.mean((score >= threshold) == label))


def run(seed: int, regime: str, protocol: Protocol = Protocol()) -> dict[str, object]:
    rng = np.random.default_rng(seed)
    groups = _groups(protocol.n_units, protocol.n_contexts, regime, rng)
    train = _make_trials(groups, rng, protocol.train_trials)
    test = _make_trials(groups, rng, protocol.test_trials)

    factor, threshold, accounting = fit_addressed_factor(
        train.cue,
        train.probe,
        train.label,
        n_units=protocol.n_units,
        rank=protocol.n_contexts,
    )
    test_accuracy = accuracy(factor, threshold, test.cue, test.probe, test.label)

    transition = factor @ factor.T
    singular_values = np.linalg.svd(transition, compute_uv=False)
    numerical_rank = int(np.sum(singular_values > 1e-10))

    return {
        "seed": seed,
        "regime": regime,
        "rank_budget": protocol.n_contexts,
        "test_accuracy": test_accuracy,
        "training_only_threshold": threshold,
        "numerical_transition_rank": numerical_rank,
        "accounting": accounting,
        "interpretation": {
            "uses_physical_positions": False,
            "uses_test_labels_for_selection": False,
            "capability_attacker_pass": bool(test_accuracy >= 0.95),
            "resource_advantage_established": False,
        },
    }


def suite() -> dict[str, object]:
    seeds = [18101, 18102, 18103, 18104, 18105]
    runs = [run(seed, regime) for regime in ("aligned", "scrambled") for seed in seeds]

    summary: dict[str, object] = {}
    for regime in ("aligned", "scrambled"):
        selected = [item for item in runs if item["regime"] == regime]
        accuracies = [float(item["test_accuracy"]) for item in selected]
        summary[regime] = {
            "accuracies": accuracies,
            "mean_accuracy": float(np.mean(accuracies)),
            "min_accuracy": float(np.min(accuracies)),
        }

    summary["frozen_checks"] = {
        "aligned_mean_at_least_0p95": bool(summary["aligned"]["mean_accuracy"] >= 0.95),
        "scrambled_mean_at_least_0p95": bool(summary["scrambled"]["mean_accuracy"] >= 0.95),
    }
    return {
        "suite": "gate1b_addressed_low_rank_attacker",
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

    result = suite() if args.suite else run(args.seed, args.regime)
    text = json.dumps(result, indent=2, sort_keys=True)
    print(text)
    if args.json is not None:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(text + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
