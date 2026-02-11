import unittest
import sys

# Add project root to path for imports using centralized paths
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from Paths.paths import PROJECT_ROOT

sys.path.insert(0, str(PROJECT_ROOT))

from Src.Utils.Classes.generator import Generator
from Src.Utils.Classes.bus import Bus


class TestGenerator(unittest.TestCase):
    """Unit tests for the Generator class."""

    def setUp(self):
        """Reset the Bus registry before each test."""
        Bus._bus_counter = 0
        Bus._bus_registry.clear()

    def test_generator_creation(self):
        """Test that a Generator can be created with correct attributes."""
        gen1 = Generator("G1", "Bus 1", 1.04, 100.0)

        self.assertEqual(gen1.name, "G1")
        self.assertEqual(gen1.bus1_name, "Bus 1")
        self.assertEqual(gen1.voltage_setpoint, 1.04)
        self.assertEqual(gen1.mw_setpoint, 100.0)

    def test_generator_with_different_values(self):
        """Test generators with various setpoint values."""
        gen_small = Generator("Small Gen", "Bus A", 1.00, 50.0)
        gen_large = Generator("Large Gen", "Bus B", 1.05, 500.0)

        self.assertEqual(gen_small.voltage_setpoint, 1.00)
        self.assertEqual(gen_small.mw_setpoint, 50.0)
        self.assertEqual(gen_large.voltage_setpoint, 1.05)
        self.assertEqual(gen_large.mw_setpoint, 500.0)

    def test_generator_nominal_voltage(self):
        """Test generator with nominal voltage setpoint (1.0 p.u.)."""
        gen_nominal = Generator("G1", "Bus 1", 1.0, 100.0)

        self.assertEqual(gen_nominal.voltage_setpoint, 1.0)

    def test_generator_bus_name(self):
        """Test that generator correctly stores bus name."""
        gen1 = Generator("G1", "Generator Bus", 1.04, 100.0)

        self.assertEqual(gen1.bus1_name, "Generator Bus")

    def test_multiple_generators(self):
        """Test creating multiple generators."""
        gen1 = Generator("G1", "Bus 1", 1.04, 100.0)
        gen2 = Generator("G2", "Bus 2", 1.02, 150.0)
        gen3 = Generator("G3", "Bus 3", 1.05, 200.0)

        # Verify each generator maintains its own attributes
        self.assertEqual(gen1.name, "G1")
        self.assertEqual(gen2.name, "G2")
        self.assertEqual(gen3.name, "G3")

        self.assertEqual(gen1.mw_setpoint, 100.0)
        self.assertEqual(gen2.mw_setpoint, 150.0)
        self.assertEqual(gen3.mw_setpoint, 200.0)

    def test_generator_repr(self):
        """Test the string representation of generator."""
        gen1 = Generator("G1", "Bus 1", 1.04, 100.0)

        repr_str = repr(gen1)

        # Check that repr contains all key information
        self.assertIn("G1", repr_str)
        self.assertIn("Bus 1", repr_str)
        self.assertIn("1.04", repr_str)
        self.assertIn("100.0", repr_str)

    def test_generator_typical_values(self):
        """Test generators with typical power system values."""
        # Typical synchronous generator
        sync_gen = Generator("Sync Gen", "Bus 1", 1.04, 250.0)

        # Typical wind farm
        wind_farm = Generator("Wind Farm", "Bus 2", 1.00, 100.0)

        # Typical solar farm
        solar_farm = Generator("Solar Farm", "Bus 3", 1.00, 75.0)

        # Voltage setpoints typically between 0.95 and 1.05 p.u.
        self.assertGreaterEqual(sync_gen.voltage_setpoint, 0.95)
        self.assertLessEqual(sync_gen.voltage_setpoint, 1.10)

        # Power setpoints should be positive
        self.assertGreater(sync_gen.mw_setpoint, 0)
        self.assertGreater(wind_farm.mw_setpoint, 0)

    def test_generator_slack_bus(self):
        """Test generator configured as slack/swing bus (reference)."""
        slack_gen = Generator("Slack Gen", "Slack Bus", 1.05, 0.0)

        # Slack bus typically has higher voltage and MW is determined by system
        self.assertEqual(slack_gen.voltage_setpoint, 1.05)
        self.assertEqual(slack_gen.mw_setpoint, 0.0)

    def test_generator_voltage_range(self):
        """Test generators with various voltage setpoints."""
        gen_low = Generator("Low V", "Bus 1", 0.95, 100.0)
        gen_nominal = Generator("Nominal V", "Bus 2", 1.00, 100.0)
        gen_high = Generator("High V", "Bus 3", 1.05, 100.0)

        self.assertEqual(gen_low.voltage_setpoint, 0.95)
        self.assertEqual(gen_nominal.voltage_setpoint, 1.00)
        self.assertEqual(gen_high.voltage_setpoint, 1.05)

    def test_generator_attribute_types(self):
        """Test that generator attributes have correct types."""
        gen1 = Generator("G1", "Bus 1", 1.04, 100.0)

        self.assertIsInstance(gen1.name, str)
        self.assertIsInstance(gen1.bus1_name, str)
        self.assertIsInstance(gen1.voltage_setpoint, float)
        self.assertIsInstance(gen1.mw_setpoint, float)

    def test_generator_modification(self):
        """Test that generator attributes can be modified."""
        gen1 = Generator("G1", "Bus 1", 1.04, 100.0)

        # Modify attributes (e.g., dispatch changes)
        gen1.mw_setpoint = 150.0
        gen1.voltage_setpoint = 1.02

        self.assertEqual(gen1.mw_setpoint, 150.0)
        self.assertEqual(gen1.voltage_setpoint, 1.02)


