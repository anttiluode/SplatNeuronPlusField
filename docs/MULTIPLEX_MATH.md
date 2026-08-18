# Multiplex morphology: local geometry, economy, attribution, and spectral overlap

Date: 2026-08-18

This note formalizes the membrane-multiplex idea without granting it an advantage by construction.

## 1. Setup

Let channel `k` have a vectorized transfer operator

```text
h_k(theta) in R^{n_k}
```

where `theta in R^p` are shared physical parameters (morphology, positions, release-site geometry, receptor geometry, etc.). Around a reference point `theta0`,

```text
delta h_k = J_k delta theta + O(||delta theta||^2)
J_k = d h_k / d theta |_{theta0}
```

Stack the channel outputs and Jacobians:

```text
h = [h_1; ...; h_m]
J = [J_1; ...; J_m]
```

Define

```text
T_k = image(J_k)
r_k = rank(J_k)

T_ind = T_1 direct-sum ... direct-sum T_m
R = sum_k r_k

S_shared = image(J)
r = rank(J)
```

Every shared perturbation produces a tuple whose `k`th component lies in `T_k`, so

```text
S_shared subset T_ind.
```

The independent attacker is allowed to choose a separate local parameter vector for each channel, and therefore has tangent space `T_ind`.

---

## 2. Exact local degree-of-freedom economy

The local number of channel-output degrees of freedom available independently is

```text
R = sum_k rank(J_k).
```

The shared morphology can realize only

```text
r = rank(J).
```

Therefore the exact local **degree-of-freedom economy** is

```text
Delta_DOF = R - r >= 0.
```

This is the correct rank statement.

It is slightly different from saying that rank deficiency is literally a byte saving. Rank measures local dimension, not code length.

For two channels,

```text
Delta_DOF = dim(row(J_1) intersect row(J_2)).
```

For more than two channels, `R-r` is the total redundancy created by overlap among the channel sensitivities in shared-parameter space.

### Important correction

Calling `Delta_DOF` the exact *description-length* saving is too strong.

At finite precision, the singular values matter. Let

```text
W = blockdiag(W_1, ..., W_m)
F_shared = J^T W J
```

and let `sigma_a` be the nonzero singular values of `W^(1/2) J`. For a local parameter range of radius `rho` and output tolerance `epsilon`, a high-rate local covering code has the schematic form

```text
L_shared(epsilon)
  ~ sum_a log2( rho * sigma_a / epsilon )_+ + constants.
```

The independent code has the analogous sum over the singular values of the individual `W_k^(1/2) J_k`.

Thus:

```text
exact zero singular values       -> true dimension saving
small singular values            -> finite-tolerance / effective saving
large singular values            -> directions that must be paid for accurately
```

A useful soft effective dimension is

```text
d_eff(lambda) = sum_a sigma_a^2 / (sigma_a^2 + lambda^2).
```

So the practical economy should be reported as a rate-distortion curve, not just one rank.

---

## 3. The exact error price of sharing

Let `t` be a desired infinitesimal change in the concatenated channel operators. Let `P_T` and `P_S` be orthogonal projectors onto `T_ind` and `S_shared` in the chosen output metric.

The best independent implementation has squared error

```text
E_ind^2 = ||(I - P_T) t||^2.
```

The best shared implementation has

```text
E_shared^2 = ||(I - P_S) t||^2.
```

Because `S_shared subset T_ind`, the projectors are nested and

```text
E_shared^2 - E_ind^2
    = ||(P_T - P_S) t||^2
    >= 0.
```

This is the clean local tradeoff.

The dimensions removed by sharing are exactly the directions in

```text
T_ind intersect S_shared^perp.
```

Sharing wins only when the task places little important energy in those discarded directions.

This is Gate 13 in multi-head form, but now the statement is explicit:

> **The economy is `R-r`; the price is the task energy projected onto the `R-r` directions that sharing removes.**

---

## 4. Analytic random-sharing baseline

Suppose the task-relevant target `t` lies in `T_ind` and compare the physical shared subspace `S_shared` of dimension `r` against a uniformly random `r`-dimensional subspace of the `R`-dimensional independent tangent space.

For a random subspace,

```text
E[ ||P_random t||^2 ] = (r / R) ||t||^2.
```

Therefore

```text
E[ extra error from random sharing ]
    = (1 - r/R) ||t||^2.
```

For a distribution of tasks with covariance `C_task` supported in `T_ind`, define the physical capture fraction

