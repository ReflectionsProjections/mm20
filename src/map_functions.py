from PIL import Image
import Queue
import objects.room
import config.handle_constants
from vector import vecLen
import sys
import os
import pickle

mapConstants = config.handle_constants.retrieveConstants("map_reader_constants")

wallColor = mapConstants["wall_color"]
doorColor = mapConstants["door_color"]
dirMarkerColor = mapConstants["dir_marker_color"]
doorSearchRadius = mapConstants["door_search_radius"]

# Furniture
roomObjectColorDict = mapConstants["objects"]
roomNames = mapConstants["room_names"]

# Progress report variables
pathStatus = {"pathsCount": 0, "totalPaths": 0}


# Gets a list of Rooms (with connections) from a given map image
# @param map_path A path to the map image
# @param start The *non-wall* point in the image to start searching from.
# @param stepSize The number of pixels the algorithm moves per step
# @returns A list of Rooms if any exist, an empty list otherwise.
def map_reader(map_path, start=(2, 2), stepSize=2):

    # Open picture
    img = Image.open(map_path).convert("RGBA")
    pixels = img.load()

    # Get connections between + objects in rooms
    roomObjects = dict()
    connections = dict()
    _floodFillConnectionsIter(start, connections, roomObjects, pixels, img.size, stepSize)

    # Show picture
    rooms = []
    for c in connections:
        room = objects.room.Room(c)  # c = room.name
        rooms.append(room)

    # Init rooms (everything but paths)
    for i in range(0, len(rooms)):
        rooms[i].connectedRooms = {r.name: r for r in rooms if r.name in connections[rooms[i].name]}

        # Room objects
        curRoomObjects = roomObjects[rooms[i].name]
        rooms[i].stand = [(r[0], r[1]) for r in curRoomObjects if r[2] == "stand"]
        rooms[i].chairs = [(r[0], r[1]) for r in curRoomObjects if r[2] == "chair"]
        rooms[i].desks = [(r[0], r[1]) for r in curRoomObjects if r[2] == "desk"]
        rooms[i].doors = [(r[0], r[1]) for r in curRoomObjects if r[2] == "door"]
        rooms[i].snacktable = [(r[0], r[1]) for r in curRoomObjects if r[2] == "snacktable"]
        rooms[i].dirmarkers = [(r[0], r[1]) for r in curRoomObjects if r[2] == "dir_marker"]

        for r in roomObjects[rooms[i].name]:
            if r[2] == "projector":
                rooms[i].addResource('PROJECTOR')
        if len(rooms[i].snacktable) != 0:
            rooms[i].addResource('FOOD')  # For now, this is how we are treating food

    # Count paths
    for r in rooms:

        # Get connected waypoints in a room
        waypoints = r.snacktable + r.stand + r.chairs + r.doors

        for p1 in waypoints:
            for p2 in waypoints:

                # Skip identical points
                if p1 == p2:
                    continue

                # Skip if the two items are both chairs (because moving between chairs doesn't happen)
                if p1 in r.chairs and p2 in r.chairs:
                    continue

                pathStatus["totalPaths"] += 1

    # Find paths
    for i in range(0, len(rooms)):
        rooms[i].paths = _getPathsInRoom(rooms[i], pixels, img.size)
        
    # Room naming code - since the map parser depends on color room names
    rooms2 = {roomNames[i.name]: i for i in rooms}
    for r in rooms2.values():
        connectedRooms2 = dict()
        for c in r.connectedRooms:
            connectedRooms2[roomNames[c]] = r.connectedRooms[c]
        r.connectedRooms = connectedRooms2
        r.name = roomNames[r.name]

    return rooms2


# --- INTERNAL CODE - DO NOT USE OUTSIDE OF THIS FILE ---
# [map_functions.py only] Converts a tuple to a string.
# @param t The tuple to convert.
def _stringify(t):

    # Edge case
    if len(t) == 0:
        return ""

    # Common case
    s = str(t[0])
    for i in range(1, len(t)):
        s += " " + str(t[i])

    # Done!
    return s

