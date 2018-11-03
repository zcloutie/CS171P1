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
          self.frontier.append((self.row+1,self.column))
          self._map[self.row][self.column+1] = "S"
          self.frontier.append((self.row+1,self.column))

        if self.gold:
            self.move_to_point(0,0)
        if glitter:
          self.gold = True
          return Agent.Action.GRAB
        if bump:
          self.hitEdge()
        if breeze:
          self.pit_danger()
        if stench and wumpus_alive:
          self.wumpus_danger()
        if not breeze and (not stench or not wumpus_alive):
          self.safe()
        if scream:
          self.wumpus_alive = False

        if len(self.frontier) == 0:
            self.move_to_point(0,0)
            return Agent.Action.CLIMB
        else:
            return self.search()
        # ======================================================================
        # YOUR CODE ENDS
        # ======================================================================
    
    # ======================================================================
    # YOUR CODE BEGINS
    # ======================================================================
    def hitEdge(self):
      if self.direction == "E":
        self.maxgrid = self.column
        self.maxgrid = self.column
      elif self.direction == "N":
        self.maxgrid = self.row
        self.maxgrid = self.row
      return
    def reverse(self):
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
    def turn_left(self):
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
    def turn_right(self):
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

    def turn_to(self,row,col):
      if row == self.row:
        if col > self.column:
          if self.direction == "E":
            return
          elif self.direction == "W":
            self.reverse()
          elif self.direction == "N":
            self.turn_right()
          elif self.direction == "S":
            self.turn_left()
        else:
          if self.direction == "W":
            return
          elif self.direction == "E":
            self.reverse()
          elif self.direction == "S":
            self.turn_right()
          elif self.direction == "N":
            self.turn_left()
      else:
        if row > self.row:
          if self.direction == "N":
            return
          elif self.direction == "S":
            self.reverse()
          elif self.direction == "W":
            self.turn_right()
          elif self.direction == "E":
            self.turn_left()
        else:
          if self.direction == "S":
            return
          elif self.direction == "N":
            self.reverse()
          elif self.direction == "E":
            self.turn_right()
          elif self.direction == "W":
            self.turn_left()
      return
    
    def whats_forward(self):
      if self.direction == "N":
        return self._map[self.row+1][self.column]
      elif self.direction == "W":
        return self._map[self.row][self.column-1]
      elif self.direction == "E":
        return self._map[self.row][self.column+1]
      elif self.direction == "S":
        return self._map[self.row-1][self.column]
    
    def update_map(self,x,y,z):
      if x > self.maxgrid or x < 0:
        return
      elif y > self.maxgrid or y < 0:
        return
      else:
        if z == "S?":
          if self._map[x][y] == "W?":
            self.wumpus_possibles.remove(x)
            self._map[x][y] = z
            if (x,y) not in self.frontier:
              self.frontier.append(x,y)
        if self._map[x][y] == "":
          self._map[x][y] = z
          if z == "W?":
            wumpus_possibles.append(x,y)
        elif self._map[x][y] == "S" or self._map[x][y] == "S?":
          return
          
    def adj_map(self,x,y,z):
      self.update_map(x+1,y,z)
      self.update_map(x-1,y,z)
      self.update_map(x,y+1,z)
      self.update_map(x,y-1,z)
  		
    def pit_danger(self):
      self.adj_map(self.row, self.column, "P?")
      
    def safe(self):
      self.adj_map(self.row, self.column, "S?")
      
    def wumpus_danger(self):
      self.adj_map(self.row, self.column, "W?")
      self.stench_sources.append((self.row,self.column))
	
    def distance(self,p1,p2):
      distance = abs(p1[0]-p2[0])
      distance+= abs(p1[1]-p2[1])
      return distance

    def move_to_point(self,row,col):
      path = self.path_to_point(row,col,self.row,self.column,0,(self.row,self.column))[0].reverse()
      while len(path) != 0:
        self.move_to_next(path[0][0],path[0][1])
        path.pop(0)
      return
      
    def move_to_next(self,row,col):
      self.turn_to(row,col)
      return Agent.Action.FORWARD

    def search(self):
        go_to = self.frontier[0]
        for i in self.frontier:
            if self.distance((self.row,self.column),i) < self.distance((self.row,self.column),go_to):
                go_to = i
        self.move_to_point(go_to[0],go_to[1])
        self.frontier.remove(go_to[0],go_to[1])

    
    def path_to_point(self,row,col,c_row,c_col,cost,previous):
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
        if len(paths) != 0:
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
        if len(paths) != 0:
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
        if len(paths) != 0:
            return False
      else:
        if self._map[self.row][self.column+1] == "S" and previous !=(c_row,c_col+1):
          info = self.path_to_point(row,col,c_row,c_col+1,cost+1,(c_row,c_col))
          if info != False:
            path = info[0]
            path.append((c_row,c_col))
            paths.append(path,info[1])
        if self._map[self.row][self.column-1] == "S" and previous !=(c_row,c_col-1):
          info = self.path_to_point(row,col,c_row,c_col-1,cost+1,(c_row,c_col))
          if info != False:
            path = info[0]
            path.append((c_row,c_col))
            paths.append(path,info[1])
        if self._map[self.row+1][self.column] == "S" and previous !=(c_row+1,c_col):
          info = self.path_to_point(row,col,c_row+1,c_col,cost+1,(c_row,c_col))
          if info != False:
            path = info[0]
            path.append((c_row,c_col))
            paths(path,info[1])
        if self._map[self.row-1][self.column] == "S" and previous !=(c_row-1,c_col):
          info = self.path_to_point(row,col,c_row-1,c_col,cost+1,(c_row,c_col))
          if info != False:
            path = info[0]
            path.append((c_row,c_col))
            paths.append(path,info[1])
        if len(paths) != 0:
            return False
      best_path = paths[0]
      for x in paths:
        if x[1] > path[1]:
          path = x
      return best_path
    # ======================================================================
    # YOUR CODE ENDS
    # ======================================================================
