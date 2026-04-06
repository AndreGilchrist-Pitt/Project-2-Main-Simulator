"""
Unit tests for Src.Utils.Classes.powerflow.PowerFlow.

Run from project root:
    python -m unittest UnitTest.Classes.UnitTest_PowerFlow -v
"""

import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from Paths.paths import PROJECT_ROOT

sys.path.insert(0, str(PROJECT_ROOT))

import numpy as np

from Src.Utils.Classes.bus import Bus
from Src.Utils.Classes.circuit import Circuit
from Src.Utils.Classes.powerflow import PowerFlow
from Src.Utils.Classes.settings import Settings


def _make_five_bus_glover_circuit() -> Circuit:
    """Same topology as MilestoneValidationHelp/milestone8_main.py."""
    Bus._bus_counter = 0
    Bus._bus_registry.clear()
    Settings(freq=60.0, sbase=100.0)

    c = Circuit("UnitTest PowerFlow — five-bus")
    c.add_bus("Bus1", 15.0, vpu=1.0, delta=0.0, bus_type="Slack")
    c.add_bus("Bus2", 345.0, vpu=1.0, delta=0.0, bus_type="PQ")
    c.add_bus("Bus3", 15.0, vpu=1.05, delta=0.0, bus_type="PV")
    c.add_bus("Bus4", 345.0, vpu=1.0, delta=0.0, bus_type="PQ")
    c.add_bus("Bus5", 345.0, vpu=1.0, delta=0.0, bus_type="PQ")

    c.add_transformer("T1", "Bus1", "Bus5", 0.0015, 0.02)
    c.add_transformer("T2", "Bus3", "Bus4", 0.00075, 0.01)
    c.add_transmission_line("Line1", "Bus4", "Bus2", 0.009, 0.1, 0.0, 1.72)
    c.add_transmission_line("Line2", "Bus5", "Bus2", 0.0045, 0.05, 0.0, 0.88)
    c.add_transmission_line("Line3", "Bus5", "Bus4", 0.00225, 0.025, 0.0, 0.44)

    c.add_generator("G1", "Bus1", 1.0, 0.0)
    c.add_generator("G2", "Bus3", 1.0, 520.0)
    c.add_load("Load2", "Bus2", 800.0, 280.0)
    c.add_load("Load3", "Bus3", 80.0, 40.0)

    c.calc_ybus()
    return c


class TestPowerFlow(unittest.TestCase):
    """Unit tests for PowerFlow."""

    def setUp(self):
        Bus._bus_counter = 0
        Bus._bus_registry.clear()

    def test_initial_attributes(self):
        pf = PowerFlow()
        self.assertFalse(pf.converged)
        self.assertEqual(pf.iterations, 0)
        self.assertIsNone(pf.final_mismatch_max)

    def test_solve_raises_without_ybus(self):
        Settings(freq=60.0, sbase=100.0)
        c = Circuit("empty ybus")
        c.add_bus("B1", 230.0, bus_type="Slack")
        c.add_bus("B2", 230.0, bus_type="PQ")
        c.add_transformer("T1", "B1", "B2", 0.01, 0.1)
        # intentionally skip calc_ybus()
        pf = PowerFlow()
        with self.assertRaises(ValueError) as ctx:
            pf.solve(c)
        self.assertIn("calc_ybus", str(ctx.exception).lower())

    def test_mismatch_vector_length_matches_jacobian(self):
        c = _make_five_bus_glover_circuit()
        pf = PowerFlow()
        f = pf.mismatch_vector(c)
        self.assertEqual(len(f), 7)

        J = pf._jac.calculate_jacobian(
            c.buses, c.ybus, c.bus_angles(), c.bus_voltages()
        )
        self.assertEqual(J.shape, (7, 7))

    def test_five_bus_converges(self):
        c = _make_five_bus_glover_circuit()
        slack_v = c.buses["Bus1"].vpu
        slack_d = c.buses["Bus1"].delta
        pv_v = c.buses["Bus3"].vpu

        pf = PowerFlow()
        pf.solve(c, tol=0.001, max_iter=50, verbose=False)

        self.assertTrue(pf.converged, "NR should converge on five-bus case")
        self.assertLess(pf.final_mismatch_max, 0.001)
        self.assertLess(np.max(np.abs(pf.mismatch_vector(c))), 0.001)

        self.assertAlmostEqual(c.buses["Bus1"].vpu, slack_v, places=9)
        self.assertAlmostEqual(c.buses["Bus1"].delta, slack_d, places=9)
        self.assertAlmostEqual(c.buses["Bus3"].vpu, pv_v, places=9)

    def test_five_bus_solution_near_reference(self):
        """Regression check against known converged state (milestone8_main output)."""
        c = _make_five_bus_glover_circuit()
        PowerFlow().solve(c, tol=1e-4, max_iter=50)

        b2, b3, b4, b5 = c.buses["Bus2"], c.buses["Bus3"], c.buses["Bus4"], c.buses["Bus5"]
        self.assertAlmostEqual(b2.vpu, 0.833770, places=4)
        self.assertAlmostEqual(b2.delta, -22.406301, places=2)
        self.assertAlmostEqual(b3.vpu, 1.05, places=5)
        self.assertAlmostEqual(b3.delta, -0.597336, places=2)
        self.assertAlmostEqual(b4.vpu, 1.019303, places=4)
        self.assertAlmostEqual(b5.vpu, 0.974289, places=4)

    def test_max_iter_zero_does_not_crash(self):
        c = _make_five_bus_glover_circuit()
        pf = PowerFlow()
        pf.solve(c, tol=1e-9, max_iter=0)
        self.assertFalse(pf.converged)


if __name__ == "__main__":
    unittest.main()
