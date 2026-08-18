from experiments.gate0_dual_geometry import run


def test_gate0_constructed_null_and_route_independence():
    result = run(seed=18001, train_samples=1200, test_samples=1200, noise=0.05)

    conditions = result["conditions"]
    routes = result["route_independence"]

    # Harness check, not a biological result: by construction the two source
    # columns of W are identical, so the wired-only path should be near chance.
    assert conditions["A_synaptic_only"] < 0.65

    # The metric path should expose the address distinction in this constructed
    # toy. If this fails, Gate 0 is measuring a bug rather than dual routes.
    assert conditions["C_synaptic_plus_metric"] > conditions["A_synaptic_only"] + 0.20

    assert routes["geometry_change_relative_W"] < 1e-12
    assert routes["geometry_change_relative_Aeph"] > 1e-3
    assert routes["rewire_change_relative_W"] > 1e-3
    assert routes["rewire_change_relative_Aeph"] < 1e-12

    # The generic attacker preserves the singular spectrum by construction.
    assert abs(routes["matched_generic_frobenius_ratio"] - 1.0) < 1e-10
    assert routes["matched_generic_singular_value_max_abs_error"] < 1e-10
