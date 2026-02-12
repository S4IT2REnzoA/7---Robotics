import numpy as np

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


        pass

    def is_in_bounds(self,y,x):
        if(x>self.W or x<0):
            return False
        if(y>self.H or y<0):
            return False
        return True

    def is_walkeable(self,y,x):
        return not(self.navigation_map[x][y])
    
    def get_neighbors(self,y,x):
        neighbors = []
        print("Neighbors of (",y,",",x,")" )
        for i in (-1,1):
                print("Testing(",y+i,",",x,")")
                if(self.is_in_bounds(y+i,x)):
                    if(self.is_walkeable(y+i,x)):
                        neighbors.append([y+i,x])
        for j in (-1,1):
            print("Testing(",y,",",x+j,")")
            if(self.is_in_bounds(y,x+j)):
                if(self.is_walkeable(y,x+j)):
                    neighbors.append([y,x+j])
        return neighbors
        
            
           
