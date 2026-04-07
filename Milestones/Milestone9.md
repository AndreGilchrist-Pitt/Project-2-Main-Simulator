## Milestone 9: Symmetrical Faults

**Target Date:** 4/8/2026

### Introduction

This milestone extends the power system analysis framework to include
symmetrical fault analysis (three-phase faults). Students will refactor their
existing solver to support both power flow and fault analysis modes,
update generator modeling to account for subtransient reactance, and
calculate fault currents and post-fault bus voltages using the Zbus matrix
derived from Ybus.
---
### Reference Materials
- **Symmetrical Fault** - Module 16 Lecture Notes and Video
---
### Update Solution Class with Fault Study
**Objective:**
- Enhance the solution framework to perform symmetrical fault analysis by adding fault mode functionality, updating generator models, construction Zbus from Ybus, and calculating fault current and resulting bus voltages.
### Implementation Steps
1. **Update Solution Framework:**  
- Modify your main Solver class to support two analysis modes:
    - Power Flow - Use existing Newton-Raphson solver
    - Fault Study - Perform symmetrical fault analysis
2. **Refactor Generator Class:**
    - Update your `Generator` class to include subtransient reactance  

3. **Modify Ybus for Fault Conditions:**  
- When a fault occurs at a bus, modify the system's admittance matrix accordingly. Include the generator
reactances and their respective admittances in Ybus calculations  
4. **Construct Zbus Matrix:**  
Invert the faulted Ybus to calculate Zbus under faulted condition
5. **Calculate Fault Current:**
For a bolted fault at bus `n`:  
- Assume defualt or choose prefault voltage
- Calculate the fault current
6. **Calculate Bus Voltages:**  
- Calculate the bus voltage at each bus in the system
---
### Validation and Testing
- **Compare with PowerWorld:** Validate fault current magnitude and post-fault voltages
against PowerWorld simulations.
- **Manual Verification:** Use textbook examples or simple systems to verify fault current calculations.
- **Bus Handling:** Confirm that faulted bus voltage becomes zero for bolted faults, and all other voltages update correctly.
---
### Final Check
- Solver class accepts both `power_flow` and `fault` modes
- Generator class includes subtransient reactance X"X"X"
- Correct Ybus modification for faulted conditions
- Zbus correctly calculated from Ybus
- Fault current and post-fault bus voltages calculated accurately
- Results validated against PowerWorld or textbook examples

    