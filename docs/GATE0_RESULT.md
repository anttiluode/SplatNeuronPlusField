# Gate 0 result — dual geometry

Date: 2026-08-18

Preregistration: [`GATE0_PREREG.md`](GATE0_PREREG.md)  
Preflight corrections: [`GATE0_PREFLIGHT.md`](GATE0_PREFLIGHT.md)

## Result

Registered local reproduction, `4000` train / `4000` test samples, noise `0.05`:

```text
seed    synaptic A   metric B   combined C   matched generic D   swap-position E   clamp F
18001     0.5008       1.0000      1.0000          1.0000            0.0150       0.5122
18002     0.5018       1.0000      1.0000          1.0000            0.0000       0.4940
18003     0.4935       1.0000      1.0000          1.0000            0.0000       0.5060
```

Route-independence checks:

```text
seed    geometry ΔW   geometry ΔA_eph   rewire ΔW   rewire ΔA_eph
18001      0.0000          0.5003          1.4172       0.0000
18002      0.0000          0.4725          1.4064       0.0000
18003      0.0000          0.5092          1.4235       0.0000
```

The matched-generic attacker preserved the metric matrix Frobenius norm to floating-point precision and its singular values to maximum absolute errors of approximately `2.7e-15` to `5.3e-15`.

## Verdict

### Structural dual-route instrument: PASS

The deliberately blind wired path remained at chance. The metric route exposed the source-address distinction. Exchanging only the two task-relevant physical source positions — while leaving source identities and `W` fixed and reusing the already-trained readout — almost completely inverted/destroyed the learned consequence. Removing the metric route returned performance to chance.

The route-independence algebra also behaved as required: changing geometry altered `A_eph` without altering `W`, while rewiring `W` altered `W` without altering `A_eph`.

### Special metric/ephaptic computational advantage: FAIL / NOT ESTABLISHED

The matched generic extra coupling solved the task perfectly in every registered seed, just like the metric route.

Therefore Gate 0 supports only the narrow structural statement:

> **Two independently manipulable coupling routes can coexist in the instrument, and a metric route can carry a distinction that a deliberately blind frozen wired route does not carry. This toy provides no evidence that metric coupling is more capable or more efficient than a generic additional coupling matrix.**

That is enough to proceed to Gate 1, because Gate 1 asks a different question: whether a **shared slow metric state** has consequences that matched independent private adaptation does not.

## What this result does not show

- nothing about the strength or importance of ephaptic coupling in real cortex;
- nothing about memory storage in electric potential;
- nothing about morphology;
- nothing about learning the metric geometry;
- nothing about natural tasks;
- nothing about efficiency relative to generic matrices;
- nothing about oscillations or a field conductor.

Gate 0 is plumbing with an attacker, not a neuroscience result.
