# import libraries
from subprocess import Popen
import subprocess
import os
import pandas as pd
import matplotlib.pyplot as plt

# input validation

# get the number of walkers for the simulation
while True:
    try:
        num_walkers = int(input("Enter the number of walkers (1 to 500): "))
        if 1 <= num_walkers <= 500:
            break
        else:
            print("Error: Please enter a number between 1 and 500")
    except ValueError:
        print("Error: Please enter an integer value")

# get the total number of steps each walker will take (max 50,000)
while True:
    try:
        num_steps = int(input("Enter the number of steps (2 to 50,000): "))
        if 2 <= num_steps <= 50000:
            break
        else:
            print("Error: Please enter a number between 1 and 50,000")
    except ValueError:
        print("Error: Please enter an integer value")

# get the x-axis drift
while True:
    try:
        driftX = float(input("Enter the x-axis drift (-1 to 1): "))
        if -1 <= driftX <= 1:
            break
        else:
            print("Error: Please enter a number between -1 and 1")
    except ValueError:
        print("Error: Please enter a value without a comma")

# get the y-axis drift
while True:
    try:
        driftY = float(input("Enter the y-axis drift (-1 to 1): "))
        if -1 <= driftY <= 1:
            break
        else:
            print("Error: Please enter a number between -1 and 1")
    except ValueError:
        print("Error: Please enter a value without a comma")

# get the side length of the square domain
while True:
    try:
        halfWidth = int(input("Enter half width of square domain (0 = unrestricted, max = 200): "))
        if 0 <= halfWidth <= 200:
            break
        else:
            print("Error: Please enter a number between 0 and 200")
    except ValueError:
        print("Error: Please enter an integer")

# get the diffusion type
while True:
    try:
        diffusionType = int(input("Enter the diffusion type (0 = normal, 1 = subdiffusion, 2 = superdiffusion): "))
        if 0 <= diffusionType <= 2:
            break
        else:
            print("Error: Please enter 0 for normal, 1 for subdiffusion, and 2 for superdiffusion")
    except ValueError:
        print("Error: Please enter a valid integer")


# Compile C++ code
# This is based on a snippet from BubbleSort.py in the Speed-Test guided project
try:
    subprocess.check_output("g++ -std=c++17 multiwalk.cpp", stdin=None, stderr=subprocess.STDOUT, shell=True)
except subprocess.CalledProcessError as e:
    print("error:\n", e.output)
    raise SystemExit

# run the C++ exe with command line argument
print("Opening C++ program")
args = f'a.exe {num_walkers} {num_steps} {driftX} {driftY} {halfWidth} {diffusionType}'

p = Popen(args, shell=True) # run the exe with num_walkers and num_steps
p.wait() # wait for the C++ program to finish

os.remove("a.exe") # remove the exe now that the program has created the CSV we need

df = pd.read_csv("randomwalk.csv") # read in CSV output from the C++ file
print("CSV read successfully") # notify user that the CSV was successfully read

# INDIVIDUAL WALKER PATHS
plt.figure(figsize=(14,12))
plt.subplot(2, 2, 1)

count_walkers = 0 # accumulator to count individual walkers
for i in range(2, len(df.columns), 2): # start at index 2, step by 2
    if count_walkers >= 5: # only doing the first 5 walkers to avoid overcrowding
        break
    x = df.columns[i] # x-axis
    y = df.columns[i+1] # y-axis
    walker_enum = x.split('_')[0] # splits walker0_x into a list ["walker0", "x"] and accesses only the first part
    plt.plot(df[x], df[y], label=walker_enum) # plot the x and y coordinates of each walker, label using walker_enum
    count_walkers += 1 # increment accumulator

plt.xlabel("X")
plt.ylabel("Y")
plt.title("Individual Random Walk Paths")
plt.grid(True)
plt.legend()

# HEATMAP OF VISITED LOCATIONS

plt.subplot(2, 2, 2)

x = [] # all x values
y = [] # all y values

# extend the lists so that we can store (in order) every coordinate that each walker has been to
for i in range(2, len(df.columns), 2): # skip first two columns and loop over walker's x values
    x.extend(df[df.columns[i]].values) # fetch all the x values for each walker
    y.extend(df[df.columns[i+1]].values) # fetch all the y values for each walker

plt.hist2d(x, y, bins=100) # 100 x 100 grid, counts/plots each matching (x,y) pair
plt.colorbar(label="Visit Count")
plt.xlabel("X")
plt.ylabel("Y")
plt.title("Heatmap of Visited Locations")
plt.grid(False)


# SQUARED DISPLACEMENT OVER TIME

plt.subplot(2, 2, 3) # 1 row, 2 columns, righthand subplot
plt.plot(df['step'], df['exp_squared_disp'])
plt.xlabel("Step")
plt.ylabel("Average Squared Displacement")
plt.title("Ensemble-Averaged Squared Displacement vs. Step")
plt.grid(True)

# HISTOGRAM OF WALKER DISPLACEMENTS

displacements = [] # collection of all final displacement numbers
for i in range(2, len(df.columns), 2): # skip first two cols, index through the x columns
    x_column = df.columns[i] # get the label of the ith column (x-axis)
    y_column = df.columns[i+1] # get the label of the i+1 column (y-axis)
    final_disp_x = df[x_column].iloc[-1] # get the last reported x coordinate
    final_disp_y = df[y_column].iloc[-1] # get the last reported y coordinate

    displacement = (final_disp_x**2 + final_disp_y**2)**0.5 # calculate the Euclidean distance from origin
    displacements.append(displacement) # append to the displacements list

plt.subplot(2, 2, 4)
plt.hist(displacements, bins=20, color='steelblue', edgecolor='black')
plt.xlabel("Displacement from Origin")
plt.ylabel("Number of Walkers")
plt.title("Histogram of Walker Displacements at Final Step")
plt.grid(True)

plt.tight_layout()
plt.show() # present the figures

os.remove("randomwalk.csv") # delete the csv file
print("CSV deleted")
