import unittest
import sys

# Add project root to path for imports using centralized paths
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from Paths.paths import PROJECT_ROOT

sys.path.insert(0, str(PROJECT_ROOT))

from Src.Utils.Classes.circuit import Circuit
from Src.Utils.Classes.bus import Bus


class TestCircuit(unittest.TestCase):
    """Unit tests for the Circuit class."""

    def setUp(self):
        """Reset the Bus registry before each test."""
        Bus._bus_counter = 0
        Bus._bus_registry.clear()

    def test_circuit_creation(self):
        """Test that a Circuit can be created with correct attributes."""
        circuit = Circuit("Test Circuit")

        self.assertEqual(circuit.name, "Test Circuit")
        self.assertIsInstance(circuit.name, str)

    def test_attribute_initialization(self):
        """Test that all equipment dictionaries are initialized as empty dicts."""
        circuit = Circuit("Test Circuit")

        self.assertIsInstance(circuit.buses, dict)
        self.assertIsInstance(circuit.transformers, dict)
        self.assertIsInstance(circuit.transmission_lines, dict)
        self.assertIsInstance(circuit.generators, dict)
        self.assertIsInstance(circuit.loads, dict)

        self.assertEqual(len(circuit.buses), 0)
        self.assertEqual(len(circuit.transformers), 0)
        self.assertEqual(len(circuit.transmission_lines), 0)
        self.assertEqual(len(circuit.generators), 0)
        self.assertEqual(len(circuit.loads), 0)

    def test_add_bus(self):
        """Test adding a bus to the circuit."""
        circuit = Circuit("Test Circuit")
        circuit.add_bus("Bus1", 230.0)

        self.assertEqual(len(circuit.buses), 1)
        self.assertIn("Bus1", circuit.buses)
        self.assertEqual(circuit.buses["Bus1"].name, "Bus1")
        self.assertEqual(circuit.buses["Bus1"].nominal_kv, 230.0)

    def test_add_multiple_buses(self):
        """Test adding multiple buses to the circuit."""
        circuit = Circuit("Test Circuit")
        circuit.add_bus("Bus1", 230.0)
        circuit.add_bus("Bus2", 115.0)
        circuit.add_bus("Bus3", 345.0)

        self.assertEqual(len(circuit.buses), 3)
        self.assertIn("Bus1", circuit.buses)
        self.assertIn("Bus2", circuit.buses)
        self.assertIn("Bus3", circuit.buses)

    def test_add_duplicate_bus(self):
        """Test that adding a duplicate bus raises ValueError."""
        circuit = Circuit("Test Circuit")
        circuit.add_bus("Bus1", 230.0)

        with self.assertRaises(ValueError) as context:
            circuit.add_bus("Bus1", 115.0)

        self.assertIn("Bus1", str(context.exception))
        self.assertIn("already exists", str(context.exception))

    def test_add_transformer(self):
        """Test adding a transformer to the circuit."""
        circuit = Circuit("Test Circuit")
        circuit.add_transformer("T1", "Bus1", "Bus2", 0.01, 0.05)

        self.assertEqual(len(circuit.transformers), 1)
        self.assertIn("T1", circuit.transformers)
        self.assertEqual(circuit.transformers["T1"].name, "T1")
        self.assertEqual(circuit.transformers["T1"].bus1_name, "Bus1")
        self.assertEqual(circuit.transformers["T1"].bus2_name, "Bus2")
        self.assertEqual(circuit.transformers["T1"].r, 0.01)
        self.assertEqual(circuit.transformers["T1"].x, 0.05)

    def test_add_duplicate_transformer(self):
        """Test that adding a duplicate transformer raises ValueError."""
        circuit = Circuit("Test Circuit")
        circuit.add_transformer("T1", "Bus1", "Bus2", 0.01, 0.05)

        with self.assertRaises(ValueError) as context:
            circuit.add_transformer("T1", "Bus3", "Bus4", 0.02, 0.10)

        self.assertIn("T1", str(context.exception))
        self.assertIn("already exists", str(context.exception))

    def test_add_transmission_line(self):
        """Test adding a transmission line to the circuit."""
        circuit = Circuit("Test Circuit")
        circuit.add_transmission_line("Line1", "Bus1", "Bus2", 0.02, 0.06, 0.0, 0.04)

        self.assertEqual(len(circuit.transmission_lines), 1)
        self.assertIn("Line1", circuit.transmission_lines)
        self.assertEqual(circuit.transmission_lines["Line1"].name, "Line1")
        self.assertEqual(circuit.transmission_lines["Line1"].bus1_name, "Bus1")
        self.assertEqual(circuit.transmission_lines["Line1"].bus2_name, "Bus2")
        self.assertEqual(circuit.transmission_lines["Line1"].r, 0.02)
        self.assertEqual(circuit.transmission_lines["Line1"].x, 0.06)
        self.assertEqual(circuit.transmission_lines["Line1"].g, 0.0)
        self.assertEqual(circuit.transmission_lines["Line1"].b, 0.04)

    def test_add_duplicate_transmission_line(self):
        """Test that adding a duplicate transmission line raises ValueError."""
        circuit = Circuit("Test Circuit")
        circuit.add_transmission_line("Line1", "Bus1", "Bus2", 0.02, 0.06, 0.0, 0.04)

        with self.assertRaises(ValueError) as context:
            circuit.add_transmission_line("Line1", "Bus3", "Bus4", 0.03, 0.07, 0.0, 0.05)

        self.assertIn("Line1", str(context.exception))
        self.assertIn("already exists", str(context.exception))

    def test_add_generator(self):
        """Test adding a generator to the circuit."""
        circuit = Circuit("Test Circuit")
        circuit.add_generator("Gen1", "Bus1", 1.05, 100.0)

        self.assertEqual(len(circuit.generators), 1)
        self.assertIn("Gen1", circuit.generators)
        self.assertEqual(circuit.generators["Gen1"].name, "Gen1")
        self.assertEqual(circuit.generators["Gen1"].bus1_name, "Bus1")
        self.assertEqual(circuit.generators["Gen1"].voltage_setpoint, 1.05)
        self.assertEqual(circuit.generators["Gen1"].mw_setpoint, 100.0)

    def test_add_duplicate_generator(self):
        """Test that adding a duplicate generator raises ValueError."""
        circuit = Circuit("Test Circuit")
        circuit.add_generator("Gen1", "Bus1", 1.05, 100.0)

        with self.assertRaises(ValueError) as context:
            circuit.add_generator("Gen1", "Bus2", 1.02, 150.0)

        self.assertIn("Gen1", str(context.exception))
        self.assertIn("already exists", str(context.exception))

    def test_add_load(self):
        """Test adding a load to the circuit."""
        circuit = Circuit("Test Circuit")
        circuit.add_load("Load1", "Bus2", 50.0, 25.0)

        self.assertEqual(len(circuit.loads), 1)
        self.assertIn("Load1", circuit.loads)
        self.assertEqual(circuit.loads["Load1"].name, "Load1")
        self.assertEqual(circuit.loads["Load1"].bus1_name, "Bus2")
        self.assertEqual(circuit.loads["Load1"].mw, 50.0)
        self.assertEqual(circuit.loads["Load1"].mvar, 25.0)

    def test_add_duplicate_load(self):
        """Test that adding a duplicate load raises ValueError."""
        circuit = Circuit("Test Circuit")
        circuit.add_load("Load1", "Bus2", 50.0, 25.0)

        with self.assertRaises(ValueError) as context:
            circuit.add_load("Load1", "Bus3", 75.0, 35.0)

        self.assertIn("Load1", str(context.exception))
        self.assertIn("already exists", str(context.exception))

    def test_complete_circuit(self):
        """Test building a complete circuit with all equipment types."""
        circuit = Circuit("Complete Test Circuit")

        # Add buses
        circuit.add_bus("Bus1", 230.0)
        circuit.add_bus("Bus2", 230.0)
        circuit.add_bus("Bus3", 115.0)

        # Add transformer
        circuit.add_transformer("T1", "Bus1", "Bus2", 0.01, 0.05)

        # Add transmission lines
        circuit.add_transmission_line("Line1", "Bus1", "Bus2", 0.02, 0.06, 0.0, 0.04)
        circuit.add_transmission_line("Line2", "Bus2", "Bus3", 0.03, 0.08, 0.0, 0.05)

        # Add generators
        circuit.add_generator("Gen1", "Bus1", 1.05, 100.0)
        circuit.add_generator("Gen2", "Bus2", 1.02, 150.0)

        # Add loads
        circuit.add_load("Load1", "Bus2", 50.0, 25.0)
        circuit.add_load("Load2", "Bus3", 75.0, 35.0)

        # Verify all components were added
        self.assertEqual(len(circuit.buses), 3)
        self.assertEqual(len(circuit.transformers), 1)
        self.assertEqual(len(circuit.transmission_lines), 2)
        self.assertEqual(len(circuit.generators), 2)
        self.assertEqual(len(circuit.loads), 2)

    def test_unique_names_across_types(self):
        """Test that the same name can be used for different equipment types."""
        circuit = Circuit("Test Circuit")

        # Same name "Component1" used for different equipment types
        circuit.add_bus("Component1", 230.0)
        circuit.add_transformer("Component1", "Bus1", "Bus2", 0.01, 0.05)
        circuit.add_transmission_line("Component1", "Bus1", "Bus2", 0.02, 0.06, 0.0, 0.04)
        circuit.add_generator("Component1", "Bus1", 1.05, 100.0)
        circuit.add_load("Component1", "Bus2", 50.0, 25.0)

        # All should be added successfully
        self.assertEqual(len(circuit.buses), 1)
        self.assertEqual(len(circuit.transformers), 1)
        self.assertEqual(len(circuit.transmission_lines), 1)
        self.assertEqual(len(circuit.generators), 1)
        self.assertEqual(len(circuit.loads), 1)

    def test_empty_circuit_name(self):
        """Test creating a circuit with an empty name."""
        circuit = Circuit("")
        self.assertEqual(circuit.name, "")
        self.assertIsInstance(circuit.name, str)

    def test_circuit_name_persistence(self):
        """Test that circuit name persists after adding equipment."""
        circuit = Circuit("My Circuit")

        circuit.add_bus("Bus1", 230.0)
        circuit.add_transformer("T1", "Bus1", "Bus2", 0.01, 0.05)

        self.assertEqual(circuit.name, "My Circuit")

    def test_add_multiple_equipment_of_same_type(self):
        """Test adding multiple equipment of the same type with unique names."""
        circuit = Circuit("Test Circuit")

        # Add multiple buses
        for i in range(5):
            circuit.add_bus(f"Bus{i+1}", 230.0)

        # Add multiple transformers
        for i in range(3):
            circuit.add_transformer(f"T{i+1}", f"Bus{i+1}", f"Bus{i+2}", 0.01, 0.05)

        # Add multiple generators
        for i in range(4):
            circuit.add_generator(f"Gen{i+1}", f"Bus{i+1}", 1.05, 100.0)

        self.assertEqual(len(circuit.buses), 5)
        self.assertEqual(len(circuit.transformers), 3)
        self.assertEqual(len(circuit.generators), 4)


if __name__ == '__main__':
    unittest.main()
