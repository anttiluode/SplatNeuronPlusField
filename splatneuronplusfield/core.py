"""Core operators for SplatNeuronPlusField.

The physics distinction is deliberate:

* ``phi = G @ q`` is a quasi-static electric-potential solve. ``phi`` has no
  autonomous temporal state here.
* ``c`` is a separate slow extracellular variable with explicit
  diffusion/clearance dynamics.

This is a toy computational instrument, not a quantitative tissue model.
"""

from __future__ import annotations

from dataclasses import dataclass
import numpy as np

Array = np.ndarray


def _as_positions(positions: Array) -> Array:
    p = np.asarray(positions, dtype=float)
    if p.ndim == 1:
        p = p[:, None]
    if p.ndim != 2:
        raise ValueError("positions must have shape [n] or [n, d]")
    return p


def metric_green(
    positions: Array,
    *,
    length_scale: float = 0.25,
    self_coupling: float = 0.0,
    normalize_rows: bool = False,
) -> Array:
    """Return a simple distance-decaying metric coupling kernel.

    This is *not* a volume-conductor solver.  It is a controlled toy Green
    operator whose entries are induced by physical distance rather than free
    pairwise weights.
    """

    if length_scale <= 0:
        raise ValueError("length_scale must be positive")

    p = _as_positions(positions)
    delta = p[:, None, :] - p[None, :, :]
    distance = np.linalg.norm(delta, axis=-1)
    g = np.exp(-distance / length_scale)
    np.fill_diagonal(g, float(self_coupling))

    if normalize_rows:
        denom = g.sum(axis=1, keepdims=True)
        denom = np.where(denom > 0, denom, 1.0)
        g = g / denom
    return g


def induced_ephaptic(
    green: Array,
    emitter_gain: Array | None = None,
    receiver_gain: Array | None = None,
) -> Array:
    """Construct A_eph = R G E from scalar emitter/receiver geometries."""

    g = np.asarray(green, dtype=float)
    if g.ndim != 2 or g.shape[0] != g.shape[1]:
        raise ValueError("green must be a square matrix")
    n = g.shape[0]

    e = np.ones(n) if emitter_gain is None else np.asarray(emitter_gain, dtype=float)
    r = np.ones(n) if receiver_gain is None else np.asarray(receiver_gain, dtype=float)
    if e.shape != (n,) or r.shape != (n,):
        raise ValueError("emitter_gain and receiver_gain must have shape [n]")

    return r[:, None] * g * e[None, :]


def metric_laplacian(positions: Array, *, length_scale: float = 0.25) -> Array:
    """Graph Laplacian induced only by metric distance.

    Suitable for a toy slow diffusive extracellular variable.
    """

    g = metric_green(
        positions,
        length_scale=length_scale,
        self_coupling=0.0,
        normalize_rows=False,
    )
    degree = np.diag(g.sum(axis=1))
    return degree - g


@dataclass(frozen=True)
class DualGeometry:
    """A fixed wired graph plus a metric-induced ephaptic overlay."""

    w_syn: Array
    positions: Array
    emitter_gain: Array
    receiver_gain: Array
    electric_length_scale: float = 0.25

    def __post_init__(self) -> None:
        w = np.asarray(self.w_syn, dtype=float)
        p = _as_positions(self.positions)
        e = np.asarray(self.emitter_gain, dtype=float)
        r = np.asarray(self.receiver_gain, dtype=float)
        n = p.shape[0]
        if w.shape != (n, n):
            raise ValueError("w_syn must have shape [n, n]")
        if e.shape != (n,) or r.shape != (n,):
            raise ValueError("emitter_gain/receiver_gain must have shape [n]")

        object.__setattr__(self, "w_syn", w)
        object.__setattr__(self, "positions", p)
        object.__setattr__(self, "emitter_gain", e)
        object.__setattr__(self, "receiver_gain", r)

    @property
    def n(self) -> int:
        return self.w_syn.shape[0]

    @property
    def green(self) -> Array:
        return metric_green(
            self.positions,
            length_scale=self.electric_length_scale,
            self_coupling=0.0,
        )

    @property
    def a_eph(self) -> Array:
        return induced_ephaptic(self.green, self.emitter_gain, self.receiver_gain)

    def drive(
        self,
        activity: Array,
        *,
        synaptic_gain: float = 1.0,
        ephaptic_gain: float = 1.0,
    ) -> Array:
        x = np.asarray(activity, dtype=float)
        if x.shape != (self.n,):
            raise ValueError("activity must have shape [n]")
        return synaptic_gain * (self.w_syn @ x) + ephaptic_gain * (self.a_eph @ x)

    def with_positions(self, positions: Array) -> "DualGeometry":
        return DualGeometry(
            w_syn=self.w_syn.copy(),
            positions=positions,
            emitter_gain=self.emitter_gain.copy(),
            receiver_gain=self.receiver_gain.copy(),
            electric_length_scale=self.electric_length_scale,
        )

    def with_w_syn(self, w_syn: Array) -> "DualGeometry":
        return DualGeometry(
            w_syn=w_syn,
            positions=self.positions.copy(),
            emitter_gain=self.emitter_gain.copy(),
            receiver_gain=self.receiver_gain.copy(),
            electric_length_scale=self.electric_length_scale,
        )


@dataclass
class SlowMilieu:
    """Toy slow shared extracellular state.

    ``c`` may later stand for a normalized extracellular ionic/homeostatic
    variable.  It is intentionally not called an electric field.
    """

    positions: Array
    concentration: Array
    diffusion: float = 0.08
    clearance: float = 0.15
    release_gain: float = 0.10
    length_scale: float = 0.25

    def __post_init__(self) -> None:
        self.positions = _as_positions(self.positions)
        self.concentration = np.asarray(self.concentration, dtype=float).copy()
        if self.concentration.shape != (self.positions.shape[0],):
            raise ValueError("concentration must have shape [n]")

    def step(self, neural_activity: Array, *, dt: float = 0.01) -> Array:
        """Euler step for diffusion + clearance + activity-dependent release."""

        if dt <= 0:
            raise ValueError("dt must be positive")
        x = np.asarray(neural_activity, dtype=float)
        if x.shape != self.concentration.shape:
            raise ValueError("neural_activity must have shape [n]")

        lap = metric_laplacian(self.positions, length_scale=self.length_scale)
        release = self.release_gain * np.maximum(x, 0.0)
        dc = -self.diffusion * (lap @ self.concentration)
        dc += -self.clearance * self.concentration
        dc += release
        self.concentration = self.concentration + dt * dc
        return self.concentration.copy()
