from Src.Utils.Classes.bus import Bus
from Src.Utils.Classes.transformer import Transformer
from Src.Utils.Classes.transmissionLine import TransmissionLine
from Src.Utils.Classes.generator import Generator
from Src.Utils.Classes.load import Load
from Src.Utils.Classes.circuit import Circuit
from Src.Utils.Classes.settings import Settings

Bus._bus_counter = 0
Bus._bus_registry.clear()

Settings(freq=60.0, sbase=100.0)
circuit = Circuit("Milestone5 Five-Bus Glover Example 6.9")

circuit.add_bus("Bus1", 15.0, vpu=1.0, delta=0.0, bus_type="Slack")
circuit.add_bus("Bus2", 345.0, vpu=1.0, delta=0.0, bus_type="PQ")
circuit.add_bus("Bus3", 15.0, vpu=1.05, delta=0.0, bus_type="PV")
circuit.add_bus("Bus4", 345.0, vpu=1.0, delta=0.0, bus_type="PQ")
circuit.add_bus("Bus5", 345.0, vpu=1.0, delta=0.0, bus_type="PQ")

circuit.add_transformer("T1", "Bus1", "Bus5", 0.0015, 0.02)
circuit.add_transformer("T2", "Bus3", "Bus4", 0.00075, 0.01)

circuit.add_transmission_line("Line1", "Bus4", "Bus2", 0.009, 0.1, 0.0, 1.72)
circuit.add_transmission_line("Line2", "Bus5", "Bus2", 0.0045, 0.05, 0.0, 0.88)
circuit.add_transmission_line("Line3", "Bus5", "Bus4", 0.00225, 0.025, 0.0, 0.44)

circuit.add_generator("G1", "Bus1", 1.0, 0.0)
circuit.add_generator("G2", "Bus3", 1.0, 520.0)

circuit.add_load("Load2", "Bus2", 800.0, 280.0)
circuit.add_load("Load3", "Bus3", 80.0, 40.0)

circuit.calc_ybus()
print("\nCalculated Ybus Matrix:\n")
bus_names = list(circuit.buses.keys())
col_width = 22

print(f"{'':>{col_width}}", end="")
for name in bus_names:
    print(f"{name:>{col_width}}", end="")
print()

print("-" * (col_width * (len(bus_names) + 1)))

for i, row in enumerate(circuit.ybus):
    print(f"{bus_names[i]:>{col_width}}", end="")
    for val in row:
        if val == 0:
            print(f"{'0':>{col_width}}", end="")
        else:
            print(f"{val.real:+9.4f}{val.imag:+9.4f}j".rjust(col_width), end="")
    print()
print()
print(f"Voltage Vector Polar:\n{circuit.voltage_vector_polar}")
print(f"Voltage Vector Rectangular:\n{circuit.voltage_vector_rectangular}")
Voltages = circuit.voltage_vector_rectangular
P,Q = circuit.compute_power_injection(circuit.buses["Bus2"], circuit.ybus,voltages=Voltages)
print(f"Power injection at Bus2: {P} kW, {Q} kVar")
f = circuit.compute_power_mismatch(circuit.buses, circuit.ybus, Voltages)
print(f)