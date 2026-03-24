import numpy as np
import random as rand
import tools
import pygame
import heapq



class Maze:
    MAZE_DISPLAY_H = 400
    MAZE_DISPLAY_W = 400
    
    def __init__(self,H,W,start_node,end_node,diagonal = 0,window = 0):
        self.H = H
        self.W = W
        self.diagonal = diagonal
        self.window = window
        self.last_explored = set()
        if(len(start_node)!=2):
            return False
        if(len(end_node)!=2):
            return False
        self.start_node = start_node
        self.end_node = end_node
        self.navigation_map = np.zeros((H,W))
        self.reward_map = np.zeros((H,W))

        self.generateMaze(0.8)
        self.generateReward()

    def is_in_bounds(self,y,x):
        if(x>=self.W or x<0):
            return False
        if(y>=self.H or y<0):
            return False
        return True

    def is_walkeable(self,y,x):
        return not(self.navigation_map[y][x])
    
    def _get_neighbors_straight(self,y,x):
        neighbors = []
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
        for i in (-1,0,1):
            for j in (-1,0,1):
                if(self.is_in_bounds(y+i,x+j)):
                    if(self.is_walkeable(y+i,x+j)):
                        neighbors.append((y+i,x+j))
        neighbors.remove((y,x))
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
        self.displayBlankMaze()
        heap = []
        g_scores = {start : 0}
        f_scores = {start : tools.manhattan_dist(end,start)}
        origins = {}
        number_nodes_explored = 0
        nodes_explored = []
        heapq.heappush(heap, (f_scores[start], start))
        while(heap):
            number_nodes_explored +=1
            current_entry = heapq.heappop(heap)
            current_tile = current_entry[1]
            nodes_explored.append(current_tile)
            if(current_tile==end):
                path = self.returnPath(origins,start,end)
                self.displayPath(path)
                print("A* explored ",number_nodes_explored, "before finding the end")
                self.waitForKey()
                return path
            for neighbor in self.get_neighbors(current_tile[0],current_tile[1]):
                temp_g = g_scores[current_tile] + self.reward_map[neighbor]
                if neighbor not in g_scores.keys() or temp_g < g_scores[neighbor]:
                    origins[neighbor] = current_tile
                    g_scores[neighbor] = temp_g
                    f = temp_g + tools.manhattan_dist(end,neighbor)
                    f_scores[neighbor] = f
                    heapq.heappush(heap, (f, neighbor))
            self.displayMaze(nodes_explored)
        self.waitForKey()
        return None
    def Dijkstra(self,start,end):
        self.displayBlankMaze()
        heap = []
        g_scores = {start : 0}
        origins = {}
        number_nodes_explored = 0
        nodes_explored = []
        heapq.heappush(heap, (0,start))
        while(heap):
            number_nodes_explored +=1
            current_entry = heapq.heappop(heap)
            current_tile = current_entry[1]
            nodes_explored.append(current_tile)
            if(current_tile==end):
                path = self.returnPath(origins,start,end)
                print("Dijkstra explored ",number_nodes_explored, "before finding the end")
                self.displayPath(path)
                self.waitForKey()
                return path
            for neighbor in self.get_neighbors(current_tile[0],current_tile[1]):
                temp_g = g_scores[current_tile] + self.reward_map[neighbor]
                if neighbor not in g_scores.keys() or temp_g < g_scores[neighbor]:
                    origins[neighbor] = current_tile
                    g_scores[neighbor] = temp_g
                    heapq.heappush(heap, (temp_g,neighbor))
            self.displayMaze(nodes_explored)
        self.waitForKey()
        return

    def returnPath(self, origins,start, end):
        path = [end]
        previous_tile = origins[end]
        path.append(previous_tile)
        while(previous_tile!=start):
            previous_tile = origins[previous_tile]
            path.append(previous_tile)
        path.reverse()
        return path

    def displayBlankMaze(self):
        if(self.window):
            step_x = self.MAZE_DISPLAY_W/self.W
            step_y = self.MAZE_DISPLAY_H/self.H
            for y in range(self.H):
                for x in range(self.W):
                    if(self.is_walkeable(y,x)):
                        pygame.draw.rect(self.window,(255,255,255),(x*step_x,y*step_y,step_x,step_y))
                    else:
                        pygame.draw.rect(self.window,(0,0,0),(x*step_x,y*step_y,step_x,step_y))
            pygame.display.flip()
            self.last_explored = set()

    def displayMaze(self,explored_nodes):
        if(self.window):
            step_x = self.MAZE_DISPLAY_W/self.W
            step_y = self.MAZE_DISPLAY_H/self.H
            explored_set = set(explored_nodes)
            newly_explored = explored_set - self.last_explored

            for y, x in newly_explored:
                pygame.draw.rect(self.window,(255,0,0),(x*step_x,y*step_y,step_x,step_y))

            self.last_explored = explored_set
            pygame.display.flip()

    def displayPath(self,path):
        if(self.window):
            step_x = self.MAZE_DISPLAY_W/self.W
            step_y = self.MAZE_DISPLAY_H/self.H
            for node in path:
                pygame.draw.rect(self.window,(0,255,0),(node[1]*step_x,node[0]*step_y,step_x,step_y))
            pygame.display.flip()

    def waitForKey(self):
        print("waitForKey: Waiting for user input...")
        if(self.window):
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        print("waitForKey: Key pressed!")
                        waiting = False
                    if event.type == pygame.QUIT:
                        print("waitForKey: Window closed!")
                        waiting = False
        print("waitForKey: Finished")

    def Dijkstra_Bi_Simple(self,start,end):
        print("Starting Bidirectional Dijkstra")
        self.displayBlankMaze()

        # Step 0: Calculate midway distance
        midway_distance = tools.manhattan_dist(start, end) / 2
        print(f"Step 0: Midway distance = {midway_distance}")

        # Step 1: Dijkstra from start until midway distance
        print("Step 1: Starting Dijkstra from start")
        heap1 = []
        g_scores1 = {start : 0}
        origins1 = {}
        nodes_explored1 = []
        visited1 = set()
        periphery_start = None
        heapq.heappush(heap1, (0, start))

        iteration_count = 0
        max_iterations = 10000
        while heap1 and iteration_count < max_iterations:
            iteration_count += 1
            if iteration_count % 1000 == 0:
                print(f"Step 1: Iteration {iteration_count}, heap size: {len(heap1)}, visited: {len(visited1)}")

            current_entry = heapq.heappop(heap1)
            current_tile = current_entry[1]

            if current_tile in visited1:
                continue

            visited1.add(current_tile)
            nodes_explored1.append(current_tile)

            # Check if we've reached midway distance
            if g_scores1[current_tile] >= midway_distance:
                periphery_start = current_tile
                print(f"Step 1: Reached midway distance at {periphery_start} after {iteration_count} iterations")
                break

            for neighbor in self.get_neighbors(current_tile[0], current_tile[1]):
                if neighbor not in visited1:
                    temp_g = g_scores1[current_tile] + self.reward_map[neighbor]
                    if neighbor not in g_scores1.keys() or temp_g < g_scores1[neighbor]:
                        origins1[neighbor] = current_tile
                        g_scores1[neighbor] = temp_g
                        heapq.heappush(heap1, (temp_g, neighbor))

        if iteration_count >= max_iterations:
            print(f"Step 1: REACHED MAX ITERATIONS ({max_iterations})")
        print(f"Step 1: Explored {len(nodes_explored1)} nodes, periphery_start = {periphery_start}")
        self.displayExplored(nodes_explored1, color1=(255, 0, 0))
        self.waitForKey()
        print("Step 1: Waiting for key completed")

        # Step 2: Dijkstra from end until midway distance
        print("Step 2: Starting Dijkstra from end")
        heap2 = []
        g_scores2 = {end : 0}
        origins2 = {}
        nodes_explored2 = []
        visited2 = set()
        periphery_end = None
        heapq.heappush(heap2, (0, end))

        iteration_count = 0
        max_iterations = 10000
        while heap2 and iteration_count < max_iterations:
            iteration_count += 1
            if iteration_count % 1000 == 0:
                print(f"Step 2: Iteration {iteration_count}, heap size: {len(heap2)}, visited: {len(visited2)}")

            current_entry = heapq.heappop(heap2)
            current_tile = current_entry[1]

            if current_tile in visited2:
                print(f"Step 2: Skipping already visited node {current_tile}")
                continue

            visited2.add(current_tile)
            nodes_explored2.append(current_tile)

            # Check if we've reached midway distance
            if g_scores2[current_tile] >= midway_distance:
                periphery_end = current_tile
                print(f"Step 2: Reached midway distance at {periphery_end} after {iteration_count} iterations")
                break

            neighbors = self.get_neighbors(current_tile[0], current_tile[1])
            print(f"Step 2: Node {current_tile} has {len(neighbors)} neighbors")

            for neighbor in neighbors:
                if neighbor not in visited2:
                    temp_g = g_scores2[current_tile] + self.reward_map[neighbor]
                    if neighbor not in g_scores2.keys() or temp_g < g_scores2[neighbor]:
                        origins2[neighbor] = current_tile
                        g_scores2[neighbor] = temp_g
                        heapq.heappush(heap2, (temp_g, neighbor))

        if iteration_count >= max_iterations:
            print(f"Step 2: REACHED MAX ITERATIONS ({max_iterations})")
        print(f"Step 2: Explored {len(nodes_explored2)} nodes, periphery_end = {periphery_end}")
        self.displayExplored(nodes_explored1, nodes_explored2, color1=(255, 0, 0), color2=(128, 0, 128), color3=(165, 42, 42))
        self.waitForKey()
        print("Step 2: Waiting for key completed")

        # Step 3: Dijkstra from periphery_start to periphery_end
        print(f"Step 3: Starting Dijkstra from {periphery_start} to {periphery_end}")
        heap3 = []
        g_scores3 = {periphery_start : 0}
        origins3 = {}
        nodes_explored3 = []
        visited3 = set()
        heapq.heappush(heap3, (0, periphery_start))

        iteration_count = 0
        max_iterations = 10000
        while heap3 and iteration_count < max_iterations:
            iteration_count += 1
            if iteration_count % 1000 == 0:
                print(f"Step 3: Iteration {iteration_count}, heap size: {len(heap3)}, visited: {len(visited3)}")

            current_entry = heapq.heappop(heap3)
            current_tile = current_entry[1]

            if current_tile in visited3:
                continue

            visited3.add(current_tile)
            nodes_explored3.append(current_tile)

            if current_tile == periphery_end:
                print(f"Step 3: Reached periphery_end after {iteration_count} iterations")
                break

            for neighbor in self.get_neighbors(current_tile[0], current_tile[1]):
                if neighbor not in visited3:
                    temp_g = g_scores3[current_tile] + self.reward_map[neighbor]
                    if neighbor not in g_scores3.keys() or temp_g < g_scores3[neighbor]:
                        origins3[neighbor] = current_tile
                        g_scores3[neighbor] = temp_g
                        heapq.heappush(heap3, (temp_g, neighbor))

        if iteration_count >= max_iterations:
            print(f"Step 3: REACHED MAX ITERATIONS ({max_iterations})")
        print(f"Step 3: Explored {len(nodes_explored3)} nodes")
        self.displayExplored(nodes_explored1, nodes_explored2, nodes_explored3, color1=(255, 0, 0), color2=(128, 0, 128), color3=(0, 255, 255))
        self.waitForKey()
        print("Step 3: Waiting for key completed")

        # Reconstruct paths
        print("Reconstructing paths...")
        path1 = self.returnPath(origins1, start, periphery_start)
        print(f"Path 1 length: {len(path1)}")
        path2 = self.returnPath(origins2, end, periphery_end)
        print(f"Path 2 length: {len(path2)}")
        path3 = self.returnPath(origins3, periphery_start, periphery_end)
        print(f"Path 3 length: {len(path3)}")

        # Reverse path2 since it goes from end to periphery_end
        print("Reversing path 2...")
        path2.reverse()

        # Combine paths
        print("Combining paths...")
        full_path = path1[:-1] + path3 + path2[1:]
        print(f"Full path length: {len(full_path)}")

        print("Displaying complete path...")
        self.displayCompletePath(full_path, (0, 255, 0), (0, 255, 255), (0, 0, 255))
        self.waitForKey()

        print("Bidirectional Dijkstra completed")
        return full_path

    def displayExplored(self, explored1, explored2=None, explored3=None, color1=(255, 0, 0), color2=(128, 0, 128), color3=(165, 42, 42)):
        """Display explored nodes with different colors for each step"""
        print(f"displayExplored called with explored1 len={len(explored1) if explored1 else 0}, explored2={len(explored2) if explored2 else 0}, explored3={len(explored3) if explored3 else 0}")
        if not self.window:
            return

        step_x = self.MAZE_DISPLAY_W / self.W
        step_y = self.MAZE_DISPLAY_H / self.H

        explored1_set = set(explored1)
        explored2_set = set(explored2) if explored2 else set()
        explored3_set = set(explored3) if explored3 else set()
        print(f"Starting to draw explored nodes...")

        # Draw nodes explored in both (overlap)
        overlap = explored1_set & explored2_set
        print(f"Drawing {len(overlap)} overlapping nodes in color3")
        for y, x in overlap:
            pygame.draw.rect(self.window, color3, (x*step_x, y*step_y, step_x, step_y))

        # Draw nodes explored only in step 1
        only_1 = explored1_set - overlap
        print(f"Drawing {len(only_1)} nodes only in step 1 in color1")
        for y, x in only_1:
            pygame.draw.rect(self.window, color1, (x*step_x, y*step_y, step_x, step_y))

        # Draw nodes explored only in step 2
        only_2 = explored2_set - overlap
        print(f"Drawing {len(only_2)} nodes only in step 2 in color2")
        for y, x in only_2:
            pygame.draw.rect(self.window, color2, (x*step_x, y*step_y, step_x, step_y))

        # Draw nodes only in step 3
        only_3 = explored3_set - explored1_set - explored2_set
        print(f"Drawing {len(only_3)} nodes only in step 3 in cyan")
        for y, x in only_3:
            pygame.draw.rect(self.window, (0, 255, 255), (x*step_x, y*step_y, step_x, step_y))

        print("Calling pygame.display.flip()...")
        pygame.display.flip()
        print("displayExplored finished")

    def displayCompletePath(self, path, color1=(0, 255, 0), color2=(0, 255, 255), color3=(0, 0, 255)):
        """Display the final complete path"""
        if not self.window:
            return

        step_x = self.MAZE_DISPLAY_W / self.W
        step_y = self.MAZE_DISPLAY_H / self.H

        for node in path:
            pygame.draw.rect(self.window, (0, 255, 0), (node[1]*step_x, node[0]*step_y, step_x, step_y))

        pygame.display.flip()





    def solve(self, method):

        return method(self.start_node,self.end_node)
           
