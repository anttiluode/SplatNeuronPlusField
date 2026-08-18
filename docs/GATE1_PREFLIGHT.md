# Gate 1 preflight — shared slow milieu

Date: 2026-08-18

## Why this exists

Gate 0 only established that a wired/topological route and a metric route can be manipulated independently. It did **not** establish a special computational advantage for the metric route.

Gate 1 changes the resource. The question is now whether a **slow shared metric state** can make past activity available to a later, physically nearby but unwired receiver in a way that matched independent private adaptation cannot.

This is a synthetic instrument. It is not a potassium model, not a tissue model, and not evidence for a biological mechanism.

## Exploratory work that does not count as the result

Scratch experiments used seeds `18011..18013` while the task and controls were being designed.

Three corrections came out of that exploration:

1. **Positive trials must use a different cue and probe unit.** Otherwise private adaptation gets a trivial advantage whenever the same unit appears twice.
2. **`no field` is not a sufficient attacker.** A generic shared linear state can also move history between units.
3. **Temporal spectrum must be matched.** If the metric field has a family of slow modes, a control with one arbitrary private decay is too weak.

Those exploratory runs were used to choose a stable toy regime and are not reported as confirmatory evidence.

## Frozen toy regime

```text
units             48
latent contexts    8
train trials    6000
test trials     6000
metric length   0.07
shared diffusion 0.70
clearance        0.25
delay             1.50
```

The slow metric state follows a linear symmetric rate operator

```text
K_metric = clearance * I + diffusion * L_metric
c(delay) = exp(-K_metric * delay) c(0)
```

where `L_metric` is induced only by physical positions.

The exact matrix exponential is evaluated by eigendecomposition; there is no Euler-step stability confound.

## Task

A cue occurs at unit `i`. After a delay, a distinct probe unit `j` is queried.

Target:

```text
1  cue and probe belong to the same latent context
0  cue and probe belong to different latent contexts
```

The probe-side receiver sees only the slow state at coordinate `j` just before the probe.

This is deliberately a **receiver-local** task. A global downstream reader of all private states could simply recover cue identity and would answer a different question.

## Structure regimes

### Aligned

Each latent context occupies a contiguous block of physical units.

### Scrambled

The same context membership structure is randomly permuted across physical positions.

This is mandatory. If the metric state helps only in the aligned regime, the supported interpretation is conditional inductive bias: the state vocabulary matches the world's structure.

## Strong attackers added during preflight

### Private matched state count

`N` independent private variables, same release/clearance, no cross-unit mixing.

### Private matched decay spectrum

Still exactly `N` independent private variables, but their diagonal decay rates are a permutation of the complete eigenvalue spectrum of the metric field.

This preserves the multiset of temporal time constants while removing shared spatial eigenvectors.

### Random shared matched spectrum

Construct a random orthogonal basis `Q` and use

```text
P_random = Q diag(exp(-lambda_metric * delay)) Q^T
```

This preserves:

- state dimension;
- every decay eigenvalue;
- symmetry;
- spectral norm/Frobenius-scale consequences of the spectrum;

while destroying the metric eigenvector alignment.

If this attacker solves the task equally well, Gate 1 has not established a metric-structure effect.

## Development-history disclosure

The protocol was frozen in the assistant scratch environment before running holdout seeds `18101..18105`, but the GitHub files were written after that in the same interactive session. Therefore this should be described as a **frozen holdout protocol**, not as a publicly timestamped preregistration.
