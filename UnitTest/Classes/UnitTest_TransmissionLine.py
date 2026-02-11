import unittest
import sys

# Add project root to path for imports using centralized paths
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from Paths.paths import PROJECT_ROOT

sys.path.insert(0, str(PROJECT_ROOT))

from Src.Utils.Classes.transmissionLine import TransmissionLine
from Src.Utils.Classes.bus import Bus


class TestTransmissionLine(unittest.TestCase):
    """Unit tests for the TransmissionLine class."""

    def setUp(self):
        """Reset the Bus registry before each test."""
        Bus._bus_counter = 0
        Bus._bus_registry.clear()

    def test_transmission_line_creation(self):
        """Test that a TransmissionLine can be created with correct attributes."""
        line1 = TransmissionLine("Line 1", "Bus 1", "Bus 2", 0.02, 0.25, 0.0, 0.04)

        self.assertEqual(line1.name, "Line 1")
        self.assertEqual(line1.bus1_name, "Bus 1")
        self.assertEqual(line1.bus2_name, "Bus 2")
        self.assertEqual(line1.r, 0.02)
        self.assertEqual(line1.x, 0.25)
        self.assertEqual(line1.g, 0.0)
        self.assertEqual(line1.b, 0.04)

    def test_transmission_line_with_different_values(self):
        """Test transmission lines with various parameter values."""
        line_short = TransmissionLine("Short Line", "Bus A", "Bus B", 0.01, 0.10, 0.0, 0.02)
        line_long = TransmissionLine("Long Line", "Bus C", "Bus D", 0.05, 0.50, 0.0, 0.10)

        self.assertEqual(line_short.r, 0.01)
        self.assertEqual(line_short.x, 0.10)
        self.assertEqual(line_long.r, 0.05)
        self.assertEqual(line_long.x, 0.50)

    def test_transmission_line_with_conductance(self):
        """Test transmission line with non-zero conductance."""
        line_g = TransmissionLine("Line G", "Bus 1", "Bus 2", 0.02, 0.25, 0.001, 0.04)

        self.assertEqual(line_g.g, 0.001)
        self.assertGreater(line_g.g, 0.0)

    def test_transmission_line_bus_names(self):
        """Test that transmission line correctly stores bus names."""
        line1 = TransmissionLine("Line 1", "Sending Bus", "Receiving Bus", 0.02, 0.25, 0.0, 0.04)

        self.assertEqual(line1.bus1_name, "Sending Bus")
        self.assertEqual(line1.bus2_name, "Receiving Bus")

    def test_multiple_transmission_lines(self):
        """Test creating multiple transmission lines."""
        line1 = TransmissionLine("Line 1", "Bus 1", "Bus 2", 0.02, 0.25, 0.0, 0.04)
        line2 = TransmissionLine("Line 2", "Bus 2", "Bus 3", 0.03, 0.30, 0.0, 0.05)
        line3 = TransmissionLine("Line 3", "Bus 3", "Bus 4", 0.025, 0.28, 0.0, 0.045)

        # Verify each line maintains its own attributes
        self.assertEqual(line1.name, "Line 1")
        self.assertEqual(line2.name, "Line 2")
        self.assertEqual(line3.name, "Line 3")

        self.assertEqual(line1.r, 0.02)
        self.assertEqual(line2.r, 0.03)
        self.assertEqual(line3.r, 0.025)

    def test_transmission_line_repr(self):
        """Test the string representation of transmission line."""
        line1 = TransmissionLine("Line 1", "Bus 1", "Bus 2", 0.02, 0.25, 0.0, 0.04)

        repr_str = repr(line1)

        # Check that repr contains all key information
        self.assertIn("Line 1", repr_str)
        self.assertIn("Bus 1", repr_str)
        self.assertIn("Bus 2", repr_str)
        self.assertIn("0.02", repr_str)
        self.assertIn("0.25", repr_str)
        self.assertIn("0.0", repr_str)
        self.assertIn("0.04", repr_str)

    def test_transmission_line_typical_values(self):
        """Test transmission line with typical power system values."""
        # Typical overhead transmission line
        line_overhead = TransmissionLine("Overhead", "Bus 1", "Bus 2", 0.02, 0.25, 0.0, 0.04)

        # Typical underground cable (higher capacitance)
        line_underground = TransmissionLine("Underground", "Bus 3", "Bus 4", 0.015, 0.10, 0.0, 0.20)

        # Overhead: x/r ratio typically 5-15
        self.assertGreater(line_overhead.x / line_overhead.r, 5)
        self.assertLess(line_overhead.x / line_overhead.r, 20)

        # Underground: higher b (capacitance)
        self.assertGreater(line_underground.b, line_overhead.b)

    def test_transmission_line_zero_values(self):
        """Test transmission line with zero values (edge cases)."""
        line_zero_g = TransmissionLine("Line Zero G", "Bus 1", "Bus 2", 0.02, 0.25, 0.0, 0.04)
        line_zero_b = TransmissionLine("Line Zero B", "Bus 1", "Bus 2", 0.02, 0.25, 0.0, 0.0)

        self.assertEqual(line_zero_g.g, 0.0)
        self.assertEqual(line_zero_b.b, 0.0)

    def test_transmission_line_same_bus_names(self):
        """Test transmission line with same bus names (edge case)."""
        line_loop = TransmissionLine("Loop", "Bus 1", "Bus 1", 0.02, 0.25, 0.0, 0.04)

        self.assertEqual(line_loop.bus1_name, "Bus 1")
        self.assertEqual(line_loop.bus2_name, "Bus 1")

    def test_transmission_line_attribute_types(self):
        """Test that transmission line attributes have correct types."""
        line1 = TransmissionLine("Line 1", "Bus 1", "Bus 2", 0.02, 0.25, 0.0, 0.04)

        self.assertIsInstance(line1.name, str)
        self.assertIsInstance(line1.bus1_name, str)
        self.assertIsInstance(line1.bus2_name, str)
        self.assertIsInstance(line1.r, float)
        self.assertIsInstance(line1.x, float)
        self.assertIsInstance(line1.g, float)
        self.assertIsInstance(line1.b, float)


