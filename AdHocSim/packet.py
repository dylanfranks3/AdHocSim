from AdHocSim import node


class Packet:
    def __init__(self, size: float, src: node, dest: node):
        self.size = size
        self.src = src
        self.dest = dest
