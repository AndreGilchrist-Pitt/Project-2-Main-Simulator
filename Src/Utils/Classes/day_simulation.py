import numpy as np


class DaySimulation:
    """
    One-day solar resource timeline: irradiance on a fixed 15-minute grid.

    Irradiance follows a smooth diurnal shape, zero at the day boundaries
    (midnight) and maximum at solar noon (middle of the 24 h window).
    """

    STEP_HOURS = 0.25  # 15 minutes
    N_STEPS = 96  # 24 h / 15 min

    def __init__(self, peak_irradiance: float = 1000.0):
        """
        Args:
            peak_irradiance: Maximum irradiance at noon in W/m² (default 1000, STC-like).
        """
        self.peak_irradiance = float(peak_irradiance)
        self.time_hours = np.arange(0.0, 24.0, self.STEP_HOURS, dtype=float)
        self.irradiance = self._build_irradiance_profile()

    def _build_irradiance_profile(self) -> np.ndarray:
        """sin²(pi * t / 24): peaks at t = 12 h, zero at t = 0 and t = 24 h."""
        t = self.time_hours
        shape = np.sin(np.pi * t / 24.0) ** 2
        return self.peak_irradiance * shape

    def __repr__(self) -> str:
        return (
            f"DaySimulation(peak_irradiance={self.peak_irradiance} W/m², "
            f"n_steps={self.N_STEPS}, step={self.STEP_HOURS} h)"
        )

    def plot_irradiance(self) -> None:
        """Plot irradiance vs time of day (system solar input)."""
        import matplotlib.pyplot as plt

        _, ax = plt.subplots(figsize=(9, 4))
        ax.plot(self.time_hours, self.irradiance, color="#e8941a", linewidth=1.8, marker=".", markersize=4)
        ax.set_xlabel("Time (hours from midnight)")
        ax.set_ylabel("Irradiance (W/m²)")
        ax.set_title("Daily irradiance profile (15-minute steps)")
        ax.set_xlim(0.0, 24.0)
        ax.set_ylim(bottom=0.0)
        ax.grid(True, alpha=0.35)
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    DaySimulation().plot_irradiance()
