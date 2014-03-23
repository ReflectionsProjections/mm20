from PIL import Image
from Queue import Queue
from objects.room import Room

# Colors used for walls
# TODO move to constants.py or something like that
wallColors = [(0,0,0,255)]

# For debugging
colorDict = {
    (0, 0, 0, 255):"black",
    (0, 255, 255, 255):"cyan",
    (255, 255, 255, 255):"white",
    (72, 0, 255, 255):"blue",
    (255, 0, 220, 255):"pink",
    (76, 255, 0, 255):"green"
}

## Gets a list of Rooms (with connections) from a given map image
# @param map_path A path to the map image
# @param start A 2-tuple representing the point in the image to start searching from. MUST NOT be a wall or an exception will be thrown.
# @param stepSize The number of pixels the algorithm moves per step
# @returns A list of Rooms if any exist, an empty list otherwise.
def getRoomsFromMap(map_path, start=(2,2), stepSize=2):

    # NOTE: The map file's colors must be exact i.e. (1,0,0) and (2,0,0) are considered different rooms
    
    # Open picture
    img = Image.open(map_path).convert("RGBA")
    pixels = img.load()

    # Find connecting rooms
    connections = dict()
    visited = []
    for x in range(0,img.size[0]):
        col = []
        for y in range(0,img.size[1]):
            col.append(False)
        visited.append(col)
   
    # Get connections between rooms
    floodFillConnectionsIter(start,connections,pixels,visited,stepSize)
   
    # Show picture
    rooms = []
    for c in connections:
        room = Room(color=c)
        rooms.append(room)
    for i in range(0,len(rooms)):
        rooms[i].connections = [r for r in rooms if r.color in connections[rooms[i].color]]
    
    # Done!
    """
    # Left for debug
    print rooms
    for r in rooms:
        print "---------------------"
        print r.connections
    """
    return rooms        

# --- INTERNAL CODE - DO NOT USE OUTSIDE OF THIS FILE ---

## [map_functions.py only] Gets the connections between rooms
# @param start A 2-tuple representing the point in the image to start searching from. MUST NOT be a wall or an exception will be thrown.
# @param connections (Output) A dictionary of rooms used to store connections
# @param pixels The pixels of the image (obtained using Image.load())
# @param visited (Output) An array indicating which pixels have been visited
# @param stepSize The number of pixels the algorithm moves per step
def floodFillConnectionsIter(start,connections,pixels,visited,stepSize):
   
    # Queues
    nodeQueue = Queue()
    parentQueue = Queue()
   
    nodeQueue.put(start)
    parentQueue.put(start)

    width = len(visited)
    height = len(visited[0])

    # Make sure start is a 2-tuple of integers
    if len(start) is not 2 or not isinstance(start[0],int) or not isinstance(start[1],int):
        raise ValueError("Starting pixel must be a 2-tuple of integers.")

    # Make sure this wasn't started on a wall or out of bounds
    x = start[0]
    y = start[1]
    if (x < 0 or y < 0) or (width <= x or height <= y):
        raise ValueError("Starting pixel must not be out of bounds.")
    if pixels[x,y] in wallColors:
        raise ValueError("Starting pixel must not be a wall.")
   
    # Begin flood search
    while not nodeQueue.empty():
   
        node = nodeQueue.get()
        parent = parentQueue.get()
      
        x = node[0]
        y = node[1]
   
        # Base case 1: out of bounds
        if (x < 0 or y < 0) or (width <= x or height <= y):
            continue
         
        # Base case 2: hit black
        curColor = pixels[parent[0], parent[1]]
        nextColor = pixels[x,y]
        if nextColor in wallColors:
           continue
         
        # Base case 3: visited
        if visited[x][y]:
            continue
        visited[x][y] = True
      
         # Iterative case 1a: hit another color (not black), so record the connection
        if curColor not in connections:
            connections[curColor] = []
        if nextColor != curColor and nextColor not in connections[curColor]:
            connections[curColor].append(nextColor)
         
            # Add a connection going the opposite direction (since edges SHOULDN'T be directed)
            if nextColor not in connections:
                connections[nextColor] = []
            if curColor not in connections[nextColor]: # Redundant, but kept for code clarity
                connections[nextColor].append(curColor) 
         
        # Iterative case 1b: further iteration (basically recursion)
        for mx in range(-1,2):
            for my in range(-1,2):
         
                # Skip identical pixels
                if mx == 0 and my == 0:
                    continue
               
                nodeQueue.put((x + mx*stepSize, y + my*stepSize))
                parentQueue.put((x,y))
            
# Do something (if appropriate)
if __name__ == "__main__":
    getRoomsFromMap("/home/ace/Desktop/mm20/src/rooms.bmp")
   
   
