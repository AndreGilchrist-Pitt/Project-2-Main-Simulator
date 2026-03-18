## Milestone 7: Jacobian Matrix

**Target Date: 3/19/2026**

### Introduction

This milestone develops the Jacobian matrix, which we will use in the Newton-Raphson
iterative solver in the next milestone. The matrix consists of partial derivatives of the
real and reactive power injection equations.
---
### Create Jacobian Class
#### Objective
- Develop a Jacobian Class with methods to calculate each quadrant of the Jacobian matrix.
#### Implementations Steps
1. **Define the Jacobian Matrix Structure**
The Jacobian matrix is a  
   $$
   (2N - 2 - N_{PV}) \times (2N - 2 - N_{PV})
   $$  
matrix, where $N$ is the total number of buses and $N_{PV}$ is the number of PV buses.
The matrix is constructed as follows:
- Remove the rows of $\Delta$P and $\Delta$Q, and the columns for $|V|$ corresponding
to the **slack bus**.
- Remove the row for $\Delta$Q and the column for $|V|$ corresponding to each **PV bus**.  
The remaining Jacobian is partitioned into four submatrices.  
$$
J = \begin{bmatrix} J_{1} & J_{2} \\ J_{3} & J_{4} \end{bmatrix} = \begin{bmatrix} \frac{\delta P}{\delta \delta} & \frac{\delta P}{\delta |V|} \\ \frac{\delta Q}{\delta \delta} & \frac{\delta Q}{\delta |V|} \end{bmatrix}
$$
2. **Implement the Jacobian Calculation Function**
- **Method:** `calculate_jacobian(buses,ybus,angles,voltages)`
    - Sub-methods compute $J_{1}$,$J_{2}$,$J_{3}$,$J_{4}$ using the current iteration angles and voltages.
    - Constructs the full Jacobian matrix **J**.
3. **Ensure Correct Handling of Bus Types**
- **PQ buses:** Include both real and reactive power derivatives.
- **PV buses:** Only include **real power derivatives** (ignore $Q$ derivatives).
- **Slack bus:** Excluded from calculations.
---
#### Validation and Testing
- Check matrix symmetry properties where applicable.
- Ensure compatibility with power mismatch calculations from Milestone 6.
    - The dimension of the Jacobian should match that of the Power Mismatch vector so that the matrix multiplication can be performed
- Verify Jacobian matrix correctness using small test cases
    - User PowerWorld to validate:
        - Ensure that your $Y_{bus}$ and the PowerWorld $Y_{bus}$ match.
        - Solve the system using PowerWorld to obtain final voltage angles and magnitudes
        - Use the PowerWorld final voltage angles and magnitudes as inputs to your Jacobian and compare against the PowerWorld Jacobian. These results should match.
---
#### Final Check
- Ensure the function correctly constructs $J_{1}$,$J_{2}$,$J_{3}$,$J_{4}$
- Validate handling of **PQ**,**PV**,and **Slack** buses.
- Confirm output format aligns with Newton-Raphson numerical solution requirements
This milestone sets the stage for the iterative Newton-Raphson power flow solver in the next phase.