import numpy as np
import random as rand

class Maze:
    
    def __init__(self,H,W,start_node,end_node):
        self.H = H
        self.W = W
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
    
    def get_neighbors(self,y,x):
        neighbors = []
        print("Neighbors of (",y,",",x,")" )
        for i in (-1,1):
                if(self.is_in_bounds(y+i,x)):
                    if(self.is_walkeable(y+i,x)):
                        neighbors.append([y+i,x])
        for j in (-1,1):
            if(self.is_in_bounds(y,x+j)):
                if(self.is_walkeable(y,x+j)):
                    neighbors.append([y,x+j])
        return neighbors
    
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
        
           
