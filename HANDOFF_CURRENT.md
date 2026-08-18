# SplatNeuronPlusField — current handoff

Date: 2026-08-18

## One-line state

> **The repo has moved from “two neural coupling geometries” to a resource question about how one physical cell participates in several coupling channels at once. Gate 1 showed a metric slow-state inductive bias; Gate 1b killed any unique-capability claim with a learned addressed transition. The newest correction is that a biological neuron should not have one abstract scalar output: its distributed membrane simultaneously changes private intracellular state and writes transmembrane-current consequences into extracellular space, while spikes/transmitters and slow chemical/ionic variables form additional channels with different address vocabularies.**

This is a synthetic computational instrument, not a tissue model.

## Physics guardrail

Keep extracellular electric and slow chemical/ionic variables distinct.

Quasi-static electric potential:

```text
phi(t) = G q(t)
```

No autonomous temporal memory in this approximation. The closed neuron-field loop can still have dynamics.

But `q` should eventually mean **distributed transmembrane current**, not merely `E f(v)` emitted after a point-neuron activation.

At a synapse, transmitter opens receptor conductances; the resulting transmembrane currents contribute to extracellular potential while also altering the receiving neuron's intracellular state. Incoming dendritic events therefore already write into extracellular space while they are being integrated.

Separate slow shared state:

```text
tau_c dc/dt = D_c Laplacian(c) - clearance(c) + release(activity)
```

`c` is normalized toy state. Do not call it potassium without physiological calibration.

Each unit can inhabit at least three non-equivalent neighborhoods:

```text
intracellular / dendritic geometry
synaptic / topological geometry
extracellular / metric geometry
```

and may additionally participate in chemical/neuromodulatory volume transmission whose receptor geometry differs again.

## Gate 0 — dual route

Files:

```text
docs/GATE0_PREREG.md
docs/GATE0_PREFLIGHT.md
docs/GATE0_RESULT.md
experiments/gate0_dual_geometry.py
```

Result: a metric route can expose a distinction deliberately collapsed by a frozen wired route, and geometry/rewiring can be manipulated independently. But a matched generic extra matrix solves the toy perfectly too.

```text
DUAL_ROUTE_INSTRUMENT       PASS
SPECIAL_METRIC_ADVANTAGE    NOT ESTABLISHED
```

Gate 0 is plumbing.

## Gate 1 — shared metric history

Files:

```text
docs/GATE1_PREFLIGHT.md
docs/GATE1_FROZEN_PROTOCOL.md
docs/GATE1_RESULT.md
experiments/gate1_shared_milieu.py
tests/test_gate1_shared_milieu.py
```

Task:

```text
cue at i
wait
probe at distinct j
label = same latent context?
```

Receiver sees only slow state at `j`.

Five frozen holdout seeds:

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

Supported narrow statement:

> **History can have an address vocabulary. A slow metric state makes past activity locally available when useful temporal context is aligned with that metric vocabulary; destroy the alignment and the advantage vanishes.**

No biological or unique-capability claim follows.

## Gate 1b — addressed attacker

Files:

```text
experiments/gate1b_addressed_attacker.py
docs/GATE1B_ADDRESSED_ATTACKER.md
tests/test_gate1b_addressed_attacker.py
```

The attacker ignores physical positions. It learns a symmetric rank-8 addressed relation from the same training cue/probe labels and uses

```text
T_addressed = U U^T
```

as the cue-to-local-receiver transition.

Five holdout seeds:

```text
seed      aligned      scrambled
18101      1.0000        1.0000
18102      1.0000        1.0000
18103      1.0000        1.0000
18104      1.0000        1.0000
18105      1.0000        1.0000

mean       1.0000        1.0000
```

Verdict:

```text
UNIQUE_METRIC_CAPABILITY       FAIL
ADDRESSED_LEARNED_ATTACKER     PASS
RESOURCE ADVANTAGE             UNDECIDED
```

Do not headline the current float payload. The rank-8 factor is 384 floats / 1536 B at float32, but it is likely highly compressible; the metric side must also honestly charge whatever geometry/schema is not physically free.

The live question is now:

> **How many persistent structure bits / physical constraints / learned edges must be installed so that a future receiver can cheaply access the relevant history?**

That is the bridge back to `SplatNeuron`'s observer-resource ledger.

## Membrane multiplex correction

New file:

```text
docs/MEMBRANE_MULTIPLEX_PREFLIGHT.md
```

Do not model a neuron as one scalar output copied into several media.

The membrane is a distributed boundary with simultaneous consequences:

```text
intracellular consequence
    local voltage / compartment state

synaptic consequence
    addressed transmitter release after suitable axonal events

quasi-static extracellular consequence
    transmembrane currents contribute immediately to phi

slow chemical / ionic consequence
    extrasynaptic transmitter, ionic accumulation, buffering, etc.
```

Important correction:

> **Neurotransmitter release is not how the neuron directly writes the extracellular electric field. Transmembrane currents write the electric field. Neurotransmitters can cause such currents at target membranes and can also participate in distinct chemical volume-transmission channels.**

Likewise, `dendrite = low-pass filter` is too weak. Passive cable properties are low-pass, but active conductances can amplify, compensate, resonate and change filtering.

Use instead:

> **Dendritic morphology plus local membrane state defines a state-dependent spatiotemporal transfer operator.**

A later compartmental model should therefore replace

```text
q = E f(v)
```

with something closer to

```text
q_i(x,t) = transmembrane_current_i(x,t)
phi = G[q]
```

and keep chemical/ionic channels separately stateful.

### New resource hypothesis

The possible interesting object is **shared physical implementation of multiple transfer kernels**.

For one source/receiver pair:

```text
H_syn[j<-i](omega)
H_eph[j<-i](omega)
H_chem[j<-i](omega)
```

are not arbitrary independent matrices in biology. They are jointly constrained by common positions, morphologies, membrane currents, release sites and receptor distributions.

Question:

> **Can one physical geometry implement a useful family of channel-specific transfer functions more cheaply than storing each channel as an unrelated generic operator?**

Mandatory attacker: generic multi-channel system with the same total state/output count, matched temporal spectra where meaningful, explicit connection-description cost, and no shared-geometry constraint.

This is the mathematical object to analyze before inventing another neuron architecture.

## Grounding / recursive projection

File:

```text
docs/GROUNDING_AND_RECURSION.md
```

The model-collapse connection is deliberately separate from Gate 1 and from the membrane multiplex result.

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

The candidate principle is:

> **A loop cannot restore a distinction its current path no longer carries unless new input contains information about that distinction that is not already a consequence of the current loop state.**

Importantly, independently informative synthetic input should be able to rescue a missing distinction too. If so, the variable is **innovation provenance**, not `reality versus imagination`.

The Gate-1 field itself gives a precise filtering analogy. In the metric-Laplacian eigenbasis:

```text
c_k(t) = exp[-(clearance + diffusion * lambda_k)t] c_k(0)
```

Large-`lambda` spatial modes decay faster. The same mechanism that cheaply spreads broad aligned context also erases rapidly varying metric distinctions.

Do not spend a gate merely demonstrating that theorem. A worthwhile experiment must make the external-innovation source matter in a nontrivial way.

## Personal neurological observations — scientific caution

Do not use the user's post-surgical jolts as evidence for a specific amygdala route, seizure mechanism, or rewiring mechanism. They are a motivating example of the general systems point that threat/body/sensory channels can converge on shared defensive circuitry, but the personal mechanism is medically unresolved.

## Next science

Three continuations are now visible. Do not mix them all into one gate.

### A. Resource frontier — still probably first

Attack Gate 1b's apparent cost:

```text
metric geometry / diffusion
vs
learned addressed low-rank factor
vs
compressed context assignment / interval code
vs
generic sparse graph / low-rank recurrent controls
```

At common held-out task error charge:

```text
persistent operator/structure description
state dimension
per-event communication
update compute
learning/search cost
```

Prediction: in the aligned world the metric/interval vocabulary may have a very short description; in the scrambled world the addressed learner should dominate flexibility. If a simple compressed context code beats both, keep that result.

### B. Multiplex transfer mathematics

Analyze the channel family

```text
H_ji(omega) = {H_syn, H_eph, H_chem}
```

when the components share latent physical parameters versus when they are stored independently.

The question is description/implementation coupling, not capability.

### C. Innovation provenance

Use known field eigenmodes and compare:

```text
closed decay
self-generated reinjection
fresh external samples
mixtures with p fresh samples
independently informative synthetic samples
fresh samples passed through the same lossy observer
```

Measure mode retention, held-out recovery, tail/rare-factor recovery and diversity.

The strong question is not whether `real data` is magic. It is whether information missing from the current internal representation must enter through an independently informative route.

## Morphology later

Only after point-unit state/coupling/resource questions survive.

Then replace scalar emit/read gains with distributed membrane shapes/current sources and ask whether morphology is a short physical implementation of useful receiver-specific transfer kernels relative to generic point machinery.

## Oja note

Do **not** pivot this repo into `Oja rule in geometric coordinates` now. Oja/PCA remains a useful historical baseline and possible later local-learning mechanism. The live object here is coupling/state/resource geometry.

## Medical note

Pregabalin is an antiepileptic prescription drug and official EMA information recommends gradual discontinuation rather than abrupt stopping. Any new or changed post-surgical jolt-like episodes after medication changes belong with the treating neurologist rather than being used as mechanistic evidence for this repo.

## Stop lines

- no second electromagnetic brain;
- no field memory claim for quasi-static `phi`;
- no unique metric capability claim after Gate 1b;
- no potassium claim from normalized `c`;
- no claim that transmitter itself is the electric field;
- no claim that all neurons use the same mix of synaptic/electric/volume channels;
- no claim that dendrites are merely passive low-pass filters;
- no reward/evolution story before the coupling/resource result earns it;
- no model-collapse-is-thought claim;
- no `real = high frequency` claim;
- no `synthetic = intrinsically inferior` claim;
- no morphology efficiency story until matched generic multi-channel attackers are settled.

## Branch / PR

Active branch:

```text
agent/shared-milieu-grounding
```

Draft PR:

```text
#1 Gate 1: shared metric history, addressed attacker, and grounding hypothesis
```

CI now passes on Python 3.10 and 3.13 after package-discovery and `python -m pytest` fixes. Treat CI only as mechanical verification, never as scientific evidence.