class TestGeneratorWithBus(unittest.TestCase):
    """Integration tests for Generator class with Bus class."""

    def setUp(self):
        """Reset the Bus registry before each test."""
        Bus._bus_counter = 0
        Bus._bus_registry.clear()

    def test_generator_with_created_bus(self):
        """Test creating a generator connected to a created bus."""
        # Create bus first
        bus1 = Bus("Generator Bus", 20.0)

        # Create generator connected to this bus
        gen1 = Generator("G1", "Generator Bus", 1.04, 100.0)

        # Verify generator references the correct bus name
        self.assertEqual(gen1.bus1_name, bus1.name)

    def test_generator_can_lookup_bus_index(self):
        """Test that generator can be used to lookup connected bus index."""
        # Create bus
        bus1 = Bus("Gen Bus", 20.0)

        # Create generator
        gen1 = Generator("G1", "Gen Bus", 1.04, 100.0)

        # Use Bus registry to find index of connected bus
        bus_index = Bus.get_bus_index(gen1.bus1_name)

        self.assertEqual(bus_index, 0)

    def test_multiple_generators_with_buses(self):
        """Test creating multiple generators with multiple buses."""
        # Create generator buses
        bus1 = Bus("Gen Bus 1", 20.0)
        bus2 = Bus("Gen Bus 2", 20.0)
        bus3 = Bus("Gen Bus 3", 20.0)

        # Create generators
        gen1 = Generator("G1", "Gen Bus 1", 1.04, 100.0)
        gen2 = Generator("G2", "Gen Bus 2", 1.02, 150.0)
        gen3 = Generator("G3", "Gen Bus 3", 1.05, 200.0)

        # Verify generator connections
        self.assertEqual(Bus.get_bus_index(gen1.bus1_name), bus1.bus_index)
        self.assertEqual(Bus.get_bus_index(gen2.bus1_name), bus2.bus_index)
        self.assertEqual(Bus.get_bus_index(gen3.bus1_name), bus3.bus_index)

    def test_generator_with_nonexistent_bus(self):
        """Test that generator can reference buses that don't exist in registry."""
        # Create only one bus
        bus1 = Bus("Bus 1", 20.0)

        # Create generator referencing a non-existent bus
        gen1 = Generator("G1", "Bus 999", 1.04, 100.0)

        # Generator should still be created
        self.assertEqual(gen1.bus1_name, "Bus 999")

        # But lookup will show Bus 999 doesn't exist
        self.assertIsNone(Bus.get_bus_index("Bus 999"))

    def test_realistic_generation_system(self):
        """Test a realistic generation system with buses and generators."""
        # Create generator buses at different voltage levels
        gen_bus_1 = Bus("Plant 1", 20.0)
        gen_bus_2 = Bus("Plant 2", 18.0)
        gen_bus_3 = Bus("Plant 3", 22.0)

        # Create generators
        coal_plant = Generator("Coal Unit 1", "Plant 1", 1.04, 300.0)
        gas_plant = Generator("Gas Unit 1", "Plant 2", 1.02, 200.0)
        hydro_plant = Generator("Hydro Unit 1", "Plant 3", 1.05, 150.0)

        # Verify the system
        self.assertEqual(gen_bus_1.bus_index, 0)
        self.assertEqual(gen_bus_2.bus_index, 1)
        self.assertEqual(gen_bus_3.bus_index, 2)

        # Verify generator connections
        self.assertEqual(Bus.get_bus_index(coal_plant.bus1_name), 0)
        self.assertEqual(Bus.get_bus_index(gas_plant.bus1_name), 1)
        self.assertEqual(Bus.get_bus_index(hydro_plant.bus1_name), 2)

        # Calculate total generation
        total_mw = coal_plant.mw_setpoint + gas_plant.mw_setpoint + hydro_plant.mw_setpoint
        self.assertEqual(total_mw, 650.0)

    def test_multiple_generators_same_bus(self):
        """Test multiple generators at the same bus (power plant with multiple units)."""
        # Create a bus for a power plant
        plant_bus = Bus("Power Plant", 20.0)

        # Create multiple generator units
        unit1 = Generator("Unit 1", "Power Plant", 1.04, 250.0)
        unit2 = Generator("Unit 2", "Power Plant", 1.04, 250.0)
        unit3 = Generator("Unit 3", "Power Plant", 1.04, 250.0)

        # All generators should reference the same bus
        self.assertEqual(unit1.bus1_name, unit2.bus1_name)
        self.assertEqual(unit2.bus1_name, unit3.bus1_name)

        # Calculate total plant output
        total_plant_mw = unit1.mw_setpoint + unit2.mw_setpoint + unit3.mw_setpoint
        self.assertEqual(total_plant_mw, 750.0)

    def test_generator_bus_voltage_coordination(self):
        """Test that generators at same bus can have coordinated voltage setpoints."""
        # Create a bus
        bus1 = Bus("Common Bus", 20.0)

        # Create generators with same voltage setpoint (coordinated control)
        gen1 = Generator("G1", "Common Bus", 1.04, 100.0)
        gen2 = Generator("G2", "Common Bus", 1.04, 150.0)

        # Verify same voltage setpoint
        self.assertEqual(gen1.voltage_setpoint, gen2.voltage_setpoint)

        # But different power setpoints
        self.assertNotEqual(gen1.mw_setpoint, gen2.mw_setpoint)


if __name__ == '__main__':
    unittest.main()