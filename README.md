# SplatNeuronPlusField

> **Two coupling geometries can coexist in the same neural tissue: an addressed synaptic graph and a metric extracellular overlay. The electric potential is treated as quasi-static and memoryless; the closed neuron–field loop has dynamics. A slower extracellular ionic milieu can carry genuine shared state.**

This repo starts where [`SplatNeuron`](https://github.com/anttiluode/SplatNeuron) stops. `SplatNeuron` remains the observer-resource project. This repo asks a different question: what changes when stateful neuron-like units interact through **both wired topology and shared physical geometry**?

## Physics guardrail

Do not give ordinary low-frequency extracellular electric potential an autonomous wave memory in the first model.

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

`phi(t)` has no independent temporal state in this approximation. The **loop** does.

A separate slow extracellular state may live in ionic/homeostatic variables such as activity-dependent extracellular potassium and glial buffering:

```text
tau_c dc/dt = diffusion(c) - clearance(c, glia) + release(neural activity)
```

The old relaxing `SmoothField` idea was therefore not a faithful ephaptic-electric model. Its *form* is closer to a toy slow extracellular concentration/state model, not specifically potassium unless the sources, diffusion and clearance are actually modelled.

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

The effective instantaneous metric coupling is

```text
A_eph = R G E
```

There is no free learned `A_eph[i,j]`; it is induced by emitter, medium and receiver geometry.

# Gate 0 — dual route

Preregistration: [`docs/GATE0_PREREG.md`](docs/GATE0_PREREG.md)  
Preflight correction: [`docs/GATE0_PREFLIGHT.md`](docs/GATE0_PREFLIGHT.md)  
Result: [`docs/GATE0_RESULT.md`](docs/GATE0_RESULT.md)

The synaptic matrix was deliberately constructed to be blind to a left-vs-right source distinction. The metric route could carry that distinction. Test-time source-position exchange changed the metric route while leaving `W` fixed; rewiring `W` changed the wired route while leaving the metric route fixed.

Registered three-seed result:

```text
seed    synaptic A   metric B   combined C   matched generic D   swap-position E   clamp F
18001     0.5008       1.0000      1.0000          1.0000            0.0150       0.5122
18002     0.5018       1.0000      1.0000          1.0000            0.0000       0.4940
18003     0.4935       1.0000      1.0000          1.0000            0.0000       0.5060
```

## Gate 0 verdict

**Dual-route structural instrument: PASS.**

**Special metric/ephaptic computational advantage: NOT ESTABLISHED.**

The matched generic extra coupling solved the toy perfectly as well. Therefore the supported claim is only:

> **A metric route can carry a distinction deliberately absent from a frozen wired route, and the two routes can be manipulated independently. This toy does not show that metric coupling is more capable or efficient than a generic additional matrix.**

That is enough to proceed because Gate 1 asks about a different resource: **shared slow state**.

# Gate 1 — two fields, not one

Add a slow extracellular ionic/homeostatic state and compare:

```text
quasi-static electric only
slow shared milieu only
both
matched independent private adaptation per unit
```

The private-adaptation attacker is mandatory. If the slow field merely implements ordinary per-unit fatigue/homeostasis, it has not earned itself.

The interesting result would be specifically metric sharing:

> one unit changes the local extracellular state and thereby changes the future excitability/history of physically nearby units **without an addressed edge**.

A stronger Gate 1 should also vary geometry while holding the synaptic graph fixed, then vary the graph while holding geometry fixed.

# Gate 2 — geometry becomes morphology

Only after the point-unit model is understood, replace scalar `E_i` and `R_i` with spatial emitter/receiver shapes:

```text
A_eph[j,i] = R_j G E_i
```

Then compare structured morphology against generic point-network emulators at fixed receiver error and explicit resource accounting.

The surviving `SplatNeuron` idea is not that morphology computes an impossible function. The interesting possibility is that morphology provides a **short physical implementation/description** of useful emitter/receiver transformations that generic point machinery reproduces only with more nodes, weights, intermediate communication or depth.

## Not claimed

- not a second electromagnetic brain;
- not evidence that ephaptic electric potential stores memories;
- not evidence that field patterns `enslave` neurons in vivo;
- not a wave-propagation model of extracellular electric potential;
- not a claim that morphology beats point neurons in capability;
- not an RL/reward architecture yet.

## Why the repo exists

> **What can a neural system gain from having addressed, rewireable coupling and metric, geometry-induced coupling living side by side, with a genuinely slow shared extracellular state layered on top?**

The desired output is a sequence of falsifiable gates, not a brain story.

See [`HANDOFF_CURRENT.md`](HANDOFF_CURRENT.md) for provenance, stop lines and the temporal/memory bridge.
