# SplatNeuronPlusField — current handoff

Date: 2026-08-18

## One-line state

> **New repo. We are testing whether neural computation can use two distinct coupling geometries side by side — a rewireable synaptic graph and a metric extracellular route — while keeping quasi-static electric potential separate from genuinely slow extracellular ionic state.**

Nothing has passed yet.

## Provenance

This repo branches conceptually from `anttiluode/SplatNeuron` after its observer-resource work through Gate 13c was merged to `main`.

`SplatNeuron` started as “splats as neurons” and was repeatedly attacked. What survived there was not a special Gabor/frequency neuron but a conditional observer-description result: when task structure aligns with a compact observation vocabulary, one-time map/configuration bits can reduce required logical measurement width; dense rotation/high task complexity removes that advantage.

Do not move those claims here. This repo asks a different question.

## Physics correction that starts the repo

The ordinary low-frequency extracellular electric potential should be treated, at first approximation, as quasi-static:

```text
phi(t) = G q(t)
```

where `q(t)` is the current source pattern and `G` is the volume-conductor/geometry operator.

`phi(t)` has no autonomous memory in this approximation.

The loop does:

```text
neural state_t
   -> source currents q_t
   -> phi_t = G q_t
   -> ephaptic perturbation of membranes
   -> neural state_{t+1}
```

A distinct slow extracellular state can live in ionic/metabolic variables such as extracellular K+, glial buffering, pH and related homeostatic variables. That state can have genuine relaxation/diffusion dynamics.

Therefore **do not collapse electric potential and ionic milieu into one “field.”**

## The architectural object

Each unit inhabits three different neighborhoods:

```text
intracellular geometry
    where inside this cell did a signal arrive?

synaptic topology
    who is wired to this cell?

extracellular metric geometry
    who is physically near/aligned in the shared medium?
```

Minimal equations:

```text
s = W f(v)
q = E f(v)
phi = G q
e = R phi

tau_c dc/dt = D_c Laplacian(c) - clearance(c) + B f(v)

tau_v dv/dt = F(v, h, s + lambda_e e, c)
dh/dt = H(h, v, input)
```

Effective ephaptic coupling:

```text
A_eph = R G E
```

The key structural property is that `A_eph` is induced by emitter geometry, medium geometry and receiver geometry. It is not stored as a free pairwise weight matrix.

## Gate 0 — dual route, before biology stories

Question:

> **Can the metric route carry a task-relevant distinction that a deliberately insufficient frozen synaptic route cannot, and can the two routes be manipulated independently?**

Conditions:

```text
A  synapses only
B  ephaptic metric only
C  synapses + ephaptic metric
D  synapses + matched generic dense/low-rank extra coupling
E  C with positions shuffled
F  C with emitter/receiver orientation pairing shuffled
G  C with ephaptic route clamped/cancelled at test time
```

Mandatory orthogonal interventions:

```text
hold W fixed, move/shuffle geometry
hold geometry fixed, rewire W
```

What would count:

- changing geometry changes the metric route while leaving `W` unchanged;
- rewiring `W` changes the synaptic route while leaving metric coupling unchanged;
- there exists at least one controlled task where `W` is blind to a distinction and the metric route exposes it;
- the matched generic route is reported honestly. If generic coupling does the same job at equal resources, the result is **dual-route existence**, not a special field-computation advantage.

## Gate 1 — slow shared milieu

Only after Gate 0.

Add a slow diffusive/relaxing extracellular state and compare:

```text
electric only
ionic only
both
matched independent private adaptation per unit
```

The private-adaptation attacker is mandatory. If a shared ionic field merely reproduces ordinary per-unit fatigue/homeostasis, it has not earned architectural importance.

Interesting result would be specifically **metric sharing**: one unit changes the local milieu and thereby changes the excitability/history of physically nearby units without an addressed edge.

## Gate 2 — morphology

Only after point units.

Replace scalar `E_i` and `R_i` with spatial emitter/receiver shapes. Then:

```text
A_eph[j,i] = R_j G E_i
```

This is the place to reconnect to the detailed geometric-neuron line.

The claim to test is not “a detailed neuron computes a function point neurons cannot.” Point-network emulators are attackers. The interesting currency is whether morphology provides a **short physical implementation/description** of receiver-specific spatiotemporal transformations that generic point machinery reproduces only with more nodes, weights, depth, communication or synchronization.

## Temporal / memory bridge

Keep this conceptual distinction clean:

```text
quasi-static phi_t       instantaneous shared metric coupling
slow extracellular c_t  shared local environmental state
neuron/synapse h_t       private/addressed memory and plasticity
recurrent loops          system-level temporal persistence
```

A memory or “momentary time window” does not have to be stored in `phi`. The field can instead alter which currently active/residual states influence one another now. The closed loop can have long history even when one component is memoryless.

## Evolution / value

Do not put “seek reward / flee pain” into Gate 0 as an RL objective. That would turn the repo into an ordinary RL system with unusual coupling before the coupling has earned itself.

If value enters later, the cleaner architectural route is a **third diffuse modulatory channel** (for example a coarse model of neuromodulatory/volume transmission) that changes gain, plasticity or thresholds over a metric neighborhood. Then test it against explicit global reward/gain controls.

## Old Units repo lesson

The old `SmoothField` update

```text
F <- (1-r) F + r new
```

was not a faithful model of quasi-static extracellular electric potential because it gave the electric field autonomous temporal state.

But that equation form is plausibly useful as a *toy* relaxation model for a slow shared extracellular variable. Do not pretend it is specifically potassium without modelling/source/clearance controls.

Also retain the old lesson: naming units `sensory`, `memory`, `integration`, etc. does not create specialization. Roles must emerge or be experimentally imposed as an explicit condition.

## Stop lines

- no “second electromagnetic brain” claim;
- no field-memory claim for quasi-static electric potential;
- no “slaving/conductor” claim from observational Granger directionality;
- no autonomous wave equation for the ephaptic electric field unless modelling a different physical regime and saying so;
- no reward story before dual coupling earns itself;
- no growth/pruning story before fixed-capacity controls;
- no claim that spatial structure supplies semantics;
- matched generic coupling and private-adaptation attackers stay mandatory.

## Immediate files to build

```text
splatneuronplusfield/core.py
experiments/gate0_dual_geometry.py
tests/test_core.py
docs/GATE0_PREREG.md
```

The repo should first become a small falsifiable instrument. Biology and morphology come later.
