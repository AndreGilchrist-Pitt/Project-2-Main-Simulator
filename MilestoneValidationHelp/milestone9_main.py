import sys
from pathlib import Path

#power flow and fault study

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import numpy as np

from Src.Utils.Classes.bus import Bus
from Src.Utils.Classes.circuit import Circuit
from Src.Utils.Classes.settings import Settings
from Src.Utils.Classes.powerflow import PowerFlow
from Src.Utils.Classes.solver import Solver
Bus._bus_counter = 0
Bus._bus_registry.clear()

Settings(freq=60.0, sbase=100.0)
circuit = Circuit("Milestone 8 — Five-Bus NR (Glover-style)")

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

circuit.add_generator("G1", "Bus1", 1.04, 0.0, x_subtransient=0.045)
circuit.add_generator("G2", "Bus3", 1.025, 520.0, x_subtransient=0.0225)
#circuit.add_generator("G1", "Bus1", 1.0, 0.0)
#circuit.add_generator("G2", "Bus3", 1.0, 520.0)

circuit.add_load("Load2", "Bus2", 800.0, 280.0)
circuit.add_load("Load3", "Bus3", 80.0, 40.0)

circuit.calc_ybus()

print("\n\nPOWER FLOW (Solver mode: power_flow)\n\n")

pf_solver = Solver(mode="power_flow")
pf_solver.run(circuit, tol=1e-4, verbose=True)
print(f"Converged: {pf_solver.converged} in {pf_solver.iterations} iterations")

print("\n\nBus voltage (p.u.) and angle (deg):\n\n")
for b in circuit.buses.values():
    print(f"  {b.name}: vpu {b.vpu:.6f}, delta {b.delta:.6f}, type {b.bus_type}")

_fault_bus = "Bus1"
_fault_v = 1.05
print(
    f"\n\nFAULT STUDY (Solver mode: fault). "
    f"Faulted bus: {_fault_bus}. V_pref {_fault_v} pu\n"
)

fault_solver = Solver(mode="fault")
fault_solver.run(circuit, faulted_bus_name=_fault_bus, prefault_voltage=_fault_v)

print(f"\nFault current magnitude: {abs(fault_solver.fault_current):.4f} pu")
print("\nPost-fault bus voltage magnitudes (pu):\n")
for name, v in fault_solver.fault_voltages.items():
    print(f"  {name}: {abs(v):.4f} pu")

ybus_fault = circuit.calc_ybus_fault()
zbus = circuit.calc_zbus(ybus_fault)

print("\n\nZbus diagonal (imaginary part):\n\n")
for i, name in enumerate(circuit.buses):
    z_nn = zbus[i, i].imag
    i_fault = _fault_v / z_nn
    print(f"  {name}: Z_nn {z_nn:.7f} pu   I_fault {i_fault:.4f} pu")
print("\n")