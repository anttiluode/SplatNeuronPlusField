import numpy as np

from experiments.multiplex_math_sanity import (
    attribution_counterexamples,
    check_projection_identity,
    random_capture_fraction,
)


def test_shared_projection_identity():
    out = check_projection_identity(seed=7)
    assert out["Delta_DOF"] >= 0
    assert out["containment_error"] < 1e-10
    assert out["projection_identity_error"] < 1e-10
    assert np.isclose(out["extra_error"], out["deleted_task_energy"], atol=1e-10)


def test_random_subspace_capture_matches_r_over_R():
    empirical, theory = random_capture_fraction(
        ambient_dim=12,
        shared_dim=4,
        trials=4000,
        seed=11,
    )
    assert abs(empirical - theory) < 0.03


def test_observational_identifiability_is_not_sharing_economy():
    out = attribution_counterexamples()
    assert out["no_sharing_Delta"] == 0
    assert out["no_sharing_sum_observation_nullity"] == 2
    assert out["max_sharing_Delta"] == 2
    assert out["max_sharing_full_observation_nullity"] == 0
