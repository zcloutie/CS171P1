# ======================================================================
# FILE:        MyAI.py
#
# AUTHOR:      Abdullah Younis
#
# DESCRIPTION: This file contains your agent class, which you will
#              implement. You are responsible for implementing the
#              'getAction' function and any helper methods you feel you
#              need.
#
# NOTES:       - If you are having trouble understanding how the shell
#                works, look at the other parts of the code, as well as
#                the documentation.
#
#              - You are only allowed to make changes to this portion of
#                the code. Any changes to other portions of the code will
#                be lost when the tournament runs your code.
# ======================================================================

from Agent import Agent

class MyAI ( Agent ):
    
    def __init__ ( self ):
        # ======================================================================
        # YOUR CODE BEGINS
        # ======================================================================
        self._map = [["" for x in range(7)] for x in range(7)]
        self.row = 0
        self.column = 0
        self.maxgrid = 6
        self.frontier = []
        self.stench_sources=[]
        self.wumpus_possibles = []
        self.wumpus_location = self._map[0][0]
        self.wumpus_alive = True
        self.gold = False       
        self.direction = "E"   
        print(self._map)
                
        pass
        # ======================================================================
        # YOUR CODE ENDS
        # ======================================================================

    def getAction( self, stench, breeze, glitter, bump, scream ):
        # ======================================================================
        # YOUR CODE BEGINS
        # ======================================================================
        if self.row == 0 and self.column == 0 and (stench or breeze):        
          return Agent.Action.CLIMB
        if self.row == 0 and self.column == 0 and self.gold:
          return Agent.Action.CLIMB
        elif self.row == 0 and self.column == 0:
          self._map[self.row][self.column] = "S"
          self._map[self.row+1][self.column] = "S"
          self._map[self.row][self.column+1] = "S"
          print(self._map)
          self.column+=1
          return Agent.Action.Forward
        
        if glitter:
          self.gold = True
          return Agent.Action.GRAB
        if bump:
          self.hitEdge()
        if breeze:
          pit_danger()
        if stench and wumpus_alive:
          wumpus_danger()
        if not breeze and (not stench or not wumpus_alive):
          safe()
        if scream:
          self.wumpus_alive = False
                
        
        return Agent.Action.CLIMB            
        # ======================================================================
        # YOUR CODE ENDS
        # ======================================================================
    
    # ======================================================================
    # YOUR CODE BEGINS
    # ======================================================================
    def hitEdge():
      if self.direction == "E":
        self.maxgrid = self.column
        self.maxgrid = self.column
      elif self.direction == "N":
        self.maxgrid = self.row
        self.maxgrid = self.row
      return
    def reverse():
      if self.direction == "N":
        Agent.Action.TURN_RIGHT
        Agent.Action.TURN_RIGHT
        self.direction = "S"
      if self.direction == "W":
        Agent.Action.TURN_RIGHT
        Agent.Action.TURN_RIGHT
        self.direction = "E"
      if self.direction == "E":
        Agent.Action.TURN_RIGHT
        Agent.Action.TURN_RIGHT
        self.direction = "W"
      if self.direction == "S":
        Agent.Action.TURN_RIGHT
        Agent.Action.TURN_RIGHT
        self.direction = "N"
      return self.direction
    def turn_left():
      if self.direction == "N":
        Agent.Action.TURN_LEFT
        self.direction = "W"
      if self.direction == "W":
        Agent.Action.TURN_LEFT
        self.direction = "S"
      if self.direction == "E":
        Agent.Action.TURN_LEFT
        self.direction = "N"
      if self.direction == "S":
        Agent.Action.TURN_LEFT
        self.direction = "E"
      return self.direction
    def turn_right():
      if self.direction == "N":
        Agent.Action.TURN_RIGHT
        self.direction = "E"
      if self.direction == "W":
        Agent.Action.TURN_RIGHT
        self.direction = "N"
      if self.direction == "E":
        Agent.Action.TURN_RIGHT
        self.direction = "S"
      if self.direction == "S":
        Agent.Action.TURN_RIGHT
        self.direction = "W"
      return self.direction
    def whats_forward():
      if self.direction == "N":
        return self._map[self.row+1][self.column]
      elif self.direction == "W":
        return self._map[self.row][self.column-1]
      elif self.direction == "E":
        return self._map[self.row][self.column+1]
      elif self.direction == "S":
        return self._map[self.row-1][self.column]
    
	
	def update_map(x,y,z):
		if x > self.maxgrid or x < 0:
			return
		elif y > self.maxgrid or y < 0:
			return
		else:
			if self._map[x][y] == "":
				self._map[x][y] = z
			elif self._map[x][y] == "S" or self._map[x][y] == "S?":
				return
				
	def adj_map(x,y,z):
		update_map(x+1,y,z)
		update_map(x-1,y,z)
		update_map(x,y+1,z)
		update_map(x,y-1,z)
		
	def pit_danger():
		adj_danger(self.row, self.column, "P?")
      
      
    def safe():
      if self.row == self.maxgrid and self.column == self.maxgrid:
        for x in [(self.row-1,self.column),(self.row,self.column-1)]:
          if "W?" in self._map[x[0]][x[1]]:
            self.wumpus_possibles.remove(x)
          self._map[x[0]][x[1]]="S"
      elif self.row == 0:
        for x in [(self.row+1,self.column),(self.row,self.column+1),(self.row,self.column-1)]:
          if "W?" in self._map[x[0]][x[1]]:
            self.wumpus_possibles.remove(x)
          self._map[x[0]][x[1]]="S"
      elif self.row == self.maxgrid:
        for x in [(self.row-1,self.column),(self.row,self.column+1),(self.row,self.column-1)]:
          if "W?" in self._map[x[0]][x[1]]:
            self.wumpus_possibles.remove(x)
          self._map[x[0]][x[1]]="S"
      elif self.column == 0:
        for x in [(self.row+1,self.column),(self.row,self.column+1),(self.row-1,self.column)]:
          if "W?" in self._map[x[0]][x[1]]:
            self.wumpus_possibles.remove(x)
          self._map[x[0]][x[1]]="S"
      elif self.column == self.maxgrid:
        for x in [(self.row-1,self.column),(self.row+1,self.column),(self.row,self.column-1)]:
          if "W?" in self._map[x[0]][x[1]]:
            self.wumpus_possibles.remove(x)
          self._map[x[0]][x[1]]="S"
      else:
        for x in [(self.row-1,self.column),(self.row+1,self.column),(self.row,self.column-1),(self.row,self.column+1)]:
          if "W?" in self._map[x[0]][x[1]]:
            self.wumpus_possibles.remove(x)
          self._map[x[0]][x[1]]="S"
      return
    def wumpus_danger():
      if self.row == self.maxgrid and self.column == self.maxgrid:
        for x in [(self.row-1,self.column),(self.row,self.column-1)]:
          if "S" not in self._map[x[0]][x[1]]:
            self._map[x[0]][x[1]]+="W?"
            wumpus_possibles.append(x)
      elif self.row == 0:
        for x in [(self.row+1,self.column),(self.row,self.column+1),(self.row,self.column-1)]:
          if "S" not in self._map[x[0]][x[1]]:
            self._map[x[0]][x[1]]+="W?"
            wumpus_possibles.append(x)
      elif self.row == self.maxgrid:
        for x in [(self.row-1,self.column),(self.row,self.column+1),(self.row,self.column-1)]:
          if "S" not in self._map[x[0]][x[1]]:
            self._map[x[0]][x[1]]+="W?"
            wumpus_possibles.append(x)
      elif self.column == 0:
        for x in [(self.row+1,self.column),(self.row,self.column+1),(self.row-1,self.column)]:
          if "S" not in self._map[x[0]][x[1]]:
            self._map[x[0]][x[1]]+="W?"
            wumpus_possibles.append(x)
      elif self.column == self.maxgrid:
        for x in [(self.row-1,self.column),(self.row+1,self.column),(self.row,self.column-1)]:
          if "S" not in self._map[x[0]][x[1]]:
            self._map[x[0]][x[1]]+="W?"
            wumpus_possibles.append(x)
      else:
        for x in [(self.row-1,self.column),(self.row+1,self.column),(self.row,self.column-1),(self.row,self.column+1)]:
          if "S" not in self._map[x[0]][x[1]]:
            self._map[x[0]][x[1]]+="W?"
            wumpus_possibles.append(x)
      self.stench_sources.append((self.row,self.column))
      """if len(self.stench_sources) >= 2:
        self.wheres_wumpus()"""
      return
    """def wheres_wumpus():
      for x in self.stench_sources:
        for i in self.wumpus_possibles"""
    def distance(p1,p2):
      distance = abs(p1[0]-p2[0])
      distance+= abs(p1[1]-p2[1])
      return distance
    def path_to_point(row,col,c_row,c_col,cost,previous):
      path = []
      paths = []
      if row == c_row and col == c_col:
        path.append((c_row,c_col))
        return (path,cost)
      if self.row == self.maxgrid and self.column == self.maxgrid:
        if self._map[self.row][self.column-1] == "S" and previous !=(c_row,c_col-1):
          info = path_to_point(row,col,c_row,c_col-1,cost+1,(c_row,c_col))
          if info != False:
            path = info[0]
            path.append((c_row,c_col))
            paths.append(path,info[1])
        if self._map[self.row-1][self.column] == "S" and previous !=(c_row-1,c_col):
          info = path_to_point(row,col,c_row-1,c_col,cost+1,(c_row,c_col))
          if info != False:
            path = info[0]
            path.append((c_row,c_col))
            paths.append(path,info[1])
        if paths.empty():
            return False
      elif self.row == self.maxgrid:
        if self._map[self.row][self.column+1] == "S" and previous !=(c_row,c_col+1):
          info = path_to_point(row,col,c_row,c_col+1,cost+1,(c_row,c_col))
          if info != False:
            path = info[0]
            path.append((c_row,c_col))
            paths.append(path,info[1])
        if self._map[self.row][self.column-1] == "S" and previous !=(c_row,c_col-1):
          info = path_to_point(row,col,c_row,c_col-1,cost+1,(c_row,c_col))
          if info != False:
            path = info[0]
            path.append((c_row,c_col))
            paths.append(path,info[1])
        if self._map[self.row-1][self.column] == "S" and previous !=(c_row-1,c_col):
          info = path_to_point(row,col,c_row-1,c_col,cost+1,(c_row,c_col))
          if info != False:
            path = info[0]
            path.append((c_row,c_col))
            paths.append(path,info[1])
        if paths.empty():
            return False
      elif self.column == self.maxgrid:
        if self._map[self.row][self.column-1] == "S" and previous !=(c_row,c_col-1):
          info = path_to_point(row,col,c_row,c_col-1,cost+1,(c_row,c_col))
          if info != False:
            path = info[0]
            path.append((c_row,c_col))
            paths.append(path,info[1])
        if self._map[self.row+1][self.column] == "S" and previous !=(c_row+1,c_col):
          info = path_to_point(row,col,c_row+1,c_col,cost+1,(c_row,c_col))
          if info != False:
            path = info[0]
            path.append((c_row,c_col))
            paths(path,info[1])
        if self._map[self.row-1][self.column] == "S" and previous !=(c_row-1,c_col):
          info = path_to_point(row,col,c_row-1,c_col,cost+1,(c_row,c_col))
          if info != False:
            path = info[0]
            path.append((c_row,c_col))
            paths.append(path,info[1])
        if paths.empty():
            return False

      else:
        if self._map[self.row][self.column+1] == "S" and previous !=(c_row,c_col+1):
          info = path_to_point(row,col,c_row,c_col+1,cost+1,(c_row,c_col))
          if info != False:
            path = info[0]
            path.append((c_row,c_col))
            paths.append(path,info[1])
        if self._map[self.row][self.column-1] == "S" and previous !=(c_row,c_col-1):
          info = path_to_point(row,col,c_row,c_col-1,cost+1,(c_row,c_col))
          if info != False:
            path = info[0]
            path.append((c_row,c_col))
            paths.append(path,info[1])
        if self._map[self.row+1][self.column] == "S" and previous !=(c_row+1,c_col):
          info = path_to_point(row,col,c_row+1,c_col,cost+1,(c_row,c_col))
          if info != False:
            path = info[0]
            path.append((c_row,c_col))
            paths(path,info[1])
        if self._map[self.row-1][self.column] == "S" and previous !=(c_row-1,c_col):
          info = path_to_point(row,col,c_row-1,c_col,cost+1,(c_row,c_col))
          if info != False:
            path = info[0]
            path.append((c_row,c_col))
            paths.append(path,info[1])
        if paths.empty():
            return False
      best_path = paths[0]
      for x in paths:
        if x[1] > path[1]:
          path = x
      return best_path
    # ======================================================================
    # YOUR CODE ENDS
    # ======================================================================
