from Src.Utils.Classes.bus import Bus
from Src.Utils.Classes.transformer import Transformer
from Src.Utils.Classes.transmissionLine import TransmissionLine
from Src.Utils.Classes.generator import Generator
from Src.Utils.Classes.load import Load
from Src.Utils.Classes.circuit import Circuit
print("\n=== Milestone 4: Ybus Validation ===\n")

Bus._bus_counter = 0
Bus._bus_registry.clear()

c = Circuit("Five-Bus Glover Example 6.9")

# PowerWorld Bus Data
c.add_bus("Bus1", 15.0)  # One
c.add_bus("Bus2", 345.0)  # Two
c.add_bus("Bus3", 15.0)  # Three
c.add_bus("Bus4", 345.0)  # Four
c.add_bus("Bus5", 345.0)  # Five

# Transformers (using PowerWorld R values)
c.add_transformer("T1", "Bus1", "Bus5", 0.0015, 0.02)
c.add_transformer("T2", "Bus3", "Bus4", 0.00075, 0.01)

# Transmission lines (using PowerWorld values)
c.add_transmission_line("Line1", "Bus4", "Bus2", 0.009, 0.1, 0.0, 1.72)
c.add_transmission_line("Line2", "Bus5", "Bus2", 0.0045, 0.05, 0.0, 0.88)
c.add_transmission_line("Line3", "Bus5", "Bus4", 0.00225, 0.025, 0.0, 0.44)

# Generators (from PowerWorld)
c.add_generator("G1", "Bus1", 1.0, 0.0)
c.add_generator("G2", "Bus3", 1.0, 520.0)

# Loads (from PowerWorld)
c.add_load("Load2", "Bus2", 800.0, 280.0)
c.add_load("Load3", "Bus3", 80.0, 40.0)

# Calculate Ybus
c.calc_ybus()

# Display results
print("\nCalculated Ybus Matrix:\n")
bus_names = list(c.buses.keys())
col_width = 22

# Header row
print(f"{'':>{col_width}}", end="")
for name in bus_names:
    print(f"{name:>{col_width}}", end="")
print()

# Separator
print("-" * (col_width * (len(bus_names) + 1)))

# Data rows
for i, row in enumerate(c.ybus):
    print(f"{bus_names[i]:>{col_width}}", end="")
    for val in row:
        if val == 0:
            print(f"{'0':>{col_width}}", end="")
        else:
            print(f"{val.real:+9.4f}{val.imag:+9.4f}j".rjust(col_width), end="")
    print()