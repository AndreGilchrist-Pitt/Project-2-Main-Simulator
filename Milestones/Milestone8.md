## Milestone 8: Newton-Raphson
**Target Date:** 3/26/2026

### Introduction
This milestone implements the Newton–Raphson method for solving the power flow problem.
Building upon the Jacobian matrix developed in Milestone 7 and the power mismatch from Milestone 6,
the iterative solution updates bus voltage angles and magnitudes until convergence is achieved.

---

### Implementation (repo)

| Deliverable | Location |
|-------------|----------|
| **PowerFlow** class | `Src/Utils/Classes/powerflow.py` |
| Validation script | `MilestoneValidationHelp/milestone8_main.py` |
| Docs / tracking | `Milestones/Milestone8.md`, `Milestones/MilestonesTracker.md` |

**Prerequisites:** `circuit.calc_ybus()` before `solve`. Uses `Circuit.compute_power_injection` (M6) and `Jacobian.calculate_jacobian` (M7).

**Public API (`PowerFlow`):**
| Member | Role |
|--------|------|
| `solve(circuit, tol=0.001, max_iter=50, verbose=False)` | Run NR; updates `bus.vpu`, `bus.delta` (degrees) in place. |
| `mismatch_vector(circuit)` | Current block-ordered **f** (same order as **J** rows). |
| `converged` | `True` if stopped with `max(|f|) < tol`. |
| `iterations` | Number of NR iterations completed (0-based index at convergence). |
| `final_mismatch_max` | `max(|f|)` when the solver stopped. |

The course PDF lists `solve(buses, ybus, …)`; **`circuit`** supplies `buses`, `ybus`, generators, and loads for mismatch.

**Loop:**
1. Build **f**: all **ΔP** (non-slack), then all **ΔQ** (PQ only) — same row order as Milestone 7 **J**.
2. Compute **J** with `Jacobian.calculate_jacobian(...)`.
3. Solve **J · Δx = f** (J = ∂P_calc/∂x, ∂Q_calc/∂x; f = P_spec−P_calc, Q_spec−Q_calc).
4. Update **δ** (degrees) for non-slack buses; update **|V|** for PQ buses only.
5. Stop if **max(|f|) < tol**; else stop after **max_iter** (`converged = False`).

**Bus types (standard NR):**
- **Slack:** fixed |V| and δ (not in Jacobian / mismatch rows).
- **PV:** update **δ** only; |V| fixed at scheduled value.
- **PQ:** update **δ** and |V|.

**Jacobian / mismatch size:** For **N** buses, **1 slack**, **N_PV** PV buses:  
**(2N − 2 − N_PV) × (2N − 2 − N_PV)** equations and unknowns.  
Example (`milestone8_main.py`): **N = 5**, **N_PV = 1** → **7×7** **J**, **length-7** **f** (4 ΔP + 3 ΔQ).

**Initialization:** Read |V| and δ from buses (flat start: e.g. |V| = 1.0 p.u., δ = 0° on PQ/slack; PV |V| at scheduled value, e.g. 1.05 p.u.).

---

### How to run validation
From the **repo root** (folder that contains `Src/`):

```text
python MilestoneValidationHelp/milestone8_main.py
```

`milestone8_main.py` prepends the repo root to `sys.path` so `Src` imports resolve. Alternatively set `PYTHONPATH` to the repo root.

---

### Original spec reference
- Power Flow class; PDF naming `solve(buses,ybus,tol=0.001,max_iter=50)`.
- Validation: small networks (five-bus in script), PowerWorld optional, Jacobian dimensions match **f**.

---

### Final Check
- [x] Solver integrates block-ordered **f** and Jacobian **J**.
- [x] Slack / PV / PQ update rules.
- [x] Tolerance and iteration limit.
- [x] Output: final |V| and δ per bus; script verifies **J** shape, residual, slack/PV constraints.
- [ ] Optional: PowerWorld comparison.