#Distance heuristic for use in A*
def _heuristic(curPix, destPix):
    xdif = abs(curPix[0] - destPix[0])
    ydif = abs(curPix[1] - destPix[1])
    return xdif + ydif


# [map_functions.py only] Finds the shortest valid player path between two points using a BFS
# @param start A 2-tuple representing the starting point of the path
# @param end A 2-tuple representing the ending point of the path
# @param roomColor The color of the current room (as a string)
# @param pixels The pixels of the image (obtained using Image.load())
# @param imgSize The size of the image as a tuple: (width, height).
# @param stepSize The number of pixels the algorithm moves per step
def _findShortestValidPath(start, end, roomColor, pixels, imgSize, stepSize=1):

    # Ace settings
    playerSize = 4  # Should be 12, use 4 for testing
    playerStep = 4

    # seen
    seen = dict()
    seen[(start[0], start[1])] = ((-1, -1), 0, False)

    # Queues
    nodeQueue = Queue.PriorityQueue()
    nodeQueue.put((0.0, 0.0, start[0], start[1]))

    width = imgSize[0]
    height = imgSize[1]

    # Do BFS
    pathFound = False
    node = None
    while not nodeQueue.empty():

        node = nodeQueue.get()
        coord = node[2:]
        seenval = seen[coord]
        seen[coord] = (seenval[0], seenval[1], True)

        x = coord[0]
        y = coord[1]

        # Base case 1: too close to a wall
        pathIsValid = True
        for i in range(x - playerSize, x + playerSize + 1, playerStep):
            if not pathIsValid:
                break

            # Bounds check (1/2)
            if (i < 0 or width <= i):
                continue

            for j in range(y - playerSize, y + playerSize + 1, playerStep):

                # Bounds check (2/2)
                if (j < 0 or height <= j):
                    continue

                color = _stringify(pixels[i, j])
                if color == wallColor:
                    pathIsValid = False
                    break
        if not pathIsValid:
            continue

        # Base case 2: hit a different color
        color = _stringify(pixels[x, y])
        if color != roomColor and color in roomNames:
            continue

        # Base case 3: hit goal
        if vecLen(coord, end) <= stepSize:
            pathFound = True
            break

        # Iterative case
        for mx in range(-1, 2):
            for my in range(-1, 2):

                # Skip identical pixels
                if (mx == 0) and (my == 0):
                    continue

                px = x + mx * stepSize
                py = y + my * stepSize

                # Skip out of bounds pixels
                if (px < 0 or width <= px or py < 0 or height <= py):
                    continue

                # Skip visited pixels
                nextCoord = (px, py)
                travelled = float(node[1]) + vecLen((0,0), (stepSize*mx, stepSize*my))
                if not seen.get(nextCoord, None):
                    # Add pixel to queue
                    seen[nextCoord] = (coord, travelled, False)
                    dist = float(travelled) + _heuristic(nextCoord, end)
                    nodeQueue.put((dist, travelled, px, py))
                elif not seen[nextCoord][2] and seen[nextCoord][1] > travelled:
                    seen[nextCoord] = (coord, travelled, False)
                    dist = float(travelled) + _heuristic(nextCoord, end)
                    nodeQueue.put((dist, travelled, px, py))

    # Backtrack to start (if possible)
    if not pathFound:
        print "\033[91mDEST NOT REACHED " + str(start) + " --> " + str(end) + "\033[0m"
        return None

    path = list()
    if coord != end:
        path.append(end)
    while coord != start:
        path.append(coord)
        coord = seen[coord][0]

    return path


