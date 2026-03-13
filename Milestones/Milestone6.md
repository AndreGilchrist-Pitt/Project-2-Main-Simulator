## Milestone 6: Power Injection Equations and Newton-Raphson Initialization

**Target Date: 3/17/2026**

### Introduction

Milestone 6 focuses on implementing the power injection equations for each bus
and calculating the power mismatch, which is a critical step in performing power flow analysis.
These calculations form the basis of iterative numerical methods, such as the Newton-Raphson method,
used to solve power flow equations.
---

### System Settings Class

#### Objective

- Develop functions to compute real and reactive power injections at each bus using the
  system admittance matrix $(Y_{bus})$ and per-unit voltage magnitudes.

#### Implementation Steps

1. **Define Power Injection Equations**  
   The complex power injected at each bus `i` is given by:  
   $S_{i} = V_{i} \displaystyle\sum_{j=1}^{N} Y_{ij}^* V_{j}^*$  
   where:
    - $S_{i} = P_{i} + jQ_{i}$ is the complex power injection at bus `i`
    - $V_{i}$ is the voltage at bus `i`
    - $Y_{ij}$ is the `(i, j)` element of the system admittance matrix $(Y_{bus})$
    - $V_{j}^*$ is the complex conjugate of the voltage bus `j`

2. **Implement Real and Reactive Power Calculations**
    - Real power injection:  
      $P_{i} = |V_{i}| \displaystyle\sum_{j=1}^{n} |V_{j}| (G_{ij} \cos(\delta_{ij}) + B_{ij} \sin(\delta_{ij}))$
    - Reactive power injection:  
      $Q_{i} = |V_{i}| \displaystyle\sum_{j=1}^{n} |V_{j}| (G_{ij} \sin(\delta_{ij}) - B_{ij} \cos(\delta_{ij}))$  
      where $\delta_{ij} = \delta_{i} - \delta_{j}$ and $G_{ij}$ and $B_{ij}$ are the real and imaginary parts of
      $Y_{ij}$, respectively.

3. **Function Implementation**  
   Define a method `compute_power_injection(bus,ybus,voltages)` that:
    - Accepts a bus object, system admittance matrix, and voltage vector as inputs
    - Computes the real and reactive power injections based on the above equations
    - Returns values $P_{i}$ and $Q_{i}$
4. **Validation**  
   Ensure the implementation correctly computes power injections for different bus types:
    - **Slack bus:** No mismatch calculation required
    - **PQ bus:** Both $P_{i}$ and $Q_{i}$ equations apply
    - **PV bus:** Only the $P_{i}$ equation applies

---

### Power Mismatch Calculation

**Objective**  
Compute the power mismatches to determine the difference between specified and calculated values for each bus.

#### Implementation Steps

1. **Define Mismatch Equations**  
   For each non-slac bus, the power mismatch is:  
   $\Delta P_{i} = P_{i}^{spec} - P_{i}^{calc}$  
   $\Delta Q_{i} = Q_{i}^{spec} - Q_{i}^{calc}$  
   PV buses do not require a $\Delta Q_{i}$ calculation, as the voltage magnitude is specified.
2. **Implement Mismatch Computation**  
   Define a method `compute_power_mismatch(buses,ybus,voltages)` that:
    - Iterates through each bus and calculates power mismatches
    - Constructs the mismatch vector `f` used in numerical methods
3. **Ensure Correct Data Handling**
    - Slack bus should have no mismatch
    - PQ buses must include both $\Delta P_{i}$ and $\Delta Q_{i}$
    - PV buses must only include $\Delta Q_{i}$
4. **Validation**
    - Verify results using a simple test case with known values
    - Ensure the computed mismatches align with expected values

---

### Final Check

- Ensure power injection functions compute correct values using sample networks
- Validate mismatch calculations for different bus types
- Confirm output format aligns with numerical solution methods
  By completing Milestone 6, we will be ready to implement the iterative power flow solutions in the next pahse


 