```text
capture_phys
    = tr(P_S C_task) / tr(C_task).
```

The isotropic random expectation is

```text
capture_random = r / R.
```

A natural alignment score is

```text
A_phys = capture_phys - r/R.
```

Interpretation:

```text
A_phys > 0   physical sharing preserves task directions better than random sharing
A_phys = 0   no special task alignment
A_phys < 0   physical sharing is worse than a random shared latent
```

This gives an analytic null before training anything.

---

## 5. Stronger matched random attacker

The uniform random-subspace null does not preserve each channel's individual sensitivity spectrum. A stronger attacker can.

Write each channel Jacobian as

```text
J_k = U_k Sigma_k V_k^T
```

with rank `r_k`. Since `r >= max_k r_k`, construct a shared latent `z in R^r` and choose a random row-isometry

```text
C_k in R^{r_k x r}
C_k C_k^T = I.
```

Then define

```text
J_k_random = U_k Sigma_k C_k.
```

This preserves, channel by channel:

```text
rank(J_k)
singular values of J_k
output sensitivity axes U_k
```

while randomizing the relative orientation of each channel in the shared latent coordinates. Generically the stacked rank is `r` when the construction is constrained accordingly.

This is a substantially fairer attacker than merely giving three random matrices the same parameter count.

The physical morphology earns something only if, at matched `r`, matched per-channel spectra and matched precision, it produces lower task distortion than this random shared-latent ensemble.

---

## 6. Where the economy / identifiability duality is exact

There is a real duality, but it is an **intervention / controllability** statement.

The independent system can move locally in `T_ind`, dimension `R`.
The shared morphology can move only in `S_shared`, dimension `r`.

Therefore the number of independent channel-control directions lost by tying all channels to one morphology is exactly

```text
Delta_intervention = R - r = Delta_DOF.
```

So:

> **Every local degree of freedom saved by sharing is also one local independent intervention direction that no longer exists.**

This is the precise form of the economy/confounding tension.

### Scalar-head special case

If each channel is summarized by one scalar effect,

```text
z_k(theta)
```

and

```text
g_k = grad_theta z_k,
G = [g_1^T; ...; g_m^T],
```

then each nonzero channel has `r_k = 1`, so

```text
R = m
r = rank(G)
Delta_DOF = m - rank(G).
```

That is exactly the number of channel-effect combinations that cannot be independently actuated through morphology.

If an experiment can perturb only morphology, high economy can therefore make causal channel separation difficult.

---

## 7. Why this is NOT automatically observational non-identifiability

Now suppose an experiment observes

```text
y = A h.
```

The number of invisible output-tangent directions inside the shared morphology is

```text
nu_obs_shared
    = dim(S_shared intersect ker(A))
    = r - rank(A J).
```

For an independent-channel model with block-diagonal Jacobian `J_ind`,

```text
nu_obs_ind
    = R - rank(A J_ind).
```

There is no general identity

```text
nu_obs = R-r.
```

Two counterexamples make this explicit.

### Counterexample A: no sharing, terrible attribution

Three independent scalar channels:

```text
h = (theta_1, theta_2, theta_3)
R = r = 3
Delta_DOF = 0.
```

Observe only the sum:

```text
y = h_1 + h_2 + h_3.
```

Then two directions are invisible:

```text
nu_obs = 2
```

although there is zero sharing economy.

### Counterexample B: maximal sharing, fully observable shared state

```text
h = (theta, theta, theta)
R = 3
r = 1
Delta_DOF = 2.
```

If all three outputs are measured separately (`A = I`), then

```text
nu_obs_shared = 0.
```

The morphology is maximally tied but its one available degree of freedom is perfectly observable.

Therefore:

> **Sharing economy equals lost independent intervention dimension, not arbitrary measurement non-identifiability.**

The connection to TWC's novelty / `eta` is therefore conditional: if TWC's perturbations are restricted to the shared morphology and the measurement asks for channel-specific causal effects, the same missing intervention directions can drive low novelty. But `eta` is not numerically identical to `R-r` in general.

---

## 8. Reciprocity: what is actually free

For a passive reciprocal extracellular volume conductor,

```text
L phi = q
L = -div(sigma grad)
```

with symmetric conductivity tensor `sigma` and reciprocal boundary conditions. `L` is self-adjoint, so its Green operator is self-adjoint:

```text
G = G^T
```

in a compatible discretization.

If the same port shapes are used to inject and read extracellular current/potential, with

```text
q = E s
readout = E^T phi,
```

then

```text
A_eph = E^T G E
```

