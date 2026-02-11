import unittest
import sys
import math

# Add project root to path for imports using centralized paths
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from Paths.paths import PROJECT_ROOT

sys.path.insert(0, str(PROJECT_ROOT))

from Src.Utils.Classes.load import Load
from Src.Utils.Classes.bus import Bus


class TestLoad(unittest.TestCase):
    """Unit tests for the Load class."""

    def setUp(self):
        """Reset the Bus registry before each test."""
        Bus._bus_counter = 0
        Bus._bus_registry.clear()

    def test_load_creation(self):
        """Test that a Load can be created with correct attributes."""
        load1 = Load("Load 1", "Bus 2", 50.0, 30.0)

        self.assertEqual(load1.name, "Load 1")
        self.assertEqual(load1.bus1_name, "Bus 2")
        self.assertEqual(load1.mw, 50.0)
        self.assertEqual(load1.mvar, 30.0)

    def test_load_with_different_values(self):
        """Test loads with various power values."""
        load_small = Load("Small Load", "Bus A", 5.0, 2.5)
        load_large = Load("Large Load", "Bus B", 200.0, 150.0)

        self.assertEqual(load_small.mw, 5.0)
        self.assertEqual(load_small.mvar, 2.5)
        self.assertEqual(load_large.mw, 200.0)
        self.assertEqual(load_large.mvar, 150.0)

    def test_load_with_zero_reactive_power(self):
        """Test load with zero reactive power (unity power factor)."""
        load_unity = Load("Unity PF Load", "Bus 1", 50.0, 0.0)

        self.assertEqual(load_unity.mw, 50.0)
        self.assertEqual(load_unity.mvar, 0.0)

    def test_load_with_zero_active_power(self):
        """Test load with zero active power (pure reactive)."""
        load_reactive = Load("Reactive Load", "Bus 1", 0.0, 30.0)

        self.assertEqual(load_reactive.mw, 0.0)
        self.assertEqual(load_reactive.mvar, 30.0)

    def test_load_with_negative_mvar(self):
        """Test load with negative MVAR (capacitive/leading power factor)."""
        capacitor = Load("Capacitor Bank", "Bus 1", 0.0, -20.0)

        self.assertEqual(capacitor.mw, 0.0)
        self.assertEqual(capacitor.mvar, -20.0)

    def test_load_bus_name(self):
        """Test that load correctly stores bus name."""
        load1 = Load("Industrial Load", "Distribution Bus", 100.0, 75.0)

        self.assertEqual(load1.bus1_name, "Distribution Bus")

    def test_multiple_loads(self):
        """Test creating multiple loads."""
        load1 = Load("Load 1", "Bus 1", 50.0, 30.0)
        load2 = Load("Load 2", "Bus 2", 75.0, 45.0)
        load3 = Load("Load 3", "Bus 3", 100.0, 60.0)

        # Verify each load maintains its own attributes
        self.assertEqual(load1.name, "Load 1")
        self.assertEqual(load2.name, "Load 2")
        self.assertEqual(load3.name, "Load 3")

        self.assertEqual(load1.mw, 50.0)
        self.assertEqual(load2.mw, 75.0)
        self.assertEqual(load3.mw, 100.0)

    def test_load_repr(self):
        """Test the string representation of load."""
        load1 = Load("Load 1", "Bus 2", 50.0, 30.0)

        repr_str = repr(load1)

        # Check that repr contains all key information
        self.assertIn("Load 1", repr_str)
        self.assertIn("Bus 2", repr_str)
        self.assertIn("50.0", repr_str)
        self.assertIn("30.0", repr_str)

    def test_load_typical_values(self):
        """Test loads with typical power system values."""
        # Typical residential load (lagging PF ~0.9)
        residential = Load("Residential", "Bus 1", 5.0, 2.4)

        # Typical industrial load (lagging PF ~0.85)
        industrial = Load("Industrial", "Bus 2", 100.0, 62.0)

        # Typical commercial load (lagging PF ~0.88)
        commercial = Load("Commercial", "Bus 3", 50.0, 27.0)

        # All should have positive MW and MVAR (consuming power)
        self.assertGreater(residential.mw, 0)
        self.assertGreater(residential.mvar, 0)
        self.assertGreater(industrial.mw, 0)
        self.assertGreater(industrial.mvar, 0)

    def test_load_power_factor_calculation(self):
        """Test that load values result in realistic power factors."""
        load1 = Load("Load 1", "Bus 1", 50.0, 30.0)

        # Calculate apparent power and power factor
        s = math.sqrt(load1.mw ** 2 + load1.mvar ** 2)
        pf = load1.mw / s

        # Power factor should be between 0 and 1
        self.assertGreaterEqual(pf, 0.0)
        self.assertLessEqual(pf, 1.0)

        # For this example, PF should be approximately 0.857
        self.assertAlmostEqual(pf, 0.857, places=2)

    def test_load_attribute_types(self):
        """Test that load attributes have correct types."""
        load1 = Load("Load 1", "Bus 2", 50.0, 30.0)

        self.assertIsInstance(load1.name, str)
        self.assertIsInstance(load1.bus1_name, str)
        self.assertIsInstance(load1.mw, float)
        self.assertIsInstance(load1.mvar, float)

    def test_load_modification(self):
        """Test that load attributes can be modified."""
        load1 = Load("Load 1", "Bus 2", 50.0, 30.0)

        # Modify attributes
        load1.mw = 75.0
        load1.mvar = 45.0

        self.assertEqual(load1.mw, 75.0)
        self.assertEqual(load1.mvar, 45.0)

    def test_multiple_loads_same_bus(self):
        """Test multiple loads connected to the same bus."""
        load1 = Load("Load 1", "Bus 1", 50.0, 30.0)
        load2 = Load("Load 2", "Bus 1", 25.0, 15.0)
        load3 = Load("Load 3", "Bus 1", 30.0, 18.0)

        # All loads should reference the same bus
        self.assertEqual(load1.bus1_name, load2.bus1_name)
        self.assertEqual(load2.bus1_name, load3.bus1_name)

        # Calculate total load on bus
        total_mw = load1.mw + load2.mw + load3.mw
        total_mvar = load1.mvar + load2.mvar + load3.mvar

        self.assertEqual(total_mw, 105.0)
        self.assertEqual(total_mvar, 63.0)


