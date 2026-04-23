# Milestones Tracker

Project: 
Owner: 
Start Date: 
Target Completion: 

## Milestones Overview
- [x] Milestone 1: Creating Equipment Classes
  - Target Date: 2/12/2026
  - Status: Finished, Checked by Collin
- [x] Milestone 2: Creating the Circuit Class
  - Target Date: 2/17/2026
  - Status: Finished
- [x] Milestone 3: Per-Unit Primitive Admittance Matrices
  - Target Date: 2/24/2026
  - Status: Finished, checked by Dr. Kerestes
- [x] Milestone 4: Ybus Admittance Matrix
  - Target Date: 3/1/2026
  - Status: Finished, checked by Dr. Kerestes
- [x] Milestone 5: Settings Class, Bus Refactoring,  Generator & Load Classes
  - Target Date: 3/4/2026
  - Status: Finished, waiting for check
- [x] Milestone 7: Jacobian Matrix
  - Target Date: 3/19/2026
  - Status: Implemented (`Jacobian`, `milestone7_main.py`)
- [x] Milestone 8: Newton–Raphson Power Flow
  - Target Date: 3/26/2026
  - Status: Implemented (`PowerFlow`, `milestone8_main.py`; docs `Milestone8.md`)
- [x] Milestone 9:
  - Target Date: 4/8/2026
  - Status:Finished, checked by Collin

## Milestone Details
### Milestone 1: Creating Equipment Classes
- [x] Bus
- [x] Transformer
- [x] Transmission Line
- [x] Load
- [x] Generator

### Bus Class

| Date      | Milestone   | Progress Update | Issues/Risks | Next Steps | Owner |
|-----------|-------------|-----------------|--------------|------------|-------|
| 2/12/2026 | Milestone 1 | Finished checked by Collin | No issues |  | AG |

### Transformer Class

| Date      | Milestone   | Progress Update | Issues/Risks | Next Steps | Owner |
|-----------|-------------|-----------------|--------------|------------|-------|
| 2/12/2026 | Milestone 1 | Finished checked by Collin | No issues |  | AG |

### Transmission Line Class

| Date      | Milestone   | Progress Update | Issues/Risks | Next Steps | Owner |
|-----------|-------------|-----------------|--------------|------------|-------|
| 2/12/2026 | Milestone 1 | Finished checked by Collin | No issues |  | AG |

### Load Class

| Date      | Milestone   | Progress Update | Issues/Risks | Next Steps | Owner |
|-----------|-------------|-----------------|--------------|------------|-------|
| 2/12/2026 | Milestone 1 | Finished checked by Collin | No issues |  | AG |

### Generator Class

| Date      | Milestone   | Progress Update | Issues/Risks | Next Steps | Owner |
|-----------|-------------|-----------------|--------------|------------|-------|
| 2/12/2026 | Milestone 1 | Finished checked by Collin | No issues |  | AG |

### Milestone 2: Creating the Circuit Class
- [x] Circuit

### Circuit Class

| Date      | Milestone   | Progress Update | Issues/Risks | Next Steps | Owner |
|-----------|-------------|-----------------|--------------|------------|-------|
| 2/17/2026 | Milestone 2 | Finished checked by Collin | No issues |  | AG |
Comments/Notes:
- Scope: Implement Bus, Transformer, TransmissionLine, Load, Generator classes as data containers.
- Deliverables: Python class files, validation script, documentation, class diagrams.
- Validation: simple object creation test cases for each class.
- Assessment: oral review covering purpose, attributes, and line-by-line understanding.

### Milestone 3: Per-Unit Primitive Admittance Matrices
- [x] Transformer Class Updates
- [x] TransmissionLine Class Updates

### Transformer Class

| Date      | Milestone   | Progress Update | Issues/Risks | Next Steps | Owner |
|-----------|-------------|-----------------|--------------|------------|-------|
| 2/22/2026 | Milestone 3 | Yseries stored; calc_yprim() returns 2×2 pandas.DataFrame with bus labels | No issues |  | AG |

### Transmission Line Class

| Date      | Milestone   | Progress Update | Issues/Risks | Next Steps | Owner |
|-----------|-------------|-----------------|--------------|------------|-------|
| 2/22/2026 | Milestone 3 | Yseries, Yshunt stored; calc_yprim() returns 2×2 pandas.DataFrame with bus labels (pi-model) | No issues |  | AG |

