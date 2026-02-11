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