class TestLoadWithBus(unittest.TestCase):
    """Integration tests for Load class with Bus class."""

    def setUp(self):
        """Reset the Bus registry before each test."""
        Bus._bus_counter = 0
        Bus._bus_registry.clear()

    def test_load_with_created_bus(self):
        """Test creating a load connected to a created bus."""
        # Create bus first
        bus1 = Bus("Bus 1", 13.8)

        # Create load connected to this bus
        load1 = Load("Load 1", "Bus 1", 50.0, 30.0)

        # Verify load references the correct bus name
        self.assertEqual(load1.bus1_name, bus1.name)

    def test_load_can_lookup_bus_index(self):
        """Test that load can be used to lookup connected bus index."""
        # Create bus
        bus1 = Bus("Load Bus", 13.8)

        # Create load
        load1 = Load("Load 1", "Load Bus", 50.0, 30.0)

        # Use Bus registry to find index of connected bus
        bus_index = Bus.get_bus_index(load1.bus1_name)

        self.assertEqual(bus_index, 0)

    def test_multiple_loads_with_buses(self):
        """Test creating multiple loads with multiple buses."""
        # Create buses
        bus1 = Bus("Bus 1", 13.8)
        bus2 = Bus("Bus 2", 13.8)
        bus3 = Bus("Bus 3", 13.8)

        # Create loads
        load1 = Load("Load 1", "Bus 1", 50.0, 30.0)
        load2 = Load("Load 2", "Bus 2", 75.0, 45.0)
        load3 = Load("Load 3", "Bus 3", 100.0, 60.0)

        # Verify load connections
        self.assertEqual(Bus.get_bus_index(load1.bus1_name), bus1.bus_index)
        self.assertEqual(Bus.get_bus_index(load2.bus1_name), bus2.bus_index)
        self.assertEqual(Bus.get_bus_index(load3.bus1_name), bus3.bus_index)

    def test_load_with_nonexistent_bus(self):
        """Test that load can reference buses that don't exist in registry."""
        # Create only one bus
        bus1 = Bus("Bus 1", 13.8)

        # Create load referencing a non-existent bus
        load1 = Load("Load 1", "Bus 999", 50.0, 30.0)

        # Load should still be created
        self.assertEqual(load1.bus1_name, "Bus 999")

        # But lookup will show Bus 999 doesn't exist
        self.assertIsNone(Bus.get_bus_index("Bus 999"))

    def test_realistic_distribution_system(self):
        """Test a realistic distribution system with buses and loads."""
        # Create distribution buses
        substation = Bus("Substation", 13.8)
        feeder1 = Bus("Feeder 1", 13.8)
        feeder2 = Bus("Feeder 2", 13.8)

        # Create loads
        residential = Load("Residential Area", "Feeder 1", 25.0, 15.0)
        commercial = Load("Shopping Center", "Feeder 2", 50.0, 30.0)
        industrial = Load("Factory", "Feeder 2", 100.0, 75.0)

        # Verify the system
        self.assertEqual(substation.bus_index, 0)
        self.assertEqual(feeder1.bus_index, 1)
        self.assertEqual(feeder2.bus_index, 2)

        # Verify load connections
        self.assertEqual(Bus.get_bus_index(residential.bus1_name), 1)
        self.assertEqual(Bus.get_bus_index(commercial.bus1_name), 2)
        self.assertEqual(Bus.get_bus_index(industrial.bus1_name), 2)

    def test_system_with_multiple_loads_per_bus(self):
        """Test a system with multiple loads on each bus."""
        # Create buses
        buses = [
            Bus("Bus 1", 13.8),
            Bus("Bus 2", 13.8),
            Bus("Bus 3", 13.8)
        ]

        # Create multiple loads per bus
        loads = [
            Load("Load 1A", "Bus 1", 20.0, 12.0),
            Load("Load 1B", "Bus 1", 30.0, 18.0),
            Load("Load 2A", "Bus 2", 40.0, 24.0),
            Load("Load 2B", "Bus 2", 35.0, 21.0),
            Load("Load 3A", "Bus 3", 50.0, 30.0)
        ]

        # Count loads per bus
        bus1_loads = [l for l in loads if l.bus1_name == "Bus 1"]
        bus2_loads = [l for l in loads if l.bus1_name == "Bus 2"]
        bus3_loads = [l for l in loads if l.bus1_name == "Bus 3"]

        self.assertEqual(len(bus1_loads), 2)
        self.assertEqual(len(bus2_loads), 2)
        self.assertEqual(len(bus3_loads), 1)

        # Calculate total load on Bus 1
        bus1_total_mw = sum(l.mw for l in bus1_loads)
        bus1_total_mvar = sum(l.mvar for l in bus1_loads)

        self.assertEqual(bus1_total_mw, 50.0)
        self.assertEqual(bus1_total_mvar, 30.0)


if __name__ == '__main__':
    unittest.main()