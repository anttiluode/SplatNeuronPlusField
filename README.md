# SplatNeuronPlusField

> **Two coupling geometries can coexist in the same neural system: an addressed/topological route and a metric/shared route. The first toy gates now separate instantaneous metric coupling from genuinely slow shared metric state and ask what each buys under matched attackers.**

This repo starts where [`SplatNeuron`](https://github.com/anttiluode/SplatNeuron) stops. `SplatNeuron` remains the observer-resource project. `SplatNeuronPlusField` asks what changes when stateful units inhabit **both wired topology and shared physical geometry**.

## Physics guardrail

Do not give ordinary low-frequency extracellular electric potential autonomous wave memory in the first model.

```text
neural source state q(t)
        |
        v
phi(t) = G q(t)                 # quasi-static electric potential
        |
        v
receiver geometry R
        |
        v
ephaptic perturbation e(t)
        |
        v
next neural state
```

`phi(t)` has no independent temporal state in this approximation. The **closed loop** does.

A separate slow extracellular/homeostatic variable can have real relaxation/diffusion dynamics:

```text
tau_c dc/dt = diffusion(c) - clearance(c) + release(neural activity)
```

The current `c` is a normalized toy state. It is not called potassium unless release, diffusion, buffering, concentration scales and timescales are actually modelled.

## Three neighborhoods

A unit can simultaneously inhabit:

1. **intracellular / dendritic geometry** — where inside the cell an input arrives;
2. **synaptic / topological geometry** — who is wired to whom;
3. **extracellular / metric geometry** — who is physically near/aligned in a shared medium.

These neighborhoods need not agree.

## Minimal model

For point units first:

```text
synaptic drive:        s = W f(v)
source geometry:       q = E f(v)
quasi-static field:    phi = G q
ephaptic readout:      e = R phi
slow milieu:           tau_c dc/dt = D_c Laplacian(c) - clearance(c) + B f(v)
unit dynamics:         tau_v dv/dt = F(v, h, s + lambda_e e, c)
private state:         dh/dt = H(h, v, input)
```

Effective instantaneous metric coupling:

```text
A_eph = R G E
```

There is no free learned `A_eph[i,j]`; it is induced by emitter, medium and receiver geometry.

# Gate 0 — dual route

Files:

- [`docs/GATE0_PREREG.md`](docs/GATE0_PREREG.md)
- [`docs/GATE0_PREFLIGHT.md`](docs/GATE0_PREFLIGHT.md)
- [`docs/GATE0_RESULT.md`](docs/GATE0_RESULT.md)
- [`experiments/gate0_dual_geometry.py`](experiments/gate0_dual_geometry.py)

The synaptic matrix was deliberately blind to a two-source distinction. The metric route carried it. Test-time source-position exchange changed the metric route while leaving `W` fixed; rewiring `W` changed the wired route while leaving the metric route fixed.

Registered result:

```text
seed    synaptic A   metric B   combined C   matched generic D   swap-position E   clamp F
18001     .5008        1.0000      1.0000          1.0000            .0150        .5122
18002     .5018        1.0000      1.0000          1.0000            .0000        .4940
18003     .4935        1.0000      1.0000          1.0000            .0000        .5060
```

## Gate 0 verdict

**Dual-route structural instrument: PASS.**

**Special metric/ephaptic computational advantage: NOT ESTABLISHED.**

The matched generic extra coupling solved the toy perfectly too.

Supported statement:

> **A metric route can carry a distinction deliberately absent from a frozen wired route, and the two routes can be manipulated independently. This toy does not show that metric coupling is more capable or efficient than a generic additional matrix.**

# Gate 1 — shared slow metric history

Files:

- [`docs/GATE1_PREFLIGHT.md`](docs/GATE1_PREFLIGHT.md)
- [`docs/GATE1_FROZEN_PROTOCOL.md`](docs/GATE1_FROZEN_PROTOCOL.md)
- [`docs/GATE1_RESULT.md`](docs/GATE1_RESULT.md)
- [`experiments/gate1_shared_milieu.py`](experiments/gate1_shared_milieu.py)

A cue occurs at one unit. After a delay, a **different** probe unit is queried. The target is whether cue and probe belong to the same latent context. The receiver sees only the slow state at the probe coordinate.

Two structure regimes:

```text
aligned    latent context occupies contiguous physical neighborhood
scrambled  same latent grouping permuted across physical positions
```

Attackers:

```text
private state with same state count / local clearance
no-diffusion local reservoirs
private state with the same complete decay-rate spectrum
shared random symmetric state with the same complete decay spectrum
post-training geometry shuffle
```

Five-seed holdout means:

```text
condition                         aligned     scrambled
no slow state                     .5028        .5027
private same clearance            .5028        .5027
shared metric diffusion           .9123        .5082
shared no diffusion               .5028        .5027
private matched spectrum          .5028        .5027
random shared matched spectrum    .5186        .5093

metric geometry shuffle           .4838        .4861
```

## Gate 1 verdict

> **In this constructed task, a slow shared state makes past activity available across unwired units when task-relevant temporal context is aligned with the state's metric coupling geometry. Matching private state count and decay constants is insufficient, and a generic shared state with the same decay spectrum is insufficient. Destroying the alignment removes the advantage.**

Shorter:

> **History can have an address vocabulary. Here metric history helps only when the world's useful history is metric.**

This is a conditional inductive-bias result, not a unique-capability result and not neuroscience evidence.

The strongest next attacker is a **trainable addressed recurrent memory** at matched state/resource budget. If it learns the same structure cheaply, the remaining question becomes whether physical geometry saves connection-description, wiring, learning or communication cost.

# Grounding / recursive projection

See [`docs/GROUNDING_AND_RECURSION.md`](docs/GROUNDING_AND_RECURSION.md).

The model-collapse connection is kept separate from Gate 1.

Do not say:

```text
real world = high frequency
ephaptic field = reality channel
internal thought = model collapse
```

The useful distinction is:

```text
external innovation
    information entering from a source not generated by the current internal model

recursive projection
    repeated observation/training/reaction to consequences generated by the current model
```

The Gate-1 field is diffusive, so in its metric-Laplacian eigenbasis:

```text
c_k(t) = exp[-(clearance + diffusion * lambda_k)t] c_k(0)
```

Large-`lambda` spatial modes decay faster. The same field that usefully spreads broad local context can erase rapidly varying metric distinctions.

That suggests a future **innovation-provenance** instrument: measure which task-relevant modes survive closed self-recurrence, fresh external observations, mixed replay, and independently informative synthetic input.

The strong prediction is not `real good / synthetic bad`:

> **A lost distinction can only be restored when new input carries information about that distinction that is not already a consequence of the current loop state.**

# Morphology later

Only after the point-unit coupling/state questions are attacked, replace scalar `E_i` and `R_i` with spatial emitter/receiver shapes:

```text
A_eph[j,i] = R_j G E_i
```

Then compare morphology against generic point-network emulators at fixed receiver error and explicit resource accounting.

The surviving idea is not that morphology computes an impossible function. The possible resource claim is that morphology supplies a **short physical implementation/description** of useful transfer kernels that generic point machinery reproduces with more nodes, weights, depth, communication or synchronization.

## Not claimed

- not a second electromagnetic brain;
- not evidence that ephaptic electric potential stores memories;
- not evidence that field patterns `enslave` neurons in vivo;
- not a wave-propagation model of ordinary extracellular electric potential;
- not a claim that metric state has unique computational capability;
- not a claim that spatial structure supplies semantics;
- not a claim that model collapse is a model of thought;
- not a claim that synthetic/internal information is intrinsically inferior;
- not an RL/reward architecture yet.

## Why the repo exists

> **What can a neural system gain from having addressed, rewireable coupling and metric, geometry-induced coupling living side by side — and from letting history itself be stored in different address vocabularies?**

The desired output is a sequence of falsifiable gates, not a brain story.

See [`HANDOFF_CURRENT.md`](HANDOFF_CURRENT.md) for the current branch state, stop lines and next experiments.
