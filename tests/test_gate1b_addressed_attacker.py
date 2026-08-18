from experiments.gate1_shared_milieu import Protocol
from experiments.gate1b_addressed_attacker import run


def small_protocol() -> Protocol:
    return Protocol(train_trials=1000, test_trials=1000)


def test_addressed_attacker_solves_aligned_world_without_positions() -> None:
    result = run(18101, "aligned", small_protocol())
    assert result["test_accuracy"] >= 0.95
    assert result["interpretation"]["uses_physical_positions"] is False
    assert result["interpretation"]["uses_test_labels_for_selection"] is False


def test_addressed_attacker_also_solves_scrambled_world() -> None:
    result = run(18101, "scrambled", small_protocol())
    assert result["test_accuracy"] >= 0.95


def test_attacker_respects_rank_budget() -> None:
    result = run(18101, "aligned", small_protocol())
    assert result["numerical_transition_rank"] <= result["rank_budget"]
