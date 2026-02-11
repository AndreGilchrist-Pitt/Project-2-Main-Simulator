import unittest
import sys

# Add project root to path for imports using centralized paths
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from Paths.paths import PROJECT_ROOT

sys.path.insert(0, str(PROJECT_ROOT))

from Src.Utils.Classes.transformer import Transformer
from Src.Utils.Classes.bus import Bus


class TestTransformer(unittest.TestCase):
    """Unit tests for the Transformer class."""

    def setUp(self):
        """Reset the Bus registry before each test."""
        Bus._bus_counter = 0
        Bus._bus_registry.clear()

    def test_transformer_creation(self):
        """Test that a Transformer can be created with correct attributes."""
        t1 = Transformer("T1", "Bus 1", "Bus 2", 0.01, 0.10)

        self.assertEqual(t1.name, "T1")
        self.assertEqual(t1.bus1_name, "Bus 1")
        self.assertEqual(t1.bus2_name, "Bus 2")
        self.assertEqual(t1.r, 0.01)
        self.assertEqual(t1.x, 0.10)

    def test_transformer_with_different_values(self):
        """Test transformers with various impedance values."""
        t_low = Transformer("T_Low", "Bus A", "Bus B", 0.001, 0.005)
        t_high = Transformer("T_High", "Bus C", "Bus D", 0.05, 0.25)

        self.assertEqual(t_low.r, 0.001)
        self.assertEqual(t_low.x, 0.005)
        self.assertEqual(t_high.r, 0.05)
        self.assertEqual(t_high.x, 0.25)

    def test_transformer_with_zero_resistance(self):
        """Test transformer with zero resistance (ideal case)."""
        t_ideal = Transformer("T_Ideal", "Bus 1", "Bus 2", 0.0, 0.10)

        self.assertEqual(t_ideal.r, 0.0)
        self.assertEqual(t_ideal.x, 0.10)

    def test_transformer_bus_names(self):
        """Test that transformer correctly stores bus names."""
        t1 = Transformer("T1", "HV Bus", "LV Bus", 0.01, 0.10)

        self.assertEqual(t1.bus1_name, "HV Bus")
        self.assertEqual(t1.bus2_name, "LV Bus")

    def test_transformer_with_negative_values(self):
        """Test transformer with negative impedance values (edge case)."""
        t_neg = Transformer("T_Neg", "Bus 1", "Bus 2", -0.01, -0.10)

        self.assertEqual(t_neg.r, -0.01)
        self.assertEqual(t_neg.x, -0.10)

    def test_multiple_transformers(self):
        """Test creating multiple transformers."""
        t1 = Transformer("T1", "Bus 1", "Bus 2", 0.01, 0.10)
        t2 = Transformer("T2", "Bus 2", "Bus 3", 0.02, 0.15)
        t3 = Transformer("T3", "Bus 3", "Bus 4", 0.015, 0.12)

        # Verify each transformer maintains its own attributes
        self.assertEqual(t1.name, "T1")
        self.assertEqual(t2.name, "T2")
        self.assertEqual(t3.name, "T3")

        self.assertEqual(t1.r, 0.01)
        self.assertEqual(t2.r, 0.02)
        self.assertEqual(t3.r, 0.015)

    def test_transformer_repr(self):
        """Test the string representation of transformer."""
        t1 = Transformer("T1", "Bus 1", "Bus 2", 0.01, 0.10)

        repr_str = repr(t1)

        # Check that repr contains all key information
        self.assertIn("T1", repr_str)
        self.assertIn("Bus 1", repr_str)
        self.assertIn("Bus 2", repr_str)
        self.assertIn("0.01", repr_str)
        self.assertIn("0.1", repr_str)

    def test_transformer_typical_values(self):
        """Test transformer with typical power system values."""
        # Typical distribution transformer
        t_dist = Transformer("T_Dist", "13.8kV", "0.48kV", 0.01, 0.05)

        # Typical transmission transformer
        t_trans = Transformer("T_Trans", "345kV", "138kV", 0.002, 0.08)

        self.assertLess(t_dist.r, t_dist.x)  # Reactance > Resistance (typical)
        self.assertLess(t_trans.r, t_trans.x)

    def test_transformer_same_bus_names(self):
        """Test transformer with same bus names (edge case - should allow but unusual)."""
        t_loop = Transformer("T_Loop", "Bus 1", "Bus 1", 0.01, 0.10)

        self.assertEqual(t_loop.bus1_name, "Bus 1")
        self.assertEqual(t_loop.bus2_name, "Bus 1")

    def test_transformer_attribute_types(self):
        """Test that transformer attributes have correct types."""
        t1 = Transformer("T1", "Bus 1", "Bus 2", 0.01, 0.10)

        self.assertIsInstance(t1.name, str)
        self.assertIsInstance(t1.bus1_name, str)
        self.assertIsInstance(t1.bus2_name, str)
        self.assertIsInstance(t1.r, float)
        self.assertIsInstance(t1.x, float)

    def test_transformer_immutability(self):
        """Test that transformer attributes can be modified (no immutability enforced)."""
        t1 = Transformer("T1", "Bus 1", "Bus 2", 0.01, 0.10)

        # Modify attributes
        t1.r = 0.02
        t1.x = 0.20

        self.assertEqual(t1.r, 0.02)
        self.assertEqual(t1.x, 0.20)


