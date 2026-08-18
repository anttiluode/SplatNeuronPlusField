# Gate 1 frozen holdout protocol

Date: 2026-08-18

See `GATE1_PREFLIGHT.md` for exploratory corrections and the disclosure that this is an in-session frozen holdout protocol rather than a publicly timestamped preregistration.

## Conditions

```text
A  no slow state
B  independent private state, same local clearance
C  shared metric diffusive state
D  shared-state implementation with diffusion removed
E  C with physical positions shuffled at test time only; reuse C readout
F  independent private state with matched metric decay spectrum
G  generic shared state with matched metric decay spectrum and random eigenvectors
```

`B` and `D` are expected to be mathematically identical in this minimal linear instrument. Keeping both names makes the decomposition explicit and gives a regression check.

## Holdout seeds

```text
18101
18102
18103
18104
18105
```

Run both:

```text
aligned
scrambled
```

with the same fixed protocol values in `experiments/gate1_shared_milieu.py`.

## Frozen success criteria

Using five-seed mean test accuracy:

```text
aligned C >= 0.75
aligned C >= aligned B + 0.20
aligned C >= aligned F + 0.20
aligned C >= aligned G + 0.20
scrambled C <= 0.60
aligned E <= 0.60
```

Also require:

```text
B and D transition matrices identical
G matches C's decay spectrum numerically
E preserves C's decay spectrum while changing which unit identity occupies which physical location
all positive trials use cue != probe
```

## Interpretation ladder

### If C does not beat B/F

The slow field has not earned itself. Independent private adaptation is sufficient in this instrument.

### If C beats private controls but G matches C

Shared history matters, but metric geometry has not earned itself.

### If C beats B/F/G only in aligned world and dies under scrambling/geometry intervention

Supported statement:

> A slow shared state can make past activity locally available across unwired units when the task-relevant statistical structure aligns with the state's metric coupling geometry. The benefit is a conditional inductive bias, not a universal computational advantage.

### Explicit non-claims even on a pass

- no claim about extracellular potassium magnitude or physiology;
- no claim that real brain tasks use this mechanism;
- no claim that metric coupling computes functions unavailable to an addressed recurrent network;
- no claim that diffusion is superior to learned generic recurrent memory;
- no reward, consciousness, identity or memory-storage claim;
- no model-collapse claim from this gate.
