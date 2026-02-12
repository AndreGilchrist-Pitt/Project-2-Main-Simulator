from Src.Utils.Classes.bus import Bus
from Src.Utils.Classes.transformer import Transformer
from Src.Utils.Classes.transmissionLine import TransmissionLine
from Src.Utils.Classes.generator import Generator
from Src.Utils.Classes.load import Load


class Circuit:
    """
    Represents a complete power system network.

    The Circuit class serves as a container for all equipment objects
    (buses, transformers, transmission lines, generators, and loads).
    """

    def __init__(self, name: str):
        """
        Initialize a Circuit instance.

        Args:
            name: The name of the circuit
        """
        self.name = name
        self.buses = {}
        self.transformers = {}
        self.transmission_lines = {}
        self.generators = {}
        self.loads = {}

    def add_bus(self, name: str, nominal_kv: float):
        """
        Add a bus to the circuit.

        Args:
            name: The name of the bus
            nominal_kv: The nominal voltage in kilovolts

        Raises:
            ValueError: If a bus with the same name already exists
        """
        if name in self.buses:
            raise ValueError(f"Bus '{name}' already exists in the circuit")

        bus = Bus(name, nominal_kv)
        self.buses[name] = bus

    def add_transformer(self, name: str, bus1_name: str, bus2_name: str, r: float, x: float):
        """
        Add a transformer to the circuit.

        Args:
            name: The name of the transformer
            bus1_name: Name of the first bus
            bus2_name: Name of the second bus
            r: Resistance in per-unit or ohms
            x: Reactance in per-unit or ohms

        Raises:
            ValueError: If a transformer with the same name already exists
        """
        if name in self.transformers:
            raise ValueError(f"Transformer '{name}' already exists in the circuit")

        transformer = Transformer(name, bus1_name, bus2_name, r, x)
        self.transformers[name] = transformer

    def add_transmission_line(self, name: str, bus1_name: str, bus2_name: str,
                             r: float, x: float, g: float, b: float):
        """
        Add a transmission line to the circuit.

        Args:
            name: The name of the transmission line
            bus1_name: Name of the first bus
            bus2_name: Name of the second bus
            r: Series resistance in per-unit or ohms
            x: Series reactance in per-unit or ohms
            g: Shunt conductance in per-unit or siemens
            b: Shunt susceptance in per-unit or siemens

        Raises:
            ValueError: If a transmission line with the same name already exists
        """
        if name in self.transmission_lines:
            raise ValueError(f"Transmission line '{name}' already exists in the circuit")

        line = TransmissionLine(name, bus1_name, bus2_name, r, x, g, b)
        self.transmission_lines[name] = line

    def add_generator(self, name: str, bus1_name: str, voltage_setpoint: float, mw_setpoint: float):
        """
        Add a generator to the circuit.

        Args:
            name: The name of the generator
            bus1_name: Name of the bus where the generator is connected
            voltage_setpoint: Voltage magnitude setpoint in per-unit
            mw_setpoint: Active power generation setpoint in megawatts (MW)

        Raises:
            ValueError: If a generator with the same name already exists
        """
        if name in self.generators:
            raise ValueError(f"Generator '{name}' already exists in the circuit")

        generator = Generator(name, bus1_name, voltage_setpoint, mw_setpoint)
        self.generators[name] = generator

    def add_load(self, name: str, bus1_name: str, mw: float, mvar: float):
        """
        Add a load to the circuit.

        Args:
            name: The name of the load
            bus1_name: Name of the bus where the load is connected
            mw: Active power consumption in megawatts (MW)
            mvar: Reactive power consumption in megavars (MVAR)

        Raises:
            ValueError: If a load with the same name already exists
        """
        if name in self.loads:
            raise ValueError(f"Load '{name}' already exists in the circuit")

        load = Load(name, bus1_name, mw, mvar)
        self.loads[name] = load


if __name__ == "__main__":
    # Validation tests from Milestone 2
    print("=== Circuit Class Validation ===\n")

    # Create an instance of the Circuit class
    print("--- Create Circuit Instance ---")
    circuit1 = Circuit("Test Circuit")
    print(circuit1.name)  # Expected output: "Test Circuit"
    print(type(circuit1.name))  # Expected output: <class 'str'>

    # Check attribute initialization
    print("\n--- Check Attribute Initialization ---")
    print(circuit1.buses)  # Expected output: {}
    print(circuit1.transformers)  # Expected output: {}
    print(circuit1.transmission_lines)  # Expected output: {}
    print(circuit1.generators)  # Expected output: {}
    print(circuit1.loads)  # Expected output: {}

    # Add and Retrieve Equipment Components
    print("\n--- Add and Retrieve Equipment Components ---")
    circuit1 = Circuit("Test Circuit")
    circuit1.add_bus("Bus_1", 20.0)
    circuit1.add_bus("Bus_2", 230.0)
    print(list(circuit1.buses.keys()))  # Expected output: ['Bus_1', 'Bus_2']
    print(circuit1.buses["Bus_1"].name, circuit1.buses["Bus_1"].nominal_kv)


    # Add and Verify a Transformer
    print("\n--- Add and Verify a Transformer ---")
    circuit1.add_transformer("T1", "Bus_1", "Bus_2", 0.01, 0.10)
    print(list(circuit1.transformers.keys())) # Expected output: ['T1']
    print(circuit1.transformers["T1"].name,
          circuit1.transformers["T1"].bus1_name,
          circuit1.transformers["T1"].bus2_name,
          circuit1.transformers["T1"].r,
          circuit1.transformers["T1"].x)

    # Add and Verify a Transmission Line
    print("\n--- Add and Verify a Transmission Line ---")
    circuit1.add_transmission_line("Line_1", "Bus_1", "Bus_2", 0.02, 0.25, 0.0, 0.04)
    print(list(circuit1.transmission_lines.keys())) # Expected output: ['Line_1']
    print(circuit1.transmission_lines["Line_1"].name,
          circuit1.transmission_lines["Line_1"].bus1_name,
          circuit1.transmission_lines["Line_1"].bus2_name,
          circuit1.transmission_lines["Line_1"].r,
          circuit1.transmission_lines["Line_1"].x,
          circuit1.transmission_lines["Line_1"].g,
          circuit1.transmission_lines["Line_1"].b)

    # Add and Verify a Load
    print("\n--- Add and Verify a Load ---")
    circuit1.add_load("Load_1", "Bus_2", 50.0, 30.0)
    print(list(circuit1.loads.keys())) # Expected output: ['Load_1']
    print(circuit1.loads["Load_1"].name,
          circuit1.loads["Load_1"].bus1_name,
          circuit1.loads["Load_1"].mw,
          circuit1.loads["Load_1"].mvar)

    # Add and Verify a Generator
    print("\n--- Add and Verify a Generator ---")
    circuit1.add_generator("G1", "Bus_1", 1.04, 100.0)
    print(list(circuit1.generators.keys())) # Expected output: ['G1']
    print(circuit1.generators["G1"].name,
          circuit1.generators["G1"].bus1_name,
          circuit1.generators["G1"].voltage_setpoint,
          circuit1.generators["G1"].mw_setpoint)
    # Test duplicate name detection
    print("\n--- Test Duplicate Name Detection ---")
    try:
        circuit1.add_bus("Bus_1", 115)
        print("ERROR: Duplicate name not detected!")
    except ValueError as e:
        print(f"Correctly caught duplicate: {e}")
