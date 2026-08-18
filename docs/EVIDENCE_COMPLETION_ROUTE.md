# Evidence, completion, and ROUTE

Date: 2026-08-18

Status: conceptual bridge + proposed measurements. **Not a result.**

This note records a connection that became visible only after looking back through `SplatWorld`, `SplatField`, `Kynnys`, `SplatNeuron`, and the current PlusField work from the same receiver-centered perspective.

The useful new object is not `hallucination`, `prediction`, or `field` by itself. It is a receiver that separates:

```text
what actually arrived
from
what the receiver reconstructed using its own learned state.
```

That distinction should become explicit in the formalism and in the resource / information ledger.

---

## 1. Receiver correction: observation is not reconstruction

The old shorthand was

```text
r_j = R_j X
```

where receiver `j` gets only a small observation subspace of a richer surrounding state `X`.

For an intelligent / generative receiver this is incomplete. Use

```text
r_j      = R_j X
Xhat_j   = G_j(r_j, h_j)
u_j      = F_j(Xhat_j, h_j)
```

where

```text
R_j      observation operator / channel
h_j      receiver's accumulated state, history, learned prior
G_j      completion / inference operator
Xhat_j   receiver-side reconstruction
F_j      downstream consequence generator
```

Two receivers can therefore receive the same `r` and construct different `Xhat`:

```text
G_A(r, h_A) != G_B(r, h_B).
```

This is not an information-theory violation. The transmitted observation does not contain every detail of `Xhat`; most of the reconstructed state can be supplied by the receiver's prior machinery.

A useful warning sentence is:

> **Large receiver-side state change does not imply large transmitted information.**

Small evidence can index a large pre-existing region of a learned model.

---

## 2. The nullspace is where the receiver gets to invent

Let a hidden state `x` be observed through

```text
y = M x.
```

If

```text
M x_a = M x_b,
```

then the observation cannot distinguish `x_a` from `x_b`.

A generative receiver may still return a complete estimate

```text
xhat = G(y, h).
```

But the components of `xhat` lying in directions not constrained by `M` are supplied by the receiver's learned structure, not by new observation.

In a simple regularized inverse view:

```text
xhat = argmin_x  ||M x - y||^2 + lambda * Phi_h(x)
```

`Phi_h` is the learned prior / geometry.

This suggests a deliberately schematic sentence:

> **Structured completion is what a learned prior does where the current observation leaves degrees of freedom unresolved.**

Do not promote this sentence into a universal theorem about all generative models. It is a useful local instrument for designing the next tests.

---

## 3. WAIT versus ROUTE becomes an epistemic distinction

Kynnys already supplied the right control language.

### WAIT

Acquire more processing or more time through the **same observation map**.

```text
y = M x
WAIT -> process y again
```

If `M` aliases two hidden states, WAIT cannot create the missing distinction.

### ROUTE

Acquire a genuinely different observation:

```text
y_1 = M_1 x
y_2 = M_2 x
```

Now the joint observation

```text
[M_1; M_2] x
```

may distinguish states that either channel alone collapses.

The important failure mode is therefore:

```text
partial evidence
    -> completion
    -> completion feels / scores as complete
    -> no ROUTE is requested
    -> reconstructed detail is treated as if observed
```

That is a closed-loop certainty problem, not proof that the completion itself is bad. Completion is necessary and useful; the error is forgetting which components were externally constrained.

---

## 4. SplatField's alpha is a real instrument here

SplatField already carries a continuous evidence-versus-internal-state dial:

```text
r(t) = (1-alpha) * internal_render(t)
     + alpha     * external_camera(t)
```

with the important interpretation guardrail:

```text
alpha is an evidence-weight / drive dial,
not a literal Bayesian posterior weight,
not a truth fraction,
not a consciousness dial.
```

Still, it gives something experimentally useful:

```text
alpha high          external observation dominates
alpha intermediate  external observation + internal continuation
alpha low           internal dynamics dominate
```

This is unusual because the evidence fraction is continuously adjustable while the same learned basis and dynamical machinery remain in place.

Do not use the old claim that projection onto the learned decoder subspace "costs essentially no gain." Later SplatField work showed that reach above chance can coexist with a substantial dynamical cost. Alignment and free gain are different measurements.

---

## 5. The SplatWorld identity-drift reading is a hypothesis, not a result

The attractive interpretation is:

```text
source identity evidence becomes weak
while
face-manifold plausibility remains strong
```

which would produce a face that remains plausible while ceasing to preserve the original person.

But ordinary off-support extrapolation can also make both identity and face-likeness degrade together.

Therefore do **not** write:

> the model prefers changing identity to ceasing to make a face.

until the following measurement is run.

### IDENTITY_VS_PLAUSIBILITY gate

Sweep the same latent departure variable / view-control variable already used to expose identity drift. At every point measure separately:

```text
I(r) = identity similarity to the source
P(r) = face plausibility / face-manifold score
```

The strong prediction is:

```text
there exists a region where I(r) falls strongly
while P(r) remains comparatively high.
```

Controls:

```text
- ordinary pixel / latent interpolation baseline
- random latent direction
- in-support versus out-of-support regions
- multiple source identities
- frozen metrics chosen before sweep inspection
```

If `I` and `P` fall together, the receiver-completion interpretation has not earned this particular SplatWorld claim.

---

## 6. Data-to-geometry is measurable only through alignment, not prose

A useful reading of trained generative models is:

```text
examples during training
    -> parameters
    -> local reachable / likely directions
    -> cheap versus expensive continuations later
```

But the statement `data becomes geometry` is too broad to count as a result.

The measurable version is an alignment statistic.

