from experiments.gate1_shared_milieu import Protocol, run


def small_protocol() -> Protocol:
    return Protocol(train_trials=1000, test_trials=1000)


def test_aligned_metric_history_beats_private_and_matched_random() -> None:
    result = run(18101, "aligned", small_protocol())
    c = result["conditions"]["C_shared_metric_diffusion"]["accuracy"]
    b = result["conditions"]["B_private_same_clearance"]["accuracy"]
    g = result["conditions"]["G_shared_random_matched_spectrum"]["accuracy"]

    assert c > 0.80
    assert c > b + 0.20
    assert c > g + 0.20


def test_scrambling_removes_metric_advantage() -> None:
    result = run(18101, "scrambled", small_protocol())
    c = result["conditions"]["C_shared_metric_diffusion"]["accuracy"]
    assert c < 0.60


def test_geometry_intervention_breaks_frozen_metric_readout() -> None:
    result = run(18101, "aligned", small_protocol())
    c = result["conditions"]["C_shared_metric_diffusion"]["accuracy"]
    e = result["interventions"]["E_metric_geometry_shuffle_test_only"]

    assert c > 0.80
    assert e < 0.60


def test_attackers_are_mechanically_matched() -> None:
    result = run(18101, "aligned", small_protocol())
    checks = result["checks"]

    assert checks["positive_trials_have_distinct_cue_probe"]
    assert checks["B_equals_D_max_abs"] == 0.0
    assert checks["metric_vs_random_decay_spectrum_max_abs"] < 1e-10
    assert checks["geometry_shuffle_decay_spectrum_max_abs"] < 1e-10
