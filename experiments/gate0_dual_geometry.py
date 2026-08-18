"""Gate 0: can a metric route carry a distinction a frozen wired route cannot?

This is intentionally a *structural* synthetic test.  The synaptic matrix is
constructed to collapse two source addresses onto the same wired consequence.
The metric route is not expected to beat an arbitrary dense matrix; that
attacker is included precisely to prevent that overclaim.

Run:
    python experiments/gate0_dual_geometry.py --seed 18001
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import json
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from splatneuronplusfield.core import DualGeometry


@dataclass
class Dataset:
    activity: np.ndarray
    labels: np.ndarray


def orthogonal(rng: np.random.Generator, n: int) -> np.ndarray:
    q, r = np.linalg.qr(rng.normal(size=(n, n)))
    signs = np.sign(np.diag(r))
    signs[signs == 0] = 1.0
    return q * signs[None, :]


def matched_generic(a: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    """Randomize singular vectors while preserving singular values exactly."""

    _, singular, _ = np.linalg.svd(a, full_matrices=True)
    u = orthogonal(rng, a.shape[0])
    v = orthogonal(rng, a.shape[1])
    sigma = np.zeros_like(a)
    np.fill_diagonal(sigma, singular)
    return u @ sigma @ v.T


def make_system(n: int, rng: np.random.Generator) -> tuple[DualGeometry, int, int]:
    positions = np.linspace(-1.0, 1.0, n)
    left = n // 4
    right = 3 * n // 4

    # Deliberately insufficient wired route: left and right source columns are
    # identical.  A downstream observer of W @ x cannot infer which source
    # produced a unit-amplitude event.
    w = rng.normal(scale=0.025, size=(n, n))
    shared_column = rng.normal(scale=0.25, size=n)
    w[:, left] = shared_column
    w[:, right] = shared_column

    # Mild orientation/gain heterogeneity.  Position remains the dominant
    # metric address in Gate 0; morphology comes later.
    emitter = 0.8 + 0.4 * rng.random(n)
    receiver = 0.8 + 0.4 * rng.random(n)

    system = DualGeometry(
        w_syn=w,
        positions=positions,
        emitter_gain=emitter,
        receiver_gain=receiver,
        electric_length_scale=0.22,
    )
    return system, left, right


def make_dataset(
    n: int,
    left: int,
    right: int,
    rng: np.random.Generator,
    samples: int,
    noise: float,
) -> Dataset:
    labels = rng.integers(0, 2, size=samples)
    x = rng.normal(scale=noise, size=(samples, n))
    for row, label in enumerate(labels):
        source = right if label else left
        x[row, source] += 1.0
    return Dataset(activity=x, labels=labels)


def features_from_matrix(matrix: np.ndarray, x: np.ndarray) -> np.ndarray:
    # Mild nonlinearity prevents the experiment from being a pure matrix
    # identity test while retaining transparent control.
    return np.tanh(x @ matrix.T)


def fit_ridge_classifier(x: np.ndarray, labels: np.ndarray, ridge: float = 1e-3) -> np.ndarray:
    y = labels.astype(float) * 2.0 - 1.0
    design = np.column_stack([x, np.ones(len(x))])
    reg = ridge * np.eye(design.shape[1])
    reg[-1, -1] = 0.0
    return np.linalg.solve(design.T @ design + reg, design.T @ y)


def accuracy(weights: np.ndarray, x: np.ndarray, labels: np.ndarray) -> float:
    design = np.column_stack([x, np.ones(len(x))])
    pred = (design @ weights >= 0.0).astype(int)
    return float(np.mean(pred == labels))


def frob_relative(a: np.ndarray, b: np.ndarray) -> float:
    denom = max(float(np.linalg.norm(a)), 1e-12)
    return float(np.linalg.norm(a - b) / denom)


def run(seed: int, train_samples: int, test_samples: int, noise: float) -> dict:
    rng = np.random.default_rng(seed)
    n = 32
    system, left, right = make_system(n, rng)

    train = make_dataset(n, left, right, rng, train_samples, noise)
    test = make_dataset(n, left, right, rng, test_samples, noise)

    w = system.w_syn
    a = system.a_eph
    combined = w + a
    generic = matched_generic(a, rng)
    combined_generic = w + generic

    matrices = {
        "A_synaptic_only": w,
        "B_metric_only": a,
        "C_synaptic_plus_metric": combined,
        "D_synaptic_plus_matched_generic": combined_generic,
    }

    results: dict[str, object] = {
        "seed": seed,
        "n": n,
        "source_indices": [left, right],
        "train_samples": train_samples,
        "test_samples": test_samples,
        "noise": noise,
        "conditions": {},
    }

    fitted: dict[str, np.ndarray] = {}
    for name, matrix in matrices.items():
        f_train = features_from_matrix(matrix, train.activity)
        f_test = features_from_matrix(matrix, test.activity)
        readout = fit_ridge_classifier(f_train, train.labels)
        fitted[name] = readout
        results["conditions"][name] = accuracy(readout, f_test, test.labels)

    # Post-training interventions on condition C.
    readout_c = fitted["C_synaptic_plus_metric"]

    permutation = rng.permutation(n)
    shuffled_positions = system.positions[permutation]
    position_system = system.with_positions(shuffled_positions)
    position_matrix = position_system.w_syn + position_system.a_eph
    pos_features = features_from_matrix(position_matrix, test.activity)

    emitter_perm = rng.permutation(n)
    receiver_perm = rng.permutation(n)
    orientation_system = DualGeometry(
        w_syn=w.copy(),
        positions=system.positions.copy(),
        emitter_gain=system.emitter_gain[emitter_perm],
        receiver_gain=system.receiver_gain[receiver_perm],
        electric_length_scale=system.electric_length_scale,
    )
    orientation_matrix = orientation_system.w_syn + orientation_system.a_eph
    orientation_features = features_from_matrix(orientation_matrix, test.activity)

    clamped_features = features_from_matrix(w, test.activity)

    results["interventions"] = {
        "E_position_shuffle_test_only": accuracy(readout_c, pos_features, test.labels),
        "F_emit_receive_pairing_shuffle_test_only": accuracy(
            readout_c, orientation_features, test.labels
        ),
        "G_ephaptic_clamp_test_only": accuracy(readout_c, clamped_features, test.labels),
    }

    # Orthogonal route sanity checks.  Moving geometry must not alter W;
    # rewiring W must not alter A_eph.
    rewired_w = w.copy()
    rewired_w[:, [left, right]] = rewired_w[:, [right, left]]
    rewired_system = system.with_w_syn(rewired_w)

    results["route_independence"] = {
        "geometry_change_relative_W": frob_relative(w, position_system.w_syn),
        "geometry_change_relative_Aeph": frob_relative(a, position_system.a_eph),
        "rewire_change_relative_W": frob_relative(w, rewired_system.w_syn),
        "rewire_change_relative_Aeph": frob_relative(a, rewired_system.a_eph),
        "matched_generic_frobenius_ratio": float(np.linalg.norm(generic) / np.linalg.norm(a)),
        "matched_generic_singular_value_max_abs_error": float(
            np.max(np.abs(np.linalg.svd(generic, compute_uv=False) - np.linalg.svd(a, compute_uv=False)))
        ),
    }

    # These are interpretation aids, not CI assertions.
    c_acc = results["conditions"]["C_synaptic_plus_metric"]
    a_acc = results["conditions"]["A_synaptic_only"]
    generic_acc = results["conditions"]["D_synaptic_plus_matched_generic"]
    results["interpretation"] = {
        "metric_route_exposes_frozen_W_null": bool(c_acc > a_acc + 0.20),
        "generic_attacker_matches_within_5pp": bool(generic_acc >= c_acc - 0.05),
        "special_field_advantage_established": False,
    }
    return results


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=18001)
    parser.add_argument("--train-samples", type=int, default=4000)
    parser.add_argument("--test-samples", type=int, default=4000)
    parser.add_argument("--noise", type=float, default=0.05)
    parser.add_argument("--json", type=Path, default=None)
    args = parser.parse_args()

    result = run(args.seed, args.train_samples, args.test_samples, args.noise)
    text = json.dumps(result, indent=2, sort_keys=True)
    print(text)
    if args.json is not None:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(text + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
