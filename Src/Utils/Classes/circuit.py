import numpy as np

from Src.Utils.Classes.bus import Bus
from Src.Utils.Classes.transformer import Transformer
from Src.Utils.Classes.transmissionLine import TransmissionLine
from Src.Utils.Classes.generator import Generator
from Src.Utils.Classes.load import Load
from Src.Utils.Classes.settings import Settings

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
        self.ybus = None
    def calc_ybus(self):
        """
        Compute the system Ybus (nodal admittance) matrix.

        Assembles Ybus by stamping the primitive admittance matrices of all
        transformers and transmission lines into an N×N complex matrix,
        where N is the number of buses.

        Updates self.ybus in-place. Does not return a value.

        Raises:
            ValueError: If an element references a bus not in the circuit,
                        if a connected bus has a zero diagonal entry,
                        or if Ybus is not symmetric.
        """
        N = len(self.buses) # NxN Ybus Matrix
        self.ybus = np.zeros((N, N), dtype=complex)
        bus_index = {name: idx for idx, name in enumerate(self.buses)}

        # Collect all power delivery elements
        pd_elements = list(self.transformers.values()) + list(self.transmission_lines.values())

        # Cache each element's yprim so we don't compute it twice
        element_yprims = []
        for element in pd_elements:
            yprim = element.calc_yprim()
            element_yprims.append((element, yprim))

        # --- Validation: check that every referenced bus exists ---
        for element, yprim in element_yprims:
            for bus_name in yprim.index:
                if bus_name not in bus_index:
                    raise ValueError(
                        f"Element '{element.name}' references bus '{bus_name}' not in circuit")

        # --- Stamp each primitive matrix into Ybus ---
        # Updates Ybus with Yprim elements

        for element, yprim in element_yprims:
            indices = [bus_index[b] for b in yprim.index]
            # Use numpy advanced indexing to stamp the full 2×2 block at once
            ix = np.ix_(indices, indices)
            self.ybus[ix] += yprim.values

        # --- Post-assembly consistency checks ---
        # Check that all connected buses have non-zero diagonal entries
        # This builds a set of only the buses that have at least one element connected to them.
        # If isolated bus (no transformer or line), it would not appear because an isolated bus has a legitimately zero diagonal.

        connected_buses = set()
        for _, yprim in element_yprims:
            connected_buses.update(yprim.index)

        # For each connected bus, it checks whether the diagonal entry Ybus[i,i] is zero.
        # The diagonal of Ybus represents the self-admittance — the sum of all admittances connected to that bus.
        # If a bus has elements connected to it but its diagonal is still zero, something went wrong during stamping (a bug, or pathological element values that cancel out exactly).

        for bus_name in connected_buses:
            idx = bus_index[bus_name]
            if self.ybus[idx, idx] == 0:
                raise ValueError(f"Bus '{bus_name}' has a zero diagonal entry in Ybus")

        # This checks that Ybus equals its own transpose (within a floating-point tolerance of 1e-10).
        # Since every individual yprim is symmetric, and stamping adds them into matching [i,j] and [j,i] positions, the final Ybus must be symmetric.
        # If it's not, it means there's a bug in the stamping logic or in one of the calc_yprim() methods.
        # np.allclose is used instead of == because complex floating-point arithmetic can introduce tiny rounding errors (e.g., 1e-16 differences)

        if not np.allclose(self.ybus, self.ybus.T, atol=1e-10):
            raise ValueError("Ybus is not symmetric")

        # Summary
        # Check             What it catches                                     Why it matters
        # Zero diagonal     A connected bus with no net self-admittance         Indicates a stamping bug or degenerate element values
        # Symmetry          Ybus[i,j] ≠ Ybus[j,i]                               All bilateral elements produce symmetric yprim, so asymmetry = a bug
    def add_bus(self, name: str, nominal_kv: float,vpu:float = 1.0,delta:float = 0.0,bus_type: str = None):
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

        bus = Bus(name, nominal_kv,vpu=vpu,delta=delta, bus_type=bus_type)
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
    @property
    def voltage_vector_polar(self):
        return [(bus.vpu, bus.delta) for bus in self.buses.values()]
    @property
    def voltage_vector_rectangular(self):
        N = len(self.buses)
        V = np.zeros(N, dtype=complex)
        for idx, bus in enumerate(self.buses):
            magnitude = self.buses[bus].vpu
            angle = np.deg2rad(self.buses[bus].delta)
            V[idx] = magnitude * np.exp(1j * angle)
        return V

    def _real_power_injection(self, bus: Bus, ybus, voltages) -> float:
        """
        Compute real power injection at a bus using the polar form.

        Pi = |Vi| * sum_j( |Vj| * (Gij*cos(δij) + Bij*sin(δij)) )

        Args:
            bus: The Bus object at which to compute Pi
            ybus: System admittance matrix
            voltages: Complex voltage vector (per-unit)

        Returns:
            P_i: Real power injection in per-unit
        """
        i = bus.bus_index
        V_i = np.abs(voltages[i])
        delta_i = np.angle(voltages[i])

        P_i = 0.0
        for j in range(len(voltages)):
            V_j = np.abs(voltages[j])
            delta_ij = delta_i - np.angle(voltages[j])
            G_ij = ybus[i, j].real
            B_ij = ybus[i, j].imag
            P_i += V_j * (G_ij * np.cos(delta_ij) + B_ij * np.sin(delta_ij))

        return V_i * P_i
    def _reactive_power_injection(self, bus: Bus, ybus, voltages) -> float:
        """
        Compute reactive power injection at a bus using the polar form.

        Qi = |Vi| * sum_j( |Vj| * (Gij*sin(δij) - Bij*cos(δij)) )

        Args:
            bus: The Bus object at which to compute Qi
            ybus: System admittance matrix
            voltages: Complex voltage vector (per-unit)

        Returns:
            Q_i: Reactive power injection in per-unit
        """
        i = bus.bus_index
        V_i = np.abs(voltages[i])
        delta_i = np.angle(voltages[i])

        Q_i = 0.0
        for j in range(len(voltages)):
            V_j = np.abs(voltages[j])
            delta_ij = delta_i - np.angle(voltages[j])
            G_ij = ybus[i, j].real
            B_ij = ybus[i, j].imag
            Q_i += V_j * (G_ij * np.sin(delta_ij) - B_ij * np.cos(delta_ij))

        return V_i * Q_i
    def compute_power_injection(self, bus: Bus, ybus, voltages):
        """
        Compute both real and reactive power injection at a bus.

        Args:
            bus: The Bus object at which to compute power
            ybus: System admittance matrix
            voltages: Complex voltage vector (per-unit)

        Returns:
            (P_i, Q_i): Tuple of real and reactive power in per-unit
        """
        P_i = self._real_power_injection(bus, ybus, voltages)
        Q_i = self._reactive_power_injection(bus, ybus, voltages)
        return P_i, Q_i

    def compute_power_mismatch(self, buses: dict, ybus, voltages) -> list:
        """
        Compute the power mismatch vector f for all non-slack buses.

        ΔP_i = P_spec - P_calc  (all non-slack buses)
        ΔQ_i = Q_spec - Q_calc  (PQ buses only)

        Args:
            buses: Dictionary of bus objects {name: Bus}
            ybus: System admittance matrix
            voltages: Complex voltage vector (per-unit)

        Returns:
            f: list of mismatches [ΔP (non-slack), ΔQ (PQ only)]
        """
        specs = {bus_name: [0.0, 0.0] for bus_name in buses}

        for gen in self.generators.values():
            specs[gen.bus1_name][0] += gen.p  # add generation

        for load in self.loads.values():
            specs[load.bus1_name][0] -= load.p  # subtract load P
            specs[load.bus1_name][1] -= load.q  # subtract load Q
        print("=== Power Mismatch Calculation ===")
        print(
            f"\n{'Bus':<8} {'Type':<7} {'P_spec':>10} {'P_calc':>10} {'ΔP':>10} {'Q_spec':>10} {'Q_calc':>10} {'ΔQ':>10}")
        print("-" * 75)

        f = []

        for bus in buses.values():
            if bus.bus_type == "Slack":
                print(f"{bus.name:<8} {'Slack':<7} {'---':>10} {'---':>10} {'---':>10} {'---':>10} {'---':>10} {'---':>10}")
                continue  # Slack bus: no mismatch

            P_spec, Q_spec = specs[bus.name]
            P_calc, Q_calc = self.compute_power_injection(bus, ybus, voltages)

            dP = P_spec - P_calc
            f.append(dP) # ΔP for all non-slack

            if bus.bus_type == "PQ":
                dQ = Q_spec - Q_calc
                f.append(dQ)
                print(f"{bus.name:<8} {'PQ':<7} {P_spec:>10.4f} {P_calc:>10.4f} {dP:>10.4f} {Q_spec:>10.4f} {Q_calc:>10.4f} {dQ:>10.4f}")
            else:
                print(f"{bus.name:<8} {'PV':<7} {P_spec:>10.4f} {P_calc:>10.4f} {dP:>10.4f} {'N/A':>10} {'N/A':>10} {'N/A':>10}")
        print("-" * 75)
        print(f"\nMismatch vector f: {[round(v, 6) for v in f]}\n")
        return f
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
