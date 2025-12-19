#include <fstream>
#include <iomanip>
#include <iostream>
#include <string>
#include <vector>
#include <random>
#include <cmath>
#include <algorithm>
using namespace std;

double computeSquaredDisplacement(const vector<vector<double>>& walkers) {
    // compute the expected squared displacement at each step
    double sumSquaredDisplacement = 0.0; // accumulator for the summation
    for (const auto& walker:walkers) {
        double squaredDisplacement = 0.0; // squared displacement for an individual walker
        for (int d = 0; d < 2; d++) {
            squaredDisplacement += walker[d] * walker[d]; // square the x and y components from position vector
        }
        sumSquaredDisplacement += squaredDisplacement; // add to the sum of the squared displacement
    }
    return sumSquaredDisplacement / walkers.size();
}


int main(int argc, char* argv[]) {

    // command line arguments from python frontend

    // get the number of walkers for the simulation
    int numWalkers;
    if (argc > 1) {
        numWalkers = stoi(argv[1]);
    } else {
        numWalkers = 10; // default number of walkers = 10
    }

    // number of steps
    int numSteps;
    if (argc > 2) {
        numSteps = stoi(argv[2]);
    } else {
        numSteps = 50; // default number of steps = 50
    }

    // x-axis drift
    double driftX = 0;
    if (argc > 3) {
        driftX = stod(argv[3]);
    }

    // y-axis drift
    double driftY = 0;
    if (argc > 4) {
        driftY = stod(argv[4]);
    }

    int domainSize = 100;
    if (argc > 5) {
        domainSize = stoi(argv[5]);
    }

    // diffusion type
    int diffusionType = 0;
    if (argc > 6) {
        diffusionType = stoi(argv[6]);
    }


    // random number generation
    // https://en.cppreference.com/w/cpp/numeric/random/uniform_int_distribution.html
    random_device rd;
    mt19937 gen(rd());
    uniform_real_distribution<double> stepDistribution(-1.0, 1.0); // step -1, or 1
    uniform_real_distribution<double> positionDistribution(-domainSize, domainSize);
    uniform_real_distribution<double> paretoDraw(0.0, 1.0); // uniform distribution for pareto distribution

    // initialize walkers
    // vector storing each walker and their x,y coords initialized at (0, 0)
    vector<vector<double>> walkers(numWalkers, vector<double>(2, 0.0));

    // number of steps each walker must wait (subdiffusive), initialized at 0
    vector<int> waitCounter(numWalkers, 0);

    ofstream out("randomwalk.csv"); // initialize the output file
    out << "step,exp_squared_disp"; // step and expected squared displacement columns

    // add columns for the walkers
    for (int w = 0; w < numWalkers; w++ ) { // for every walker
        out << ",walker" << w << "_x,walker" << w << "_y"; // ex: walker0_x, walker0_y. x and y columns for each walker
    }
    out << "\n";


    // loop to add position data to the CSV for all steps and for all walkers
    for (int s = 0; s <= numSteps; s++) {

        // update the displacement
        double expectedSquaredDisplacement = computeSquaredDisplacement(walkers);

        // write the row to CSV
        out << s << "," << expectedSquaredDisplacement; // step, expected displacement
        for (auto& walker:walkers) {
            out << "," << walker[0] << "," << walker[1]; // x and y coordinates
        }
        out << "\n";

        // if user defined number of steps is reached, exit
        if (s == numSteps) {
            break;
        }

        for (int i = 0; i < numWalkers; i++) { // loop through each walker

            auto& walker = walkers[i]; // assign a walker to the current walker in the vector

            // pareto distribution time waiting (subdiffusion)
            if (diffusionType == 1) {
                if (waitCounter[i] > 0) { // if the walker has more than 0 steps to wait
                    waitCounter[i]--; // decrement number of steps to wait
                    continue; // walkers cant make two consecutive moves
                }

                double u = paretoDraw(gen); // draw a random number between 0 and 1
                double x = 10.0; // minimum waiting time
                double alpha = 0.5; // tail heaviness

                // inverse transformation sampling (citations #2 and #3)
                double wait = x / pow(1 - u, 1.0 / alpha);

                waitCounter[i] = round(wait); // round to accept an integer value
            }

            // normal step
            double xStep = stepDistribution(gen) + driftX; // random x-direction step with drift
            double yStep = stepDistribution(gen) + driftY; // random y-direction step with drift

            // superdiffusion
            if (diffusionType == 2) {
                uniform_real_distribution<double> angleDist(0, 2*3.14159); // choose a random angle between 0 and 2*pi

                // pareto distribution parameters
                double u = paretoDraw(gen);

                // set a cap on the uniform value to avoid blow ups
                if (u > 0.999999999) {
                    u = 0.999999999;
                }

                double xMin = 1.0; // minimum x value
                double alpha = 1.5; // tail index
                double radius = xMin / pow(1-u, 1.0/alpha); // inverse CDF of the pareto distribution

                // have to do polar coordinates since superdiffusion is tricky with grids
                double angle = angleDist(gen);
                xStep = radius*cos(angle);
                yStep = radius*sin(angle);
            }

            double newX = walker[0] + xStep; // updated x position
            double newY = walker[1] + yStep; // updated y position

            // square boundary detection
            if (domainSize != 0) {
                if (newX > domainSize || newX < -domainSize){
                    newX = walker[0];
                 }

                if (newY > domainSize || newY < -domainSize) {
                    newY = walker[1];
                }
            }

            walker[0] = newX;
            walker[1] = newY;
        }

    }
    return 0;
}
