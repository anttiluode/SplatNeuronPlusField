# Anchored world model: content, support, lineage, and ROUTE

Date: 2026-08-18

Status: architectural proposal + mathematical bridge. **Not a novelty claim and not yet an experiment.**

This note records a possible world-model architecture suggested by the receiver/provenance work.

The key distinction is not merely

```text
known versus unknown
```

or

```text
low versus high uncertainty.
```

A generative world model can be highly confident because its prior/manifold strongly prefers one completion, while the current world supplied little evidence for that specific completion.

So the state should not contain only a best reconstruction.

It should also retain how that reconstruction is anchored.

---

## 1. Type knowledge versus token knowledge

A pretrained generative model can know broad regularities before seeing a particular environment:

```text
walls tend to continue
objects have coherent shapes
faces have paired eyes
rigid bodies persist
roads usually connect
```

Call this **type knowledge**.

A newly instantiated world begins with little **token knowledge**:

```text
this wall is here
this object is red
this face is this person
this corridor turns left
```

The prior can therefore generate a plausible hidden world before enough evidence exists to determine which particular world is present.

The engineering goal is not to forbid that completion. It is to prevent type-level plausibility from being silently promoted into token-level evidence.

---

## 2. Two coupled world states

A minimal anchored world model should maintain at least

```text
Xhat_t     completed / predicted world state
Q_t        evidential support state
```

and preferably a third object

```text
L_t        source lineage / dependency state
```

`Xhat_t` answers:

> what world state best explains current evidence under the learned model?

`Q_t` answers:

> which directions / regions / variables of that state are constrained by actual observations rather than mainly by the prior?

`L_t` answers:

> which support came from genuinely independent sources, and which support shares an ancestor and must not be counted twice?

This gives the schematic state

```text
W_t = (Xhat_t, Q_t, L_t).
```

---

## 3. Local information decomposition

For a latent world state `z`, suppose the current objective / negative log posterior near a solution is

```text
E(z)
    = E_model(z)
    + sum_s E_obs,s(z).
```

At a local linearization, define Hessian / Fisher-information contributions

```text
H_model = d2 E_model / dz2
H_obs   = sum_s d2 E_obs,s / dz2
H_post  = H_model + H_obs.
```

For a decision-relevant direction `v`, define the observation-support fraction

```text
q_ext(v)
    = (v^T H_obs v)
      / (v^T H_post v)
```

when the denominator is positive.

This separates two cases that a scalar posterior confidence can conflate:

```text
high confidence + high observation support
high confidence + low observation support
```

The second state can be low entropy and still be weakly anchored to the particular environment now being observed.

This quantity is not claimed as a universal uncertainty metric. It is a local provenance statistic.

---

## 4. The no-self-evidence rule

A generative world model may use its own completed state to predict forward:

```text
Xhat_t -> model dynamics -> Xhat_{t+1}^-.
```

But a prediction generated only from the current model state is not an independent observation of the external world.

Therefore:

> **Self-generated completion may update the prior/prediction state, but must not be added again as independent external evidence.**

If a model generates `Y_self` entirely from its current state / belief and then re-ingests it as if it were a new sensor sample, naïve evidence accumulation can double-count information and create overconfidence without new external constraint.

This is closely related to the classical common-information / double-counting problem in decentralized Bayesian data fusion. The world-model version should therefore track source dependencies, not just agreement.

---

## 5. New external routes

Let hidden target `Z` be decision relevant.

A proposed new observation route `Y_new` has useful novelty only to the extent that

```text
I(Z ; Y_new | Y_old, lineage)
```

is positive.

Examples:

```text
move camera around an occluder
query depth instead of RGB
wait for a moving object to reveal itself
ask a second model trained on different private data
use touch when vision is aliased
```

A second signal derived from the same original evidence may agree perfectly while contributing little conditional novelty.

So ROUTE should score expected **new support**, not raw agreement.

---

## 6. Support should age with the world

External evidence should not remain equally authoritative forever.

A static wall observed ten seconds ago may still be strongly anchored.
A pedestrian observed ten seconds ago is not.

So support needs its own dynamics:

```text
Q_t -> propagate / decay according to modelled process uncertainty -> Q_{t+1}^-.
```

The exact update depends on the world model.

Important principle:

