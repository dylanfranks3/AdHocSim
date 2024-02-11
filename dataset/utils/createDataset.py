import numpy as np
import os

def random_walk_2d(n, m, k):
    # Initialize an array to store the random walk positions
    walk_positions = []

    # Start the walk at a random position within the grid
    current_position = [np.random.randint(m), np.random.randint(k)]

    # Perform the random walk
    for _ in range(n):
        # Generate random step offsets
        step_x = np.random.choice([-1, 0, 1])
        step_y = np.random.choice([-1, 0, 1])

        # Update the current position by adding the step offsets
        current_position[0] += step_x
        current_position[1] += step_y

        # Ensure the position stays within the grid bounds
        current_position[0] = max(0, min(current_position[0], m - 1))
        current_position[1] = max(0, min(current_position[1], k - 1))

        # Append the current position to the walk_positions array
        walk_positions.append(tuple(current_position))

    return walk_positions

# Example usage

path = "/Users/dylan/Code/thirdYearProject/NANSimulation/dataset/dartmouthCleanedSimData"
directory = os.fsencode(path)
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename.isnumeric():
        newPath = path + f'/{filename}/'
        with open(newPath, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['time', 'x', 'y', 'z'])  # Write header row
        time = 0
        for position in positions:
            x, y = position
            writer.writerow([time, x, y, 0])
            time += 1





n = 800  # Number of steps in the random walk
m = 1000   # Number of rows in the grid
k = 1000   # Number of columns in the grid
random_walk = random_walk_2d(n, m, k)
print("Random walk positions:")
print(random_walk)
