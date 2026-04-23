from Src.Utils.Classes.bus import Bus
from Src.Utils.Classes.transformer import Transformer
from Src.Utils.Classes.transmissionLine import TransmissionLine
from Src.Utils.Classes.generator import Generator
from Src.Utils.Classes.load import Load
from Src.Utils.Classes.circuit import Circuit
from Src.Utils.Classes.settings import Settings
from Src.Utils.Classes.jacobian import Jacobian
from Src.Utils.Classes.powerflow import PowerFlow
from Paths.paths import MILESTONE_VALIDATION_HELP_DIR
import numpy as np

'''
Temporary Main 
For milestone validation, go to:
  {MILESTONE_VALIDATION_HELP_DIR}
'''
print("\nFor milestone validation, go to:")
print(f"  {MILESTONE_VALIDATION_HELP_DIR}")


# ─────────────────────────────────────────────
#  Helpers
# ─────────────────────────────────────────────

def _reset():
    """Reset the Bus class-level state between demo sections."""
    Bus._bus_counter = 0
    Bus._bus_registry.clear()


def _print_ybus(circuit):
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


def _print_matrix(title, M, bus_names, part="imag"):
    print(f"\n{title}")
    header = "        " + "  ".join(f"{n:>10}" for n in bus_names)
    print(header)
    for i, name in enumerate(bus_names):
        cells = []
        for j in range(len(bus_names)):
            z = M[i, j]
            if part == "imag":
                cells.append(f"{z.imag:+10.5f}j")
            elif part == "real":
                cells.append(f"{z.real:+10.5f}")
            else:
                cells.append(f"{z.real:+.4f}{z.imag:+.4f}j")
        print(f"{name:>6}  " + "  ".join(cells))


def _build_base_circuit(name, g2_vpu=1.0, g1_xsub=0.0, g2_xsub=0.0):
    """
    Build the standard five-bus Glover circuit.
    Optional args allow milestone-specific parameter variations.
    """
    _reset()
    Settings(freq=60.0, sbase=100.0)
    c = Circuit(name)

    c.add_bus("Bus1", 15.0, vpu=1.0, delta=0.0, bus_type="Slack")
    c.add_bus("Bus2", 345.0, vpu=1.0, delta=0.0, bus_type="PQ")
    c.add_bus("Bus3", 15.0, vpu=g2_vpu, delta=0.0, bus_type="PV")
    c.add_bus("Bus4", 345.0, vpu=1.0, delta=0.0, bus_type="PQ")
    c.add_bus("Bus5", 345.0, vpu=1.0, delta=0.0, bus_type="PQ")

    c.add_transformer("T1", "Bus1", "Bus5", 0.0015, 0.02)
    c.add_transformer("T2", "Bus3", "Bus4", 0.00075, 0.01)

    c.add_transmission_line("Line1", "Bus4", "Bus2", 0.009, 0.1, 0.0, 1.72)
    c.add_transmission_line("Line2", "Bus5", "Bus2", 0.0045, 0.05, 0.0, 0.88)
    c.add_transmission_line("Line3", "Bus5", "Bus4", 0.00225, 0.025, 0.0, 0.44)

    c.add_generator("G1", "Bus1", 1.0, 0.0, x_subtransient=g1_xsub)
    c.add_generator("G2", "Bus3", 1.0, 520.0, x_subtransient=g2_xsub)

    c.add_load("Load2", "Bus2", 800.0, 280.0)
    c.add_load("Load3", "Bus3", 80.0, 40.0)

    return c


# ─────────────────────────────────────────────
#  Milestone 4 — Ybus Assembly
# ─────────────────────────────────────────────

def demo_milestone4():
    print("=" * 60)
    print("  MILESTONE 4 — Ybus Assembly")
    print("=" * 60)

    c = _build_base_circuit("M4 — Five-Bus Glover")
    c.calc_ybus()

    print("\nCalculated Ybus Matrix:")
    _print_ybus(c)
    print()


