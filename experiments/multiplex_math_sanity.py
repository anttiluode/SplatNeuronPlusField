"""Numerical sanity checks for docs/MULTIPLEX_MATH.md.

This is not a biological model and not a performance gate. It checks three local
linear-algebra statements used by the multiplex-morphology argument:

1. shared tangent S is contained in independent tangent T;
2. E_shared^2 - E_ind^2 = ||(P_T - P_S)t||^2;
3. a random r-plane in R dimensions captures r/R of fixed-vector energy in
   expectation.

It also prints two counterexamples showing that sharing economy is not the same
thing as observational non-identifiability.
"""

from __future__ import annotations

import numpy as np


def orth_basis(a: np.ndarray, tol: float = 1e-10) -> np.ndarray:
    """Return an orthonormal basis for the column space of a."""
    u, s, _ = np.linalg.svd(a, full_matrices=False)
    r = int(np.sum(s > tol))
    return u[:, :r]


def projector(a: np.ndarray) -> np.ndarray:
    q = orth_basis(a)
    return q @ q.T


def block_diag_columns(mats: list[np.ndarray]) -> np.ndarray:
    """Block diagonal matrix with mats as blocks."""
    rows = sum(m.shape[0] for m in mats)
    cols = sum(m.shape[1] for m in mats)
    out = np.zeros((rows, cols), dtype=float)
    r0 = c0 = 0
    for m in mats:
        nr, nc = m.shape
        out[r0 : r0 + nr, c0 : c0 + nc] = m
        r0 += nr
        c0 += nc
    return out


def make_case(seed: int = 7) -> tuple[list[np.ndarray], np.ndarray]:
    rng = np.random.default_rng(seed)
    # Three channel Jacobians sharing the same 4 morphology knobs.
    j1 = rng.normal(size=(5, 4))
    j2 = rng.normal(size=(4, 4))
    j3 = rng.normal(size=(6, 4))
    # Force some exact redundancy so R-r is nonzero and easy to see.
    j2[:, 3] = j2[:, 0] + j2[:, 1]
    j3[:, 3] = 2.0 * j3[:, 0] - j3[:, 2]
    return [j1, j2, j3], rng.normal(size=15)


def check_projection_identity(seed: int = 7) -> dict[str, float]:
    js, t = make_case(seed)
    j_shared = np.vstack(js)
    j_ind = block_diag_columns(js)

    p_s = projector(j_shared)
    p_t = projector(j_ind)

    r = np.linalg.matrix_rank(j_shared)
    r_ind = sum(np.linalg.matrix_rank(j) for j in js)

    e_s2 = np.linalg.norm((np.eye(len(t)) - p_s) @ t) ** 2
    e_i2 = np.linalg.norm((np.eye(len(t)) - p_t) @ t) ** 2
    deleted2 = np.linalg.norm((p_t - p_s) @ t) ** 2

    containment_error = np.linalg.norm(p_t @ p_s - p_s)
    identity_error = abs((e_s2 - e_i2) - deleted2)

    return {
        "R": float(r_ind),
        "r": float(r),
        "Delta_DOF": float(r_ind - r),
        "containment_error": float(containment_error),
        "projection_identity_error": float(identity_error),
        "extra_error": float(e_s2 - e_i2),
        "deleted_task_energy": float(deleted2),
    }


def random_capture_fraction(
    ambient_dim: int = 12,
    shared_dim: int = 4,
    trials: int = 20_000,
    seed: int = 11,
) -> tuple[float, float]:
    rng = np.random.default_rng(seed)
    t = rng.normal(size=ambient_dim)
    t /= np.linalg.norm(t)

    captures = []
    for _ in range(trials):
        a = rng.normal(size=(ambient_dim, shared_dim))
        q, _ = np.linalg.qr(a)
        captures.append(np.linalg.norm(q.T @ t) ** 2)

    return float(np.mean(captures)), shared_dim / ambient_dim


def attribution_counterexamples() -> dict[str, int]:
    # A: no sharing economy, but sum-only observation loses two directions.
    j_independent = np.eye(3)
    a_sum = np.ones((1, 3))
    delta_a = 3 - np.linalg.matrix_rank(j_independent)
    nu_a = 3 - np.linalg.matrix_rank(a_sum @ j_independent)

    # B: maximal sharing h=(theta,theta,theta), but full observation sees the
    # one actually available shared degree of freedom perfectly.
    j_shared = np.ones((3, 1))
    delta_b = 3 - np.linalg.matrix_rank(j_shared)
    a_full = np.eye(3)
    r_b = np.linalg.matrix_rank(j_shared)
    nu_b = r_b - np.linalg.matrix_rank(a_full @ j_shared)

    return {
        "no_sharing_Delta": int(delta_a),
        "no_sharing_sum_observation_nullity": int(nu_a),
        "max_sharing_Delta": int(delta_b),
        "max_sharing_full_observation_nullity": int(nu_b),
    }


def main() -> None:
    check = check_projection_identity()
    empirical, theory = random_capture_fraction()
    counter = attribution_counterexamples()

    print("MULTIPLEX MATH SANITY")
    for key, value in check.items():
        print(f"{key:34s}: {value:.12g}")

    print("\nRANDOM SUBSPACE NULL")
    print(f"empirical capture                 : {empirical:.6f}")
    print(f"theory r/R                       : {theory:.6f}")

    print("\nATTRIBUTION COUNTEREXAMPLES")
    for key, value in counter.items():
        print(f"{key:40s}: {value}")


if __name__ == "__main__":
    main()
