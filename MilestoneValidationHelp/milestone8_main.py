"""
Milestone 8 validation: Newton–Raphson on the five-bus Glover-style network.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import numpy as np

from Src.Utils.Classes.bus import Bus
from Src.Utils.Classes.circuit import Circuit
from Src.Utils.Classes.settings import Settings
from Src.Utils.Classes.powerflow import PowerFlow

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

circuit.add_generator("G1", "Bus1", 1.0, 0.0)
circuit.add_generator("G2", "Bus3", 1.0, 520.0)

circuit.add_load("Load2", "Bus2", 800.0, 280.0)
circuit.add_load("Load3", "Bus3", 80.0, 40.0)

circuit.calc_ybus()

slack_vpu0 = circuit.buses["Bus1"].vpu
slack_delta0 = circuit.buses["Bus1"].delta
pv_vpu0 = circuit.buses["Bus3"].vpu

print("=== Milestone 8: Newton-Raphson ===\n")
print("Initial state:")
for b in circuit.buses.values():
    print(f"  {b.name}: vpu={b.vpu:.4f}, delta={b.delta:.4f} deg, type={b.bus_type}")

pf = PowerFlow()
pf.solve(circuit, tol=0.001, max_iter=50, verbose=True)

print()
if pf.converged:
    print(f"Converged in {pf.iterations} iterations (max|f| = {pf.final_mismatch_max:.6g} p.u.).")
else:
    print(
        f"Did not converge within iteration limit ({pf.iterations} iters, "
        f"max|f| = {pf.final_mismatch_max:.6g} p.u.)."
    )

print("\nFinal bus voltages (p.u.) and angles (deg):")
for b in circuit.buses.values():
    print(f"  {b.name}: vpu={b.vpu:.6f}, delta={b.delta:.6f}, type={b.bus_type}")
Voltages = circuit.voltage_vector_rectangular
f = circuit.compute_power_mismatch(circuit.buses, circuit.ybus, Voltages)
print("\n--- Verification ---")
f_final = pf.mismatch_vector(circuit)
#max_f = float(np.max(np.abs(f_final)))
max_f = float(np.max(np.abs(f)))
print(f"  max|f| after solve: {max_f:.6g} p.u.")

J = pf._jac.calculate_jacobian(
    circuit.buses, circuit.ybus, circuit.bus_angles(), circuit.bus_voltages()
)
print(f"  Jacobian shape: {J.shape}, mismatch length: {len(f_final)}")

ok = True
if J.shape[0] != len(f_final) or J.shape[1] != len(f_final):
    print("  FAIL: J dimensions do not match mismatch vector.")
    ok = False
if not pf.converged:
    print("  FAIL: solver did not report convergence.")
    ok = False
if max_f >= 0.001:
    print("  FAIL: residual mismatch not below tolerance.")
    ok = False
if abs(circuit.buses["Bus1"].vpu - slack_vpu0) > 1e-9 or abs(
    circuit.buses["Bus1"].delta - slack_delta0
) > 1e-9:
    print("  FAIL: slack bus voltage/angle changed.")
    ok = False
if abs(circuit.buses["Bus3"].vpu - pv_vpu0) > 1e-9:
    print("  FAIL: PV bus magnitude changed.")
    ok = False

if ok:
    print("  All checks passed.")
else:
    raise SystemExit(1)
