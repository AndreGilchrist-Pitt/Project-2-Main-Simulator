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

## Weekly/Check-In Log
| Date      | Milestone   | Progress Update                                                | Issues/Risks | Next Steps      | Owner |
|-----------|-------------|----------------------------------------------------------------|--------------|-----------------|----|
| 2/12/2026 | Milestone 1 | Finished checked by Collin<br/>would like JW review            | No issues    |                 | AG |
| 2/17/2026 | Milestone 1 | Created a new Milestone1 Branch to submit                      | No issues    |                 | AG |
| 2/17/2026 | Milestone 2 | Finished checked by Collin                                     | No issues    |                 | AG |
| 2/19/2026 | Milestone 3 | Misc Merges & Created Milestone 3/4 Info                       | No issues    | Update Classes  | AG |
| 2/22/2026 | Milestone 3 | Implemented calc_yprim for Transformer and TransmissionLine    | No issues    |  | JW |
| 2/23/2026 | Milestone 3 | Reviewed JW updates. Updated Yseries and Yshunt with @property | None         |  | AG |
| 2/24/2026 | Milestone 3 | Update to Milestone 3 and checked off by Dr. Kerestes          | None         |  | AG |
| 2/24/2026 | Milestone 4 | Update to Milestone 4 introduced calc_ybus                     | None         |  | AG |
## Change Log
| Date      | Change  | Reason                                                         | Approved By |
|-----------|---------|----------------------------------------------------------------|-------------|
| 2/12/2026 | e230a0d | Updated Completed Milestone1<br/>Merged to Main                | AG          |
| 2/12/2026 | a5a3186 | Created Milestone 2                                            | AG          |
| 2/12/2026 | a369a02 | Updated Milestone Tracker                                      | AG          |
| 2/12/2026 | 9aeb4c9 | Created Circuit class and supporting documents                 | AG          |
| 2/17/2026 | 5948e70 | Merged Circuit class Dev->Main                                 | AG          |
| 2/19/2026 | 4d0f49f | Update Milestone 3 & 4 Info and Tracker                        | AG          |
| 2/22/2026 | 5366793 | Implemented calc_yprim for Transformer and TransmissionLine    | JW          |
| 2/23/2026 | 0c0567e | Reviewed JW updates. Updated Yseries and Yshunt with @property | AG          |
| 2/24/2026 | f386dec | Update to Milestone 3 Yseries and Yshunt                       | AG          |
| 2/24/2026 | d3510ea | Update to Milestone 4 calc_bus                                 | AG          |
| 2/26/2026 | 2b7c650 | Update to Milestone 4 calc_bus                                 | AG          |
