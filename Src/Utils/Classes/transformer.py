

class Transformer:
    """
    Represents a transformer in a power system network.

    A transformer connects two buses and has series impedance (r + jx).
    """

    def __init__(self, name: str, bus1_name: str, bus2_name: str, r: float, x: float):
        """
        Initialize a Transformer instance.

        Args:
            name: The name/identifier of the transformer
            bus1_name: Name of the first bus (typically high voltage side)
            bus2_name: Name of the second bus (typically low voltage side)
            r: Resistance in per-unit or ohms
            x: Reactance in per-unit or ohms
        """
        self.name = name
        self.bus1_name = bus1_name
        self.bus2_name = bus2_name
        self.r = r
        self.x = x

    def __repr__(self):
        return f"Transformer(name='{self.name}', bus1='{self.bus1_name}', bus2='{self.bus2_name}', r={self.r}, x={self.x})"


if __name__ == "__main__":
    # Simple validation test
    print("=== Transformer Class Validation ===\n")

    # Create transformer
    t1 = Transformer("T1", "Bus 1", "Bus 2", 0.01, 0.10)

    # Test attributes
    print(f"Transformer name: {t1.name}")
    print(f"Bus 1 name: {t1.bus1_name}")
    print(f"Bus 2 name: {t1.bus2_name}")
    print(f"Resistance (r): {t1.r}")
    print(f"Reactance (x): {t1.x}")

    # Test __repr__
    print(f"\nString representation:\n{repr(t1)}")

    # Create multiple transformers
    print("\n--- Creating Multiple Transformers ---")
    t2 = Transformer("T2", "Bus 2", "Bus 3", 0.02, 0.15)
    t3 = Transformer("T3", "Bus 3", "Bus 4", 0.015, 0.12)

    print(repr(t2))
    print(repr(t3))