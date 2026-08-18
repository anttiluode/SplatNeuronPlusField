# SplatNeuronPlusField — current handoff

Date: 2026-08-18

## One-line state

> **Gate 0 has established only the structural existence of two independently manipulable coupling routes in the toy instrument. It has *not* established a special computational advantage for metric/ephaptic coupling. The next live question is whether a slow shared extracellular state buys something that matched private adaptation does not.**

## Provenance

This repo branches conceptually from `anttiluode/SplatNeuron` after its observer-resource work through Gate 13c was merged to `main`.

`SplatNeuron` started as “splats as neurons” and was repeatedly attacked. What survived there was a conditional observer-description result: when task structure aligns with a compact observation vocabulary, one-time map/configuration bits can reduce required logical measurement width; dense rotation/high task complexity removes that advantage.

Do not move those empirical claims here. This repo asks a different question.

## Physics correction that starts the repo

Treat ordinary low-frequency extracellular electric potential, at first approximation, as quasi-static:

```text
phi(t) = G q(t)
```

where `q(t)` is the current-source pattern and `G` is a volume-conductor/geometry operator.

`phi(t)` has no autonomous memory in this approximation.

The loop does:

```text
neural state_t
   -> source currents q_t
   -> phi_t = G q_t
   -> ephaptic perturbation of membranes
   -> neural state_{t+1}
```

A distinct slow extracellular state can live in ionic/homeostatic variables such as extracellular K+, glial buffering, pH and related variables. That state can have real relaxation/diffusion dynamics.

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

Effective instantaneous metric coupling:

```text
A_eph = R G E
```

The structural property is that `A_eph` is induced by emitter geometry, medium geometry and receiver geometry. It is not stored as a free pairwise weight matrix.

# Gate 0 — completed

Preregistration: `docs/GATE0_PREREG.md`  
Preflight correction: `docs/GATE0_PREFLIGHT.md`  
Result: `docs/GATE0_RESULT.md`

The wired matrix was deliberately constructed to collapse a two-source distinction. The metric route could expose it.

Registered local reproduction:

```text
seed    synaptic A   metric B   combined C   matched generic D   source-swap E   clamp F
18001     0.5008       1.0000      1.0000          1.0000            0.0150       0.5122
18002     0.5018       1.0000      1.0000          1.0000            0.0000       0.4940
18003     0.4935       1.0000      1.0000          1.0000            0.0000       0.5060
```

Route algebra behaved as required:

```text
move metric source positions  -> A_eph changes, W unchanged
rewire W                      -> W changes, A_eph unchanged
```

The source-position counterfactual reused the already-trained C readout; no retraining was allowed.

## Gate 0 verdict

```text
DUAL_ROUTE_INSTRUMENT              PASS
SPECIAL_METRIC_ADVANTAGE           NOT ESTABLISHED
MATCHED_GENERIC_ATTACKER           PERFECT TOO
```

Supported statement:

> **A metric route can carry a distinction deliberately absent from a frozen wired route, and the two routes can be independently manipulated. This constructed toy does not show a metric/ephaptic advantage over generic additional coupling.**

This is plumbing, not neuroscience.

# Gate 1 — live next experiment

Question:

> **Does a slow shared metric state create useful history/coupling that cannot be reproduced by giving each unit matched independent private adaptation?**

Add only one new object:

```text
c_i(t)  slow extracellular/homeostatic state over physical positions
```

Toy dynamics:

```text
tau_c dc/dt = D_c Laplacian(c) - k_clear c + b release(v)
```

Neural units receive `c_i` as a local excitability/gain/threshold perturbation.

## Mandatory conditions

```text
A  no slow adaptation
B  independent private adaptation per unit
C  shared slow metric milieu
D  C with diffusion removed (local extracellular reservoirs only)
E  C with geometry shuffled at test time / intervention
F  private adaptation with matched total state dimension and decay constants
```

The key attacker is B/F, not “no field.”

If private adaptation matches C, then the slow field is just an expensive implementation of ordinary fatigue/homeostasis in this toy.

What would be interesting is specifically **non-addressed shared history**:

```text
unit i fires
   -> local shared c changes
   -> nearby unwired j changes future excitability
   -> effect decays/diffuses with metric distance
```

