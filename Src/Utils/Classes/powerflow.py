"""
Milestone 8: Newton–Raphson power flow solver.

Mismatch vector f uses the same physics as Milestone 6, in block order to match
Milestone 7 Jacobian rows: [all ΔP for non-slack][all ΔQ for PQ only].
"""

import numpy as np

from Src.Utils.Classes.jacobian import Jacobian


class PowerFlow:
    """
    Newton–Raphson solver: updates bus angles and PQ voltage magnitudes until
    mismatch is below tolerance or max_iter is reached.
    """

    def __init__(self):
        self._jac = Jacobian()
        self.iterations = 0
        self.converged = False
        self.final_mismatch_max = None

    @staticmethod
    def _non_slack_buses(buses: dict):
        return [b for b in buses.values() if b.bus_type != "Slack"]

    @staticmethod
    def _pq_buses(buses: dict):
        return [b for b in buses.values() if b.bus_type == "PQ"]

    def _mismatch_vector_block_ordered(self, circuit, buses: dict, ybus, voltages) -> np.ndarray:
        specs = {name: [0.0, 0.0] for name in buses}
        for gen in circuit.generators.values():
            specs[gen.bus1_name][0] += gen.p
        for load in circuit.loads.values():
            specs[load.bus1_name][0] -= load.p
            specs[load.bus1_name][1] -= load.q

        p_buses = self._non_slack_buses(buses)
        pq_buses = self._pq_buses(buses)

        f_list = []
        for bus in p_buses:
            p_spec, _ = specs[bus.name]
            p_calc, _ = circuit.compute_power_injection(bus, ybus, voltages)
            f_list.append(p_spec - p_calc)
        for bus in pq_buses:
            _, q_spec = specs[bus.name]
            _, q_calc = circuit.compute_power_injection(bus, ybus, voltages)
            f_list.append(q_spec - q_calc)
        return np.asarray(f_list, dtype=float)

    def mismatch_vector(self, circuit) -> np.ndarray:
        """Block-ordered mismatch f for current bus state (same order as Jacobian rows)."""
        return self._mismatch_vector_block_ordered(
            circuit, circuit.buses, circuit.ybus, circuit.voltage_vector_rectangular
        )

    def solve(self, circuit, tol: float = 0.001, max_iter: int = 50, verbose: bool = False):
        """
        Run Newton–Raphson on ``circuit`` (``vpu``, ``delta`` in degrees on each bus).

        Requires ``circuit.calc_ybus()`` already called.

        Bus updates: Slack excluded; PV — angle only; PQ — angle and |V|.
        Linear step: **J Δx = f** with J = ∂(P_calc,Q_calc)/∂(δ,|V|), f = spec − calc.
        """
        buses = circuit.buses
        ybus = circuit.ybus
        if ybus is None:
            raise ValueError("circuit.ybus is None; call circuit.calc_ybus() first.")

        self.converged = False
        self.iterations = 0
        self.final_mismatch_max = None
        f = None

        for k in range(max_iter):
            v_complex = circuit.voltage_vector_rectangular
            f = self._mismatch_vector_block_ordered(circuit, buses, ybus, v_complex)
            self.final_mismatch_max = float(np.max(np.abs(f)))

            if verbose:
                print(f"  NR iter {k}: max|f| = {self.final_mismatch_max:.6g}")

            if self.final_mismatch_max < tol:
                self.converged = True
                self.iterations = k
                return self

            angles = circuit.bus_angles()
            vmag = circuit.bus_voltages()
            J = self._jac.calculate_jacobian(buses, ybus, angles, vmag)
            dx = np.linalg.solve(J, f)

            p_buses = self._non_slack_buses(buses)
            pq_buses = self._pq_buses(buses)
            n_p = len(p_buses)

            for r, bus in enumerate(p_buses):
                bus.delta += float(np.rad2deg(dx[r]))
            for c, bus in enumerate(pq_buses):
                bus.vpu += float(dx[n_p + c])

            self.iterations = k + 1

        self.converged = False
        return self