Comments/Notes:
- Scope: Implement calc_yprim for Transformer and TransmissionLine; compute and store Yseries (and Yshunt for lines).
- Deliverables: Updated Python class files, validation script, documentation, class diagrams.
- Validation: Yseries/Yshunt and calc_yprim() output per Milestone 3 spec.

### Milestone 4: Ybus Admittance Matrix

- [x] Extending the Circuit Class

| Date      | Milestone   | Progress Update | Issues/Risks | Next Steps | Owner |
|-----------|-------------|-----------------|--------------|------------|-------|
| 2/26/2026 | Milestone 4 | calc_ybus       | No issues | JW Review  | AG |

### Milestone 5:  Settings Class, Bus Refactoring, Generator & Load Classes

- [x] System Settings Class
- [x] Refactor Bus Class
- [x] Refactor Generator Class
- [x] Refactor Load Class

### Milestone 6:  Power Injection Equations and Newton-Raphson Initialization

- [x] Define Power Injection Equations
- [x] Implement Real and Reactive Power Calcuations
- [x] Validation


| Date      | Milestone   | Progress Update   | Issues/Risks               | Next Steps                 | Owner |
|-----------|-------------|-------------------|----------------------------|----------------------------|-------|
| 3/13/2026 | Milestone 6 | Initial Update    |  | Validation needs completed | AG    |
| 3/17/2026 | Milestone 6 | Updated Functions |  | JW Review                  | AG    |

### Milestone 7: Jacobian Matrix

- [x] `Jacobian` class (`Src/Utils/Classes/jacobian.py`)
- [x] `calculate_jacobian(buses, ybus, angles, voltages)` — J1–J4, full **J**
- [x] `MilestoneValidationHelp/milestone7_main.py` — five-bus demo

| Date      | Milestone   | Progress Update | Issues/Risks | Next Steps | Owner |
|-----------|-------------|-----------------|--------------|------------|-------|
| —         | Milestone 7 | Jacobian + milestone7_main | — | — | — |

### Milestone 8: Newton–Raphson Power Flow

- [x] `PowerFlow` (`Src/Utils/Classes/powerflow.py`)
- [x] `solve(circuit, tol, max_iter, verbose)` — NR loop, **J·Δx = f**, bus-type updates
- [x] `mismatch_vector(circuit)` — residual **f** for verification
- [x] `MilestoneValidationHelp/milestone8_main.py` — five-bus validation + automated checks
- [x] `Milestones/Milestone8.md` — implementation notes, run instructions, API table

| Date      | Milestone   | Progress Update | Issues/Risks | Next Steps | Owner |
|-----------|-------------|-----------------|--------------|------------|-------|
| 3/23/2026 | Milestone 8 | PowerFlow, milestone8_main, Milestone8.md, `.gitignore` (`.vscode/`) | — | Instructor review / PowerWorld optional | — |

## Milestone 9:

- [x] Update Solution Framework
- [x] Refactor Generator Class
- [x] Modify Ybus for Fault Conditions
- [x] Construct Zbus Matrix
- [x] Calculate Fault Current
- [x] Calculate Bus Voltages

| Date      | Milestone   | Progress Update                                    | Issues/Risks | Next Steps | Owner |
|-----------|-------------|----------------------------------------------------|--------------|------------|-------|
| 4/7/2026  | Milestone 9 | Generator/circuit/solver class updates             | — | JW review  | AG    |
| 4/19/2026 | Milestone 9 | Update to faulted ybus                             | — | JW review  | AG    |
| 4/21/2026  | Milestone 9 | Update to milestone9_main.py,circuit,classDiagrams | — | JW review  | AG    |