# [map_functions.py only] Gets the paths within a room
def _getPathsInRoom(room, pixels, imgSize):

    # Get connected waypoints in a room
    waypoints = room.snacktable + room.stand + room.chairs + room.doors

    # Find paths
    paths = dict()
    for p1 in waypoints:
        paths[p1] = dict()
        for p2 in waypoints:

            # Skip identical points
            if p1 == p2:
                continue

            # Skip if the two items are both chairs (because moving between chairs doesn't happen)
            if p1 in room.chairs and p2 in room.chairs:
                continue

            # Add path
            path = _findShortestValidPath(p1, p2, room.name, pixels, imgSize, mapConstants["path_step_size"])

            if path:
                paths[p1][p2] = path
            else:
                print "\033[91mPath " + str(p1) + " --> " + str(p2) + " failed.\033[0m"

            # Print progress
            pathStatus["pathsCount"] += 1
            sys.stdout.write('\r')
            sys.stdout.write('Paths found: \033[92m{}\033[0m/{} (\033[92m{}%\033[0m)'.format(
                pathStatus["pathsCount"],
                pathStatus["totalPaths"],
                int(float(pathStatus["pathsCount"])/pathStatus["totalPaths"]*100)
            ))
            sys.stdout.flush()

    return paths


# [map_functions.py only] Gets the closest point with the specified color, else NONE.
# @param inX The x coordinate in the image to start searching from.
# @param inY The y coordinate in the image to start searching from.
# @param targetColor The color to search for
# @param pixels The pixels of the image (obtained using Image.load())
# @param imgSize The size of the image as a tuple: (width, height).
# @param searchRadius The max distance the search can have from start
# @param stepSize The number of pixels the algorithm moves per step
def _findClosestPixel(inX, inY, targetColor, pixels, imgSize, searchRadius, stepSize=1):

    start = (inX, inY)

    # Queues
    coordQueue = Queue.Queue()
    coordQueue.put(start)

    width = imgSize[0]
    height = imgSize[1]

    # Visited
    visited = dict()
    visited[start] = True

    # Search
    while not coordQueue.empty():

        coord = coordQueue.get()

        x = coord[0]
        y = coord[1]

        # Base case 1: hit target
        curColor = _stringify(pixels[x, y])
        if curColor == targetColor:
            return coord

        # Base case 2: out of search range
        if vecLen(coord, start) > searchRadius:
            continue

        # Iterative case 1: further iteration (basically recursion)
        for mx in range(-1, 2):

            px = x + mx * stepSize

            # Skip out of bounds pixels (pt 1/2)
            if (px < 0 or width <= px):
                continue

            for my in range(-1, 2):

                # Skip identical pixels
                if (mx == 0) and (my == 0):
                    continue

                py = y + my * stepSize

                # Skip out of bounds pixels (pt 2/2)
                if (py < 0 or height <= py):
                    continue

                # Add pixel to queue
                nextPos = (px, py)
                if not visited.get(nextPos, False):
                    visited[nextPos] = True
                    coordQueue.put((px, py))

    # No match found
    return None

# [map_functions.py only] Finds the top left corner of a marker
# @param pos The initial position of the marker
# @param pixekls The pixels of the image (obtained using Image.load())
def _findTopLeftCorner(pos, pixels):

    ox = x = pos[0]
    oy = y = pos[1]
    c = _stringify(pixels[x, y])

    if _stringify(pixels[x - 1, y - 1]) == c:
        ox = x - 1
        oy = y - 1
    elif _stringify(pixels[x - 1, y]) == c:
        ox = x - 1
        oy = y
    elif _stringify(pixels[x, y - 1]) == c:
        ox = x
        oy = y - 1

    return (ox, oy)


