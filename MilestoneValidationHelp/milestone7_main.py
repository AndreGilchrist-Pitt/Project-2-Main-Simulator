from Src.Utils.Classes.bus import Bus
from Src.Utils.Classes.transformer import Transformer
from Src.Utils.Classes.transmissionLine import TransmissionLine
from Src.Utils.Classes.generator import Generator
from Src.Utils.Classes.load import Load
from Src.Utils.Classes.circuit import Circuit
from Src.Utils.Classes.settings import Settings
from Src.Utils.Classes.jacobian import Jacobian


def print_matrix(label, matrix, row_labels=None, col_labels=None, precision=4, width=12):
    print(f"\n{label}")

    if col_labels is not None:
        print(f"{'':<{width}}", end="")
        for col in col_labels:
            print(f"{col:>{width}}", end="")
        print()

    for i, row in enumerate(matrix):
        if row_labels is not None and i < len(row_labels):
            row_name = row_labels[i]
        else:
            row_name = f"r{i + 1}"

        print(f"{row_name:<{width}}", end="")

        for val in row:
            if isinstance(val, complex):
                text = f"{val.real:+.{precision}f}{val.imag:+.{precision}f}j"
            else:
                text = f"{val:.{precision}f}"
            print(f"{text:>{width}}", end="")
        print()


Bus._bus_counter = 0
Bus._bus_registry.clear()

Settings(freq=60.0, sbase=100.0)
circuit = Circuit("Milestone5 Five-Bus Glover Example 6.9")

circuit.add_bus("Bus1", 15.0, vpu=1.0, delta=0.0, bus_type="Slack")
circuit.add_bus("Bus2", 345.0, vpu=1.0, delta=0.0, bus_type="PQ")
circuit.add_bus("Bus3", 15.0, vpu=1.05, delta=0.0, bus_type="PV")
circuit.add_bus("Bus4", 345.0, vpu=1.0, delta=-0.0, bus_type="PQ")
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

angles = circuit.bus_angles()
voltages = circuit.bus_voltages()

jac = Jacobian()
J = jac.calculate_jacobian(circuit.buses, circuit.ybus, angles, voltages)

# Use safe labels: if the Jacobian is larger than the bus list, fall back to generic row/column names.
bus_names = list(circuit.buses.keys())
print_matrix(
    "Jacobian Matrix J:",
    J,
    row_labels=bus_names,
    col_labels=bus_names
)

print()