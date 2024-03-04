from .node import Node
class Packet():
    def __init__(self, size: float, src: Node, dest: Node):
        self.size = size
        self.src = src
        self.dest = dest
       
        