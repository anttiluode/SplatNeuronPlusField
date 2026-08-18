# Receiver provenance: what was seen versus what was supplied

Date: 2026-08-18

Status: mathematical / architectural proposal. **Not a biological claim and not yet an experiment.**

`EVIDENCE_COMPLETION_ROUTE.md` adds a completion operator to the receiver:

```text
r      = R X
Xhat   = G(r, h)
```

This note adds the missing epistemic state.

A receiver should not ideally return only a completed state `Xhat`. It should also preserve some representation of **support provenance**:

```text
(Xhat, Q)
```

where `Q` says which distinctions in `Xhat` are strongly constrained by current observations and which are mainly inherited from prior / internal structure.

The central failure mode is therefore not simply

```text
receiver predicts
```

but

```text
receiver predicts
    +
forgets which parts were predictions
```

---

## 1. Linear-Gaussian version

Take a hidden state

```text
x ~ N(mu0, Sigma0)
```

and an observation

```text
y = M x + epsilon
epsilon ~ N(0, Sigma_y).
```

Write prior precision and evidence precision as

```text
Lambda_prior = Sigma0^{-1}
Lambda_obs   = M^T Sigma_y^{-1} M
```

Then posterior precision is

```text
Lambda_post = Lambda_prior + Lambda_obs.
```

This decomposition is useful because it preserves provenance:

```text
posterior certainty
    = certainty supplied by prior
    + certainty supplied by current observation.
```

A completed estimate can be sharp even when `Lambda_obs` is weak in the decision-relevant direction.

So **confidence is not the same as external support**.

---

## 2. Direction-specific support

For a decision-relevant direction `v`, define a simple external-support fraction

```text
q_ext(v)
    = (v^T Lambda_obs v)
      / (v^T Lambda_post v)
```

when the denominator is nonzero.

Interpretation:

```text
q_ext(v) near 1
    current observation provides most of the precision in direction v

q_ext(v) near 0
    the receiver may be very certain, but that certainty is mainly prior-supplied
```

This is deliberately a simple local quantity, not a universal epistemic metric.

The important conceptual distinction is:

```text
posterior confidence
versus
external evidential support.
```

They can move in opposite ways.

---

## 3. WAIT and ROUTE in precision form

A new route

```text
y_2 = M_2 x + epsilon_2
```

adds

```text
Lambda_route = M_2^T Sigma_2^{-1} M_2
```

so

```text
Lambda_post,new
    = Lambda_prior
    + Lambda_old
    + Lambda_route.
```

ROUTE is useful when `Lambda_route` contributes precision in directions that matter to the current ambiguity.

By contrast, simply re-running the same deterministic observation through more internal computation does not add a new likelihood term.

Important nuance: repeated **independent noisy measurements through the same sensor** can add evidence because they are new samples. `WAIT` means reprocessing the already available observation, not acquiring statistically independent measurements.

---

## 4. A possible ROUTE rule

Suppose an action depends on a direction / feature set `V_decision`.

A receiver should consider ROUTE when all three are true:

```text
1. posterior confidence is high enough to tempt action;
2. external-support q_ext is low in decision-relevant directions;
3. an available route is expected to add conditional information there.
```

This is the dangerous quadrant:

```text
high confidence
low external support
```

because internally completed structure can feel settled while remaining weakly constrained by the present world.

A Kynnys-like controller could therefore distinguish

```text
CONFIDENT_AND_OBSERVED
CONFIDENT_BUT_PRIOR_DRIVEN
UNCERTAIN_BUT_ROUTABLE
UNCERTAIN_AND_UNROUTABLE
```

rather than treating one scalar confidence score as sufficient.

---

## 5. Nonlinear / learned receiver version

For a general learned receiver there may be no explicit Gaussian precision matrix.

Possible empirical proxies for support provenance include:

```text
- sensitivity of Xhat to masking / perturbing the current observation;
- disagreement across receiver priors under the exact same observation;
- conditional decodability of the hidden factor from raw evidence alone;
- posterior change caused by an independent ROUTE observation;
- ensembles / counterfactual completions consistent with the same evidence;
- local Jacobian rank / singular values of observation-to-reconstruction maps.
```

The goal is not merely uncertainty estimation.

It is to separate:

```text
uncertainty because evidence is weak
from
certainty created mainly by the receiver's prior.
```

---

## 6. SplatField interpretation

SplatField's `alpha` can be used as a controlled way to change how much current external drive contributes relative to internal field state.

A useful future plot would therefore contain at least two axes / traces:

```text
reconstruction confidence / plausibility
external support / source answerability
```

The interesting regime is not simply `alpha low`.

It is a regime where

```text
internal plausibility remains high
while
source-specific evidential support becomes low.
```

That must be measured, not assumed.

---

## 7. Human motivation, kept outside the result column

Ambiguous social cues make the distinction intuitive:

```text
small present cue
+
large learned history
->
rich interpretation.
```

The interpretation may be useful and may even be correct. The computational danger is that the receiver may not experience a clear boundary between

```text
what the cue constrained
and
what its own history supplied.
```

This motivates the provenance instrument but is not empirical evidence for it.

---

## 8. Relation to multi-model / multi-sensor systems

Independent receivers or sensors are valuable not merely because they add more samples, but because they may contribute evidence in different blind directions.

For hidden target `Z`, the relevant quantity remains conditional novelty:

```text
I(Z ; Y_new | Y_old).
```

A second model that repeats the first model's projection may add little.
A second model with different private data / errors may add a distinction the first lacks.

Thus a useful system should track both:

```text
agreement
and
provenance / independence of the agreeing evidence.
```

Ten copies of the same blind spot should not count like ten independent routes.

---

## 9. Stop lines

- no claim that brains explicitly represent Gaussian precision matrices;
- no claim that subjective confidence equals posterior precision;
- no claim that prior-driven inference is intrinsically wrong;
- no claim that repetition never adds information: new independent samples can;
- no claim that disagreement automatically means useful independence;
- no claim that low external support implies a completion is false;
- no human diagnosis from this formalism.

---

## 10. Narrow headline

> **The receiver should preserve not only a completed state but evidence provenance. A state can be internally coherent and highly confident while being weakly constrained by the current observation. ROUTE is most valuable when it adds support in exactly those decision-relevant directions where confidence is prior-driven rather than externally anchored.**