# ─────────────────────────────────────────────
#  Milestone 5 — Bus Types & Settings
# ─────────────────────────────────────────────

def demo_milestone5():
    print("=" * 60)
    print("  MILESTONE 5 — Bus Types & Settings")
    print("=" * 60)

    c = _build_base_circuit("M5 — Five-Bus Glover")
    c.calc_ybus()

    print(f"\nCircuit : {c.name}")
    print(f"Settings: {Settings}\n")
    print("Bus summary:")
    for bus in c.buses.values():
        print(f"  {bus.name}: nominal_kv={bus.nominal_kv} kV, "
              f"vpu={bus.vpu:.4f}, delta={bus.delta:.4f}°, type={bus.bus_type}")
    print()


# ─────────────────────────────────────────────
#  Milestone 6 — Power Injections & Mismatch
# ─────────────────────────────────────────────

def demo_milestone6():
    print("=" * 60)
    print("  MILESTONE 6 — Power Injections & Mismatch Vector")
    print("=" * 60)

    c = _build_base_circuit("M6 — Five-Bus Glover", g2_vpu=1.05)
    c.calc_ybus()

    V = c.voltage_vector_rectangular
    print(f"\nVoltage vector (polar):       {c.voltage_vector_polar}")
    print(f"Voltage vector (rectangular): {V}\n")

    P, Q = c.compute_power_injection(c.buses["Bus2"], c.ybus, V)
    print(f"Power injection at Bus2:  P = {P:.6f} pu,  Q = {Q:.6f} pu")

    f = c.compute_power_mismatch(c.buses, c.ybus, V)
    print(f"\nInitial mismatch vector f:\n  {f}\n")


# ─────────────────────────────────────────────
#  Milestone 7 — Jacobian
# ─────────────────────────────────────────────

def demo_milestone7():
    print("=" * 60)
    print("  MILESTONE 7 — Jacobian Matrix")
    print("=" * 60)

    c = _build_base_circuit("M7 — Five-Bus Glover", g2_vpu=1.05)
    c.calc_ybus()

    angles = c.bus_angles()
    voltages = c.bus_voltages()
    J = Jacobian().calculate_jacobian(c.buses, c.ybus, angles, voltages)

    print(f"\nJacobian shape: {J.shape}")
    print(f"Jacobian matrix (initial flat-start):\n{np.round(J, 4)}\n")


# ─────────────────────────────────────────────
#  Milestone 8 — Newton-Raphson Power Flow
# ─────────────────────────────────────────────

def demo_milestone8():
    print("=" * 60)
    print("  MILESTONE 8 — Newton-Raphson Power Flow")
    print("=" * 60)

    c = _build_base_circuit("M8 — Five-Bus Glover NR", g2_vpu=1.05)
    c.calc_ybus()

    slack_vpu0 = c.buses["Bus1"].vpu
    slack_delta0 = c.buses["Bus1"].delta
    pv_vpu0 = c.buses["Bus3"].vpu

    print("\nInitial bus state:")
    for b in c.buses.values():
        print(f"  {b.name}: vpu={b.vpu:.4f}, delta={b.delta:.4f}°, type={b.bus_type}")

    pf = PowerFlow()
    pf.solve(c, tol=0.001, max_iter=50, verbose=True)

    print()
    if pf.converged:
        print(f"  Converged in {pf.iterations} iterations  "
              f"(max|f| = {pf.final_mismatch_max:.6g} pu)")
    else:
        print(f"  Did NOT converge ({pf.iterations} iters, "
              f"max|f| = {pf.final_mismatch_max:.6g} pu)")

    print("\nFinal bus voltages:")
    for b in c.buses.values():
        print(f"  {b.name}: vpu={b.vpu:.6f}, delta={b.delta:.6f}°, type={b.bus_type}")

    # Verification checks
    f_final = pf.mismatch_vector(c)
    max_f = float(np.max(np.abs(f_final)))
    J = pf._jac.calculate_jacobian(c.buses, c.ybus, c.bus_angles(), c.bus_voltages())
    ok = True

    print("\nVerification:")
    checks = {
        "J dimensions match mismatch vector": J.shape == (len(f_final), len(f_final)),
        "Solver reports convergence": pf.converged,
        "Residual below tolerance (0.001)": max_f < 0.001,
        "Slack bus unchanged": (abs(c.buses["Bus1"].vpu - slack_vpu0) < 1e-9
                                and abs(c.buses["Bus1"].delta - slack_delta0) < 1e-9),
        "PV bus |V| unchanged": abs(c.buses["Bus3"].vpu - pv_vpu0) < 1e-9,
    }
    for label, passed in checks.items():
        status = "PASS" if passed else "FAIL"
        print(f"  [{status}] {label}")
        if not passed:
            ok = False

    print(f"\n  {'All checks passed.' if ok else 'Some checks FAILED.'}\n")


