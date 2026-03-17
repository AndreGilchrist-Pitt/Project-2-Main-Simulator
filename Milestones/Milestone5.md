## Milestone 5: Settings Class, Bus Refactoring, Generator & Load Classes

**Target Date: 3/4/26**

### Introduction

In Milestone 5, you will enhance the power system data model to prepare for full power flow analysis. This milestone introduces:

- **Settings class**: A system-wide `Settings` class for per-unit definitions
- **Bus refactoring**: Refactoring of the `Bus` class to include voltage state variables
- **Generator and Load refactoring**: Refactoring of the `Generator` and `Load` classes to model power injections

These changes transition the project from network topology modeling to numerical power flow formulation.

This milestone builds directly on:

- **Milestone 1**: Equipment classes
- **Milestone 3**: Primitive admittance matrices
- **Milestone 4**: Ybus assembly

### Reference Materials

- Module 10 – Per Unit System Lecture Notes and Video
- Module 11 – Power Flow Lecture Notes and Video

---

### 1. System Settings Class

**Objective:**  
Create a centralized class that defines system-wide per-unit parameters.

**Requirements:**

- Create a class named `Settings`.
- Define the following attributes:
  - `freq`: System frequency (default = 60 Hz)
  - `sbase`: System base apparent power (default = 100 MVA)
- Ensure default values are assigned during initialization.
- Ensure the object can be accessed throughout the system model.

This class establishes consistent per-unit scaling across all equipment.

---

### 2. Refactor Bus Class

**Objective:**  
Extend the `Bus` class to include voltage state variables and classification for power flow analysis.

**Add the following attributes:**

- `vpu`: Per-unit voltage magnitude (default = 1.0 p.u.)
- `delta`: Voltage phase angle in degrees (default = 0.0 degrees)
- `bus_type`: Bus classification

**Allowed bus types:**

- `Slack`
- `PQ`
- `PV`

**Implementation requirements:**

- Modify the constructor to initialize all new attributes.
- Enforce validation of `bus_type`.
- Raise an error if an invalid bus type is provided.

These attributes represent the state variables required for Newton–Raphson power flow.

---

### 3. Refactor Generator Class

**Objective:**  
Model real power injection at a bus.

**Add the following attribute:**

- `p`: Per-unit real power injection

**Add the following method:**

- `calc_p()`

The method should return the generator’s real power injection in per-unit form.

---

### 4. Refactor Load Class

**Objective:**  
Model real and reactive power consumption at a bus.

**Add the following attributes:**

- `p`: Per-unit real power consumption
- `q`: Per-unit reactive power consumption

**Add the following methods:**

- `calc_p()`
- `calc_q()`

These methods should return the load’s real and reactive power in per-unit form.

---

### Final Check

Before submission, ensure:

- The `Settings` class correctly initializes default system parameters.
- The `Bus` class enforces valid bus types.
- `Generator` and `Load` objects correctly store per-unit power values.
- All new classes integrate cleanly with the existing `Circuit` structure.
- No hard-coded assumptions conflict with future Newton–Raphson implementation.

By completing Milestone 5, you will establish the full data structure required for implementing the nonlinear power flow equations in the next milestone.

