# import libraries
from subprocess import Popen, PIPE, check_output
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

# get the total number of steps each walker will take (max 100,000)
while True:
    try:
        num_steps = int(input("Enter the number of steps (2 to 100,000): "))
        if 1 <= num_steps <= 100000:
            break
        else:
            print("Error: Please enter a number between 1 and 100,000")
    except ValueError:
        print("Error: Please enter an integer value")

# Compile C++ code
# This is based on a snippet from BubbleSort.py in the Speed-Test guided project
try:
    subprocess.check_output("g++ -std=c++17 multiwalk.cpp", stdin=None, stderr=subprocess.STDOUT, shell=True)
except subprocess.CalledProcessError as e:
    print("error:\n", e.output)
    raise SystemExit

# run the C++ exe with command line argument
print("Opening C++ program")
p = Popen('a.exe ' + str(num_walkers) + ' ' + str(num_steps), shell=True) # run the exe with num_walkers and num_steps
p.wait() # wait for the C++ program to finish

os.remove("a.exe") # remove the exe now that the program has created the CSV we need

df = pd.read_csv("randomwalk.csv") # read in CSV output from the C++ file
print("CSV read successfully") # notify user that the CSV was successfully read

# plot the data

# plotting the random walk paths of each walker
plt.figure(figsize=(10,5))
plt.subplot(1, 2, 1) # 1 row, 2 columns, lefthand subplot

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
plt.legend() # tells us which walker corresponds to which path

# plot expected squared displacement over time
plt.subplot(1, 2, 2) # 1 row, 2 columns, righthand subplot
plt.plot(df['step'], df['exp_squared_disp'])
plt.xlabel("Step")
plt.ylabel("Expected Squared Displacement")
plt.title("Ensemble-Averaged Squared Displacement vs. Step")
plt.grid(True)
plt.tight_layout()
plt.show()

os.remove("randomwalk.csv")
print("CSV deleted")