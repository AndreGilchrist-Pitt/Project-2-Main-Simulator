# Milestone 4: Ybus Admittance Matrix

**Target Date: 3/1/26**

## Introduction

In Milestone 4, you will extend the Circuit class to compute the full system-wide Ybus matrix by:

- Adding a ybus attribute to the Circuit class
- Implementing a `calc_ybus()` method

The Ybus matrix (nodal admittance matrix) is the mathematical foundation of power flow analysis. It captures all electrical interconnections between buses through transformers and transmission lines.

This milestone builds directly on:

- Primitive admittance matrices developed in Milestone 3
- Proper equipment connectivity (Bus, Transformer, TransmissionLine)

## Reference Materials

- Module 10 – Ybus Lecture Notes and Video
- Module 11 – PowerWorld Modeling Lecture Notes and Video
- Section 2.4 of the textbook
- Case 6.9 (Five-Bus System) from Power System Analysis and Design by Glover, Sarma, and Overbye

## Extending the Circuit Class

**Objective:**

Develop the `calc_ybus()` method to construct the Ybus matrix by assembling and summing the primitive admittance matrices of:

- Transformers
- Transmission Lines

This method should:

- Not return a value
- Update the `self.ybus` attribute directly

## Steps to Implement

### 1. Initialize the Ybus Matrix

- Let N be the number of buses in the circuit.
- Initialize Ybus as an N × N complex zero matrix.

### 2. Establish Bus Index Mapping

- Create a consistent mapping between bus names and matrix indices.
- This mapping must remain fixed throughout the calculation.

### 3. Iterate Through All Power Delivery Elements

For each transformer and transmission line:

- Retrieve its primitive admittance matrix (Yprim).
- Identify the connected buses.
- Determine the corresponding indices in Ybus.

### 4. Stamp the Primitive Matrix into Ybus

- Add self-admittances to diagonal entries.
- Add mutual admittances to off-diagonal entries (negative coupling terms).
- Carefully accumulate values, do not overwrite existing entries.

### 5. Numerical Consistency Checks

- Verify that every connected bus has a nonzero diagonal entry.
- Confirm symmetry of Ybus for passive networks.
- Ensure no indexing errors occur.

### 6. Store the Result

- Assign the final matrix to `self.ybus`.

## Validation of Ybus

You must validate your implementation using two independent methods:

### 1. Validation with PowerWorld

- Construct the system from Milestone 3 in PowerWorld.
- Generate the Ybus matrix in PowerWorld.
- Run `calc_ybus()` in Python.
- Verify that both matrices match exactly (numerically and structurally).

### 2. Validation with Glover and Sarma Case 6.9

- Implement the five-bus system from Case 6.9.
- Construct the network using your equipment classes.
- Compute Ybus using your method.
- Verify that your result matches the published Ybus matrix.

Both validations are required for full credit.

## Final Check

Before submission, ensure:

- All equipment correctly stamps into Ybus.
- The matrix dimensions are correct.
- Results match PowerWorld.
- Results match Case 6.9.
- The method runs without errors on multiple test systems.

By completing Milestone 4, you will have successfully implemented system-wide nodal admittance assembly, forming the foundation for the Newton–Raphson power flow solver in the next milestone.
