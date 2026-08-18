# Gate 0 preregistration — dual geometry

Date frozen: 2026-08-18

Preflight note: [`GATE0_PREFLIGHT.md`](GATE0_PREFLIGHT.md).

## Question

Can a metric, geometry-induced coupling route carry a distinction that a deliberately insufficient frozen synaptic route cannot, while the two routes remain independently manipulable?

This gate does **not** test whether ephaptic coupling is a uniquely efficient computational primitive. A generic matched coupling route is an explicit attacker and is allowed to win.

## Toy world

- `N = 32` point units on a one-dimensional physical axis.
- Two source identities are used: one initially left and one initially right.
- Each sample activates exactly one source plus small independent activity noise.
- Label = which source identity was activated.
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

Condition D preserves the singular values of the metric coupling exactly while randomizing its left/right singular vectors. It prevents interpreting `C > A` as a special advantage of metric geometry.

## Frozen test-time interventions

Use the readout trained under C. No retraining.

```text
E  exchange only the physical positions of the two task-relevant source identities
   keep W and symbolic source identities fixed

F  clamp/remove the metric route
   keep W and the trained readout fixed
```

The rejected preflight controls — arbitrary full position shuffle and scalar gain shuffle — are documented separately and are not part of the registered verdict.

## Route-independence checks

Two orthogonal manipulations are measured directly:

```text
hold W fixed, change task-source geometry
hold geometry fixed, rewire W
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

A ridge-linear classifier is trained on the one-step nonlinear consequence `tanh(A x)` for each independently trained condition A-D. Interventions E/F reuse the C readout.

## Interpretation before registered results

### Structural keep

Keep the phrase **dual coupling geometry** if:

1. route-independence checks pass;
2. C recovers substantially more of the constructed source distinction than A;
3. exchanging the two physical source positions substantially breaks the C readout without changing W;
4. clamping the metric route substantially breaks the C readout.

Use `>0.20` accuracy difference only as a harness heuristic, not as a discovered scientific threshold.

### Generic attacker

If D matches or beats C, the honest result is:

> **A second metric route can carry information hidden from the deliberately blind frozen wired route, but this toy establishes no special computational advantage for the metric operator over a generic additional coupling matrix.**

That is an acceptable Gate 0 result.

### Kill

Kill the implementation if:

- A reliably solves the constructed null;
- changing geometry changes `W` or rewiring `W` changes `A_eph`;
- C fails to expose the distinction;
- E/F require readout retraining to look important;
- the matched-generic spectrum accounting is wrong.

## What Gate 0 does not contain

- no autonomous extracellular electric-field dynamics;
- no ionic field;
- no morphology/orientation model;
- no growth/pruning;
- no RL/reward objective;
- no learned geometry;
- no biological parameter fit.

Those are later gates only if this structural instrument is sound.
