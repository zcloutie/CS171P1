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
        self._map = [["  " for x in range(7)] for x in range(7)]
        self.row = 0
        self.column = 0
        self.t_row = 0
        self.t_col = 0
        self.t_dir = "R"
        self.maxgrid = 6
        self.frontier = []
        self.stench_sources=[]
        self.wumpus_possibles = []
        self.wumpus_location = self._map[0][0]
        self.wumpus_alive = True
        self.gold = False       
        self.direction = "R"
        self.to_do = []
        self.arrived = True
        self.retreat = False
        self.initial = True
        self.bumped = False
                
        pass
        # ======================================================================
        # YOUR CODE ENDS
        # ======================================================================

    def getAction( self, stench, breeze, glitter, bump, scream ):
        # ======================================================================
        # YOUR CODE BEGINS
        # ======================================================================
        
        if self.row == 0 and self.column == 0 and (stench or breeze) and self.arrived:        
          return Agent.Action.CLIMB
        if self.row == 0 and self.column == 0 and (self.gold or self.retreat) and (self.t_row,self.t_col) == (self.row,self.column):
          self.to_do.append((Agent.Action.CLIMB,(self.row,self.column),self.direction))
        elif self.row == 0 and self.column == 0 and self.initial:
          self._map[self.row][self.column] = "S"
          self._map[self.row+1][self.column] = "S?"
          self.frontier.append((self.row+1,self.column))
          self._map[self.row][self.column+1] = "S?"
          self.frontier.append((self.row,self.column+1))
        self.initial = False
        self._map[self.row][self.column] = "S"
        for r in range(len(self._map)):
          for c in range(len(self._map)):
            if self._map[r][c] == "S?":
              if (r,c) not in self.frontier:
                self.frontier.append((r,c))
        "self.print_info()"
        if glitter:
            """print("FOUND GOLD")"""
            self.row = self.t_row
            self.column = self.t_col
            self.direction = self.t_dir
            self.gold = True
            self.to_do = []
            self.arrived = True
            return Agent.Action.GRAB
        if bump:
            self.to_do = []
            self.hitEdge()
            self.row = self.t_row
            self.column = self.t_col
            self.arrived = True
        if len(self.to_do) == 0:
          self.arrived = True
          
          if breeze:
            self.pit_danger()
          if stench and self.wumpus_alive:
            self.wumpus_danger()
          if not breeze and (not stench or not self.wumpus_alive):
            self.safe()
          if scream:
            self.wumpus_alive = False
            
          if self.gold:
            """print("MOVING HOME")"""
            self.arrived = False
            self.move_to_point(0,0)
          else:
              if len(self.frontier) == 0:
                self.arrived = False
                self.retreat = True
                self.move_to_point(0,0)
              elif not self.gold:
                self.arrived = False
                self.search()
        if len(self.to_do) != 0:          
          next_action = self.to_do[0][0]
          self.t_row = self.to_do[0][1][0]
          self.t_col = self.to_do[0][1][1]
          self.t_dir = self.to_do[0][2]
          self.to_do.pop(0)
          return next_action
        # ======================================================================
        # YOUR CODE ENDS
        # ======================================================================
    
    # ======================================================================
    # YOUR CODE BEGINS
    # ======================================================================

    def print_info(self):
        print("""{},{},{},{},{},{},{} \n
{},{},{},{},{},{},{} \n
{},{},{},{},{},{},{} \n
{},{},{},{},{},{},{} \n
{},{},{},{},{},{},{} \n
{},{},{},{},{},{},{} \n
{},{},{},{},{},{},{} \n
self.row = {} \n
self.column = {} \n
self.frontier = {} \n
self.direction = {} \n
self.t_row = {}
self.t_col = {}
self.maxgrid""".format(self._map[6][0],self._map[6][1],self._map[6][2],self._map[6][3],self._map[6][4],self._map[6][5],self._map[6][6],self._map[5][0],self._map[5][1],self._map[5][2],self._map[5][3],self._map[5][4],self._map[5][5],self._map[5][6],self._map[4][0],self._map[4][1],self._map[4][2],self._map[4][3],self._map[4][4],self._map[4][5],self._map[4][6],self._map[3][0],self._map[3][1],self._map[3][2],self._map[3][3],self._map[3][4],self._map[3][5],self._map[3][6],self._map[2][0],self._map[2][1],self._map[2][2],self._map[2][3],self._map[2][4],self._map[2][5],self._map[2][6],self._map[1][0],self._map[1][1],self._map[1][2],self._map[1][3],self._map[1][4],self._map[1][5],self._map[1][6],self._map[0][0],self._map[0][1],self._map[0][2],self._map[0][3],self._map[0][4],self._map[0][5],self._map[0][6],self.row,self.column,self.frontier,self.direction,self.t_row,self.t_col,self.maxgrid))

    def hitEdge(self):
      if self.bumped == False:
        if self.direction == "R":
          self.bumped = True
          self.t_col+=-1
          self.maxgrid = self.t_col
          self.maxgrid = self.t_col
        elif self.direction == "U":
          self.bumped = True
          self.t_row+=-1
          self.maxgrid = self.t_row
          self.maxgrid = self.t_row
      if self.bumped:
        to_remove = []
        for i in self.frontier:
          if not self.in_bounds(i):
            to_remove.append(i)
        for e in to_remove:
          self.frontier.remove(e)
      return

    def in_bounds(self,coor):
      if coor[0] > self.maxgrid or coor[0] < 0:
        return False
      if coor[1] > self.maxgrid or coor[1] < 0:
        return False
      return True

    def reverse(self):
      if self.direction == "U":
        self.direction = "D"
      elif self.direction == "L":
        self.direction = "R"
      elif self.direction == "R":
        self.direction = "L"
      elif self.direction == "D":
        self.direction = "U"
      self.to_do.append((Agent.Action.TURN_RIGHT,(self.row,self.column),self.direction))
      self.to_do.append((Agent.Action.TURN_RIGHT,(self.row,self.column),self.direction))
      return self.direction

    def turn_left(self):
      if self.direction == "U":
        self.direction = "L"
      elif self.direction == "L":
        self.direction = "D"
      elif self.direction == "R":
        self.direction = "U"
      elif self.direction == "D":
        self.direction = "R"
      self.to_do.append((Agent.Action.TURN_LEFT,(self.row,self.column),self.direction))
      return self.direction

    def turn_right(self):
      if self.direction == "U":
        self.direction = "R"
      elif self.direction == "L":
        self.direction = "U"
      elif self.direction == "R":
        self.direction = "D"
      elif self.direction == "D":
        self.direction = "L"
      self.to_do.append((Agent.Action.TURN_RIGHT,(self.row,self.column),self.direction))
      return self.direction

    def turn_to(self,row,col):
      if self.row == row and self.column == col:
        return self.direction
      if (self.row+1,self.column) == (row,col):
        if self.direction == "U":
          return self.direction
        elif self.direction == "L":
          self.turn_right()
        elif self.direction == "R":
          self.turn_left()
        elif self.direction == "D":
          self.reverse()
      elif (self.row-1,self.column) == (row,col):
        if self.direction == "D":
          return self.direction
        elif self.direction == "R":
          self.turn_right()
        elif self.direction == "L":
          self.turn_left()
        elif self.direction == "U":
          self.reverse()
      elif (self.row,self.column+1) == (row,col):
        if self.direction == "R":
          return self.direction
        elif self.direction == "U":
          self.turn_right()
        elif self.direction == "D":
          self.turn_left()
        elif self.direction == "L":
          self.reverse()
      elif (self.row,self.column-1) == (row,col):
        if self.direction == "L":
          return self.direction
        elif self.direction == "D":
          self.turn_right()
        elif self.direction == "U":
          self.turn_left()
        elif self.direction == "R":
          self.reverse()
      return self.direction
    
    def whats_forward(self):
      if self.direction == "U":
        return self._map[self.row+1][self.column]
      elif self.direction == "L":
        return self._map[self.row][self.column-1]
      elif self.direction == "R":
        return self._map[self.row][self.column+1]
      elif self.direction == "D":
        return self._map[self.row-1][self.column]
    
    
    def update_map(self,r,c,z):
      if r > self.maxgrid or r < 0:
        return
      elif c > self.maxgrid or c < 0:
        return
      else:
        if self._map[r][c] == "S" or self._map[r][c] == "S?":
          return
        if z == "S?":
          if self._map[r][c] == "W?":
            self.wumpus_possibles.remove((r,c))
          self._map[r][c] = z
          if (r,c) not in self.frontier:
            self.frontier.append((r,c))
        if self._map[r][c] == "":
          self._map[r][c] = z
          if z == "W?":
            self.wumpus_possibles.append((r,c))
        
          
    def adj_map(self,r,c,z):
      self.update_map(r+1,c,z)
      self.update_map(r-1,c,z)
      self.update_map(r,c+1,z)
      self.update_map(r,c-1,z)
  		
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
      self.t_row = self.row
      self.t_col = self.column
      """print("TRYING TO GET PATH TO {},{} from {},{}".format(row,col,self.row,self.column))"""
      """self.print_info()"""
      path = self.path_to_point(row,col,self.row,self.column,0,[])[0]
      path.reverse()
      """print("PATH TO {},{}:{}".format(row,col,path))"""
      while len(path) != 0:
        self.move_to_next(path[0][0],path[0][1])
        path.pop(0)
      return
      
    def move_to_next(self,row,col):
      if self.row == row and self.column == col:
        return
      self.turn_to(row,col)
      self.row = row
      self.column = col
      self.to_do.append((Agent.Action.FORWARD,(self.row,self.column),self.direction))
      return

    def search(self):
        go_to = self.frontier[0]
        for i in self.frontier:
            if self.distance((self.row,self.column),i) < self.distance((self.row,self.column),go_to):
                go_to = i
        self.move_to_point(go_to[0],go_to[1])
        self.frontier.remove((go_to[0],go_to[1]))

    
    def path_to_point(self,row,col,c_row,c_col,cost,explored):
      path = []
      paths = []
      explored.append((c_row,c_col))
      if row == c_row and col == c_col:
        path.append((c_row,c_col))
        return (path,cost)
      if c_row == self.maxgrid and c_col == self.maxgrid:
        if "S" in self._map[c_row][c_col-1] and not (c_row,c_col-1) in explored:
          info = self.path_to_point(row,col,c_row,c_col-1,cost+1,explored)
          if info != False:
            path = info[0]
            path.append((c_row,c_col))
            paths.append((path,info[1]))
        if "S" in self._map[c_row-1][c_col] and not (c_row-1,c_col)in explored:
          info = self.path_to_point(row,col,c_row-1,c_col,cost+1,explored)
          if info != False:
            path = info[0]
            path.append((c_row,c_col))
            paths.append((path,info[1]))
      elif c_row == 0 and c_col == 0:
        if "S" in self._map[c_row][c_col+1] and not (c_row,c_col+1)in explored:
          info = self.path_to_point(row,col,c_row,c_col+1,cost+1,explored)
          if info != False:
            path = info[0]
            path.append((c_row,c_col))
            paths.append((path,info[1]))
        if "S" in self._map[c_row+1][c_col] and not (c_row+1,c_col)in explored:
          info = self.path_to_point(row,col,c_row+1,c_col,cost+1,explored)
          if info != False:
            path = info[0]
            path.append((c_row,c_col))
            paths.append((path,info[1]))
      elif c_row == self.maxgrid:
        if "S" in self._map[c_row][c_col+1] and not (c_row,c_col+1)in explored:
          info = self.path_to_point(row,col,c_row,c_col+1,cost+1,explored)
          if info != False:
            path = info[0]
            path.append((c_row,c_col))
            paths.append((path,info[1]))
        if "S" in self._map[c_row][c_col-1] and not (c_row,c_col-1)in explored:
          info = self.path_to_point(row,col,c_row,c_col-1,cost+1,explored)
          if info != False:
            path = info[0]
            path.append((c_row,c_col))
            paths.append((path,info[1]))
        if "S" in self._map[c_row-1][c_col] and not (c_row-1,c_col)in explored:
          info = self.path_to_point(row,col,c_row-1,c_col,cost+1,explored)
          if info != False:
            path = info[0]
            path.append((c_row,c_col))
            paths.append((path,info[1]))
      elif c_row == 0:
        if "S" in self._map[c_row][c_col+1] and not (c_row,c_col+1)in explored:
          info = self.path_to_point(row,col,c_row,c_col+1,cost+1,explored)
          if info != False:
            path = info[0]
            path.append((c_row,c_col))
            paths.append((path,info[1]))
        if "S" in self._map[c_row][c_col-1] and not (c_row,c_col-1)in explored:
          info = self.path_to_point(row,col,c_row,c_col-1,cost+1,explored)
          if info != False:
            path = info[0]
            path.append((c_row,c_col))
            paths.append((path,info[1]))
        if "S" in self._map[c_row+1][c_col] and not (c_row+1,c_col)in explored:
          info = self.path_to_point(row,col,c_row+1,c_col,cost+1,explored)
          if info != False:
            path = info[0]
            path.append((c_row,c_col))
            paths.append((path,info[1]))
      elif c_col == self.maxgrid:
        if "S" in self._map[c_row][c_col-1] and not (c_row,c_col-1)in explored:
          info = self.path_to_point(row,col,c_row,c_col-1,cost+1,explored)
          if info != False:
            path = info[0]
            path.append((c_row,c_col))
            paths.append((path,info[1]))
        if "S" in self._map[c_row+1][c_col] and not (c_row+1,c_col)in explored:
          info = self.path_to_point(row,col,c_row+1,c_col,cost+1,explored)
          if info != False:
            path = info[0]
            path.append((c_row,c_col))
            paths.append((path,info[1]))
        if "S" in self._map[c_row-1][c_col] and not(c_row-1,c_col)in explored:
          info = self.path_to_point(row,col,c_row-1,c_col,cost+1,explored)
          if info != False:
            path = info[0]
            path.append((c_row,c_col))
            paths.append((path,info[1]))
      elif c_col == 0:
        if "S" in self._map[c_row][c_col+1] and not(c_row,c_col+1)in explored:
          info = self.path_to_point(row,col,c_row,c_col+1,cost+1,explored)
          if info != False:
            path = info[0]
            path.append((c_row,c_col))
            paths.append((path,info[1]))
        if "S" in self._map[c_row+1][c_col] and not(c_row+1,c_col)in explored:
          info = self.path_to_point(row,col,c_row+1,c_col,cost+1,explored)
          if info != False:
            path = info[0]
            path.append((c_row,c_col))
            paths.append((path,info[1]))
        if "S" in self._map[c_row-1][c_col] and not(c_row-1,c_col)in explored:
          info = self.path_to_point(row,col,c_row-1,c_col,cost+1,explored)
          if info != False:
            path = info[0]
            path.append((c_row,c_col))
            paths.append((path,info[1]))
      else:
        if "S" in self._map[c_row][c_col+1] and not(c_row,c_col+1)in explored:
          info = self.path_to_point(row,col,c_row,c_col+1,cost+1,explored)
          if info != False:
            path = info[0]
            path.append((c_row,c_col))
            paths.append((path,info[1]))
        if "S" in self._map[c_row][c_col-1] and not(c_row,c_col-1)in explored:
          info = self.path_to_point(row,col,c_row,c_col-1,cost+1,explored)
          if info != False:
            path = info[0]
            path.append((c_row,c_col))
            paths.append((path,info[1]))
        if "S" in self._map[c_row+1][c_col] and not(c_row+1,c_col)in explored:
          info = self.path_to_point(row,col,c_row+1,c_col,cost+1,explored)
          if info != False:
            path = info[0]
            path.append((c_row,c_col))
            paths.append((path,info[1]))
        if "S" in self._map[c_row-1][c_col] and not(c_row-1,c_col)in explored:
          info = self.path_to_point(row,col,c_row-1,c_col,cost+1,explored)
          if info != False:
            path = info[0]
            path.append((c_row,c_col))
            paths.append((path,info[1]))
      if len(paths) == 0:
        return False
      best_path = paths[0]
      for x in paths:
        if x[1] < best_path[1]:
          best_path = x
      return best_path
    # ======================================================================
    # YOUR CODE ENDS
    # ======================================================================
