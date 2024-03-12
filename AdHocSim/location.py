from __future__ import annotations
import math

# class that would contain location info for a particular nodes and some helper
# and relevant functions about location


class Location:
    def __init__(self, location: list[float, float, float]):
        # [x,y,z]
        self.location = location

    def updateLocation(self, newLocation: Location):
        self.location = newLocation.location

    @staticmethod
    def distance(pos1: Location, pos2: Location):
        return math.dist(pos1.location[:2], pos2.location[:2])

    def getLocation(self):
        return self.location
