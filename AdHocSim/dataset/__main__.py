#!/usr/bin/env python
import argparse, os
from AdHocSim.dataset.dataset import setup

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="DATASET CLI TOOL")
    parser.add_argument(
        "-d",
        "--dir",
        help="<Required> arg to the path that you'd like to create the new dataset in, if it is no",
        required=True,
        type=str,
    )
    parser.add_argument(
        "-i",
        "--interval",
        help="<Required> arg for size of the interval within the sim",
        required=True,
        type=float,
    )

    parser.add_argument(
        "-nc",
        "--nodeCount",
        help="<Required> arg for the number of nodes",
        required=True,
        type=int,
    )
    parser.add_argument(
        "-x",
        "--xSize",
        help="<Required> arg for the width of the simulation area",
        required=True,
        type=int,
    )
    parser.add_argument(
        "-y",
        "--ySize",
        help="<Required> arg for the height of the simulation area",
        required=True,
        type=int,
    )
    parser.add_argument(
        "-t",
        "--time",
        help="<Required> arg for the running time of the simulation",
        required=True,
        type=int,
    )
    parser.add_argument(
        "-p",
        "--packetSize",
        help="optional arg for the distribution of a packet ",
        choices=["low", "med", "high"],
        required=False,
        default="med",
    )  # TODO write about this in dis, average packet size
    parser.add_argument(
        "-v",
        "--volume",
        help="optional arg for the volume of packet generation per node per unique recipitent",
        choices=["low", "med", "high"],
        required=False,
        default="med",
    )
    args = vars(parser.parse_args())

    path = args["dir"]
    nodeCount = args["nodeCount"]
    interval = args["interval"]
    xSize = args["xSize"]
    ySize = args["ySize"]
    time = args["time"]
    packetSize = args["packetSize"]
    throughput = args["volume"]

    

    setup(path, nodeCount, interval, xSize, ySize, time, packetSize, throughput)
