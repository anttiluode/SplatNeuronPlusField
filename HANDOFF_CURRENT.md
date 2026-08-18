# SplatNeuronPlusField — current handoff

Date: 2026-08-18

## One-line state

> **Gate 0 established two independently manipulable coupling routes. Gate 1 now establishes a narrower conditional result: a slow shared metric state can make past activity available to a later unwired receiver when task-relevant temporal structure aligns with physical geometry; matched private history and a generic shared state with the same decay spectrum do not solve the aligned toy, and the effect disappears when geometry/task alignment is destroyed.**

This is still a synthetic computational instrument, not a claim about extracellular physiology.

## Provenance

This repo branches conceptually from `anttiluode/SplatNeuron` after its observer-resource work through Gate 13c was merged to `main`.

`SplatNeuron` asks what an observer must pay to expose a distinction. The surviving result there is conditional: if task structure aligns with a compact observation vocabulary, one-time observer/configuration bits can reduce the repeated logical interface; dense rotation/high task complexity remove the advantage.

`SplatNeuronPlusField` asks a different question:

> **What changes when stateful units inhabit both addressed/topological and metric/shared neighborhoods, and when the metric neighborhood can itself carry slow shared state?**

Do not transfer `SplatNeuron` claims here without new tests.

# Physics guardrail

Treat ordinary low-frequency extracellular electric potential, at first approximation, as quasi-static:

```text
phi(t) = G q(t)
```

where `q(t)` is the current-source pattern and `G` is a volume-conductor/geometry operator.

`phi(t)` has no autonomous temporal memory in this approximation.

The closed loop can have dynamics:

```text
neural state_t
   -> source currents q_t
   -> phi_t = G q_t
   -> ephaptic perturbation
   -> neural state_{t+1}
```

A distinct slow extracellular/homeostatic state can have genuine relaxation/diffusion dynamics:

```text
tau_c dc/dt = D_c Laplacian(c) - clearance(c) + release(activity)
```

Possible biological analogues include ionic/homeostatic variables such as extracellular K+, buffering and pH, but the current `c` is normalized toy state. Do not call it potassium without physiological release, diffusion, buffering, concentration and timescale calibration.

## Three neighborhoods

```text
intracellular / dendritic geometry
    where inside this cell did a signal arrive?

synaptic / topological geometry
    who is wired to whom?

extracellular / metric geometry
    who is physically near/aligned in the shared medium?
```

The central architectural fact is that these neighborhoods need not agree.

Minimal point-unit equations:

```text
s = W f(v)
q = E f(v)
phi = G q
e = R phi

tau_c dc/dt = D_c Laplacian(c) - clearance(c) + B f(v)

tau_v dv/dt = F(v, h, s + lambda_e e, c)
dh/dt = H(h, v, input)
```

Effective instantaneous metric coupling:

```text
A_eph = R G E
```

`A_eph` is induced by emitter geometry, medium geometry and receiver geometry rather than stored as a free pairwise weight matrix.

# Gate 0 — dual route — completed

Files:

```text
docs/GATE0_PREREG.md
docs/GATE0_PREFLIGHT.md
docs/GATE0_RESULT.md
experiments/gate0_dual_geometry.py
```

Three-seed registered result:

```text
seed    synaptic A   metric B   combined C   matched generic D   source-swap E   clamp F
18001     .5008        1.0000      1.0000          1.0000            .0150        .5122
18002     .5018        1.0000      1.0000          1.0000            .0000        .4940
18003     .4935        1.0000      1.0000          1.0000            .0000        .5060
```

Route algebra behaved as required:

```text
move metric source positions  -> A_eph changes, W unchanged
rewire W                      -> W changes, A_eph unchanged
```

Verdict:

```text
DUAL_ROUTE_INSTRUMENT        PASS
SPECIAL_METRIC_ADVANTAGE     NOT ESTABLISHED
MATCHED_GENERIC ATTACKER     PERFECT TOO
```

Supported statement:

> **A metric route can carry a distinction deliberately absent from a frozen wired route, and the two routes can be manipulated independently. This toy does not show a special metric/ephaptic computational advantage over generic additional coupling.**

Gate 0 is plumbing.

# Gate 1 — slow shared metric history — completed