and hence

```text
A_eph = A_eph^T.
```

An arbitrary symmetric `N x N` coupling requires

```text
N(N+1)/2
```

entries rather than `N^2`, asymptotically a factor of two.

But the more general abstraction in this repo is

```text
A_eph = R G E.
```

Electromagnetic reciprocity guarantees the symmetry of the passive medium operator `G`; it does **not** by itself guarantee

```text
R = E^T
```

for a biological whole-cell transfer, because emitting transmembrane currents and receiving extracellular fields involve membrane/cable state, orientation, conductances and potentially nonlinear active dynamics.

So the ledger may donate symmetry of `G` for free. It should donate symmetry of the complete cell-to-cell `A_eph` only when a matched-port approximation is explicitly justified.

---

## 9. Quasi-static does not mean frequency-flat cell-to-cell transfer

Write the ephaptic channel in frequency space as

```text
H_eph(omega)
    = R_eph(omega) G(omega) E_eph(omega).
```

In the simplest resistive electro-quasistatic approximation, `G` may be real and nearly frequency-independent over a range. But the membrane/cable source and receiver factors `E_eph(omega)` and `R_eph(omega)` can be strongly frequency-dependent and can carry phase.

Therefore

```text
quasi-static medium
```

does not imply

```text
frequency-flat, zero-phase neuron-to-neuron ephaptic transfer.
```

The chemical diffusion-decay channel is explicitly frequency dependent. For spatial Fourier mode `k`,

```text
dc/dt = D Laplacian(c) - kappa c + B u
```

gives

```text
H_chem(k, omega)
    = R_chem(k,omega) B
      / (kappa + D |k|^2 + i omega).
```

It is low-pass and phase-lagged.

Synaptic channels also have receptor and membrane kinetics spanning multiple scales. Therefore the three biological channels should not be assumed to occupy disjoint frequency bands.

---

## 10. Two economies that must be measured separately

There are two independent geometric questions.

### A. Parameter / morphology economy

Do the channel operators depend on the same parameter directions?

Measured by the singular geometry of

```text
J_1, ..., J_m
```

and summarized at zero tolerance by

```text
Delta_DOF = sum r_k - rank(J).
```

### B. Signal non-interference

Do the actual channel signals occupy approximately orthogonal temporal / spatial / molecular subspaces?

For compatible channel signal representations, define a spectral Gram matrix

```text
Omega_kl
    = integral <H_k(omega), H_l(omega)>_W d omega
```

and normalized overlap

```text
rho_kl
    = |Omega_kl| / sqrt(Omega_kk Omega_ll).
```

Small `rho_kl` means low signal-space interference.

These quantities are logically independent.

Possible systems include:

```text
high parameter sharing + low spectral interference
high parameter sharing + high spectral interference
low parameter sharing  + low spectral interference
low parameter sharing  + high spectral interference
```

So frequency/time-scale multiplexing and description saving must not be conflated.

---

## 11. The experiment this math now demands

A fair local Gate should choose a family of target multi-channel perturbations and compare at fixed distortion or fixed local code length:

```text
1. physical shared morphology Jacobian
2. independent channel Jacobians
3. random r-dimensional shared subspace
4. matched-spectrum random shared latent
5. optionally a learned generic shared latent
```

Report separately:

```text
R, r, Delta_DOF
singular spectra / finite-tolerance effective dimensions
rate-distortion curve
physical task capture fraction
random expected capture r/R
matched-random attacker distribution
intervention deficit R-r
observational nullity for each measurement operator A
spectral-overlap matrix rho_kl
```

### Frozen prediction

Before numbers:

```text
If task directions align with the physical morphology manifold,
physical sharing should beat matched random sharing at equal r / rate.

After dense rotation of task structure,
that advantage should disappear.

If physical sharing does not beat the matched random attacker even in the aligned condition,
there is no morphology-specific computational resource result here.
```

This is the direct multi-channel descendant of Gate 13.

---

## 12. Current mathematical headline

The strongest clean statement is not

```text
one morphology implements three channels cheaply.
```

It is:

> **Locally, sharing one physical parameterization removes exactly `R-r` independently tunable channel directions. The same number is an economy of degrees of freedom and a deficit of independent interventions. Whether that economy is useful is determined by how much task-relevant variation lies in the retained shared tangent space. Observational attribution is a separate nullspace problem determined jointly by the shared tangent and the measurement operator.**

That statement is strong enough to test and narrow enough to survive the obvious counterexamples.
