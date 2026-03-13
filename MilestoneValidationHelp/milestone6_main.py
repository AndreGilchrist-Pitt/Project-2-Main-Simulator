from Src.Utils.Classes.bus import Bus
from Src.Utils.Classes.transformer import Transformer
from Src.Utils.Classes.transmissionLine import TransmissionLine
from Src.Utils.Classes.generator import Generator
from Src.Utils.Classes.load import Load
from Src.Utils.Classes.circuit import Circuit
from Src.Utils.Classes.settings import Settings

Bus._bus_counter = 0
Bus._bus_registry.clear()

settings = Settings(freq=60.0, sbase=100.0)
circuit = Circuit("Milestone5 Five-Bus Glover Example 6.9", settings)

circuit.add_bus("Bus1", 15.0, vpu=1.06, delta=0.0, bus_type="Slack")
circuit.add_bus("Bus2", 345.0, vpu=1.02, delta=-2.0, bus_type="PQ")
circuit.add_bus("Bus3", 15.0, vpu=1.01, delta=-3.0, bus_type="PV")
circuit.add_bus("Bus4", 345.0, vpu=0.99, delta=-5.0, bus_type="PQ")
circuit.add_bus("Bus5", 345.0, vpu=0.98, delta=-7.0, bus_type="PQ")

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
circuit.vector_voltage_injection
circuit.vector_current_injection
Voltages = circuit.vector_voltage_injection
circuit.compute_power_injection(circuit.buses["Bus1"], voltages=Voltages)
print()