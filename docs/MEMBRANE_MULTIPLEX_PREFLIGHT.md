# Membrane multiplex preflight

Date: 2026-08-18

## Trigger

The next architectural correction is not another field and not another neuron type.

A neuron should not be modeled as producing one scalar `output` that is then copied into several media.

The cell membrane is a distributed boundary at which the same ongoing cellular event can have several simultaneous consequences:

```text
intracellular consequence
    membrane voltage / compartment state changes

synaptic consequence
    action potentials drive transmitter release at addressed contacts

quasi-static extracellular consequence
    transmembrane currents contribute immediately to extracellular potential

slow chemical / ionic consequence
    transmitter spillover, neuromodulator release, ionic accumulation, buffering, etc.
```

These are different channels with different address vocabularies, time constants and plasticity mechanisms.

## Physics correction

Do **not** say that neurotransmitter release is how a neuron controls the extracellular electric field.

At ordinary synapses, transmitter binds receptors and opens postsynaptic conductances. Those transmembrane ionic currents, together with active membrane currents, contribute to extracellular potentials.

Likewise, an incoming dendritic synaptic current can contribute to the local extracellular field while it is still being integrated inside the receiving neuron. The neuron does not have to wait for a somatic spike before it writes back into the shared electric medium.

Therefore the current point-unit shorthand

```text
q = E f(v)
phi = G q
```

is acceptable only as Gate-0 plumbing. It should not become the biological interpretation.

A later compartmental form should look more like

```text
q_i(x,t) = transmembrane_current_i(x,t)
phi(x,t) = G[q](x,t)
```

where `q_i` is distributed over the membrane and depends on synaptic input, local voltage, channel state and active currents.

## Dendrite correction

Passive dendritic cable properties are low-pass: fast voltage components attenuate more strongly with electrotonic distance. But active conductances can compensate, amplify, resonate or otherwise reshape this filtering.

So the useful statement is not

```text
dendrite = low-pass filter
```

but

> **dendritic morphology plus local membrane state defines a state-dependent spatiotemporal transfer operator.**

The same local synaptic event is seen differently by:

```text
1. the soma / axon initial segment
2. nearby dendritic branches
3. the extracellular field around that membrane patch
4. downstream synaptic targets if a spike is eventually emitted
```

This is a genuine multi-receiver object.

## Multiplex-transducer abstraction

For unit `i`, replace one abstract output with several channel-specific writes:

```text
private state:      h_i
membrane state:     v_i(x)

synaptic write:     u_i^syn(t)
electric write:     q_i^eph(x,t)
chemical write:     u_i^chem(x,t)
```

and several channel-specific receive operators:

```text
r_i^syn  = W_i * presynaptic events
r_i^eph  = R_i^eph phi
r_i^chem = R_i^chem c
```

with

```text
phi = G_eph q^eph                         # quasi-static, no autonomous memory

dc/dt = D_c Laplacian(c) - K c + B u^chem   # slow shared state
```

The important point is that `R_i^eph`, `R_i^chem`, synaptic receptors and intracellular dendritic transfer need not define the same neighborhood.

One biological cell therefore participates in several overlapping networks at once.

## Do not confuse the channels

```text
synaptic graph
    addressed / rewritable / receptor-specific

quasi-static electric overlay
    metric / geometry-induced / essentially instantaneous medium solve

chemical or ionic milieu
    metric / diffusive / stateful / transmitter- and receptor-specific

intracellular dendritic tree
    private geometry / stateful / nonlinear / filtering
```

A neuron can couple these channels because its membrane and secretory machinery sit at their intersection.

## New hypothesis suggested by this architecture

The possible advantage is **not** that one neuron has more outputs.

A generic simulator can always add more matrices.

The interesting question is whether one physical morphology provides a compact shared implementation of several transfer functions at once.

Schematically, for receiver `j` and source `i`:

```text
H_syn[j<-i](tau)
H_eph[j<-i](tau)
H_chem[j<-i](tau)
```

are not independent arbitrary objects. They are jointly constrained by the same physical cell positions, morphologies, membrane currents, release sites and receptor distributions.

This suggests a later resource question:

> **Can one shared physical geometry implement a useful family of channel-specific transfer kernels more cheaply than storing each channel as an unrelated addressed operator?**

That is the version worth attacking.

## Mandatory attacker

Before any `multiplex neuron` claim, compare against a generic multi-channel system with:

- the same total state dimension;
- the same number of channel outputs;
- matched singular spectra / temporal decay constants where meaningful;
- explicit connection-description cost;
- no requirement that its three channel operators share geometry.

If the generic system matches at comparable resource cost, the biological geometry has not earned itself.

## Relation to Gate 1

Gate 1/1b already showed:

```text
metric slow state        solves aligned history cheaply
learned addressed state  solves aligned and scrambled history perfectly
```

So unique capability is dead.

This multiplex correction changes the next resource question from

```text
field versus graph
```

to

```text
shared physical implementation of multiple transfer kernels
versus
independently stored generic channel operators
```

That is a better connection to actual cells.

## Relation to sensory innovation

Keep this separate from the grounding/model-collapse branch.

External sensory channels inject evidence about the world. The synaptic/electric/chemical channels here mainly describe how the nervous system internally propagates, transforms and shares consequences after that evidence enters.

A later architecture may combine the two:

```text
independent sensory innovations
        -> private dendritic dynamics
        -> multiplex internal writes
        -> other receivers
        -> prediction / action
        -> new sensory innovation
```

The system remains grounded because the loop is repeatedly perturbed by inputs not generated by its own internal state.

## Stop lines

- no claim that neurotransmitter itself *is* the electric field;
- no claim that every neuron uses all channel types in the same way;
- no claim that dendrites are merely passive low-pass filters;
- no claim that extracellular electric potential stores history;
- no claim that a multi-channel neuron has unique computational capability;
- no biological efficiency claim until a matched generic multi-channel resource attacker is run.

## Immediate next mathematical object

The clean formal object is a **multiplex transfer operator**:

```text
H_ji(omega) = {
    H_syn,ji(omega),
    H_eph,ji(omega),
    H_chem,ji(omega)
}
```

with each component living on a different geometry and timescale, while sharing latent physical parameters.

That is the object to analyze next rather than adding another ad-hoc neuron architecture.
