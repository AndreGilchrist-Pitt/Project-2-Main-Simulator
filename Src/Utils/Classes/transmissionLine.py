class TransmissionLine:
    """
    Represents a transmission line in a power system network.

    A transmission line connects two buses and has series impedance (r + jx)
    and shunt admittance (g + jb).
    """

    def __init__(self, name: str, bus1_name: str, bus2_name: str,
                 r: float, x: float, g: float, b: float):
        """
        Initialize a TransmissionLine instance.

        Args:
            name: The name/identifier of the transmission line
            bus1_name: Name of the first bus
            bus2_name: Name of the second bus
            r: Series resistance in per-unit or ohms
            x: Series reactance in per-unit or ohms
            g: Shunt conductance in per-unit or siemens
            b: Shunt susceptance in per-unit or siemens
        """
        self.name = name
        self.bus1_name = bus1_name
        self.bus2_name = bus2_name
        self.r = r
        self.x = x
        self.g = g
        self.b = b

    def __repr__(self):
        return (f"TransmissionLine(name='{self.name}', bus1='{self.bus1_name}', "
                f"bus2='{self.bus2_name}', r={self.r}, x={self.x}, g={self.g}, b={self.b})")


if __name__ == "__main__":
    # Simple validation test
    print("=== TransmissionLine Class Validation ===\n")

    # Create transmission line
    line1 = TransmissionLine("Line 1", "Bus 1", "Bus 2", 0.02, 0.25, 0.0, 0.04)

    # Test attributes
    print(f"Line name: {line1.name}")
    print(f"Bus 1 name: {line1.bus1_name}")
    print(f"Bus 2 name: {line1.bus2_name}")
    print(f"Series resistance (r): {line1.r}")
    print(f"Series reactance (x): {line1.x}")
    print(f"Shunt conductance (g): {line1.g}")
    print(f"Shunt susceptance (b): {line1.b}")

    # Test __repr__
    print(f"\nString representation:\n{repr(line1)}")

    # Create multiple lines
    print("\n--- Creating Multiple Transmission Lines ---")
    line2 = TransmissionLine("Line 2", "Bus 2", "Bus 3", 0.03, 0.30, 0.0, 0.05)
    line3 = TransmissionLine("Line 3", "Bus 3", "Bus 4", 0.025, 0.28, 0.0, 0.045)

    print(repr(line2))
    print(repr(line3))

    # Test typical values
    print("\n--- Typical Values Check ---")
    print(f"Line 1: x/r ratio = {line1.x / line1.r:.2f} (typical: 5-15 for overhead lines)")
    print(f"Line 1: Shunt conductance g = {line1.g} (typically zero or very small)")