class TestTransmissionLineWithBus(unittest.TestCase):
    """Integration tests for TransmissionLine class with Bus class."""

    def setUp(self):
        """Reset the Bus registry before each test."""
        Bus._bus_counter = 0
        Bus._bus_registry.clear()

    def test_transmission_line_with_created_buses(self):
        """Test creating a transmission line that connects two created buses."""
        # Create buses first
        bus1 = Bus("Bus 1", 230.0)
        bus2 = Bus("Bus 2", 230.0)

        # Create transmission line connecting these buses
        line1 = TransmissionLine("Line 1", "Bus 1", "Bus 2", 0.02, 0.25, 0.0, 0.04)

        # Verify line references the correct bus names
        self.assertEqual(line1.bus1_name, bus1.name)
        self.assertEqual(line1.bus2_name, bus2.name)

    def test_transmission_line_can_lookup_bus_indices(self):
        """Test that transmission line can be used to lookup connected bus indices."""
        # Create buses
        bus1 = Bus("Sending Bus", 345.0)
        bus2 = Bus("Receiving Bus", 345.0)

        # Create transmission line
        line1 = TransmissionLine("Line 1", "Sending Bus", "Receiving Bus", 0.02, 0.25, 0.0, 0.04)

        # Use Bus registry to find indices of connected buses
        bus1_index = Bus.get_bus_index(line1.bus1_name)
        bus2_index = Bus.get_bus_index(line1.bus2_name)

        self.assertEqual(bus1_index, 0)
        self.assertEqual(bus2_index, 1)

    def test_multiple_transmission_lines_with_buses(self):
        """Test creating multiple transmission lines with multiple buses."""
        # Create a simple 4-bus system
        bus1 = Bus("Bus 1", 230.0)
        bus2 = Bus("Bus 2", 230.0)
        bus3 = Bus("Bus 3", 230.0)
        bus4 = Bus("Bus 4", 230.0)

        # Create transmission lines
        line1 = TransmissionLine("Line 1", "Bus 1", "Bus 2", 0.02, 0.25, 0.0, 0.04)
        line2 = TransmissionLine("Line 2", "Bus 2", "Bus 3", 0.03, 0.30, 0.0, 0.05)
        line3 = TransmissionLine("Line 3", "Bus 3", "Bus 4", 0.025, 0.28, 0.0, 0.045)

        # Verify line connections
        self.assertEqual(Bus.get_bus_index(line1.bus1_name), bus1.bus_index)
        self.assertEqual(Bus.get_bus_index(line1.bus2_name), bus2.bus_index)
        self.assertEqual(Bus.get_bus_index(line2.bus1_name), bus2.bus_index)
        self.assertEqual(Bus.get_bus_index(line3.bus2_name), bus4.bus_index)

    def test_transmission_line_with_nonexistent_bus(self):
        """Test that transmission line can reference buses that don't exist in registry."""
        # Create only one bus
        bus1 = Bus("Bus 1", 230.0)

        # Create line referencing a non-existent bus
        line1 = TransmissionLine("Line 1", "Bus 1", "Bus 999", 0.02, 0.25, 0.0, 0.04)

        # Line should still be created
        self.assertEqual(line1.bus1_name, "Bus 1")
        self.assertEqual(line1.bus2_name, "Bus 999")

        # But lookup will show Bus 999 doesn't exist
        self.assertEqual(Bus.get_bus_index("Bus 1"), 0)
        self.assertIsNone(Bus.get_bus_index("Bus 999"))

    def test_realistic_transmission_network(self):
        """Test a realistic transmission network scenario."""
        # Create transmission buses
        bus1 = Bus("Station A", 345.0)
        bus2 = Bus("Station B", 345.0)
        bus3 = Bus("Station C", 345.0)

        # Create transmission lines
        line_ab = TransmissionLine("Line A-B", "Station A", "Station B", 0.02, 0.25, 0.0, 0.04)
        line_bc = TransmissionLine("Line B-C", "Station B", "Station C", 0.03, 0.30, 0.0, 0.05)

        # Verify the network
        self.assertEqual(bus1.bus_index, 0)
        self.assertEqual(bus2.bus_index, 1)
        self.assertEqual(bus3.bus_index, 2)

        # Verify line connections
        self.assertEqual(Bus.get_bus_index(line_ab.bus1_name), 0)
        self.assertEqual(Bus.get_bus_index(line_ab.bus2_name), 1)
        self.assertEqual(Bus.get_bus_index(line_bc.bus1_name), 1)
        self.assertEqual(Bus.get_bus_index(line_bc.bus2_name), 2)

    def test_meshed_network_topology(self):
        """Test building a meshed network topology with transmission lines."""
        # Create a 3-bus meshed system (triangle)
        buses = [
            Bus("Bus 1", 230.0),
            Bus("Bus 2", 230.0),
            Bus("Bus 3", 230.0)
        ]

        lines = [
            TransmissionLine("Line 1-2", "Bus 1", "Bus 2", 0.02, 0.25, 0.0, 0.04),
            TransmissionLine("Line 2-3", "Bus 2", "Bus 3", 0.03, 0.30, 0.0, 0.05),
            TransmissionLine("Line 3-1", "Bus 3", "Bus 1", 0.025, 0.28, 0.0, 0.045)
        ]

        # Verify all buses are registered
        self.assertEqual(len(Bus._bus_registry), 3)

        # Verify meshed topology: each bus is connected to two others
        bus1_connections = sum(1 for line in lines if "Bus 1" in [line.bus1_name, line.bus2_name])
        bus2_connections = sum(1 for line in lines if "Bus 2" in [line.bus1_name, line.bus2_name])
        bus3_connections = sum(1 for line in lines if "Bus 3" in [line.bus1_name, line.bus2_name])

        self.assertEqual(bus1_connections, 2)
        self.assertEqual(bus2_connections, 2)
        self.assertEqual(bus3_connections, 2)


if __name__ == '__main__':
    unittest.main()