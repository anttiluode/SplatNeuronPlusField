# Gate 1 result — shared slow milieu

Date: 2026-08-18

Protocol: `docs/GATE1_FROZEN_PROTOCOL.md`  
Experiment: `experiments/gate1_shared_milieu.py`

## Result

Five frozen holdout seeds were run in both the aligned and scrambled structure regimes.

### Aligned world

```text
seed     A none    B private    C metric    D no-diff    F private-spectrum    G random-spectrum    E geom-shuffle
18101    .5040      .5040       .9158       .5040          .5040                 .5373               .5002
18102    .5050      .5050       .9088       .5050          .5050                 .5312               .5057
18103    .4922      .4922       .9162       .4922          .4922                 .4815               .4773
18104    .5098      .5098       .9118       .5098          .5098                 .5102               .4877
18105    .5028      .5028       .9088       .5028          .5028                 .5330               .4480

mean     .5028      .5028       .9123       .5028          .5028                 .5186               .4838
```

### Scrambled world

```text
seed     A none    B private    C metric    D no-diff    F private-spectrum    G random-spectrum    E geom-shuffle
18101    .5050      .5050       .4848       .5050          .5050                 .5050               .4717
18102    .5042      .5042       .5195       .5042          .5042                 .5083               .5133
18103    .4930      .4930       .5223       .4930          .4930                 .5067               .4603
18104    .5097      .5097       .5135       .5097          .5097                 .5137               .5062
18105    .5018      .5018       .5008       .5018          .5018                 .5128               .4788

mean     .5027      .5027       .5082       .5027          .5027                 .5093               .4861
```

## Frozen checks

```text
aligned C >= .75                         PASS
aligned C >= B + .20                    PASS
aligned C >= F + .20                    PASS
aligned C >= G + .20                    PASS
scrambled C <= .60                      PASS
aligned geometry-shuffle E <= .60       PASS
```

Mechanical checks also pass in the instrument:

```text
positive cue != probe
B and D transitions identical
G shares C's decay spectrum to numerical precision
geometry shuffle preserves the metric decay spectrum while reassigning unit identities to positions
```

## What happened

The private-state controls fail for a simple structural reason that was deliberately enforced: the cue and probe are different units. Independent local memory can preserve the cue at the cue unit, but cannot make that history available to the later probe receiver without a coupling route.

The shared metric state does make the cue's residue available to nearby receivers. That only helps when the latent context statistics are aligned with physical locality.

The stronger `G` attacker is important. It has:

```text
same number of state variables
same complete decay spectrum
same symmetric linear-state form
shared cross-unit history
```

but random eigenvectors instead of metric eigenvectors. It remains near chance. Therefore the Gate-1 effect is not explained by `more slow state`, `more temporal modes`, or `any shared linear memory` alone.

The test-time geometry intervention then changes only which unit identities occupy which physical coordinates. The learned local receiver collapses.

## Supported statement

> **In this constructed task, a slow shared state makes past activity available across unwired units when task-relevant temporal context is aligned with the state's metric coupling geometry. Matching private state count and decay constants is insufficient, and a generic shared state with the same decay spectrum is insufficient. Destroying the alignment removes the advantage.**

Shorter:

> **History can have an address vocabulary. Here the metric field helps only when the world's useful history is metric.**

## What this does not establish

It does **not** establish:

- that extracellular potassium or another biological slow variable performs this task;
- that metric extracellular state is computationally superior to a trainable addressed recurrent network;
- that diffusion is a generally efficient memory mechanism;
- that brains use this mechanism for episodic memory, identity or cognition;
- that the metric system has unique computational capability;
- that the effect survives realistic release, buffering, concentration scales, morphology or noise.

The result is a conditional inductive-bias receipt in a controlled synthetic world.

## Strong next attacker

A trainable addressed recurrent memory with the same state dimension and an explicit connection-description cost should be allowed to learn the same context structure.

If it matches or beats the metric field cheaply, then the metric route's remaining advantage is not task performance but **having the relevant neighborhood built into physical geometry without storing those pairwise edges explicitly**.

That would reconnect this repo to `SplatNeuron`'s observer-description/resource accounting without conflating the two projects.
