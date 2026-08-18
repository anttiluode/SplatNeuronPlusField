# Gate 0 preregistration — dual geometry

Date frozen: 2026-08-18

## Question

Can a metric, geometry-induced coupling route carry a distinction that a deliberately insufficient frozen synaptic route cannot, while the two routes remain independently manipulable?

This gate does **not** test whether ephaptic coupling is a uniquely efficient computational primitive. A generic matched coupling route is an explicit attacker and is allowed to win.

## Toy world

- `N = 32` point units on a one-dimensional physical axis.
- Two source addresses are used: one left and one right.
- Each sample activates exactly one source plus small independent activity noise.
- Label = which source was activated.
- The frozen synaptic matrix is constructed so that its two source columns are identical. Therefore the wired route intentionally collapses the task distinction.
- The metric route is induced from physical position using a distance-decaying Green-like kernel and scalar emit/receive gains.

This is a **constructed null** for the wired route. It is not evidence that real synaptic networks are generally blind to metric distinctions.

## Conditions

```text
A  synaptic only
B  metric only
C  synaptic + metric
D  synaptic + generic extra coupling
```

Condition D preserves the singular values of the metric coupling exactly while randomizing its left/right singular vectors. It is therefore a strong warning against interpreting a C>A result as a special geometric advantage.

Post-training interventions use the readout trained under C:

```text
E  shuffle physical positions at test time only
F  shuffle emitter/receiver gain pairing at test time only
G  clamp the metric route at test time only
```

## Route-independence checks

Two orthogonal manipulations are measured directly:

```text
hold W fixed, change positions
hold positions fixed, rewire W
```

Required algebraic sanity:

```text
changing positions changes A_eph but not W
rewiring W changes W but not A_eph
```

where

```text
A_eph = R G E
```

## Readout

A ridge-linear classifier is trained on the one-step nonlinear response `tanh(A x)` for each independently trained condition. The intervention conditions E/F/G do **not** retrain the readout.

## Interpretation before results

### Structural keep

Keep the phrase **dual coupling geometry** if:

1. the algebraic route-independence checks pass;
2. C recovers substantially more of the constructed source distinction than A;
3. post-training geometric/clamp interventions perturb C in the expected direction.

A useful heuristic for item 2 is `C - A > 0.20` accuracy, but report the full values and seeds rather than treating this as a discovered threshold.

### Generic attacker

If D matches or beats C, the honest result is:

> a second route can carry information hidden from the frozen wired route, but this toy does not establish a special computational advantage for metric coupling.

That is an acceptable Gate 0 result.

### Kill

Kill the current implementation if:

- A already solves the constructed null reliably (the harness leaked source identity);
- changing positions changes `W` or rewiring `W` changes `A_eph` (routes not actually separated);
- C fails to expose the distinction despite the metric kernel having different source columns;
- E/F/G appear impressive only after retraining the readout.

## What Gate 0 does not contain

- no autonomous extracellular electric-field dynamics;
- no ionic field;
- no morphology;
- no growth/pruning;
- no RL/reward objective;
- no learned geometry;
- no biological parameter fit.

Those are later gates only if the structural instrument is sound.
