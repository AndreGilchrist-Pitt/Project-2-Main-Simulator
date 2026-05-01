## Project 3 — time-series power flow + solar

### How to run

Run the project3_main.py script from the repo root.

User can change the time here:
#SET TIME HERE, 0-24 hour scale, w/ 15 minute intervals
time_window = "10:00-13:00"

That script utilizes 3 additional classes specific to Project 3.

day_simulation.py
- creates the irradiance throughout the day at 15 minute intervals for 24 hours for a total of 360 steps
- the irradiance vs time plot can be viewed if matlabplot package is installed

solar_generation.py
- this acts a circuit component modeling the solar panels and solar generation. 
- user input is P and PF, user has the option to change the G cap and choose whether leading or lagging (lagging is more common for solar panels)
- power generation and irradiance vs time plot can be viewed if matlabplot package is installed

time_series_solver.py
- this creates the time series simulation
- step time is automatically chosen to be 15 minutes
- user can input the time window in hours (e.g. 11:00-13:00)
- class utilizes the solver.py for the powerflow algorithm