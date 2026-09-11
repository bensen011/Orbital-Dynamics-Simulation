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

### Maintaining Orbit:

<img width="320" height="240" alt="Untitled - 11 September 2026 at 02 33 52" src="https://github.com/user-attachments/assets/1fa1711e-b2d6-40fe-a0c2-42f244a80783" />

### Periapsis Stabilisation:

<img width="320" height="240" alt="Untitled - 11 September 2026 at 02 33 52-2" src="https://github.com/user-attachments/assets/e780b110-bc64-4112-af8f-3bbc11de3b07" />

### Apoapsis Stabilisation:

<img width="320" height="240" alt="Untitled - 11 September 2026 at 02 33 52-3" src="https://github.com/user-attachments/assets/cb81d363-c8aa-420c-a8ce-266e05a8be42" />



