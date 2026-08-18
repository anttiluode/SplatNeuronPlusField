# Gate 1b — addressed low-rank attacker

Date: 2026-08-18

Experiment: `experiments/gate1b_addressed_attacker.py`

## Why this attacker exists

Gate 1 showed that a fixed slow metric state solves the aligned temporal-context toy while matched private state and a random shared same-spectrum state do not.

That does **not** establish unique computational capability. An addressed system should be allowed to learn the task relation directly.

Gate 1b therefore removes physical geometry entirely and learns a symmetric low-rank addressed transition from the same cue/probe training labels.

```text
training pair relation
        ↓
rank-K factor U
        ↓
T_addressed = U U^T
        ↓
cue at i -> local receiver j sees T[j,i]
```

`K=8`, matching the latent-context count. Threshold selection uses training data only.

## Five-seed holdout result

Seeds are the same Gate-1 holdouts: `18101..18105`.

```text
seed      aligned      scrambled
18101      1.0000        1.0000
18102      1.0000        1.0000
18103      1.0000        1.0000
18104      1.0000        1.0000
18105      1.0000        1.0000

mean       1.0000        1.0000
```

The attacker uses no physical positions and no test labels for fitting or threshold selection.

## Verdict

```text
UNIQUE_METRIC_CAPABILITY          FAIL
ADDRESSED_LEARNED_ATTACKER        PASS
RESOURCE_ADVANTAGE                UNDECIDED
```

Gate 1 should therefore be read as an **inductive-bias** result:

> **The metric slow state has the useful neighborhood built into its physical vocabulary. A learned addressed system can acquire the same task relation and also handles the scrambled world.**

The remaining scientific question is not capability.

It is installation/resource cost:

> **What must each system pay to acquire or physically instantiate the neighborhood that makes the relevant history available?**

## First accounting, deliberately not a frontier claim

The current generic factor is `48 × 8` floating-point values:

```text
384 float parameters
1536 bytes at float32
```

A free dense `48 × 48` matrix would be 9216 bytes at float32.

These numbers are **not** a fair final comparison against the metric system. The learned factor may be highly compressible, and the metric implementation must also honestly account for whatever geometry/schema is not physically given for free.

In the ideal task, a context assignment itself could be represented much more compactly than the generic float factor. Therefore do not headline `1536 B versus a few field scalars`.

The next resource experiment must quantize/compress both sides under a common task-error target, reusing the observer-resource discipline from `SplatNeuron`.

## What survives

Gate 1 + Gate 1b jointly support a cleaner statement than either alone:

> **A shared state can encode history in a metric address vocabulary. That vocabulary is useful when the world's regularities align with it, but an addressed learner can install another vocabulary when they do not.**

That is the bridge back to `SplatNeuron`: persistent structure can buy cheaper future access to selected distinctions, but the structure itself has to be charged.