Files:

```text
docs/GATE1_PREFLIGHT.md
docs/GATE1_FROZEN_PROTOCOL.md
docs/GATE1_RESULT.md
experiments/gate1_shared_milieu.py
tests/test_gate1_shared_milieu.py
```

## Question

> **Does a slow shared metric state make past activity available to a later unwired receiver in a way that matched independent private history does not?**

## Task

Two-event temporal-context task:

```text
cue at unit i
wait
probe at distinct unit j

label = whether i and j belong to same latent context
```

The receiver is local: it reads only the slow state at `j` immediately before the probe. Positive trials force `i != j`, so exact self-memory cannot solve the task.

Two worlds:

```text
aligned    latent context occupies contiguous physical neighborhood
scrambled  same latent grouping permuted across physical positions
```

## Strong controls

```text
A  no slow state
B  independent private state, same local clearance
C  shared metric diffusion
D  C with diffusion removed
E  C with physical positions shuffled at test time only
F  independent private state with same complete decay-rate multiset as C
G  generic shared symmetric state with exactly C's decay spectrum but random eigenvectors
```

`G` is the important generic-shared attacker. It prevents interpretation as merely `more slow state` or `more temporal modes`.

## Frozen holdout result

Five seeds `18101..18105`:

```text
mean accuracy                  aligned      scrambled
A no slow state                .5028         .5027
B private same clearance       .5028         .5027
C shared metric diffusion      .9123         .5082
D shared no diffusion          .5028         .5027
F private matched spectrum     .5028         .5027
G random shared spectrum       .5186         .5093

E geometry-shuffle test-only   .4838         .4861
```

Frozen criteria all passed.

## Gate 1 verdict

Supported statement:

> **In this constructed task, a slow shared state makes past activity available across unwired units when task-relevant temporal context is aligned with the state's metric coupling geometry. Matching private state count and decay constants is insufficient, and a generic shared state with the same decay spectrum is insufficient. Destroying the alignment removes the advantage.**

Short form:

> **History can have an address vocabulary. Here metric history helps only when the world's useful history is metric.**

This is a conditional inductive-bias result, not a unique-capability result and not neuroscience evidence.

## Important next attacker

A trainable addressed recurrent memory with the same state dimension and explicit connection-description cost should be allowed to learn the same context structure.

If it matches C, that is not a failure. The remaining question becomes:

> **What does physical geometry buy in connection-description, wiring, learning or communication cost relative to learning/storing the equivalent addressed graph?**

That would reconnect naturally to `SplatNeuron`'s resource ledger.

# Grounding / recursive-projection bridge

New note:

```text
docs/GROUNDING_AND_RECURSION.md
```

The model-collapse literature suggested a useful connection, but the initial phrasing must be corrected.

Do **not** say:

```text
real world = high-frequency channel
ephaptic field = reality channel
internal thought = model collapse
```

The ephaptic field is generated by the brain. The external world has structure at many scales.

The cleaner distinction is:

```text
external innovation
    information entering from a source not generated by the current internal model

recursive projection
    repeated observation/training/reaction to consequences generated by the current model
```

Shumailov et al. show that recursive generative training can lose distribution tails. Vu/Reeves/Wenger show a more nuanced multi-model case: synthetic interaction can transmit novel concepts while also homogenizing shared performance.

So the candidate principle is not `synthetic bad / real good`.

It is:

> **A loop cannot recover a distinction that its current observation/generation path no longer carries unless new input enters that contains information about the missing distinction.**

That is closely related to Kynnys's `WAIT versus ROUTE` lesson and TWC's identifiability lesson.

## Why this specifically touches Gate 1

The Gate-1 field is diffusive. In the metric-Laplacian eigenbasis:

```text
c_k(t) = exp[-(clearance + diffusion * lambda_k)t] c_k(0)
```

Therefore large-`lambda` spatial modes decay faster.

The toy field is literally a selective forgetting/smoothing operator in its own spatial vocabulary.

Gate 1 measured the beneficial side: broad aligned context is cheap to share.

A later experiment should measure the destructive side: distinctions carried by rapidly varying metric modes should disappear unless they are continually re-injected.

# Candidate next gate — innovation provenance

Do not build another neuron first.

