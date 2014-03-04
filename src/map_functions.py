from PIL import Image
from Queue import Queue

def map_reader(map_url):

   # This function takes a path to a map file and turns it into a list of nodes (edges are stored on the nodes)

   # Open picture
   img = Image.open(map_url)
   pixels = img.load()

   # Find connecting rooms
   connections = dict()
   visited = []
   for x in range(0,img.size[0]):
      col = []
      for y in range(0,img.size[1]):
         col.append(False)
      visited.append(col)
   
   floodFillConnectionsIter(0,0,connections,pixels,visited)
   
   # Show picture
   print connections
   img.show()

# --- INTERNAL CODE - DO NOT USE OUTSIDE OF THIS FILE ---

# Gets the connections between rooms
def floodFillConnectionsIter(x,y,connections,pixels,visited):
   
   # Queues
   nodeQueue = Queue()
   parentQueue = Queue()
   
   nodeQueue.put((0,0))
   parentQueue.put((0,0))
   
   while not nodeQueue.empty():
   
      node = nodeQueue.get()
      parent = parentQueue.get()
      
      x = node[0]
      y = node[1]
   
      # Base case 1: out of bounds
      if (x < 0 or y < 0) or (len(visited) <= x or len(visited[0]) <= y):
         continue
         
      # Base case 2: hit black
      curColor = pixels[parent[0], parent[1]]
      nextColor = pixels[x,y]
      if nextColor == (0,0,0):
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
         
      # Iterative case 1b: further iteration (basically recursion)
      for mx in range(-1,2):
         for my in range(-1,2):
         
            # Skip identical pixels
            if mx == 0 and my == 0:
               continue
               
            nodeQueue.put((x+mx, y+my))
            parentQueue.put((x,y))
            
# Do something
map_reader("./drawing2.bmp")
   
   
