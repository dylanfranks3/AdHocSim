import numpy as np
import matplotlib.pyplot as plt
import os, csv, random, math


# Function to check if a point is inside the bounds
def is_inside_bounds(x, y, xmin, xmax, ymin, ymax):
    return xmin <= x <= xmax and ymin <= y <= ymax


# Function to pick a new angle, considering the side that was hit
def pick_new_angle(x, y, xmin, xmax, ymin, ymax):
    """Pick a new angle randomly between the two furthest corners from the current position."""
    corners = [(xmin, ymin), (xmin, ymax), (xmax, ymin), (xmax, ymax)]
    distances = [np.hypot(x - cx, y - cy) for cx, cy in corners]
    farthest_corners = sorted(range(len(corners)), key=lambda i: -distances[i])[:2]

    # Get angles to the two furthest corners
    angle1 = np.arctan2(
        corners[farthest_corners[0]][1] - y, corners[farthest_corners[0]][0] - x
    )
    angle2 = np.arctan2(
        corners[farthest_corners[1]][1] - y, corners[farthest_corners[1]][0] - x
    )

    # Ensure angle1 is smaller than angle2
    if angle1 > angle2:
        angle1, angle2 = angle2, angle1

    # Handle the case when the range crosses the -pi/pi discontinuity
    if angle2 - angle1 > np.pi:
        angle1, angle2 = angle2, angle1 + 2 * np.pi

    # Pick a random angle between the two angles
    new_angle = np.random.uniform(angle1, angle2) % (2 * np.pi)
    return new_angle


def random_walk_2d(gxmin, gxmax, gymin, gymax, gsteps, gInterval):
    # Rectangle bounds
    xmin, xmax = gxmin, gxmax
    ymin, ymax = gymin, gymax

    # Starting point
    x, y = np.random.uniform(xmin, xmax), np.random.uniform(ymin, ymax)

    # Number of steps
    n_steps = int(gsteps / gInterval)

    # Step size and angle initialization
    angle = np.random.uniform(0, 2 * np.pi)
    step_size = 1 * gInterval 

    # Lists to store x and y coordinates
    x_positions = [x]
    y_positions = [y]

    # Simulate the walk
    count = 0
    for _ in range(n_steps - 1):

        # Randomly change the direction and step size slightly for smoothness

        count += step_size
        if count >= 1:
            angle += np.random.uniform(-np.pi / 13, np.pi / 13)
            count = 0
        # step_size = np.clip(step_size + np.random.uniform(-0.5, 0.5), 0.5, 2.0)

        # Calculate new position
        x_new = x + np.cos(angle) * step_size
        y_new = y + np.sin(angle) * step_size

        # Check if the new position is inside bounds, adjust if necessary
        while not is_inside_bounds(x_new, y_new, xmin, xmax, ymin, ymax):
            angle = pick_new_angle(x, y, xmin, xmax, ymin, ymax)
            x_new = x + np.cos(angle) * step_size
            y_new = y + np.sin(angle) * step_size

        # Update the current position
        x, y = x_new, y_new
        x_positions.append(x)
        y_positions.append(y)

    return list(zip(x_positions, y_positions))


def createNodeDirectories(gPath, gNodeCount):
    for i in range(1, gNodeCount + 1):
        os.mkdir(f"{gPath}/{i}/")


def createRandomIntegers(size, mean, value_range):

    min_val, max_val = value_range
    random_integers = np.random.randint(min_val, max_val + 1, size=size)

    adjustment_factor = mean - np.mean(random_integers)
    random_integers = np.round(random_integers + adjustment_factor).astype(int)

    random_integers[random_integers < min_val] = min_val
    random_integers[random_integers > max_val] = max_val

    return random_integers


def createPacketData(gPath, gTime, gThroughput, gNodeCount, gPacket):
    nodeNos = [i for i in range(1, gNodeCount + 1)]

    for i in nodeNos:

        # how many unique nodes a single node will communicate to across the sim
        match gThroughput:
            case "low":
                uniqueComs = math.ceil(gNodeCount / 10)
                uniqueNodesPerSec = random.uniform(0.4, 0.2)
            case "med":
                uniqueComs = math.ceil(gNodeCount / 8)
                uniqueNodesPerSec = random.normalvariate(0.7, 0.25)
            case "high":
                uniqueComs = math.ceil(gNodeCount / 5)
                uniqueNodesPerSec = random.normalvariate(1.6, 0.3)

        nodeNosSansCurrent = nodeNos.copy()
        nodeNosSansCurrent.remove(i)  # you can't send packets to yourself, duh
        choiceOfNodes = random.sample(nodeNosSansCurrent, k=uniqueComs)
        amountToChoose = createRandomIntegers(
            gTime + 1,
            uniqueNodesPerSec,
            (math.floor(0.8 * uniqueNodesPerSec), math.ceil(1.2 * uniqueNodesPerSec)),
        )
        with open(f"{gPath}/{i}/{i}.data.csv", mode="w+", newline="") as file:
            writer = csv.writer(file)
            for time in range(0, gTime):
                messagesToSend = []
                # given we want to talk to so many unique people per second, let's get some subset of nodes to communicate to that has a mean of this

                if amountToChoose[time] > len(choiceOfNodes):
                    atc = len(choiceOfNodes)
                else:
                    atc = amountToChoose[time]
                atc = abs(atc)
                thisSecondsRecipetents = random.sample(choiceOfNodes, atc)

                for recipitent in thisSecondsRecipetents:
                    # how many packets a given frame will be
                    match gThroughput:
                        case "low":
                            packetSize = round(random.normalvariate(2.5, 1))
                        case "med":
                            packetSize = round(random.uniform(3.2, 1))
                        case "high":
                            packetSize = round(random.uniform(4.3, 1.1))

                    for _ in range(packetSize):
                        nothing = False
                        messagesToSend.append(
                            [
                                "1300",
                                str(time),
                                str(f"11.0.0.{str(i)}"),
                                f"11.0.0.{str(recipitent)}",
                            ]
                        )

                random.shuffle(messagesToSend)
                if messagesToSend:
                    writer.writerows(messagesToSend)


def setup(gPath, gNodeCount, gInterval, gXSize, gYSize, gTime, gPacketSize, gThrougput):
    if not os.path.isdir(
        gPath
    ):  # if the directory the user wants to use doesn't exist, make it
        os.mkdir(gPath)

    createNodeDirectories(gPath, gNodeCount)
    createLocationData(gPath, gTime, gXSize, gYSize, gNodeCount, gInterval)
    createPacketData(gPath, gTime, gThrougput, gNodeCount, gPacketSize)


def createLocationData(gPath, gTime, gXSize, gYSize, gNodeCount, gInterval):
    
    for i in range(1, gNodeCount + 1):

        newPath = gPath + f"/{i}/{i}.position.csv"
        with open(newPath, mode="w+", newline="") as file:
            writer = csv.writer(file)
            time = 0.0
            random_walk = random_walk_2d(0, gXSize, 0, gYSize, gTime, gInterval)
            for position in random_walk:
                x, y = position
                writer.writerow([time, x, y, 0])  # no 3D consideration
                time = time + gInterval
