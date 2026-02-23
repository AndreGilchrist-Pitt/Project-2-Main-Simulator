# Project Milestones

This file tracks milestones and the work items needed to complete them.

## Milestone 1: Creating Equipment Classes

### Overview
Create the core equipment classes used to represent a power system network. These
classes serve as data containers in this milestone and will later be extended with
network stamping methods and primitive admittance matrices.

### Required Classes
- Bus
- Transformer
- TransmissionLine
- Load
- Generator

### Reference Materials
- Transformer modeling sections 3.1-3.5 in textbook
- Transmission line modeling sections 4.2, 4.6, and 4.10
- Transformer and Transmission Line videos on Canvas

### Bus Class
Required parameters:
- name: str
- nominal_kv: float

Required attributes:
- name
- nominal_kv
- bus_index: int (class-level counter; each Bus instance gets a unique index)

Implementation steps:
1. Define the Bus class.
2. Add an __init__ method with parameters name and nominal_kv.
3. Store these attributes.
4. Use a class-level counter to assign a unique bus_index.

### Transformer Class
Required parameters:
- name: str
- bus1_name: str
- bus2_name: str
- r: float
- x: float

Required attributes:
- name
- bus1_name
- bus2_name
- r
- x

Note: No impedance calculations or primitive admittance matrices are required in
this milestone.

### TransmissionLine Class
Required parameters:
- name: str
- bus1_name: str
- bus2_name: str
- r: float
- x: float
- g: float
- b: float

Required attributes:
- name
- bus1_name
- bus2_name
- r
- x
- g
- b

### Load Class
Required parameters:
- name: str
- bus1_name: str
- mw: float
- mvar: float

Required attributes:
- name
- bus1_name
- mw
- mvar

### Generator Class
Required parameters:
- name: str
- bus1_name: str
- voltage_setpoint: float
- mw_setpoint: float

Required attributes:
- name
- bus1_name
- voltage_setpoint
- mw_setpoint

### Validation (Simple Test Cases)
Bus:
```
bus1 = Bus("Bus 1", 20.0)
bus2 = Bus("Bus 2", 230.0)
print(bus1.name, bus1.nominal_kv, bus1.bus_index)
print(bus2.name, bus2.nominal_kv, bus2.bus_index)
```

Transformer:
```
t1 = Transformer("T1", "Bus 1", "Bus 2", 0.01, 0.10)
print(t1.name, t1.bus1_name, t1.bus2_name, t1.r, t1.x)
```

Transmission line:
```
line1 = TransmissionLine("Line 1", "Bus 1", "Bus 2", 0.02, 0.25, 0.0, 0.04)
print(line1.name, line1.bus1_name, line1.bus2_name, line1.r, line1.x, line1.g, line1.b)
```

Load:
```
load1 = Load("Load 1", "Bus 2", 50.0, 30.0)
print(load1.name, load1.bus1_name, load1.mw, load1.mvar)
```

Generator:
```
gen1 = Generator("G1", "Bus 1", 1.04, 100.0)
print(gen1.name, gen1.bus1_name, gen1.voltage_setpoint, gen1.mw_setpoint)
```

### Deliverables
1. Python files implementing the five classes.
2. A short validation script demonstrating object creation and verification of class
   attributes.
3. Written documentation describing the purpose and structure of each class.
4. Class diagrams illustrating relationships between the implemented classes.

### Assessment Method
An oral milestone review with the instructors. Be prepared to explain:
- The purpose of each class
- The role of every attribute
- The reasoning behind implementation choices
- The function of each line of code when prompted

## Tracking These Items

Use one MilestonesTracker to keep track of milestone work