## Weekly/Check-In Log
| Date      | Milestone       | Progress Update                                                                                 | Issues/Risks | Next Steps      | Owner |
|-----------|-----------------|-------------------------------------------------------------------------------------------------|--------------|-----------------|-------|
| 2/12/2026 | Milestone 1     | Finished checked by Collin<br/>would like JW review                                             | No issues    |                 | AG    |
| 2/17/2026 | Milestone 1     | Created a new Milestone1 Branch to submit                                                       | No issues    |                 | AG    |
| 2/17/2026 | Milestone 2     | Finished checked by Collin                                                                      | No issues    |                 | AG    |
| 2/19/2026 | Milestone 3     | Misc Merges & Created Milestone 3/4 Info                                                        | No issues    | Update Classes  | AG    |
| 2/22/2026 | Milestone 3     | Implemented calc_yprim for Transformer and TransmissionLine                                     | No issues    |  | JW    |
| 2/23/2026 | Milestone 3     | Reviewed JW updates. Updated Yseries and Yshunt with @property                                  | None         |  | AG    |
| 2/24/2026 | Milestone 3     | Update to Milestone 3 and checked off by Dr. Kerestes                                           | None         |  | AG    |
| 2/24/2026 | Milestone 4     | Update to Milestone 4 introduced calc_ybus                                                      | None         |  | AG    |
| 3/5/2026  | Misc            | Per Dr. Kerestes (update to include a main)                                                     | None         |  | AG    |
| 3/6/2026  | Milestone 5     | Big updates for milestone 5                                                                     | None         |  | AG    |
| 3/13/2026 | Milestone 6     | Initial Milestone 6                                                                             | None         |  | AG    |
| 3/17/2026 | Milestone 5 & 6 | Updated Milestone 5 (Merged to Main and Milestone5 branch) and 6. Settings Class was refactored | None         |  | AG    |
| 3/23/2026 | Milestone 8     | Newton–Raphson: `PowerFlow`, `milestone8_main.py`, updated `Milestone8.md` & tracker            | None | Push to `Development` | —     |
| 4/23/2026 | Milestone 9     | Finished Milestone 9                                                                            | None |  | AG    |
## Change Log
| Date      | Change  | Reason                                                                                                                | Approved By |
|-----------|---------|-----------------------------------------------------------------------------------------------------------------------|-------------|
| 2/12/2026 | e230a0d | Updated Completed Milestone1<br/>Merged to Main                                                                       | AG          |
| 2/12/2026 | a5a3186 | Created Milestone 2                                                                                                   | AG          |
| 2/12/2026 | a369a02 | Updated Milestone Tracker                                                                                             | AG          |
| 2/12/2026 | 9aeb4c9 | Created Circuit class and supporting documents                                                                        | AG          |
| 2/17/2026 | 5948e70 | Merged Circuit class Dev->Main                                                                                        | AG          |
| 2/19/2026 | 4d0f49f | Update Milestone 3 & 4 Info and Tracker                                                                               | AG          |
| 2/22/2026 | 5366793 | Implemented calc_yprim for Transformer and TransmissionLine                                                           | JW          |
| 2/23/2026 | 0c0567e | Reviewed JW updates. Updated Yseries and Yshunt with @property                                                        | AG          |
| 2/24/2026 | f386dec | Update to Milestone 3 Yseries and Yshunt                                                                              | AG          |
| 2/24/2026 | d3510ea | Update to Milestone 4 calc_bus                                                                                        | AG          |
| 2/26/2026 | 2b7c650 | Update to Milestone 4 calc_bus                                                                                        | AG          |
| 3/5/2026  | f831176 | Update to include main.py                                                                                             | AG          |
| 3/6/2026  | 67851cc | Updates for milestone 5                                                                                               | AG          |
| 3/13/2026 | 8c2617b | Updates for milestone 6                                                                                               | AG          |
| 3/17/2026 | 5bead86 | Updates for milestone 5 settings class and Milestone 6                                                                | AG          |
| 3/23/2026 | —       | Milestone 8: PowerFlow, milestone8_main, Milestone8.md; tracker (M7+M8 sections, weekly log); `.gitignore` `.vscode/` | —           |
| 4/7/2026  | 16a026c | Milestone 9: Generator/Circuit/Solver Class updates                                                                   | AG          |
| 4/7/2026  | f36b9d6 | Updated to faulted ybus ( dont reuse ybus from prior runs)                                                                   | AG          |
| 4/7/2026  | 3a9b4de | update to milestone 9                                                                  | AG          |
| 4/7/2026  | 715d55b | Update powerflow.py                                                                   | AG          |
