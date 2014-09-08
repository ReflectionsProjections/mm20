from PIL import Image
import Queue
import objects.room
import config.handle_constants

mapConstants = config.handle_constants.retrieveConstants("map_reader_constants")

wallColor = mapConstants["wall_color"]
doorColor = mapConstants["wall_color"]

# Furniture
roomObjectColorDict = mapConstants["objects"]
roomNames = mapConstants["room_names"]

## Gets a list of Rooms (with connections) from a given map image
# @param map_path A path to the map image
# @param start A 2-tuple representing the point in the image to start searching from. MUST NOT be a wall or an exception will be thrown.
# @param stepSize The number of pixels the algorithm moves per step
# @returns A list of Rooms if any exist, an empty list otherwise.
def map_reader(map_path, start=(2, 2), stepSize=2):

    # NOTE: The map file's colors must be exact i.e. (1,0,0) and (2,0,0) are considered different rooms

    # Open picture
    img = Image.open(map_path).convert("RGBA")
    pixels = img.load()

    # Find connecting rooms
    connections = dict()
    visited = []
    for x in range(0, img.size[0]):
        col = []
        for y in range(0, img.size[1]):
            col.append(False)
        visited.append(col)

    # Get connections between + objects in rooms
    roomObjects = dict()
    _floodFillConnectionsIter(start, connections, roomObjects, pixels, visited, img.size, stepSize)

    # Show picture
    rooms = []
    for c in connections:
        room = objects.room.Room(c)  # c = room.name
        rooms.append(room)
    for i in range(0, len(rooms)):
        rooms[i].connectedRooms = {r.name: r for r in rooms if r.name in connections[rooms[i].name]}

        # Room objects
        rooms[i].stand = [(r[0], r[1])       for r in roomObjects[rooms[i].name] if r[2] == "stand"]
        rooms[i].chairs = [(r[0], r[1])      for r in roomObjects[rooms[i].name] if r[2] == "chair"]
        rooms[i].desks = [(r[0], r[1])       for r in roomObjects[rooms[i].name] if r[2] == "desk"]
        rooms[i].doors = [(r[0], r[1], r[3]) for r in roomObjects[rooms[i].name] if r[2] == "door"]
        rooms[i].snacktables = [(r[0], r[1]) for r in roomObjects[rooms[i].name] if r[2] == "snacktable"]
        rooms[i].chair_dirs = [(r[0], r[1]) for r in roomObjects[rooms[i].name] if r[2] == "chair_dir"]

        for r in roomObjects[rooms[i].name]:
            if r[2] == "projector":
                rooms[i].addResource('PROJECTOR')
        if len(rooms[i].snacktables) != 0:
            rooms[i].addResource('FOOD')  # For now, this is how we are treating food

    # Hacky transformation code
    rooms2 = {i.name: i for i in rooms}
    return rooms2


# --- INTERNAL CODE - DO NOT USE OUTSIDE OF THIS FILE ---
## [map_functions.py only] Converts a tuple to a string.
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


## [map_functions.py only] Gets the closest pixel with the specified color. Returns NONE if no matches are found.
# @param start A 2-tuple representing the point in the image to start searching from.
# @param targetColor The color to search for
# @param pixels The pixels of the image (obtained using Image.load())
# @param imgsize The size of the image as a tuple: (width, height).
# @param stepSize The number of pixels the algorithm moves per step
def _findClosestPixel(start, targetColor, pixels, imgsize, stepSize=1):

    # Queues
    nodeQueue = Queue.Queue()
    nodeQueue.put((start[0], start[1]))

    width = imgsize[0]
    height = imgsize[1]

    # Make sure start is a 2-tuple of integers
    if len(start) != 2 or not isinstance(start[0], int) or not isinstance(start[1], int):
        raise ValueError("Starting pixel must be a 2-tuple of integers.")

    # Make sure this wasn't started on a wall or out of bounds
    x = start[0]
    y = start[1]
    if (x < 0 or y < 0) or (width <= x or height <= y):
        raise ValueError("Starting pixel must not be out of bounds.")

    # Visited
    visited = []
    for x in range(0, width):
        col = []
        for y in range(0, height):
            col.append(False)
        visited.append(col)
    visited[start[0]][start[1]] = True

    # Search
    while not nodeQueue.empty():

        node = nodeQueue.get()

        x = node[0]
        y = node[1]

        # Base case 1: hit target
        curColor = _stringify(pixels[x, y])
        if curColor == "0 38 255 255":
            print (x, y)

        if curColor == targetColor:
            return (x, y)

        # Iterative case 1: further iteration (basically recursion)
        for mx in range(-1, 2):

            px = x + mx * stepSize

            # Skip out of bounds pixels (pt 1/2)
            if (px < 0 or width <= px):
                continue

            for my in range(-1, 2):

                # Skip identical pixels
                if mx == 0 and my == 0:
                    continue

                py = y + my * stepSize

                # Skip out of bounds pixels (pt 2/2)
                if (py < 0 or height <= py):
                    continue

                # Add pixel to queue
                if not visited[px][py]:
                    visited[px][py] = True
                    nodeQueue.put((px, py))

    # No match found
    return None


