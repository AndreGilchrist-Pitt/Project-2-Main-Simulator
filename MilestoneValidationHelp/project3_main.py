"""
Project 3: seven-bus radial — two sync generators (slack + PV at Bus3) and
solar as a PQ injection at Bus4 (no Load there; solar replaces that bus load).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from Src.Utils.Classes.bus import Bus
from Src.Utils.Classes.circuit import Circuit
from Src.Utils.Classes.day_simulation import DaySimulation
from Src.Utils.Classes.settings import Settings
from Src.Utils.Classes.time_series_solver import TimeSeriesSolver

Bus._bus_counter = 0
Bus._bus_registry.clear()

Settings(freq=60.0, sbase=100.0)
circuit = Circuit("Project 3 - Seven-bus system + solar w/ Time Series Simulation")


circuit.add_bus("Bus1", 15.0, vpu=1.0, delta=0.0, bus_type="Slack")
circuit.add_bus("Bus2", 345.0, vpu=1.0, delta=0.0, bus_type="PQ")
circuit.add_bus("Bus3", 345.0, vpu=1.03, delta=0.0, bus_type="PV")
circuit.add_bus("Bus4", 345.0, vpu=1.0, delta=0.0, bus_type="PQ") # solar generation is attatched to PQ bus
circuit.add_bus("Bus5", 345.0, vpu=1.0, delta=0.0, bus_type="PQ")
circuit.add_bus("Bus6", 345.0, vpu=1.0, delta=0.0, bus_type="PQ")
circuit.add_bus("Bus7", 345.0, vpu=1.0, delta=0.0, bus_type="PQ")

circuit.add_transformer("T1", "Bus1", "Bus2", 0.0015, 0.02)

z_line = (0.003, 0.035, 0.0, 0.5)
circuit.add_transmission_line("L23", "Bus2", "Bus3", *z_line)
z_to_solar = (0.008, 0.08, 0.0, 1.0)
circuit.add_transmission_line("L34", "Bus3", "Bus4", *z_to_solar)
circuit.add_transmission_line("L45", "Bus4", "Bus5", *z_line)
circuit.add_transmission_line("L56", "Bus5", "Bus6", *z_line)
circuit.add_transmission_line("L67", "Bus6", "Bus7", *z_line)

circuit.add_generator("G1", "Bus1", 1.04, 0.0, x_subtransient=0.045)
circuit.add_generator("G2", "Bus3", 1.03, 120.0, x_subtransient=0.0225)

circuit.add_load("Ld2", "Bus2", 350.0, 120.0)
circuit.add_load("Ld5", "Bus5", 180.0, 70.0)
circuit.add_load("Ld6", "Bus6", 60.0, 20.0)
circuit.add_load("Ld7", "Bus7", 90.0, 30.0)

day = DaySimulation(peak_irradiance=1000.0)

circuit.add_solar_generation(
    "Solar1",
    "Bus4",
    220.0, # P = 220MW
    1.0, # unity
    day,
    g_stc=1000.0, # cap
    inject_reactive=False, # Q = 0
)

circuit.calc_ybus()

solar_plant = circuit.solar_generations["Solar1"]
ts = TimeSeriesSolver(circuit)

#SET TIME HERE, 0-24 hour scale, w/ 15 minute intervals
time_window = "9:00-12:00"

print(f"\nImplementing time series simulation along with solar generation.\n")
result = ts.run(time_window, tol=1e-4, max_iter=50, verbose=False)

print(f"Steps solved: {len(result.steps)}")
print(f"All converged: {result.all_converged}")

if result.steps:
    bus_names = sorted(result.steps[0].vpu_by_bus.keys())

    for s in result.steps:
        p_mw = solar_plant.p_mw_at_step(s.step_index)
        print(
            f"t = {s.time_hours:6.2f} hr,  steps = {s.step_index:2d},  "
            f"P_Solar1 (Bus 4) = {p_mw:7.3f} MW,  NR iters = {s.iterations},  converged = {s.converged}"
        )
        print(f"{'bus':8s}  {'vpu':>12s}  {'angle':>12s}")
        for name in bus_names:
            v = s.vpu_by_bus[name]
            ang = s.delta_by_bus[name]
            print(f"{name:8s}  {v:12.6f}  {ang:12.4f}")
        print()

print()
