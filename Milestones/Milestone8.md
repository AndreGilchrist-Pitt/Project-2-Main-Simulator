## Milestone 8: Newton-Raphson
**Target Date:** 3/26/2026

### Introduction
This milestone implements the Newton-Raphson method for solving the power flow problem.
Building upon the Jacobian matrix developed in the Mileston 7 and the power mismatch vector from Milestone 6,
the iterative solution updates bus voltage angles and magnitudes until convergence is achieved.
---
### Create Power Flow Class
**Objective:**  
- Develop a Newton-Raphson solver class that iteratively solves for bus voltage magnitudes and angles 
in a power system using the Jacobian matrix and power mismatches
### Implementation Steps:
1. Create Power Flow Class
**Methods:**
- `solve(buses,ybus,tol=0.001,max_iter=50)`
2. Initialize Variables
- Extract initial voltage magnitudes and angles from bus data. Flat start is all voltage magnitudes
equal to 1.0 and all angles equal to 0 degrees.
- Initialize iteration counter and convergence flag
3. Iterative Solution Loop
Inside the `solve()` method:
    - **Step 1:** Use Milestone 6's power mismatch function to calculate mismatch vector $\Delta P$
    - **Step 2:** Use Milestone 7’s Jacobian class to compute Jacobian matrix $J$
    - **Step 3:** Solve the linear system $J \cdot \Delta x = f$, where $\Delta x$ contains corrections to voltage and angles and magnitudes
    - **Step 4:** Update voltages and angles
    - **Step 5:** Check convergence: `if max(|f |) < tol, break loop`
    - **Step 6:** If max iterations are exceeded, report non-convergence
4. Handle Bus Types Properly
- **Slack bus:** No updates to voltage or angle
- **PQ bus:** Update only angle, not voltage magnitude
- **PV bus:** Update both voltage and angle
---
### Validation and Testing
- **Test Systems:** Use small test networks (e.g., 5-bus and 7-bus systems)
- **Cross-Validation:** Use PowerWorld’s solved voltages as inputs and compare Newton– Raphson results
- **Convergence Check:** Confirm that mismatch norm converges below tolerance
- **Jacobian Verification:** Ensure Jacobian dimensions match mismatch vector
---
### Final Check
- Solver correctly integrates mismatch vector and Jacobian
- Proper voltage and angle updates for each bus type
- Tolerance and iteration limits implemented
- Output includes final voltage magnitudes and angles per bus
- Compatible with PowerWorld results for validation