For a learned reachable tangent `S` and a target / dynamical covariance `C`, use the same family of statistics already derived in `MULTIPLEX_MATH.md`:

```text
capture_structured = tr(P_S C) / tr(C)
capture_random     = expected capture of a matched random subspace
A                   = capture_structured - capture_random
```

This is the sharp question:

> **Did training orient the reachable manifold toward useful / persistent directions better than construction alone or a matched random manifold would?**

SplatField already contains positive and negative alignment-style measurements worth re-auditing under this single statistic. Do not copy old qualitative summaries across files without checking later retractions and matched controls.

---

## 7. New ledger: received, reconstructed, routed

For receiver experiments report three currencies separately.

### A. Received evidence

What distinctions are actually present in the current observation?

Possible measures:

```text
conditional mutual information about the hidden factor
rank / singular spectrum of the observation map
held-out decodability from raw observation alone
```

### B. Receiver-supplied reconstruction

How much structure appears only after the receiver's prior / generative machinery acts?

Do not call this "extra transmitted information."

Measure instead:

```text
change in reconstructed state
accuracy / calibration of hidden-variable inference
prior sensitivity under matched evidence
```

### C. ROUTE novelty

How much genuinely new distinction enters through a new channel?

For a hidden target `Z`, a clean information form is

```text
I(Z ; Y_route | Y_old).
```

If this is approximately zero, the new route is redundant for that target.

If positive, the route carries distinction not already available through the old observation.

This is the information-theoretic counterpart of Kynnys/TWC's novelty idea.

---

## 8. Four experiments now suggested

### E1 — alpha calibration curve

Run one identity / percept under a continuous `alpha` sweep.

Measure simultaneously:

```text
external fit
identity retention
face / percept plausibility
field-mode occupancy
internal prediction error
```

Question:

> At what evidence level does the system remain plausible while ceasing to remain specifically answerable to the source?

The important output is a curve, not a demo frame.

### E2 — WAIT versus ROUTE completion

Create an observation where two hidden states are intentionally aliased under `M_1`.

Compare:

```text
WAIT: repeated inference / recurrence with M_1 only
ROUTE: add M_2 that distinguishes the states
```

Measure:

```text
confidence
accuracy
identity / hidden-state recovery
calibration
```

Frozen prediction:

```text
WAIT can sharpen the receiver's preferred completion
but cannot systematically recover a distinction absent from M_1.
ROUTE can, if M_2 carries conditional information about that distinction.
```

### E3 — recursive completion versus independent innovation

After generating `Xhat`, feed a consequence of `Xhat` back as the next observation and compare against a genuinely independent observation of the hidden state.

Arms:

```text
self-generated reinjection
independent fresh observation
independent synthetic source carrying the hidden factor
fresh observation passed through the same lossy map
```

Measure whether confidence can rise under self-reinjection while ground-truth recovery does not.

This connects directly to `GROUNDING_AND_RECURSION.md` without claiming that synthetic data is intrinsically inferior.

### E4 — same evidence, different histories

Train / initialize two receivers with different priors while holding the test observation exactly fixed.

```text
same y
receiver A history h_A
receiver B history h_B
```

Measure divergence of `Xhat_A` and `Xhat_B` and which receiver is better calibrated to the true hidden state.

This is the model-side version of the human intuition that history can dominate an ambiguous cue. It is an AI experiment, not a psychological claim about any particular person.

---

## 9. Relation to SplatNeuronPlusField

This does not replace the current membrane / multiplex work.

It adds a missing receiver-side half.

The emerging abstraction is:

```text
rich surrounding state X
        -> channel-specific observation R_j X
        -> receiver completion G_j(R_j X, h_j)
        -> private state transition
        -> multiplex consequences
             synaptic
             ephaptic
             chemical / slow milieu
        -> other receivers
```

The neuron / unit therefore need not transmit a rich internal representation. A small consequence can trigger a large downstream reconstruction when the receiver already owns the relevant latent machinery.

But the repo must always distinguish:

```text
information carried by the consequence
from
structure supplied by the receiver.
```

That is the guardrail that prevents "gesture contains paragraphs," "spike contains thought," or "small signal transmits a whole latent" from becoming misleading information claims.

---

## 10. Human interpretation guardrail

The motivating social example is useful because it exposes the computational asymmetry:

```text
small ambiguous cue
+
large personal prior
->
very detailed hypothesis
```

But a detailed hypothesis is not evidence that the inferred hidden state is correct.

The broader human lesson may be important — prior history can shape interpretation of ambiguous events — but this repo should not diagnose individual psychology or promote social examples as empirical support for the computational claim.

Use the human examples to generate controls, then test the controls in models.

---

## 11. Stop lines

- no claim that completion creates information absent from both observation and prior;
- no claim that receiver state change equals transmitted bits;
- no claim that repeated WAIT recovers distinctions annihilated by the observation map;
- no claim that SplatWorld preserves face plausibility after identity loss until measured separately;
- no reuse of retracted / mismatched SplatField gain comparisons;
- no claim that `alpha` is a literal Bayesian belief weight;
- no `hallucination = low alpha` slogan as a result;
- no human social inference presented as ground truth;
- no grand-unification headline from `partial observation + completion` alone.

---

## 12. Current narrow headline

> **A receiver should be modeled as both an observation operator and a completion operator. The observation determines which distinctions actually arrive; the receiver's learned history fills unresolved directions. Reprocessing the same aliased observation can strengthen a completion without adding the missing distinction, whereas a new ROUTE can add genuinely new information. SplatField's continuous evidence dial makes this separation experimentally accessible.**

That is the claim worth carrying forward.
