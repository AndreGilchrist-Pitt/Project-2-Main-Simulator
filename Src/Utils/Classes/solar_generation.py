from __future__ import annotations

import math
import sys
from pathlib import Path

# Repo root (…/Project-2-Main-Simulator) so Play / `python solar_generation.py` resolves `Src.*`
# __file__ = …/Src/Utils/Classes/solar_generation.py → parents[3] = repo root
_repo_root = Path(__file__).resolve().parents[3]
if str(_repo_root) not in sys.path:
    sys.path.insert(0, str(_repo_root))

import numpy as np

from Src.Utils.Classes.day_simulation import DaySimulation
from Src.Utils.Classes.settings import Settings


class SolarGeneration:
    """
    Solar plant scheduled like a PQ injection: active power from irradiance (STC
    linear model). Voltage magnitude at the connection bus is an NR unknown when
    that bus is type PQ; reactive power follows PF or can be forced to zero.

    Rated ``p_mw`` is the nameplate at irradiance ``g_stc`` (default 1000 W/m²).
    Each step uses ``P ≈ P_rated * (G / G_stc)``, clipped to rated.
    """

    def __init__(
        self,
        name: str,
        bus1_name: str,
        p_mw: float,
        power_factor: float,
        day_simulation: DaySimulation,
        *,
        g_stc: float = 1000,
        leading_power_factor: bool = False,
        inject_reactive: bool = True,
    ):
        """
        Args:
            name: Element name / id.
            bus1_name: Bus where the solar plant is connected.
            p_mw: Nameplate real power (MW) at STC irradiance ``g_stc``.
            power_factor: Displacement power factor (0 < PF ≤ 1), used when
                ``inject_reactive`` is True.
            day_simulation: Provides ``irradiance`` (W/m²) on the 15-minute grid.
            g_stc: Irradiance (W/m²) at which the plant reaches ``p_mw`` before clipping.
            leading_power_factor: If True, use leading-PF sign on Q; default is lagging.
            inject_reactive: If False, Q is 0 at all steps (P still from irradiance).
        """
        if not 0.0 < power_factor <= 1.0:
            raise ValueError("power_factor must be in (0, 1].")
        if p_mw < 0.0:
            raise ValueError("p_mw (nameplate MW) must be non-negative.")
        if g_stc <= 0.0:
            raise ValueError("g_stc must be positive.")

        self.name = name
        self.bus1_name = bus1_name
        self.p_mw = float(p_mw)
        self.power_factor = float(power_factor)
        self.day_simulation = day_simulation
        self.g_stc = float(g_stc)
        self.leading_power_factor = bool(leading_power_factor)
        self.inject_reactive = bool(inject_reactive)

        self._tan_theta = 0.0
        if self.inject_reactive:
            theta = math.acos(self.power_factor)
            self._tan_theta = math.tan(theta)
            if self.leading_power_factor:
                self._tan_theta = -self._tan_theta

        g = np.asarray(day_simulation.irradiance, dtype=float)
        self.p_mw_profile = self.p_mw * np.minimum(1.0, g / self.g_stc)
        if self.inject_reactive:
            self.q_mvar_profile = self.p_mw_profile * self._tan_theta
        else:
            self.q_mvar_profile = np.zeros_like(self.p_mw_profile)

    def n_steps(self) -> int:
        return int(len(self.p_mw_profile))

    def p_mw_at_step(self, step: int) -> float:
        """Delivered active power (MW) at time index ``step``."""
        return float(self.p_mw_profile[step])

    def mvar_at_step(self, step: int) -> float:
        """Delivered reactive power (MVAR) at ``step`` for the chosen PF convention."""
        return float(self.q_mvar_profile[step])

    def calc_p_pu_at_step(self, step: int) -> float:
        """Active generation in per-unit on ``Settings.sbase``."""
        return self.p_mw_at_step(step) / Settings.sbase

    def calc_q_pu_at_step(self, step: int) -> float:
        """Reactive term in per-unit on ``Settings.sbase`` (see class docstring)."""
        return self.mvar_at_step(step) / Settings.sbase

    def __repr__(self) -> str:
        qmode = "PF" if self.inject_reactive else "Q=0"
        return (
            f"SolarGeneration(name='{self.name}', bus='{self.bus1_name}', "
            f"p_rated_mw={self.p_mw}, PF={self.power_factor}, g_stc={self.g_stc}, "
            f"q_mode={qmode}, steps={self.n_steps()})"
        )

    def plot_mw_over_day(self, show_irradiance: bool = True) -> None:
        """
        Matplotlib figure: active power (MW) vs time over 24 h (15-min steps).
        Optional right axis: irradiance (W/m²) from ``DaySimulation`` to show
        the resource scaled by ``g_stc`` into the MW profile.
        """
        import matplotlib.pyplot as plt

        t = np.asarray(self.day_simulation.time_hours, dtype=float)
        p = np.asarray(self.p_mw_profile, dtype=float)
        if len(t) != len(p):
            raise ValueError("time_hours and p_mw_profile length mismatch.")

        fig, ax_p = plt.subplots(figsize=(9, 4.5))
        ax_p.plot(
            t,
            p,
            color="#2a9d3a",
            linewidth=2.0,
            marker=".",
            markersize=4,
            label=f"P (MW), rated {self.p_mw} MW @ {self.g_stc:g} W/m²",
        )
        ax_p.set_xlabel("Time (hours from midnight)")
        ax_p.set_ylabel("Active power (MW)")
        ax_p.set_xlim(0.0, 24.0)
        ax_p.set_ylim(bottom=0.0)
        ax_p.grid(True, alpha=0.35)
        ax_p.set_title(f"Solar output — {self.name} ({self.n_steps()} steps, 15 min)")

        if show_irradiance:
            g = np.asarray(self.day_simulation.irradiance, dtype=float)
            ax_g = ax_p.twinx()
            ax_g.plot(
                t,
                g,
                color="#e8941a",
                linewidth=1.2,
                linestyle="--",
                alpha=0.9,
                label="Irradiance G (W/m²)",
            )
            ax_g.set_ylabel("Irradiance (W/m²)")
            ax_g.set_ylim(bottom=0.0)
            lines_p, labels_p = ax_p.get_legend_handles_labels()
            lines_g, labels_g = ax_g.get_legend_handles_labels()
            ax_p.legend(lines_p + lines_g, labels_p + labels_g, loc="upper right")
        else:
            ax_p.legend(loc="upper right")

        fig.tight_layout()
        plt.show()


if __name__ == "__main__":
    day = DaySimulation(peak_irradiance=1000.0)
    pv = SolarGeneration(
        "Solar1",
        "Bus 5",
        p_mw=50.0,
        power_factor=0.95,
        day_simulation=day,
    )
    print(repr(pv))
    noon_step = int(12.0 / DaySimulation.STEP_HOURS)
    print(
        f"At step {noon_step} (noon): P = {pv.p_mw_at_step(noon_step):.3f} MW, "
        f"Q = {pv.mvar_at_step(noon_step):.3f} MVAR"
    )
    print(f"p pu @ noon: {pv.calc_p_pu_at_step(noon_step):.5f}")
    pv.plot_mw_over_day()
