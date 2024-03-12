from AdHocSim import network, simulator, nanNetwork, location, packet, node
import os, math, random
from manim import *
from manim.utils.file_ops import open_file as open_media_file
from utils.minimumBoundingBox import MinimumBoundingBox, rotate_points
from collections.abc import Iterable
from scipy.interpolate import splprep, splev, interp1d
import matplotlib.pyplot as plt


SCALE = 0.95


def play_timeline(scene, timeline):
    previous_t = 0
    ending_time = 0
    for t, anims in sorted(timeline.items()):
        to_wait = t - previous_t
        if to_wait > 0:
            scene.wait(to_wait)
        previous_t = t
        if not isinstance(anims, Iterable):
            anims = [anims]
        for anim in anims:
            turn_animation_into_updater(anim)
            scene.add(anim.mobject)
            ending_time = max(ending_time, t + anim.run_time)
    if ending_time > t:
        scene.wait(ending_time - t)


class networkVisualiser(Scene):
    def __init__(self, simulation, **kwargs):
        super().__init__(**kwargs)

        self.simulation = simulation
        self.allNodes = []
        self.packets = []

        self.requests = self.simulation.historicRequests.copy()
        self.requests = sorted(self.requests, key=lambda x: x[0])

        self.nodes = self.simulation.network.nodeContainer
        self.timeScale = 10  # n times faster than the real sim

        # scale the nodes in x and y direction
        self.scaleNodesX = None
        self.scaleNodesY = None
        self.angleRotate = None  # this is the angle to rotate all the coords by
        self.centreOfRotation = None
        self.translate = None
        self.fixCoords()  # find the bounding box etc.. append to attributes

    def construct(self):

        # self.plane()
        # self.counter()
        # self.wait(1)
        self.makeSimulation()

    def plane(self):
        rect2 = Rectangle(width=6, height=6)
        rect2.set_fill(color=GREEN, opacity=0.7)
        y_arrow = DoubleArrow(
            start=rect2.get_corner(DL) + LEFT * 0.3,
            end=rect2.get_corner(UL) + LEFT * 0.3,
        )
        x_arrow = DoubleArrow(
            start=rect2.get_corner(DL) + DOWN * 0.3,
            end=rect2.get_corner(DR) + DOWN * 0.3,
        )
        yArrowMid = (y_arrow.get_start() + y_arrow.get_end()) / 2
        xArrowMid = (x_arrow.get_start() + x_arrow.get_end()) / 2

        yText = (
            Text("300 meters", font_size=24)
            .rotate(-PI / 2)
            .move_to(yArrowMid + LEFT * 0.30)
        )
        xText = Text("300 meters", font_size=24).move_to(xArrowMid + DOWN * 0.25)

        self.add(rect2)
        self.wait(2)

        self.play(FadeIn(y_arrow, x_arrow, xText, yText), run_time=1.5)
        self.wait(0.5)
        number_plane = NumberPlane(
            x_length=6,
            y_length=6,
            x_range=(-6, 6, 1),
            y_range=(-6, 6, 1),
            background_line_style={"stroke_color": TEAL},
        )
        self.play(FadeIn(number_plane, scale=1), run_time=1.5)
        self.wait(0.5)

        plane = Group(rect2, y_arrow, x_arrow, yText, xText, number_plane)
        animation = plane.animate.shift(LEFT * 3)
        self.play(animation, run_time=2.5)

    def fixNodeCoord(self, coord):
        coord = rotate_points(self.centreOfRotation, self.angleRotate, [coord])[0]
        coord = (coord[0] - self.translate[0], coord[1] - self.translate[1])
        coord = (coord[0] * self.scaleNodesX, coord[1] * self.scaleNodesY)
        coord = np.array([coord[0], coord[1], 0])
        return coord + 3 * LEFT  # move to where the plane is

    def findCorners(
        self, points
    ):  # given the vertices of a rectangle label them tr,tl,br,bl
        tl = max(sorted(points, key=lambda x: x[0]), key=lambda x: x[1])

        points.remove(tl)
        oCorners = points

        def distance(num):
            x1, y1 = tl
            x2, y2 = num
            return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

        oCorners = sorted(oCorners, key=distance)
        if abs(oCorners[0][1] - tl[1]) < abs(oCorners[1][1] - tl[1]):
            tr, br, bl = oCorners[0], oCorners[2], oCorners[1]

        else:
            tr, br, bl = oCorners[1], oCorners[2], oCorners[0]

        return (tl, tr, br, bl)

    def fixCoords(self):
        allHistory = []
        for i in self.nodes:
            for hL in i.historicLocation:
                if hL != None:
                    allHistory.append((hL.location[0], hL.location[1]))

        coords = allHistory
        boundingBox = MinimumBoundingBox(coords)
        corners = [
            i for i in boundingBox.corner_points
        ]  # getting the smallest box around all these points
        corners = self.findCorners(corners)
        tl, tr, br, bl = corners
        self.centreOfRotation = ((tl[0] + tr[0]) / 2, (tl[1] + br[1]) / 2)
        xDist = tr[0] - tl[0]
        yDist = tr[1] - tl[1]
        angle = math.atan(
            yDist / xDist
        )  # + 0.5*math.pi #find the angle that the top left point of the rectangle has and the top right and rotate all these points accordingly
        self.angleRotate = angle

        cornersOld = (tl, tr, br, bl)
        corners = rotate_points(self.centreOfRotation, self.angleRotate, cornersOld)
        corners = self.findCorners(corners)

        tl, tr, br, bl = corners

        newXDist = tr[0] - tl[0]
        newYDist = tr[1] - br[1]
        centreOfRect = ((tl[0] + tr[0]) / 2, (tl[1] + br[1]) / 2)
        # newPointsMoved = [(i[0]-centreOfRect[0],i[1]-centreOfRect[1]) for i in newPointsRotated]
        self.translate = centreOfRect

        scalex = 6 / newXDist
        scaley = 6 / newXDist
        self.scaleNodesX = scalex * SCALE
        self.scaleNodesY = scaley * SCALE

    def makeSimulation(self):
        def getNode(gNode):
            for i in self.allNodes:
                if i.uid == gNode.uid:
                    return i
            return False

        def update_path_c(dot1, dot2):
            def updater(mob, dt):
                mob.set_points_smoothly([dot1.get_center(), dot2.get_center()])

            return updater

        self.allNodes = self.nodes

        allDotAnims = []
        for idx, i in enumerate(sorted(self.allNodes, key=lambda i: i.uid)):
            historicLocation = [
                self.fixNodeCoord(j.location)
                for j in i.historicLocation
                if j is not None
            ]
            historicLocation = historicLocation[: int(len(historicLocation) / 4)]
            path = VMobject()
            path.set_points_smoothly(historicLocation).set_opacity(0)

            d = Dot().set_color(ORANGE)

            i.visualDot = d
            self.add(i.visualDot, path)
            anim = MoveAlongPath(d, path).set_rate_func(linear)
            allDotAnims.append(anim)

        self.allNodes = sorted(self.allNodes, key=lambda i: i.uid)

        timeline = {}
        timeline[0.0] = [
            AnimationGroup(*allDotAnims, run_time=self.requests[-1][0] / self.timeScale)
        ]

        for idx, request in enumerate(self.requests):
            if (
                request[1].__func__ == network.Network.sendPacketDirectCall
            ):  # and request[2].uid == 1:
                fromNode = request[2]
                toNode = request[3]
                fromDot = getNode(fromNode).visualDot
                toDot = getNode(toNode).visualDot

                path = VMobject()
                path.set_points_smoothly([fromDot.get_center(), toDot.get_center()])
                path.set_opacity(0)
                path.add_updater(update_path_c(fromDot, toDot))
                vt = ValueTracker(0)
                c = Dot().set_color(RED).scale(0.5)
                self.add(c, path)
                c.add_updater(
                    lambda mob, vt=vt, path=path, toDot=toDot, c=c: mob.move_to(
                        path.point_from_proportion(vt.get_value())
                    )
                )  # Using RED for visibility
                anim1 = AnimationGroup(
                    vt.animate(run_time=2, rate_func=linear).set_value(1).build()
                )

                if request[0] / self.timeScale in timeline:
                    timeline[request[0] / self.timeScale] = [
                        *timeline[request[0] / self.timeScale],
                        anim1,
                    ]
                else:
                    timeline[request[0] / self.timeScale] = [anim1]

                if len(timeline) > 40:
                    break

        play_timeline(self, timeline)

    def counter(self):
        number = DecimalNumber().set_color(WHITE).scale(3)
        self.add(number.move_to(RIGHT * 3))
        self.wait(2)
        # Play the Count Animation to count from 0 to 100 in 4 seconds
        self.play(Count(number, 0, 100), run_time=3)
        self.wait(1)
        number.generate_target()
        self.play(number.animate.move_to(3.2 * UP + 5.9 * RIGHT).scale(0.4), run_time=2)
        time = Text("Time: ").scale(3 * 0.35).next_to(number, LEFT).shift(0.05 * UP)
        self.add(time)

        newTime = (
            DecimalNumber(number=0)
            .set_color(WHITE)
            .scale(3)
            .shift(3.2 * UP + 5.9 * RIGHT)
            .scale(0.4)
        )
        self.play(Transform(number, newTime))

    # this works out how much we need to s
    def specs(self):
        xCoords = []
        yCoords = []
        issues = 0
        for node in self.nodes:
            hL = node.historicLocation
            for i in hL:
                try:
                    xCoords.append(i.location.location[0])
                    yCoords.append(i.location.location[1])
                except:
                    issues += 1

        minX = min(xCoords)
        maxX = max(xCoords)
        maxY = max(yCoords)
        minY = min(yCoords)
        return minX, minY, maxX, maxY


