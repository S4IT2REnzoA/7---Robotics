import numpy as np
import random as rand
import tools


class Maze:
    
    def __init__(self,H,W,start_node,end_node,diagonal = 0):
        self.H = H
        self.W = W
        self.diagonal = diagonal
        if(len(start_node)!=2):
            return False
        if(len(end_node)!=2):
            return False
        self.start_node = start_node
        self.end_node = end_node
        self.navigation_map = np.zeros((H,W))
        self.reward_map = np.zeros((H,W))

        self.generateMaze()
        self.generateReward()

    def is_in_bounds(self,y,x):
        if(x>self.W or x<0):
            return False
        if(y>self.H or y<0):
            return False
        return True

    def is_walkeable(self,y,x):
        return not(self.navigation_map[y][x])
    
    def _get_neighbors_straight(self,y,x):
        neighbors = []
        print("Neighbors of (",y,",",x,")" )
        for i in (-1,1):
                if(self.is_in_bounds(y+i,x)):
                    if(self.is_walkeable(y+i,x)):
                        neighbors.append((y+i,x))
        for j in (-1,1):
            if(self.is_in_bounds(y,x+j)):
                if(self.is_walkeable(y,x+j)):
                    neighbors.append((y,x+j))
        return neighbors
    
    def _get_neighbors_diag(self,y,x):
        neighbors = []
        print("Neighbors of (",y,",",x,")" )
        for i in (-1,0,1):
            for j in (-1,0,1):
                if(self.is_in_bounds(y+i,x+j)):
                    if(self.is_walkeable(y+i,x+j)):
                        neighbors.append((y+i,x+j))
        neighbors.remove([y,x])
        return neighbors
    
    def get_neighbors(self,y,x):
        if(self.diagonal):
            return self._get_neighbors_diag(y,x)
        else:
            return self._get_neighbors_straight(y,x)
    
    def generateMaze(self,prob=0.5):
        for y in range(self.H):
            for x in range(self.W):
                self.navigation_map[y][x] = (rand.random()>prob)
        self.navigation_map[self.start_node] = 0
        self.navigation_map[self.end_node] = 0
        
    def generateReward(self):
        for y in range(self.H):
            for x in range(self.W):
                if(self.is_walkeable(y,x)):
                    self.reward_map[y][x] = 1
        self.reward_map[self.end_node] = -10
    

    def a_star(self,start,end):
        queue = []
        g_scores = {start : 0}
        f_scores = {start : tools.manhattan_dist(end,start)}
        origins = {}
        queue.append((f_scores[start],start))
        while(queue):
            current_entry = min(queue)
            current_tile = current_entry[1]
            queue.remove(current_entry)
            if(current_tile==end):
                path = self.returnPath(origins,start,end)
                return
            for neighbor in self.get_neighbors(current_tile[0],current_tile[1]):
                temp_g = g_scores[current_tile] + self.reward_map[neighbor]
                if neighbor not in g_scores.keys() or temp_g < g_scores[neighbor]:
                    origins[neighbor] = current_tile
                    g_scores[neighbor] = temp_g
                    f = temp_g + tools.manhattan_dist(end,neighbor)
                    f_scores[neighbor] = f
                    queue.append((f,neighbor))
        return None

    def returnPath(self, origins,start, end):
        reversed_path = []
        previous_tile = origins[end]
        reversed_path.append(previous_tile)
        while(previous_tile!=start):
            previous_tile = origins[previous_tile]
        path = reversed_path.reverse()
        return path


            




    def solve(self, method):

        return method(self.start_node,self.end_node)
           