Use the same linear field and construct a latent world whose task information is placed in known metric eigenmodes.

Compare:

```text
A  closed decay / no new input
B  self-generated reinjection from current reduced state
C  fresh samples from original world process
D  self-replay + fraction p fresh samples
E  independently generated samples containing modes missing from current model
F  fresh samples passed through the same lossy observer as the internal model
```

Measure:

```text
variance retained by mode
held-out task recovery
rare-mode / tail recovery
cross-validated latent-factor decoding
representation diversity
```

Strong prediction:

> **Independently informative synthetic input should rescue a missing distinction too. If it does, the relevant variable is not metaphysical `reality`; it is innovation provenance relative to the current model.**

This is a candidate Gate 2/3 only after the addressed-memory attacker is decided or explicitly separated as a parallel branch.

# Morphology later

Only after point-unit coupling/state behavior is understood.

Replace scalar emit/read gains with spatial emitter/receiver shapes:

```text
A_eph[j,i] = R_j G E_i
```

Then compare morphology against generic point-network emulators at fixed receiver error and explicit resource accounting.

The live claim is not that morphology computes an impossible function. The possible resource claim is that morphology supplies a short physical implementation/description of useful transfer kernels that generic point machinery reproduces with more nodes, weights, depth, communication or synchronization.

# Temporal / memory bridge

Keep variables separate:

```text
quasi-static phi_t       instantaneous shared metric coupling
slow extracellular c_t  shared metric history
neuron/synapse h_t       private/addressed history and plasticity
recurrent loops          system-level persistence
sensory input y_t        fresh external evidence / innovation
```

A memory does not have to be stored in `phi`.

Useful formulation:

> **The individual `phi_t` has no memory; the closed loop does.**

And after Gate 1:

> **Which history becomes available next depends partly on the address vocabulary of the state that carried it.**

# Context / identity bridge — keep out of early gates

Scientifically usable abstraction:

```text
current context
   -> reinstates a distributed old state/trajectory
   -> reinstated state changes what is likely next
   -> repeated re-entry changes accessibility/plasticity over longer times
```

Do not turn this into a literal ephaptic-memory claim.

Identity/self-state can later be studied as invariance over a drifting distribution of accessible trajectories, but that is not a Gate-1 result.

# Evolution / value — still parked

Do not add `seek reward / flee pain` as a generic RL objective yet.

If value enters later, a more architecture-specific route is a diffuse modulatory channel changing gain/plasticity/threshold over metric neighborhoods, attacked against explicit global gain/reward controls.

# Oja note

Do not pivot this repo into `Oja rule in geometric parameter space` now.

Oja/PCA remains historically and technically relevant as a simple observer-learning baseline. The live result here is about coupling/state geometry. Add Oja-style local learning only when a future gate explicitly asks how an observer or coupling structure is learned.

# Stop lines

- no `second electromagnetic brain` claim;
- no field-memory claim for quasi-static electric potential;
- no autonomous wave equation for ordinary ephaptic electric potential in this regime;
- no `field enslaves neurons` claim from observational directionality;
- no special metric-compute claim from Gate 0;
- no biological slow-field claim from Gate 1;
- no unique-capability claim from Gate 1;
- no reward story before coupling/state earns itself;
- no growth/pruning story before fixed-capacity controls;
- no claim that spatial structure supplies semantics;
- no claim that external reality is simply `high frequency`;
- no claim that synthetic/internal data is intrinsically bad;
- no claim that model collapse is a model of thought or memory;
- no claim that the old `SmoothField` was secretly potassium.

# Current branch state

Active development branch:

```text
agent/shared-milieu-grounding
```

New/updated material on that branch:

```text
experiments/gate1_shared_milieu.py
docs/GATE1_PREFLIGHT.md
docs/GATE1_FROZEN_PROTOCOL.md
docs/GATE1_RESULT.md
docs/GROUNDING_AND_RECURSION.md
tests/test_gate1_shared_milieu.py
HANDOFF_CURRENT.md
```

Next builder should choose between two clean continuations rather than mixing them:

1. **Attacker path:** train an addressed recurrent memory at matched state/resource budget against Gate 1.
2. **Grounding path:** build the innovation-provenance spectral instrument without adding biological detail.