class Count(Animation):
    def __init__(
        self, number: DecimalNumber, start: float, end: float, **kwargs
    ) -> None:
        # Pass number as the mobject of the animation
        super().__init__(number, **kwargs)
        # Set start and end
        self.start = start
        self.end = end

    def interpolate_mobject(self, alpha: float) -> None:
        # Set value of DecimalNumber according to alpha
        value = self.start + (alpha * (self.end - self.start))
        self.mobject.set_value(value)


def buildSim(dataDirectory, model, visualise, logging, interval, length):
    length = dataDirectory

    if model == "normal":
        n = network.Network()
        s = simulator.Simulator(
            network=n,
            length=length,
            time=0.0,
            output=logging,
            interval=interval,
        )  # for the dartmouth dataset

    elif model == "NAN":
        n = nanNetwork.NANNetwork()
        s = simulator.Simulator(
            network=n,
            length=length,
            time=0.0,
            output=logging,
            interval=interval,
        )  # for the dartmouth dataset

    getNodes(s, n, dataDirectory)

    return
    s.run()
    if logging == True:
        print(s.showState())

    if visualise:
        scene = networkVisualiser(s)
        scene.render()


# plaintext directory, gets nodes and packets and adds them to sim/net
def getNodes(sim, net, directory):
    # creating nodes and adding to sim/network
    failedAdds = 0  # how many nodes have packets to send to non-existent nodes
    ptDirectory = directory
    directory = os.fsencode(directory)
    nodeArr = []
    for file in os.listdir(directory):
        filename = os.fsdecode(file)

        if filename.isnumeric():  # removing chance for DS_store etc
            # nodes
            # open position file, add the requests to
            positionFilePath = f"{ptDirectory}/{filename}/{filename}.position.csv"
            nodeUID = int(filename)
            newNode = node.Node(nodeUID)
            nodeArr.append(newNode)
    net.nodeContainer = nodeArr

    # taking existing nodes and adding packets and location movement
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.isnumeric():  # removing chance for DS_store etc
            # nodes
            # open position file, add the requests to
            positionFilePath = f"{ptDirectory}/{filename}/{filename}.position.csv"
            nodeUID = filename
            newNode = sim.findNode(int(nodeUID))
            with open(positionFilePath, "r") as f:
                lines = f.read().splitlines()
                for line in lines:
                    line = line.split(",")
                    sim.request(
                        int(float(line[0])),
                        newNode.updateLocation,
                        location.Location(
                            [float(line[1]), float(line[2]), float(line[3])]
                        ),
                    )

    # print (len(sim.requests))
    # taking existing nodes and adding packets and location movement
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.isnumeric():  # removing chance for DS_store etc
            # packets
            # open node packet data
            newNode = sim.findNode(int(filename))
            dataFilePath = f"{ptDirectory}/{filename}/{filename}.data.csv"
            with open(dataFilePath, "r") as f:
                lines = f.read().splitlines()
                for line in lines:
                    line = line.split(",")
                    dest = int(line[3].split(".")[-1])  # destination node
                    destNode = sim.findNode(dest)
                    if (
                        destNode == False
                    ):  # if we can't find the destination node in the sim
                        # print (f"ERROR: tried to add a packet where the destination ({dest}) doesn't exist")
                        failedAdds += 1
                    else:
                        p = packet.Packet(int(float(line[0])), newNode, destNode)
                        sim.request(0, newNode.addPacket, p)
                        sim.request(
                            int(float(line[1])),
                            net.sendPacketDirect,
                            newNode,
                            destNode,
                            p,
                        )