class TestTransformerWithBus(unittest.TestCase):
    """Integration tests for Transformer class with Bus class."""

    def setUp(self):
        """Reset the Bus registry before each test."""
        Bus._bus_counter = 0
        Bus._bus_registry.clear()

    def test_transformer_with_created_buses(self):
        """Test creating a transformer that connects two created buses."""
        # Create buses first
        bus1 = Bus("Bus 1", 20.0)
        bus2 = Bus("Bus 2", 230.0)

        # Create transformer connecting these buses
        t1 = Transformer("T1", "Bus 1", "Bus 2", 0.01, 0.10)

        # Verify transformer references the correct bus names
        self.assertEqual(t1.bus1_name, bus1.name)
        self.assertEqual(t1.bus2_name, bus2.name)

    def test_transformer_can_lookup_bus_indices(self):
        """Test that transformer can be used to lookup connected bus indices."""
        # Create buses
        bus1 = Bus("HV Bus", 345.0)
        bus2 = Bus("LV Bus", 138.0)

        # Create transformer
        t1 = Transformer("T1", "HV Bus", "LV Bus", 0.002, 0.08)

        # Use Bus registry to find indices of connected buses
        bus1_index = Bus.get_bus_index(t1.bus1_name)
        bus2_index = Bus.get_bus_index(t1.bus2_name)

        self.assertEqual(bus1_index, 0)
        self.assertEqual(bus2_index, 1)

    def test_multiple_transformers_with_buses(self):
        """Test creating multiple transformers with multiple buses."""
        # Create a simple 4-bus system
        bus1 = Bus("Bus 1", 20.0)
        bus2 = Bus("Bus 2", 230.0)
        bus3 = Bus("Bus 3", 230.0)
        bus4 = Bus("Bus 4", 115.0)

        # Create transformers
        t1 = Transformer("T1", "Bus 1", "Bus 2", 0.01, 0.10)
        t2 = Transformer("T2", "Bus 3", "Bus 4", 0.015, 0.12)

        # Verify transformer connections
        self.assertEqual(Bus.get_bus_index(t1.bus1_name), bus1.bus_index)
        self.assertEqual(Bus.get_bus_index(t1.bus2_name), bus2.bus_index)
        self.assertEqual(Bus.get_bus_index(t2.bus1_name), bus3.bus_index)
        self.assertEqual(Bus.get_bus_index(t2.bus2_name), bus4.bus_index)

    def test_transformer_with_nonexistent_bus(self):
        """Test that transformer can reference buses that don't exist in registry."""
        # Create only one bus
        bus1 = Bus("Bus 1", 20.0)

        # Create transformer referencing a non-existent bus
        t1 = Transformer("T1", "Bus 1", "Bus 999", 0.01, 0.10)

        # Transformer should still be created
        self.assertEqual(t1.bus1_name, "Bus 1")
        self.assertEqual(t1.bus2_name, "Bus 999")

        # But lookup will show Bus 999 doesn't exist
        self.assertEqual(Bus.get_bus_index("Bus 1"), 0)
        self.assertIsNone(Bus.get_bus_index("Bus 999"))

    def test_realistic_power_system(self):
        """Test a realistic power system scenario with buses and transformer."""
        # Generator bus at 20kV
        gen_bus = Bus("Generator Bus", 20.0)

        # Transmission bus at 230kV
        trans_bus = Bus("Transmission Bus", 230.0)

        # Step-up transformer
        step_up = Transformer("Step-Up T1", "Generator Bus", "Transmission Bus", 0.01, 0.10)

        # Verify the system
        self.assertEqual(gen_bus.bus_index, 0)
        self.assertEqual(trans_bus.bus_index, 1)
        self.assertEqual(step_up.bus1_name, "Generator Bus")
        self.assertEqual(step_up.bus2_name, "Transmission Bus")

        # Verify we can look up buses connected to transformer
        self.assertEqual(Bus.get_bus_index(step_up.bus1_name), 0)
        self.assertEqual(Bus.get_bus_index(step_up.bus2_name), 1)

    def test_transformer_network_topology(self):
        """Test building a simple network topology with buses and transformers."""
        # Create a 3-bus system with 2 transformers
        buses = [
            Bus("Gen Bus", 20.0),
            Bus("HV Bus", 230.0),
            Bus("MV Bus", 115.0)
        ]

        transformers = [
            Transformer("T1", "Gen Bus", "HV Bus", 0.01, 0.10),
            Transformer("T2", "HV Bus", "MV Bus", 0.015, 0.12)
        ]

        # Verify all buses are registered
        self.assertEqual(len(Bus._bus_registry), 3)

        # Verify transformer connections form a chain
        self.assertEqual(transformers[0].bus2_name, transformers[1].bus1_name)

        # Verify we can trace the path: Gen -> HV -> MV
        self.assertEqual(Bus.get_bus_index(transformers[0].bus1_name), 0)  # Gen
        self.assertEqual(Bus.get_bus_index(transformers[0].bus2_name), 1)  # HV
        self.assertEqual(Bus.get_bus_index(transformers[1].bus2_name), 2)  # MV


if __name__ == '__main__':
    unittest.main()