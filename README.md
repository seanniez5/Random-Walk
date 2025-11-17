Random Walk Simulation

This project seeks to simulate a simple random walk. The user will define a number of walkers, and a total number of steps. At each step, each walker will travel in a random direction at a distance of either 1 or -1. The backend calculations of the simulation are handled in C++, whereas the user-interface and graphing is handled using python. 



Visualization

Individual Paths: On the left-hand side, the complete trajectories of the first 5 walkers are displayed.

Ensemble-Averaged Squared Displacement: On the right-hand side, a plot shows the average squared distance of all walkers from the origin as a function of time (​t).  This quantity is computed as follows:

\[
\langle r^2(t) \rangle = \frac{1}{N} \sum_{i=1}^{N} \big(x_i(t)^2 + y_i(t)^2\big)
\]

where \(N\) is the number of walkers and \((x_i(t), y_i(t))\) is the position of walker \(i\) at step \(t\).