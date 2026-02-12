# Milestone 2: Creating the Circuit Class

**Target Completion Date:** 2/17/2026

## Overview

In Milestone 2, you will create the core `Circuit` class, which will serve as the container used to assemble a complete
power system network. The `Circuit` class will store and manage all equipment objects created in Milestone 1, and it
will provide a clean interface for building a network by adding buses, transformers, transmission lines, generators, and
loads.

At this stage, the `Circuit` class is primarily responsible for organizing data and enforcing consistent network
construction. Network stamping methods and power flow solution methods will be introduced in later milestones.

## Reference Materials

- Milestone 1: Equipment class definitions and required parameters
- Course notes and videos on Canvas related to network modeling workflow

## Circuit Class

The `Circuit` class represents the full network to be solved. It is responsible for storing each piece of equipment and
providing methods that allow users to build the network directly from the circuit object.

### Required Parameters

- `name`: str

### Required Attributes

All attributes other than `name` must be dictionaries. In each dictionary, the keys are component names (strings) and
the values are the corresponding objects.

- `name`: str
- `buses`: dict
- `transformers`: dict
- `transmission_lines`: dict
- `generators`: dict
- `loads`: dict

### Implementation Steps

1. Create a new file named `circuit.py` in the `Src/Utils/Classes/` directory.
2. Define the `Circuit` class.
3. Add an `__init__` method with parameter `name`.
4. Store `name` and initialize all equipment dictionaries as empty dictionaries.
5. Create an `add` method for each equipment model implemented in Milestone 1.

## Add Methods

Each add method must create an equipment object and store it in the appropriate dictionary.

### Required Add Methods

- `add_bus(name, nominal_kv)`
- `add_transformer(name, bus1_name, bus2_name, r, x)`
- `add_transmission_line(name, bus1_name, bus2_name, r, x, g, b)`
- `add_generator(name, bus1_name, voltage_setpoint, mw_setpoint)`
- `add_load(name, bus1_name, mw, mvar)`

### General Rules for Add Methods

- The component name must be used as the dictionary key.
- Each component name must be unique within its equipment type.
- If a duplicate name is added, raise a `ValueError` with a clear message.
- For now, equipment objects should store bus references using bus names (strings), consistent with Milestone 1.

## Validation of the Circuit Class

After implementing the `Circuit` class, verify functionality using a simple test script.

### Create an Instance of the Circuit Class
```python
from circuit import Circuit
circuit1 = Circuit("Test Circuit")
print(circuit1.name)  # Expected output: "Test Circuit"
print(type(circuit1.name))  # Expected output: <class 'str'>
```

### Check Attribute Initialization
```python
print(circuit1.buses)  # Expected output: {}
print(circuit1.transformers)  # Expected output: <class 'dict'>
print(circuit1.transmission_lines)  # Expected output: {}
print(circuit1.generators)  # Expected output: {}
print(circuit1.loads)  # Expected output: {}
```

### Add and Retrieve Equipment Components
```python
from circuit import Circuit

circuit1 = Circuit("Test_Circuit")
circuit1.add_bus("Bus_1" , 20.0 )
circuit1.add_bus("Bus_1" , 230.0)
print ( list(circuit1.buses.keys())) # Expected output:["Bus_1" ,"Bus_2"]
print (circuit1.buses["Bus_1"].name, circuit1.buses["Bus_1"].nominal kv 
```
### Add and Verify Transformer
```python
circuit1.add_transformer("T1", "Bus_1","Bus_2",0.1,0.10)
print(list(circuit1.transformers.keys())) # Expected output:["T1"]
print(circuit1.transformers["T1"].name,
      circuit1.transformers["T1"].bus1_name,
      circuit1.transformers["T1"].bus2_name,
      circuit1.transformers["T1"].r,
      circuit1.transformers["T1"].x)
```
### Add and Verify Transmission Line
```python
circuit1.add_transmission_line("Line_1", "Bus_1", "Bus_2", 0.02, 0.06, 0.0, 0.0)
print(list(circuit1.transmission_lines.keys())) # Expected output:["Line_1"]
print(circuit1.transmission_lines["Line_1"].name,
      circuit1.transmission_lines["Line_1"].bus1_name,
      circuit1.transmission_lines["Line_1"].bus2_name,
      circuit1.transmission_lines["Line_1"].r,
      circuit1.transmission_lines["Line_1"].x,
      circuit1.transmission_lines["Line_1"].b,
      circuit1.transmission_lines["Line_1"].charging_mvar)
```
### Add and Verify Load
```python
circuit1.add_load("Load_1","Bus_2",50.0,30.0)
print(list(circuit1.loads.keys())) # Expected output:["Load_1"]
print(circuit1.loads["Load_1"].name,
      circuit1.loads["Load_1"].bus_name,
      circuit1.loads["Load_1"].mw,
      circuit1.loads["Load_1"].mvar)
```
### Add and Verify Generator
```python
circuit1.add_generator("Gen_1","Bus_1",1.04,100.0)
print(list(circuit1.generators.keys())) # Expected output:["Gen_1"]
print(circuit1.generators["Gen_1"].name,
      circuit1.generators["Gen_1"].bus_name,
      circuit1.generators["Gen_1"].voltage_setpoint,
      circuit1.generators["Gen_1"].mw_setpoint)
```
### Deliverables and Assessment
All work for this milestone must be committed to the student's GitHub repository. Code should
be organized clearly and professionally within the repository.
Students are required to submit:
1. A Python file implementing the `Circuit` class.
    - Circuit
2. A short validation script demonstrating:
    - Circuit object creation
    - initialization of equipment dictionaries
    - adding and retrieving each equipment type
3. Written documentation describing:
    - the purpose of the `Circuit` class
    - how each add_ method works
    - how equipment objects are stored and retrieved
4. A class diagram illustrating the relationship between:
    - Circuit and each equipment class

### Assessment Method
Assessment will be conducted through an oral milestone review with the instructors. During this review, students must
be able to clearly and articulately explain:
- The purpose of the `Circuit` class
- The role of each dictionary attribute
- The logic of each add_ method
- The function of each line of code when prompted

Students are expected to demonstrate full ownership of their implementation.
They must understand and be able to explain every line of code included in their submission.
