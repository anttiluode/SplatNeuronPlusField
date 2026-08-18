# Gate 0 preflight — why the intervention was tightened

Date: 2026-08-18

This note records a pre-result harness correction made before treating Gate 0 as a registered result.

The first implementation used two test-time controls:

```text
randomly permute all physical positions
shuffle scalar emitter/receiver gains
```

Local scratch runs immediately showed that these were poor controls.

Across several seeds, the constructed task behaved as expected at the coarse level:

```text
synaptic only            ~0.49–0.51
metric only              1.00
synaptic + metric        1.00
matched generic route    1.00
field clamp              ~0.49–0.52
```

But:

- a random global position permutation sometimes destroyed the trained readout and sometimes left it almost perfect, depending on the permutation;
- shuffling the mild scalar emit/read gains had essentially no effect (`~1.00`) because those gains did not encode a meaningful orientation/morphology relation in Gate 0.

Therefore the original controls were **not** retained merely because some random shuffles looked dramatic.

The registered intervention was tightened prospectively to a deterministic counterfactual:

```text
swap only the physical positions of the two task-relevant source identities
keep W and source identities fixed
reuse the readout trained under the original geometry
```

This directly asks whether the trained consequence is tied to metric address rather than symbolic source address.

In the same scratch seeds, this source-position swap drove the original C readout to approximately `0.000–0.015` accuracy while field clamp returned it to chance. The matched generic route remained perfect. Those scratch values are **preflight observations**, not the registered scientific result.

The scalar gain-shuffle condition was removed rather than renamed “orientation.” True emitter/receiver orientation or morphology is deferred to a later gate with an explicit spatial model.
