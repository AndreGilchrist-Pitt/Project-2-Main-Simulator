"""
Time-series power flow over a sub-window of the 15-minute day grid, using Solver.
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, List, Optional, Tuple, Union

import numpy as np

# Repo root so Play / `python time_series_solver.py` resolves `Src.*`
# __file__ = …/Src/Utils/Classes/time_series_solver.py → parents[3] = repo root
_repo_root = Path(__file__).resolve().parents[3]
if str(_repo_root) not in sys.path:
    sys.path.insert(0, str(_repo_root))

from Src.Utils.Classes.day_simulation import DaySimulation
from Src.Utils.Classes.solar_generation import SolarGeneration
from Src.Utils.Classes.solver import Solver

TimeRangeSpec = Union[str, Tuple[float, float], Tuple[int, int]]


def parse_time_range(spec: TimeRangeSpec) -> Tuple[float, float]:
    """
    Parse a time window in hours from midnight.

    Accepts:
        - (t0, t1) or (h0, h1) in hours (float or int), order may be reversed.
        - "1-3" → 1.0 h to 3.0 h
        - "2:15-4:45" or "2:15 - 4:45" → fractional hours

    Returns:
        (t_lo, t_hi) with t_lo <= t_hi, in hours in [0, 24].
    """
    if isinstance(spec, tuple):
        a, b = float(spec[0]), float(spec[1])
    else:
        s = spec.strip()
        m = re.match(
            r"^\s*(\d{1,2}):(\d{2})\s*-\s*(\d{1,2}):(\d{2})\s*$",
            s,
        )
        if m:
            h1, mi1, h2, mi2 = (int(m.group(i)) for i in range(1, 5))
            if not (0 <= mi1 < 60 and 0 <= mi2 < 60):
                raise ValueError(f"Minutes must be in 0..59: {spec!r}")
            a = h1 + mi1 / 60.0
            b = h2 + mi2 / 60.0
        else:
            parts = re.split(r"\s*-\s*", s)
            if len(parts) != 2:
                raise ValueError(
                    f"Expected 'start-end' or 'H:MM-H:MM', got {spec!r}"
                )
            a = float(parts[0])
            b = float(parts[1])

    if a > b:
        a, b = b, a
    a = max(0.0, min(24.0, a))
    b = max(0.0, min(24.0, b))
    if a > b:
        a, b = b, a
    return a, b


def time_hours_grid(step_hours: float) -> np.ndarray:
    """Sample times from midnight [0, 24) on a uniform step (default 15 min)."""
    if step_hours <= 0.0:
        raise ValueError("step_hours must be positive.")
    return np.arange(0.0, 24.0, step_hours, dtype=float)


def step_indices_in_range(
    t_lo: float,
    t_hi: float,
    time_hours: np.ndarray,
    *,
    inclusive: bool = True,
) -> List[int]:
    """
    Indices into ``time_hours`` whose times lie in [t_lo, t_hi] (inclusive both
    ends by default). Uses a small tolerance so float edges match the grid.
    """
    eps = 1e-6
    idx: List[int] = []
    for i, t in enumerate(time_hours):
        if inclusive:
            if t_lo - eps <= t <= t_hi + eps:
                idx.append(i)
        else:
            if t_lo - eps <= t < t_hi - eps:
                idx.append(i)
    return idx


@dataclass
class TimeSeriesStepResult:
    step_index: int
    time_hours: float
    converged: bool
    iterations: int
    vpu_by_bus: dict
    delta_by_bus: dict


@dataclass
class TimeSeriesRunResult:
    steps: List[TimeSeriesStepResult] = field(default_factory=list)

    @property
    def all_converged(self) -> bool:
        return all(s.converged for s in self.steps)


class TimeSeriesSolver:
    """
    Run repeated power-flow solves on a ``Circuit`` over selected 15-minute
    (or custom ``step_hours``) steps, using :class:`Solver` in ``power_flow`` mode.

    Solar dispatch:

    - **Circuit-integrated:** use :meth:`Circuit.add_solar_generation`; each step
      calls :meth:`Circuit.set_solar_dispatch_step` so mismatch includes solar
      P and Q at that index.
    - **Legacy:** pass ``solar`` and ``solar_generator_name`` to overwrite a
      generator's MW each step (avoid also duplicating the same plant on the circuit).
    """

    def __init__(
        self,
        circuit,
        *,
        solar: Optional[SolarGeneration] = None,
        solar_generator_name: Optional[str] = None,
        step_hours: Optional[float] = None,
    ):
        """
        Args:
            circuit: Built ``Circuit`` with ``calc_ybus()`` already done.
            solar: Legacy: with ``solar_generator_name``, updates that generator's
                ``mw_setpoint`` / ``p`` each step from this object.
            solar_generator_name: Legacy generator name to overwrite each step.
            step_hours: Grid spacing in hours; default from circuit solar or
                ``DaySimulation.STEP_HOURS``.
        """
        self.circuit = circuit
        self.solar = solar
        self.solar_generator_name = solar_generator_name

        if step_hours is not None:
            self.step_hours = float(step_hours)
        elif circuit.solar_generations:
            first = next(iter(circuit.solar_generations.values()))
            self.step_hours = float(first.day_simulation.STEP_HOURS)
        else:
            self.step_hours = DaySimulation.STEP_HOURS

        self._solver = Solver(mode="power_flow")

        if solar is not None and solar_generator_name is None:
            raise ValueError(
                "solar_generator_name is required when solar is provided."
            )
        if solar is None and solar_generator_name is not None:
            raise ValueError(
                "solar must be provided when solar_generator_name is set."
            )
        if solar is not None:
            if abs(solar.day_simulation.STEP_HOURS - self.step_hours) > 1e-9:
                raise ValueError(
                    "SolarGeneration day grid step must match TimeSeriesSolver "
                    f"step_hours ({self.step_hours} != {solar.day_simulation.STEP_HOURS})."
                )
        elif circuit.solar_generations:
            first = next(iter(circuit.solar_generations.values()))
            if abs(first.day_simulation.STEP_HOURS - self.step_hours) > 1e-9:
                raise ValueError(
                    "Circuit solar day grid step must match TimeSeriesSolver "
                    f"step_hours ({self.step_hours} != {first.day_simulation.STEP_HOURS})."
                )

    def _time_hours(self) -> np.ndarray:
        if self.solar is not None:
            return np.asarray(self.solar.day_simulation.time_hours, dtype=float)
        if self.circuit.solar_generations:
            first = next(iter(self.circuit.solar_generations.values()))
            return np.asarray(first.day_simulation.time_hours, dtype=float)
        return time_hours_grid(self.step_hours)

    def _apply_solar_to_generator(self, step_index: int) -> None:
        assert self.solar is not None and self.solar_generator_name is not None
        gen = self.circuit.generators.get(self.solar_generator_name)
        if gen is None:
            raise KeyError(
                f"Generator '{self.solar_generator_name}' not in circuit.generators."
            )
        mw = self.solar.p_mw_at_step(step_index)
        gen.mw_setpoint = float(mw)
        gen.p = gen.calc_p()

    def run(
        self,
        time_range: TimeRangeSpec,
        *,
        apply_step: Optional[Callable[[int, float], None]] = None,
        tol: float = 1e-4,
        max_iter: int = 50,
        verbose: bool = False,
    ) -> TimeSeriesRunResult:
        """
        Solve power flow at each timestep in the parsed window.

        Args:
            time_range: e.g. ``(1, 3)``, ``"1-3"``, ``"2:15-4:45"`` (hours from midnight).
            apply_step: Optional ``callable(step_index, time_hours)`` invoked before
                each solve (after solar MW update, if configured). Mutate ``circuit``.
            tol, max_iter, verbose: Passed to :meth:`Solver.run` for power flow.

        Returns:
            TimeSeriesRunResult with one entry per solved timestep.
        """
        if self.circuit.ybus is None:
            raise ValueError("circuit.calc_ybus() must be called before run().")

        t_lo, t_hi = parse_time_range(time_range)
        th = self._time_hours()
        indices = step_indices_in_range(t_lo, t_hi, th, inclusive=True)
        if not indices:
            raise ValueError(
                f"No simulation steps in [{t_lo}, {t_hi}] h for step_hours={self.step_hours}."
            )

        result = TimeSeriesRunResult()

        for step_index in indices:
            t = float(th[step_index])

            if self.circuit.solar_generations:
                self.circuit.set_solar_dispatch_step(step_index)
            if self.solar is not None and self.solar_generator_name is not None:
                self._apply_solar_to_generator(step_index)

            if apply_step is not None:
                apply_step(step_index, t)

            self._solver.run(
                self.circuit, tol=tol, max_iter=max_iter, verbose=verbose
            )

            vpu = {b.name: float(b.vpu) for b in self.circuit.buses.values()}
            delta = {b.name: float(b.delta) for b in self.circuit.buses.values()}

            result.steps.append(
                TimeSeriesStepResult(
                    step_index=step_index,
                    time_hours=t,
                    converged=self._solver.converged,
                    iterations=self._solver.iterations,
                    vpu_by_bus=vpu,
                    delta_by_bus=delta,
                )
            )

        return result


