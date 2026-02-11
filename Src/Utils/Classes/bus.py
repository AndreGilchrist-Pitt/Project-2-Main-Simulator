class Bus:
    """
    Represents a bus (node) in a power system network.

    Each bus has a unique index assigned automatically using a class-level counter.
    A dictionary tracks all created buses by name.
    """

    # Class-level counter for unique bus indices
    _bus_counter = 0

    # Dictionary to track all buses: {name: bus_index}
    _bus_registry = {}

    def __init__(self, name: str, nominal_kv: float):
        """
        Initialize a Bus instance.

        Args:
            name: The name of the bus
            nominal_kv: The nominal voltage in kilovolts
        """
        self.name = name
        self.nominal_kv = nominal_kv

        # Assign unique bus index and increment counter
        self.bus_index = Bus._bus_counter
        Bus._bus_counter += 1

        # Register this bus in the dictionary
        Bus._bus_registry[self.name] = self.bus_index

    @classmethod
    def get_bus_index(cls, name: str):
        """
        Get the bus index for a given bus name.

        Args:
            name: The name of the bus

        Returns:
            The bus index, or None if the bus doesn't exist
        """
        return cls._bus_registry.get(name)


if __name__ == "__main__":
    # Simple validation test
    print("=== Bus Class Validation ===\n")

    # Create buses
    bus1 = Bus("Bus 1", 20.0)
    bus2 = Bus("Bus 2", 230.0)
    bus3 = Bus("Bus 3", 115.0)

    # Test bus creation
    print(f"Bus 1: name={bus1.name}, nominal_kv={bus1.nominal_kv}, index={bus1.bus_index}")
    print(f"Bus 2: name={bus2.name}, nominal_kv={bus2.nominal_kv}, index={bus2.bus_index}")
    print(f"Bus 3: name={bus3.name}, nominal_kv={bus3.nominal_kv}, index={bus3.bus_index}")

    # Test registry
    print(f"\nBus Registry: {Bus._bus_registry}")

    # Test get_bus_index
    print(f"\nLookup 'Bus 1' index: {Bus.get_bus_index('Bus 1')}")
    print(f"Lookup 'Bus 2' index: {Bus.get_bus_index('Bus 2')}")
    print(f"Lookup 'Nonexistent' index: {Bus.get_bus_index('Nonexistent')}")