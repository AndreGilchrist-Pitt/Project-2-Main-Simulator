import unittest
import sys

# Add project root to path for imports using centralized paths
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from Paths.paths import PROJECT_ROOT

sys.path.insert(0, str(PROJECT_ROOT))

from Src.Utils.Classes.bus import Bus


class TestBus(unittest.TestCase):
    """Unit tests for the Bus class."""

    def setUp(self):
        """Reset the Bus registry before each test."""
        Bus._bus_counter = 0
        Bus._bus_registry.clear()

    def test_bus_creation(self):
        """Test that a Bus can be created with correct attributes."""
        bus = Bus("Bus 1", 20.0)

        self.assertEqual(bus.name, "Bus 1")
        self.assertEqual(bus.nominal_kv, 20.0)
        self.assertEqual(bus.bus_index, 0)

    def test_bus_counter_increments(self):
        """Test that bus_index increments for each new bus."""
        bus1 = Bus("Bus 1", 20.0)
        bus2 = Bus("Bus 2", 230.0)
        bus3 = Bus("Bus 3", 115.0)

        self.assertEqual(bus1.bus_index, 0)
        self.assertEqual(bus2.bus_index, 1)
        self.assertEqual(bus3.bus_index, 2)

    def test_bus_registry_updates(self):
        """Test that the bus registry tracks all created buses."""
        bus1 = Bus("Bus 1", 20.0)
        bus2 = Bus("Bus 2", 230.0)

        self.assertEqual(len(Bus._bus_registry), 2)
        self.assertIn("Bus 1", Bus._bus_registry)
        self.assertIn("Bus 2", Bus._bus_registry)
        self.assertEqual(Bus._bus_registry["Bus 1"], 0)
        self.assertEqual(Bus._bus_registry["Bus 2"], 1)

    def test_get_bus_index_found(self):
        """Test retrieving bus index by name."""
        bus1 = Bus("Bus 1", 20.0)
        bus2 = Bus("Bus 2", 230.0)

        self.assertEqual(Bus.get_bus_index("Bus 1"), 0)
        self.assertEqual(Bus.get_bus_index("Bus 2"), 1)

    def test_get_bus_index_not_found(self):
        """Test that get_bus_index returns None for non-existent bus."""
        bus = Bus("Bus 1", 20.0)

        self.assertIsNone(Bus.get_bus_index("Bus 99"))
        self.assertIsNone(Bus.get_bus_index("Nonexistent"))

    def test_different_voltage_levels(self):
        """Test buses with different voltage levels."""
        bus_low = Bus("Low Voltage", 13.8)
        bus_medium = Bus("Medium Voltage", 69.0)
        bus_high = Bus("High Voltage", 345.0)

        self.assertEqual(bus_low.nominal_kv, 13.8)
        self.assertEqual(bus_medium.nominal_kv, 69.0)
        self.assertEqual(bus_high.nominal_kv, 345.0)

    def test_duplicate_names(self):
        """Test that buses with the same name overwrite in registry."""
        bus1 = Bus("Duplicate", 20.0)
        bus2 = Bus("Duplicate", 230.0)

        # Both buses get different indices
        self.assertEqual(bus1.bus_index, 0)
        self.assertEqual(bus2.bus_index, 1)

        # Registry contains the last bus with that name
        self.assertEqual(Bus.get_bus_index("Duplicate"), 1)

    def test_registry_persistence(self):
        """Test that registry persists across multiple bus creations."""
        Bus("Bus 1", 20.0)
        Bus("Bus 2", 230.0)

        # Create another bus
        Bus("Bus 3", 115.0)

        # All previous buses should still be accessible
        self.assertEqual(Bus.get_bus_index("Bus 1"), 0)
        self.assertEqual(Bus.get_bus_index("Bus 2"), 1)
        self.assertEqual(Bus.get_bus_index("Bus 3"), 2)

    def test_bus_index_uniqueness(self):
        """Test that each bus gets a unique index."""
        buses = [Bus(f"Bus {i}", 20.0 + i) for i in range(5)]
        indices = [bus.bus_index for bus in buses]

        # All indices should be unique
        self.assertEqual(len(indices), len(set(indices)))

        # Indices should be sequential
        self.assertEqual(indices, [0, 1, 2, 3, 4])


if __name__ == '__main__':
    unittest.main()