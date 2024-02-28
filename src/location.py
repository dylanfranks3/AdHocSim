import math
# class that would contain location info for a particular nodes and some helper
# and relevant functions about location

class Location:
    def __init__(self,location):
        # [x,y,z]
        self.location = location

    def updateLocation(self, newLocation):
        self.location = newLocation.location

    @staticmethod
    def distance(pos1,pos2):
        return math.dist(pos1,pos2)






    