# Milestone 3: Per-Unit Primitive Admittance Matrices

**Target Completion Date: 2/24/2026**

## Introduction

In Milestone 3, you will enhance the Transformer and TransmissionLine classes by implementing a new method for each class to compute the primitive admittance matrix, Yprim. These updates align with the industry-standard approach for modeling power systems and prepare your codebase for later construction of network matrices (e.g., Ybus) and power flow analysis.

**Important note:** In this course implementation, per-unit parameters are entered directly. You will not compute per-unit quantities from physical conductor or geometry data.

## Reference Materials

- Primitive Admittance Matrix, Module 8 lecture notes and video
- Transformer modeling section from the textbook
- Transmission line modeling section from the textbook

## What You Will Implement

### Transformer Class Updates

**Objective:** Using per-unit inputs r and x, compute the series admittance and implement `calc_yprim()`.

- Treat r and x as per-unit values entered directly by the user.
- Compute and store the series admittance:
  ```
  Yseries = 1 / (r + jx)
  ```
- Implement `calc_yprim()` to return the 2 × 2 primitive admittance matrix for a two-terminal series element.
- Return Yprim in a labeled `pandas.DataFrame` so each row/column is clearly associated with bus1_name and bus2_name.

### TransmissionLine Class Updates

**Objective:** Using per-unit inputs r, x, g, and b, compute the series and shunt admittances and implement `calc_yprim()`.

- Treat r, x, g, and b as per-unit values entered directly by the user.
- Compute and store the series admittance:
  ```
  Yseries = 1 / (r + jx)
  ```
- Compute and store the shunt admittance:
  ```
  Yshunt = g + jb
  ```
- Implement `calc_yprim()` to return the 2 × 2 primitive admittance matrix for the transmission line model used in this course.
- Return Yprim in a labeled `pandas.DataFrame` so each row/column is clearly associated with bus1_name and bus2_name.

## Validation of Refactored Classes

You must demonstrate correctness by instantiating each object and printing key computed values, followed by printing the computed primitive admittance matrix.

### Transformer Class Validation

Create an instance:
```python
transformer1 = Transformer("T1", "Bus 1", "Bus 2", 0.01, 0.10)
```

Check series admittance:
```python
print(transformer1.Yseries)
```

Verify the primitive admittance matrix:
```python
print(transformer1.calc_yprim())
```

### Transmission Line Class Validation

Create an instance:
```python
line1 = TransmissionLine("Line 1", "Bus 1", "Bus 2", 0.02, 0.25, 0.0, 0.04)
```

Check series and shunt admittances:
```python
print(line1.Yseries, line1.Yshunt)
```

Verify the primitive admittance matrix:
```python
print(line1.calc_yprim())
```

## Final Checks

Before you submit, verify the following:

- Transformer validation includes only Yseries and Yprim.
- Transmission line validation includes only Yseries, Yshunt, and Yprim.
- `calc_yprim()` correctly outputs a 2 × 2 admittance matrix for both devices.
- Your `pandas.DataFrame` output includes bus names as row/column labels for clarity.
- You ran multiple test cases (different transformers and different lines) and confirmed results are consistent and reasonable.

## Submission Requirements

All work for this milestone must be committed to your GitHub repository.

Students must submit:

1. Updated Python files implementing the refactored Transformer and TransmissionLine classes.
2. A short validation script that instantiates test objects and prints computed admittances and Yprim.
3. Clear, readable code with appropriate comments.
4. Generated documentation and class diagrams for each updated class.

## Assessment

For assessment, you will be required to talk through this milestone with the instructors. You are responsible for articulately describing each relevant line of code when prompted.