# ─────────────────────────────────────────────
#  Milestone 9 — Fault Analysis
# ─────────────────────────────────────────────

def demo_milestone9():
    print("=" * 60)
    print("  MILESTONE 9 — Symmetrical Fault Analysis")
    print("=" * 60)

    c = _build_base_circuit(
        "M9 — Five-Bus Fault Study",
        g2_vpu=1.05,
        g1_xsub=0.045,
        g2_xsub=0.0225,
    )
    # Override generator voltage setpoints to match milestone 9 values
    c.generators["G1"].voltage_setpoint = 1.04
    c.generators["G2"].voltage_setpoint = 1.025

    c.calc_ybus()
    bus_names = list(c.buses)

    # Power flow first
    pf = c.solve(mode="power_flow", tol=1e-4, verbose=True)
    print(f"\n  Power flow: converged={pf.converged}, iterations={pf.iterations}\n")

    # Ybus_fault and Zbus
    ybus_fault = c.calc_ybus_fault()
    zbus = c.calc_zbus(ybus_fault)
    _print_matrix("Ybus_fault (imaginary part, pu)", ybus_fault, bus_names, part="imag")
    _print_matrix("Zbus       (imaginary part, pu)", zbus, bus_names, part="imag")

    # Single fault at Bus2
    fs = c.solve(mode="fault", faulted_bus_name="Bus2", prefault_voltage=1.05)
    print(f"\nFault at Bus2  →  |I_fault| = {abs(fs.fault_current):.4f} pu")
    print("Post-fault voltages:")
    for bname, v in fs.fault_voltages.items():
        print(f"  {bname}: {abs(v):.4f} pu")

    # Voltage sweep — fault each bus in turn
    print("\n--- Fault voltage sweep (Vf = 1.05 pu) ---")
    _reset()  # reset counter so we can re-run circuit.solve safely
    # Re-use the already-solved circuit; just sweep fault bus
    fault_results = {}
    for faulted in bus_names:
        fault_results[faulted] = c.solve(
            mode="fault", faulted_bus_name=faulted, prefault_voltage=1.05
        )

    header = "           " + "  ".join(f"{n:>6}" for n in bus_names)
    print(header)
    for faulted in bus_names:
        fs = fault_results[faulted]
        mags = [abs(fault_results[obs].fault_voltages[faulted]) for obs in bus_names]
        row = "  ".join(f"{m:6.4f}" for m in mags)
        print(f"Fault@{faulted}  {row}  |I_f|={abs(fs.fault_current):8.4f} pu")
    print()


# ─────────────────────────────────────────────
#  Entry point
# ─────────────────────────────────────────────

if __name__ == "__main__":
    demo_milestone4()
    demo_milestone5()
    demo_milestone6()
    demo_milestone7()
    demo_milestone8()
    demo_milestone9()