# [map_functions.py only] Gets the connections between rooms
# @param start The non-wall point in the image to start searching from.
# @param connections (Output) A dictionary of rooms used to store connections
# @param roomObjects (Output) A dictionary of lists of objects and their positions in a room
# @param pixels The pixels of the image (obtained using Image.load())
# @param imgSize The size of the image as a tuple: (width, height).
# @param stepSize The number of pixels the algorithm moves per step
def _floodFillConnectionsIter(
        start, connections, roomObjects, pixels, imgSize, stepSize=1):

    # Find connecting rooms
    visited = []
    for x in range(0, imgSize[0]):
        col = []
        for y in range(0, imgSize[1]):
            col.append(False)
        visited.append(col)

    # Queues
    nodeQueue = Queue.Queue()
    roomColor = _stringify(pixels[start[0], start[1]])
    nodeQueue.put((start[0], start[1], start[0], start[1], roomColor))

    width = imgSize[0]
    height = imgSize[1]

    # Make sure this wasn't started on a wall or out of bounds
    x = start[0]
    y = start[1]
    if pixels[x, y] == wallColor:
        raise ValueError("Starting pixel must not be a wall.")

    # Initialize roomObjects/connections
    for color in roomNames:
        roomObjects[color] = set()
        connections[color] = set()

    # Begin flood search
    while not nodeQueue.empty():

        node = nodeQueue.get()

        x = node[0]
        y = node[1]

        # Base case 1: hit black
        curColor = node[4]
        nextColor = _stringify(pixels[x, y])
        updateRoomColor = False
        if nextColor == wallColor:
            continue

        # Base case 2: hit an object (don't do Iterative Case 1a if this triggers)
        if nextColor in roomObjectColorDict and nextColor != doorColor:

            # Find the top left coord of the object marker
            (objX, objY) = _findTopLeftCorner((x, y), pixels)
            roomObjects[curColor].update({(objX, objY, roomObjectColorDict[nextColor])})

        # Iterative case 1a: hit another room, so record the connection
        elif curColor in roomNames and nextColor in roomNames:
            updateRoomColor = True
            if nextColor != curColor:

                # Update connections if necessary
                if nextColor not in connections[curColor]:
                    connections[curColor].update({nextColor})
                    connections[nextColor].update({curColor})

                # Skip door finding process if we're within a known one's search radius
                doDoorSearch = True
                for obj in roomObjects[curColor]:
                    if obj[2] != "door":
                        continue
                    if abs(obj[0] - x) + abs(obj[1] - y) <= doorSearchRadius + 2:
                        doDoorSearch = False
                        break

                # Find nearest door (if appropriate)
                if doDoorSearch:
                    doorPos = _findClosestPixel(x, y, doorColor, pixels, imgSize, doorSearchRadius)
                    if doorPos:

                        # Find top left corner
                        doorPos = _findTopLeftCorner(doorPos, pixels)

                        # Add door to room objects list
                        roomObjects[curColor].update({(doorPos[0], doorPos[1], "door")})
                        roomObjects[nextColor].update({(doorPos[0], doorPos[1], "door")})

        # Determine room color
        roomColor = nextColor if updateRoomColor else curColor

        # Iterative case 1b: further iteration (basically recursion)
        for mx in range(-1, 2):
            for my in range(-1, 2):

                # Skip identical pixels and diagonals
                if (mx == 0) == (my == 0):
                    continue

                px = x + mx * stepSize
                py = y + my * stepSize

                # Skip out of bounds pixels
                if (px < 0 or width <= px or py < 0 or height <= py):
                    continue

                # Skip visited pixels
                if not visited[px][py]:
                    visited[px][py] = True

                    # Add pixel to queue
                    nodeQueue.put((px, py, x, y, roomColor))

# Run a simple test
if __name__ == "__main__":

    # Execute function
    serverConstants = config.handle_constants.retrieveConstants("serverDefaults")
    mapPath = serverConstants['map']
    

    map_cache_str = "map.cache"
    rooms = None
    if os.path.isfile(map_cache_str):
        with open(map_cache_str, 'r') as f:
            rooms = pickle.load(f)
    else:
        rooms = map_reader(mapPath, tuple(serverConstants["mapParseStartPos"]))

    print rooms["2"].doors
    print rooms["8"].doors