## [map_functions.py only] Gets the connections between rooms
# @param start A 2-tuple representing the point in the image to start searching from. MUST NOT be a wall or an exception will be thrown.
# @param connections (Output) A dictionary of rooms used to store connections
# @param roomObjects (Output) A dictionary of lists of objects and their positions in a room
# @param pixels The pixels of the image (obtained using Image.load())
# @param visited (Output) An array indicating which pixels have been visited
# @param imgsize The size of the image as a tuple: (width, height).
# @param stepSize The number of pixels the algorithm moves per step
def _floodFillConnectionsIter(
        start, connections, roomObjects, pixels,
        visited, imgsize, stepSize=1):

    # Queues
    nodeQueue = Queue.Queue()
    roomColor = _stringify(pixels[start[0], start[1]])
    nodeQueue.put((start[0], start[1], start[0], start[1], roomColor))

    width = imgsize[0]
    height = imgsize[1]

    # Make sure start is a 2-tuple of integers
    if len(start) != 2 or not isinstance(start[0], int) or not isinstance(start[1], int):
        raise ValueError("Starting pixel must be a 2-tuple of integers.")

    # Make sure this wasn't started on a wall or out of bounds
    x = start[0]
    y = start[1]
    if (x < 0 or y < 0) or (width <= x or height <= y):
        raise ValueError("Starting pixel must not be out of bounds.")
    if pixels[x, y] == wallColor:
        raise ValueError("Starting pixel must not be a wall.")

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
        if nextColor in roomObjectColorDict:
            if curColor not in roomObjects:
                roomObjects[curColor] = []

            if roomObjectColorDict[nextColor] != "door":
                roomObjects[curColor].append((x, y, roomObjectColorDict[nextColor]))

        # Iterative case 1a: hit another color (not black), so record the connection
        elif curColor not in roomObjectColorDict:
            updateRoomColor = True
            if curColor not in connections:
                connections[curColor] = []
            if nextColor != curColor and nextColor not in connections[curColor]:
                connections[curColor].append(nextColor)

                if curColor not in roomObjects:
                    roomObjects[curColor] = []
                if nextColor not in roomObjects:
                    roomObjects[nextColor] = []

                # Doors
                doorPos = _findClosestPixel((x, y), doorColor, pixels, imgsize)

                dx = doorPos[0]
                dy = doorPos[1]

                roomObjects[curColor].append((dx, dy, "door", nextColor))
                roomObjects[nextColor].append((dx, dy, "door", curColor))

                # Add a connection going the opposite direction (since edges SHOULDN'T be directed)
                if nextColor not in connections:
                    connections[nextColor] = []
                if curColor not in connections[nextColor]:  # Redundant, but kept for code clarity
                    connections[nextColor].append(curColor)

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
    rooms = map_reader("./rooms_full.bmp")
    for loc in rooms:
        
        if loc != "255 114 0 255":
            continue

        r = rooms[loc]

        #print '-----------------------------------'
        #print loc
        print r.stand
        print r.chairs
        #print r.desks
        #print r.doors
        #print r.snacktables
        #print r.connectedRooms.keys()
