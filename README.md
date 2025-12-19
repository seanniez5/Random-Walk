# Random Walk Simulation with Anomalous Diffusion

## Overview
This project implements a two-dimensional random walk simulation that supports normal diffusion, subdiffusion, and superdiffusion, with optional drift factors and bounded domains. The core of the simulation is written in C++ for its superior performance, with data analysis and visualization done in Python.  

The goal of the project is to explore how different stochastic step and waiting-time distributions affect ensemble-averaged behavior by analyzing mean squared displacement and walking patterns.

## Mathematical Model  
Each walker evolves in continuous space according to a stochastic update rule:  
* **Normal Diffusion**: Steps are drawn from a uniform distribution.
* **Subdiffusion**: Walkers experience heavy-tailed waiting times between steps, sampled from a Pareto distribution, leading to sublinear presentations of mean squared displacement.
* **Superdiffusion**: Step lengths are drawn from a heavy-tailed Pareto distribution with random directions, producing a Lévy flight-like behavior.

For an ensemble of walkers, the expected squared displacement is computed as follows:  

<div align="center">
  <img width="247" height="37" alt="equation" src="https://github.com/user-attachments/assets/0f12ce4d-0587-4ac9-92cf-48cc84a12595" />
</div>



Optional square-domain boundary constraints can be imposed to study confinement effects.  

## Implementation Details  
* C++ handles the simulation loop, random number generation, and CSV output.
* Walkers are stored as position vectors
* Inverse transform sampling is used to generate Pareto-distributed waiting times and step lengths.
* Python serves as a frontend for parameter input, compiling C++ code, and visualization with pandas and matplotlib

## Usage  
The Python script prompts the user for:
* Number of walkers
* Number of steps
* Drift parameters
* Domain size
* diffusion type (normal / subdiffusive / superdiffusive)

It then executes the C++ backend and produces plots automatically.

## Example Results  
Outputs include:
* Individual walker trajectories
* Heatmaps of visited spatial locations
* Ensemble-averaged mean squared displacement vs. time
* Distribution of final walker displacements

In this example, the following parameters were simulated:  
* Number of walkers: *250*
* Number of steps: *50,000*
* x-axis drift: *0*
* y-axis drift: *0.00002*
* Half-width of square domain: *150*
* Diffusion type: *Normal*

<img width="1620" height="1236" alt="results" src="https://github.com/user-attachments/assets/bf87678f-04f2-41fc-a4ba-d4bcfd79c319" />
<p align="center"><em>
Figure 1: Individual trajectories, spatial heatmap, ensemble-averaged mean squared displacement, and final displacement distribution for a 2D normal diffusion process (250 walkers, 50,000 steps).
</em></p>
