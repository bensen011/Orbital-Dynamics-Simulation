# Orbital Dynamics & Maneuver Simulator

## Overview:

An interacitve Python simulation that models Keplerian trajectories and calucltes the $\Delta v$ requirements for apsidal circularisation maneuvers. This tool visualises unpowered spaceflight and orbital phase shifting in real-time, functioning as a dynamics mission-control telemetry display.

## Key Features:

**Physics Engine:** Calulates real-time orbital velocity and maneuver requirements using the Vis-viva equation:


$$v = \sqrt{GM(2/r - 1/a)}$$

**Dynamic Rendering:** Utilises Matplotlib's _FuncAnimation_ to generate seamless track-switching between elliptical and circular coordinate arrays.

**Memory Management:** Implements a sliding-window algorithm for the satellite's telemetry trail, ensuring memory-efficinet rendering over 100,000+ frames.

**Interactive UI:** Reads a _.csv_ database of planetary parameters and handles dynamic user inputs for manoeuver selection (Periapsis vs. Apoapsis stabilisation)

## Dependencies:

To run this simulation, you will need Python 3 installed along with the following libraries:
- numpy
- scipy
- Matplotlib

## Usage:

1. Clone this repository to your local machine
2. Ensure Planets.csv is located in the same directory as the python script
3. Run the script via your terminal:
   ````python
   python Satellite_Orbit.py
4. Follow the terminal prompts to select a celestrial body, define your Apsides, and execute orbital manoeuvres.

## Visuals:

### Planets:



<img width="121" height="121"  alt="image" src="https://github.com/user-attachments/assets/fc424449-53d2-4368-b871-9fbfd98e6488"  />








