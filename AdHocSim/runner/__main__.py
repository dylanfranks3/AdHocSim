#!/usr/bin/env python
# cli interface to run and visualise sim
import argparse
from AdHocSim.runner import runner

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SIMULATOR CLI TOOL")
    parser.add_argument(
        "-d",
        "--directory",
        help="<Required> arg to pass the directory, see readme",
        required=True,
    )
    parser.add_argument(
        "-i",
        "--interval",
        help="<Required> arg for the interval in the simulation, to capture all data ensure databaseInterval%%--interval==0",
        required=True,
        type = float
    )
    parser.add_argument(
        "-len",
        "--length",
        help="<Required> arg for the length of the simulation, to capture all the data, ensure databaselength<=--length",
        required=True,
        type=float
    )
    parser.add_argument(
        "-m",
        "--model",
        help="arg that decides the model, pass: normal, NAN",
        required=False,
        default="normal",
    )
    parser.add_argument(
        "-v",
        "--visualise",
        help="arg whether to create a visualising .mp3 in exec path",
        type=bool,
        required=False,
        default=False,
    )
    parser.add_argument(
        "-l",
        "--logging",
        help="arg whether to show state of network post execution in stdout",
        type=bool,
        required=False,
        default=False,
    )

    args = vars(parser.parse_args())

    dataDirectory = args["directory"]
    model = args["model"]
    visualise = args["visualise"]
    logging = args["logging"]
    interval = args["interval"]
    length = args["length"]

    runner.buildSim(dataDirectory, model, visualise, logging, interval, length)
