# SplatNeuronPlusField

> **Two coupling geometries can coexist in the same neural tissue: an addressed synaptic graph and a metric extracellular overlay. The electric field is quasi-static and memoryless; the closed neuron–field loop has dynamics. A slower ionic milieu can carry genuine shared state.**

This repo starts from the point where `SplatNeuron` stops. `SplatNeuron` remains the observer-resource project. This repo asks a different, more biological question: what changes when stateful neuron-like units interact through **both wired topology and shared physical geometry**?

## Physics guardrail

Do not give the ordinary low-frequency extracellular electric potential an artificial autonomous wave memory.

Use, schematically:

```text
neural transmembrane/source state q(t)
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

A separate slow extracellular state may exist in ionic/metabolic variables, for example activity-dependent extracellular potassium and glial buffering. That belongs in a different equation:

```text
tau_c * dc/dt = diffusion(c) - clearance(c, glia) + release(neural activity)
```

This means the old idea of a relaxing `SmoothField` was not a faithful ephaptic-electric model, but the *form* is much closer to a slow ionic/extracellular milieu.

## Three neighborhoods

A neuron can simultaneously inhabit:

1. **intracellular / dendritic geometry** — where inside the cell an input arrives;
2. **synaptic / topological geometry** — who is wired to whom;
3. **extracellular / metric geometry** — who is physically near and aligned in a shared medium.

The first two can be very different from the third.

## Minimal model

For point units first:

```text
synaptic drive:        s = W f(v)
source geometry:       q = E f(v)
quasi-static field:    phi = G q
ephaptic readout:      e = R phi
slow ionic field:      tau_c dc/dt = D_c Laplacian(c) - clearance(c) + B f(v)
unit dynamics:         tau_v dv/dt = F(v, h, s + lambda_e e, c)
private state:         dh/dt = H(h, v, input)
```

The effective instantaneous ephaptic coupling is

```text
A_eph = R G E
```

There is no free learned `A_eph[i,j]`; it is induced by emitter geometry, medium geometry and receiver geometry.

## Gate 0 — the claim that must earn the repo

Do **not** ask merely whether adding a field improves a task. A matched arbitrary coupling matrix can do that.

Freeze a synaptic matrix `W` that is deliberately insufficient for a discrimination. Then ask whether a metric field route can carry a distinction that the topological route cannot.

Registered conditions:

```text
A  synapses only
B  metric ephaptic route only
C  synapses + metric ephaptic route
D  synapses + matched generic dense/low-rank coupling
E  C with physical positions shuffled
F  C with emitter/receiver orientation pairing shuffled
G  C with the ephaptic route clamped/cancelled at test time
```

The key intervention is orthogonal:

```text
hold W fixed, change geometry
vs
hold geometry fixed, rewire W
```

If those manipulations do not produce separable consequences, `two networks` is only a description, not a computational result.

## Gate 1 — two fields, not one

Only if Gate 0 survives, add a slow extracellular ionic field. Compare:

```text
quasi-static electric only
slow ionic only
both
matched scalar adaptation / homeostasis baseline
```

Ask whether the slow metric state creates history-dependent local excitability that cannot be reproduced by giving every unit an independent private adaptation variable at matched state/parameter count.

That private-adaptation attacker is mandatory: otherwise a shared potassium-like field may just be an expensive way to implement local fatigue/homeostasis.

## Gate 2 — geometry becomes morphology

Only after the point-unit version is understood, replace scalar emit/read coefficients with spatial emitter and receiver shapes:

```text
A_eph[j,i] = R_j G E_i
```

Then compare real/structured morphology against generic point-network emulators at fixed receiver error and explicit resource accounting.

The surviving `SplatNeuron` idea is not that morphology enables an impossible function. It may provide a **short physical description of useful emitter/receiver transformations** that a generic point network can emulate only with more nodes, weights, intermediate communication or depth.

## Not claimed

- not a second electromagnetic brain;
- not evidence that ephaptic fields store memories;
- not evidence that field patterns `enslave` neurons in vivo;
- not a wave-propagation model of extracellular electric potential;
- not a claim that morphology beats point neurons in capability;
- not an RL/reward architecture yet.

## Why the repo exists

The working question is narrower:

> **What can a neural system gain from having addressed, rewireable coupling and metric, geometry-induced coupling living side by side, with shared slow extracellular state layered on top?**

The desired output is a sequence of falsifiable gates, not a brain story.

See [`HANDOFF_CURRENT.md`](HANDOFF_CURRENT.md) for provenance and stop lines.
