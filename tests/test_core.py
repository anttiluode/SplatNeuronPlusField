import numpy as np

from splatneuronplusfield.core import DualGeometry, SlowMilieu, induced_ephaptic, metric_green


def test_induced_ephaptic_is_rge():
    positions = np.array([-1.0, 0.0, 1.0])
    g = metric_green(positions, length_scale=0.5)
    emitter = np.array([1.0, 2.0, 3.0])
    receiver = np.array([4.0, 5.0, 6.0])
    a = induced_ephaptic(g, emitter, receiver)
    expected = np.diag(receiver) @ g @ np.diag(emitter)
    np.testing.assert_allclose(a, expected)


def test_geometry_and_wired_route_can_be_changed_independently():
    rng = np.random.default_rng(4)
    n = 8
    w = rng.normal(size=(n, n))
    positions = np.linspace(-1.0, 1.0, n)
    system = DualGeometry(
        w_syn=w,
        positions=positions,
        emitter_gain=np.ones(n),
        receiver_gain=np.ones(n),
        electric_length_scale=0.3,
    )

    a0 = system.a_eph.copy()
    w0 = system.w_syn.copy()

    moved = system.with_positions(positions[::-1].copy())
    np.testing.assert_allclose(moved.w_syn, w0)
    # Reversal preserves pairwise distances, so use a non-isometric permutation.
    moved = system.with_positions(positions[[0, 3, 1, 7, 2, 6, 4, 5]])
    assert not np.allclose(moved.a_eph, a0)

    rewired = system.with_w_syn(w[:, rng.permutation(n)])
    assert not np.allclose(rewired.w_syn, w0)
    np.testing.assert_allclose(rewired.a_eph, a0)


def test_quasistatic_phi_has_no_hidden_state():
    n = 6
    system = DualGeometry(
        w_syn=np.zeros((n, n)),
        positions=np.linspace(-1.0, 1.0, n),
        emitter_gain=np.ones(n),
        receiver_gain=np.ones(n),
        electric_length_scale=0.4,
    )
    x = np.arange(n, dtype=float)
    first = system.a_eph @ x
    second = system.a_eph @ x
    np.testing.assert_allclose(first, second)


def test_slow_milieu_really_has_state_and_relaxes():
    positions = np.linspace(-1.0, 1.0, 5)
    milieu = SlowMilieu(
        positions=positions,
        concentration=np.zeros(5),
        diffusion=0.0,
        clearance=1.0,
        release_gain=1.0,
    )

    activity = np.array([0.0, 0.0, 1.0, 0.0, 0.0])
    after_release = milieu.step(activity, dt=0.1)
    assert after_release[2] > 0.0

    after_relax = milieu.step(np.zeros(5), dt=0.1)
    assert 0.0 < after_relax[2] < after_release[2]