> **Prediction can propagate old support through a trusted dynamics model, but process uncertainty should generally reduce source-specific anchoring over time rather than create new anchoring.**

This links the evidence ledger to temporal windows without claiming a biological memory mechanism.

---

## 7. A less-hallucinatory 3D world model

A concrete system could use a persistent 3D representation (e.g. Gaussian/splat/object/voxel/implicit state) with at least two attached fields:

```text
content field
    geometry / semantics / appearance / dynamics

support field
    how strongly each local variable or latent direction is tied to independent observations
```

Optionally add

```text
lineage field
    sensor/model/source ancestry for correlation accounting.
```

At startup:

```text
pretrained prior       strong type knowledge
instance support       near zero except where actually observed
```

As observations arrive:

```text
plausible completion -> increasingly anchored instance model.
```

Crucially, hidden regions need not remain blank. They may be generated for planning/rendering, but the system should be able to distinguish

```text
plausible but prior-driven
from
source-anchored.
```

---

## 8. Why uncertainty alone is not enough

Two states can have similar low posterior variance:

```text
A. many independent observations agree
B. one ambiguous observation + a very strong prior
```

A scalar uncertainty estimate can report both as confident.

The support/provenance state asks a different question:

> where did the confidence come from?

This is complementary to epistemic/aleatoric uncertainty, calibration, OOD detection, and active sensing rather than a replacement for them.

---

## 9. ROUTE policy

For a task-sensitive subspace `V_decision`, a route should be considered when

```text
1. action consequences are sensitive to V_decision;
2. posterior confidence is high enough to encourage commitment;
3. observation support is weak in V_decision;
4. an available route is predicted to add conditional novelty there.
```

A simple schematic score is

```text
route_value
    = expected task-weighted increase in external support
      - sensing / action cost.
```

This makes the dangerous state explicit:

```text
CONFIDENT_BUT_WEAKLY_ANCHORED.
```

---

## 10. Relation to SplatField alpha

SplatField already provides a controlled evidence-drive dial:

```text
alpha high -> external observation dominates
alpha low  -> internal dynamics dominate
```

The next useful measurement is not merely output quality versus alpha.

Measure two axes independently:

```text
P(alpha) = plausibility / internal coherence
A(alpha) = source answerability / external anchoring
```

The interesting region would be

```text
P remains high
while
A falls.
```

That region must be measured rather than assumed.

---

## 11. First synthetic gate

Construct a tiny partially observed 3D or latent world with a pretrained completion prior.

Hidden worlds `x_a` and `x_b` should be intentionally aliased under one view `M_1` but distinguishable under another view `M_2`.

Compare:

```text
A. observation only
B. completion from M_1
C. repeated self-reinjection / WAIT
D. independent second observation / ROUTE
E. second receiver with shared ancestry
F. second receiver with independent hidden-factor information
```

Track separately:

```text
posterior confidence
external-support fraction
true hidden-state accuracy
calibration
source lineage
conditional novelty of new route
```

Frozen qualitative prediction:

```text
completion can improve point estimates under ambiguity;
self-reinjection can increase internal coherence but must not count as new external support;
ROUTE improves hidden-state recovery only when it carries conditional novelty;
independent receivers can add support when their blind spots / private data differ.
```

---

## 12. What is established elsewhere versus what remains open here

Established neighboring ideas include:

```text
Bayesian filtering / smoothing
SLAM and belief-space planning
POMDPs / active perception
information-gain exploration
epistemic uncertainty and calibrated world models
common-information / covariance-intersection methods for correlated fusion
```

Therefore do not claim novelty for

```text
maintaining uncertainty
active sensing
Bayesian prior + likelihood updates
avoiding double-counting in generic sensor fusion
```

The possibly useful research combination to test is narrower:

> **A high-dimensional generative world model that explicitly preserves source-specific evidential support, separately from its completed content, and uses conditional support novelty to decide when to ROUTE.**

Whether that combination is new or useful is an empirical/literature question, not established by this note.

---

## 13. Narrow headline

> **A less-hallucinatory world model need not generate less. It can generate freely while keeping a second ledger of which parts of the generated world are actually anchored by independent observations. Predictions may propagate belief, but they should not manufacture new evidence. When task-relevant confidence is mostly prior-driven, the system should seek a ROUTE that adds conditionally novel support.**