and a task where that shared history is useful under matched state/parameter count.

## Gate 1 design warning

Do not hand the task a label that is literally “which cells are physically near.” That would make the metric field win by construction.

Use at least two structure regimes:

```text
aligned world   task-relevant events have physical locality
scrambled world same latent task after permutation/dense remapping
```

Prediction to register before result:

```text
shared metric state may help only in aligned world;
private adaptation should be competitive or superior after scrambling.
```

If so, the result is conditional inductive bias again, not a universal field advantage.

# Gate 2 — morphology later

Only after point-unit Gate 1.

Replace scalar `E_i` and `R_i` with spatial emitter/receiver shapes:

```text
A_eph[j,i] = R_j G E_i
```

Reconnect to the detailed geometric-neuron line only here.

The claim to test is not “detailed neurons compute functions point neurons cannot.” Point-network emulators remain mandatory attackers. The interesting currency is whether morphology gives a **short physical implementation/description** of receiver-specific spatiotemporal transformations that generic point machinery reproduces only with more nodes, weights, depth, communication or synchronization.

# Temporal / memory bridge

Keep these layers separate:

```text
quasi-static phi_t       instantaneous shared metric coupling
slow extracellular c_t  shared local environmental state
neuron/synapse h_t       private/addressed memory and plasticity
recurrent loops          system-level temporal persistence
```

A memory or momentary time window does not have to be stored in `phi`.

A memory-bearing loop can instead be distributed across stateful neurons/synapses/slow milieu while the quasi-static field continually redraws the instantaneous metric coupling produced by the current sources.

This is the useful formulation of:

> **the individual phi_t has no memory; the closed loop does.**

# Context reinstatement / identity bridge

Do not turn the personal “loop” intuition into a literal field-memory claim.

The scientifically usable abstraction is:

```text
current context
   -> reinstates a distributed old state/trajectory
   -> reinstated state changes what is likely next
   -> repeated re-entry changes accessibility/plasticity over longer times
```

The environment can therefore be a route back into an old neural state without being a direct knob over memory strength.

At the architecture level this suggests that **identity/self-state is not one fixed point**. It can be a slowly changing distribution of recurrently accessible states, anchored by persistent structure but continually rewritten by experience and plasticity.

That concept belongs in later memory/context experiments, not Gate 1.

# Evolution / value

Do not put “seek reward / flee pain” into Gate 1 as a generic RL loss. That would make the repo ordinary RL with unusual coupling before the coupling has earned itself.

If value enters later, the cleaner architectural route is a **third diffuse modulatory channel** changing gain/plasticity/threshold over metric neighborhoods. Compare it against explicit global reward/gain controls.

# Old Units repo lesson

The old `SmoothField` update

```text
F <- (1-r) F + r new
```

was not a faithful model of quasi-static extracellular electric potential because it endowed that variable with autonomous temporal state.

But the equation form is useful as a toy relaxation law for a slow shared extracellular variable. Do not label it potassium without explicit release, diffusion, buffering/clearance and physiological scaling.

Also retain the old rule: naming roles `sensory`, `memory`, `integration`, etc. does not make them emerge.

# Stop lines

- no “second electromagnetic brain” claim;
- no field-memory claim for quasi-static electric potential;
- no “slaving/conductor” claim from observational Granger directionality;
- no autonomous wave equation for the ephaptic electric field unless explicitly modelling another physical regime;
- no special metric-compute claim from Gate 0 — generic coupling matched it;
- no slow-field claim without matched private adaptation;
- no reward story before coupling/state earns itself;
- no growth/pruning story before fixed-capacity controls;
- no claim that spatial structure supplies semantics;
- no claim that the old `SmoothField` was secretly a potassium model; at most it had the right *qualitative form* for a relaxing shared variable.

# Current files

```text
README.md
HANDOFF_CURRENT.md
splatneuronplusfield/core.py
experiments/gate0_dual_geometry.py
docs/GATE0_PREFLIGHT.md
docs/GATE0_PREREG.md
docs/GATE0_RESULT.md
tests/test_core.py
tests/test_gate0_harness.py
.github/workflows/ci.yml
```

Next builder: design and preregister Gate 1 before adding biological detail.
