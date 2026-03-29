import numpy as np
import random as rand
import tools
import pygame
import heapq
import sys
import time



class Maze:
    MAZE_DISPLAY_H = 800
    MAZE_DISPLAY_W = 800
    DISPLAY_THROTTLE = 500
    COLOR_WALL = (0, 0, 0)
    COLOR_WALKABLE = (255, 255, 255)
    COLOR_EXPLORED = (255, 0, 0)
    
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

        self.pixel_array = np.zeros((self.H, self.W, 3), dtype=np.uint8)
        if self.window:
            self._cell_surface = pygame.Surface((self.W, self.H))
            self._pending_flush = 0

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

            # Skip non-walkable tiles
            if not self.is_walkeable(current_tile[0], current_tile[1]):
                continue

            nodes_explored.append(current_tile)
            if(current_tile==end):
                path = self.returnPath(origins,start,end)
                self._last_nodes_explored = number_nodes_explored
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

            # Skip non-walkable tiles
            if not self.is_walkeable(current_tile[0], current_tile[1]):
                continue

            nodes_explored.append(current_tile)
            if(current_tile==end):
                path = self.returnPath(origins,start,end)
                print("Dijkstra explored ",number_nodes_explored, "before finding the end")
                self._last_nodes_explored = number_nodes_explored
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

    def returnPath(self, origins, start, end):
        if end == start:
            return [start]
        if end not in origins:
            print(f"returnPath: Warning - end {end} not reachable from start {start}")
            return [start, end]  # Direct connection as fallback
        path = [end]
        previous_tile = origins[end]
        path.append(previous_tile)
        while(previous_tile != start):
            if previous_tile not in origins:
                print(f"returnPath: Warning - broken path at {previous_tile}")
                break
            previous_tile = origins[previous_tile]
            path.append(previous_tile)
        path.reverse()
        return path

    def _flush(self):
        if not self.window:
            return
        pygame.surfarray.blit_array(self._cell_surface,
                                    self.pixel_array.transpose(1, 0, 2))
        scaled = pygame.transform.scale(self._cell_surface,
                                        (self.MAZE_DISPLAY_W, self.MAZE_DISPLAY_H))
        self.window.blit(scaled, (0, 0))
        pygame.display.flip()

    def displayBlankMaze(self):
        if not self.window:
            return
        self.pixel_array[self.navigation_map == 0] = self.COLOR_WALKABLE
        self.pixel_array[self.navigation_map != 0] = self.COLOR_WALL
        self._flush()
        self.last_explored = set()

    def displayMaze(self,explored_nodes):
        if not self.window:
            return
        explored_set = set(explored_nodes)
        newly_explored = explored_set - self.last_explored
        if newly_explored:
            ys, xs = zip(*newly_explored)
            self.pixel_array[list(ys), list(xs)] = self.COLOR_EXPLORED
        self.last_explored = explored_set
        self._pending_flush += len(newly_explored)
        if self._pending_flush >= self.DISPLAY_THROTTLE:
            self._flush()
            self._pending_flush = 0

    def displayPath(self,path):
        if not self.window:
            return
        for node in path:
            self.pixel_array[node[0], node[1]] = (0, 255, 0)
        self._flush()
        self._pending_flush = 0

    def waitForKey(self, close_on_key=False):
        """Wait for spacebar press. If close_on_key=True, return True when spacebar is pressed."""
        print("waitForKey: Press SPACEBAR to continue...")
        if not self.window:
            return False
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        print("waitForKey: Spacebar pressed!")
                        waiting = False
                        if close_on_key:
                            return True
                if event.type == pygame.QUIT:
                    print("waitForKey: Window closed!")
                    waiting = False
                    return True
        print("waitForKey: Finished")
        return False

    def Dijkstra_Bi_Simple(self,start,end):
        print("Starting Bidirectional Dijkstra")
        self.displayBlankMaze()

        # Step 0: Calculate exploration target (explore ~25% of maze from each end)
        total_cells = self.H * self.W
        target_explore_count = max(100, total_cells // 4)
        print(f"Step 0: Will explore ~{target_explore_count} nodes from each end")

        # Step 1: Dijkstra from start until target node count
        print("Step 1: Starting Dijkstra from start")
        heap1 = []
        g_scores1 = {start : 0}
        origins1 = {}
        nodes_explored1 = []
        visited1 = set()
        periphery_start = None
        heapq.heappush(heap1, (0, start))

        iteration_count = 0
        while heap1 and len(nodes_explored1) < target_explore_count:
            iteration_count += 1

            current_entry = heapq.heappop(heap1)
            current_tile = current_entry[1]

            if current_tile in visited1:
                continue

            # Only process walkable tiles
            if not self.is_walkeable(current_tile[0], current_tile[1]):
                continue

            visited1.add(current_tile)
            nodes_explored1.append(current_tile)
            periphery_start = current_tile

            for neighbor in self.get_neighbors(current_tile[0], current_tile[1]):
                if neighbor not in visited1 and self.is_walkeable(neighbor[0], neighbor[1]):
                    temp_g = g_scores1[current_tile] + self.reward_map[neighbor]
                    if neighbor not in g_scores1.keys() or temp_g < g_scores1[neighbor]:
                        origins1[neighbor] = current_tile
                        g_scores1[neighbor] = temp_g
                        heapq.heappush(heap1, (temp_g, neighbor))

        print(f"Step 1: Explored {len(nodes_explored1)} nodes, periphery_start = {periphery_start}")
        self.displayExplored(nodes_explored1, color1=(255, 0, 0))
        self.waitForKey()
        print("Step 1: Waiting for key completed")
        print("Step 1: Waiting for key completed")

        # Step 2: Dijkstra from end until target node count
        print("Step 2: Starting Dijkstra from end")
        heap2 = []
        g_scores2 = {end : 0}
        origins2 = {}
        nodes_explored2 = []
        visited2 = set()
        periphery_end = None
        heapq.heappush(heap2, (0, end))

        iteration_count = 0
        while heap2 and len(nodes_explored2) < target_explore_count:
            iteration_count += 1

            current_entry = heapq.heappop(heap2)
            current_tile = current_entry[1]

            if current_tile in visited2:
                continue

            # Only process walkable tiles
            if not self.is_walkeable(current_tile[0], current_tile[1]):
                continue

            visited2.add(current_tile)
            nodes_explored2.append(current_tile)
            periphery_end = current_tile

            for neighbor in self.get_neighbors(current_tile[0], current_tile[1]):
                if neighbor not in visited2 and self.is_walkeable(neighbor[0], neighbor[1]):
                    temp_g = g_scores2[current_tile] + self.reward_map[neighbor]
                    if neighbor not in g_scores2.keys() or temp_g < g_scores2[neighbor]:
                        origins2[neighbor] = current_tile
                        g_scores2[neighbor] = temp_g
                        heapq.heappush(heap2, (temp_g, neighbor))

        print(f"Step 2: Explored {len(nodes_explored2)} nodes, periphery_end = {periphery_end}")
        self.displayExplored(nodes_explored1, nodes_explored2, color1=(255, 0, 0), color2=(128, 0, 128), color3=(165, 42, 42))
        self.waitForKey()
        print("Step 2: Waiting for key completed")

        # Step 3: Dijkstra from periphery_start to find closest node from explored2 region
        print(f"Step 3: Starting Dijkstra from {periphery_start}, searching for nodes in region 2")
        explored2_set = set(nodes_explored2)
        heap3 = []
        g_scores3 = {periphery_start : 0}
        origins3 = {}
        nodes_explored3 = []
        visited3 = set()
        connection_node = None
        heapq.heappush(heap3, (0, periphery_start))

        iteration_count = 0
        max_iterations = 50000  # May need more iterations to reach region 2
        while heap3 and connection_node is None:
            iteration_count += 1

            current_entry = heapq.heappop(heap3)
            current_tile = current_entry[1]

            if current_tile in visited3:
                continue

            # Only process walkable tiles
            if not self.is_walkeable(current_tile[0], current_tile[1]):
                continue

            visited3.add(current_tile)
            nodes_explored3.append(current_tile)

            # Check if we reached a node from region 2
            if current_tile in explored2_set:
                connection_node = current_tile
                print(f"Step 3: Found connection to region 2 at {connection_node} after {iteration_count} iterations")
                break

            for neighbor in self.get_neighbors(current_tile[0], current_tile[1]):
                if neighbor not in visited3 and self.is_walkeable(neighbor[0], neighbor[1]):
                    temp_g = g_scores3[current_tile] + self.reward_map[neighbor]
                    if neighbor not in g_scores3.keys() or temp_g < g_scores3[neighbor]:
                        origins3[neighbor] = current_tile
                        g_scores3[neighbor] = temp_g
                        heapq.heappush(heap3, (temp_g, neighbor))

        if iteration_count >= max_iterations:
            print(f"Step 3: REACHED MAX ITERATIONS ({max_iterations})")
        if connection_node is None:
            connection_node = nodes_explored3[-1] if nodes_explored3 else periphery_start
            print(f"Step 3: Could not reach region 2, using closest node {connection_node}")
        print(f"Step 3: Explored {len(nodes_explored3)} nodes, connection at {connection_node}")
        self.displayExplored(nodes_explored1, nodes_explored2, nodes_explored3, color1=(255, 0, 0), color2=(128, 0, 128), color3=(0, 255, 255))
        # Force final flush to ensure all pixels are drawn
        self._flush()
        self._pending_flush = 0
        self.waitForKey()
        print("Step 3: Waiting for key completed")

        # Reconstruct paths
        print("Reconstructing paths...")
        path1 = self.returnPath(origins1, start, periphery_start)
        print(f"Path 1 length: {len(path1)}")
        path2 = self.returnPath(origins2, end, connection_node)
        print(f"Path 2 length: {len(path2)}")
        path3 = self.returnPath(origins3, periphery_start, connection_node)
        print(f"Path 3 length: {len(path3)}")

        # Reverse path2 since it goes from end to connection_node
        print("Reversing path 2...")
        path2.reverse()

        # Combine paths: path1 ends at periphery_start, path3 connects to connection_node, path2 starts at connection_node and ends at end
        print("Combining paths...")
        # path1[:-1] to skip duplicate periphery_start, path3[:-1] to skip duplicate connection_node, path2 as is (starts at connection_node after reverse)
        full_path = path1[:-1] + path3 + path2
        print(f"Full path length: {len(full_path)}")

        print("Displaying complete path...")
        self.displayCompletePath(full_path, (0, 255, 0), (0, 255, 255), (0, 0, 255))

        self._last_nodes_explored = len(nodes_explored1) + len(nodes_explored2) + len(nodes_explored3)
        should_close = self.waitForKey(close_on_key=True)
        if should_close:
            sys.exit()

        print("Bidirectional Dijkstra completed")
        return full_path

    def displayExplored(self, explored1, explored2=None, explored3=None, color1=(255, 0, 0), color2=(128, 0, 128), color3=(165, 42, 42)):
        """Display explored nodes with different colors for each step"""
        if not self.window:
            return

        explored1_set = set(explored1)
        explored2_set = set(explored2) if explored2 else set()
        explored3_set = set(explored3) if explored3 else set()

        # Draw nodes explored in both (overlap)
        overlap = explored1_set & explored2_set
        only_1 = explored1_set - overlap
        only_2 = explored2_set - overlap
        only_3 = explored3_set - explored1_set - explored2_set

        for group, color in [(overlap, color3), (only_1, color1), (only_2, color2), (only_3, (0, 255, 255))]:
            if group:
                ys, xs = zip(*group)
                self.pixel_array[list(ys), list(xs)] = color

        self._flush()
        self._pending_flush = 0

    def displayCompletePath(self, path, color1=(0, 255, 0), color2=(0, 255, 255), color3=(0, 0, 255)):
        """Display the final complete path"""
        if not self.window:
            return
        for node in path:
            self.pixel_array[node[0], node[1]] = (0, 255, 0)
        self._flush()
        self._pending_flush = 0

    def a_star_Bi_Simple(self, start, end):
        """Bidirectional A* with Manhattan heuristic - 3-step approach"""
        print("Starting Bidirectional A*")
        self.displayBlankMaze()

        # Step 0: Calculate exploration target
        total_cells = self.H * self.W
        target_explore_count = max(100, total_cells // 4)
        print(f"Step 0: Will explore ~{target_explore_count} nodes from each end")

        # Step 1: A* from start until target node count
        print("Step 1: Starting A* from start")
        heap1 = []
        g_scores1 = {start: 0}
        origins1 = {}
        nodes_explored1 = []
        visited1 = set()
        periphery_start = None
        h_start = tools.manhattan_dist(end, start)
        heapq.heappush(heap1, (h_start, start))

        while heap1 and len(nodes_explored1) < target_explore_count:
            _, current_tile = heapq.heappop(heap1)

            if current_tile in visited1:
                continue

            # Only process walkable tiles
            if not self.is_walkeable(current_tile[0], current_tile[1]):
                continue

            visited1.add(current_tile)
            nodes_explored1.append(current_tile)
            periphery_start = current_tile

            for neighbor in self.get_neighbors(current_tile[0], current_tile[1]):
                if neighbor not in visited1 and self.is_walkeable(neighbor[0], neighbor[1]):
                    temp_g = g_scores1[current_tile] + self.reward_map[neighbor]
                    if neighbor not in g_scores1 or temp_g < g_scores1[neighbor]:
                        origins1[neighbor] = current_tile
                        g_scores1[neighbor] = temp_g
                        f = temp_g + tools.manhattan_dist(end, neighbor)
                        heapq.heappush(heap1, (f, neighbor))

        print(f"Step 1: Explored {len(nodes_explored1)} nodes, periphery_start = {periphery_start}")
        self.displayExplored(nodes_explored1, color1=(255, 0, 0))
        self.waitForKey()

        # Step 2: A* from end until target node count
        print("Step 2: Starting A* from end")
        heap2 = []
        g_scores2 = {end: 0}
        origins2 = {}
        nodes_explored2 = []
        visited2 = set()
        periphery_end = None
        h_end = tools.manhattan_dist(start, end)
        heapq.heappush(heap2, (h_end, end))

        while heap2 and len(nodes_explored2) < target_explore_count:
            _, current_tile = heapq.heappop(heap2)

            if current_tile in visited2:
                continue

            # Only process walkable tiles
            if not self.is_walkeable(current_tile[0], current_tile[1]):
                continue

            visited2.add(current_tile)
            nodes_explored2.append(current_tile)
            periphery_end = current_tile

            for neighbor in self.get_neighbors(current_tile[0], current_tile[1]):
                if neighbor not in visited2 and self.is_walkeable(neighbor[0], neighbor[1]):
                    temp_g = g_scores2[current_tile] + self.reward_map[neighbor]
                    if neighbor not in g_scores2 or temp_g < g_scores2[neighbor]:
                        origins2[neighbor] = current_tile
                        g_scores2[neighbor] = temp_g
                        f = temp_g + tools.manhattan_dist(start, neighbor)
                        heapq.heappush(heap2, (f, neighbor))

        print(f"Step 2: Explored {len(nodes_explored2)} nodes, periphery_end = {periphery_end}")
        self.displayExplored(nodes_explored1, nodes_explored2, color1=(255, 0, 0), color2=(128, 0, 128), color3=(165, 42, 42))
        self.waitForKey()

        # Step 3: A* from periphery_start to find closest node from explored2 region
        print(f"Step 3: Starting A* from {periphery_start}, searching for nodes in region 2")
        explored2_set = set(nodes_explored2)
        heap3 = []
        g_scores3 = {periphery_start: 0}
        origins3 = {}
        nodes_explored3 = []
        visited3 = set()
        connection_node = None
        h3 = tools.manhattan_dist(end, periphery_start)
        heapq.heappush(heap3, (h3, periphery_start))

        while heap3 and connection_node is None:
            _, current_tile = heapq.heappop(heap3)

            if current_tile in visited3:
                continue

            # Only process walkable tiles
            if not self.is_walkeable(current_tile[0], current_tile[1]):
                continue

            visited3.add(current_tile)
            nodes_explored3.append(current_tile)

            # Check if we reached a node from region 2
            if current_tile in explored2_set:
                connection_node = current_tile
                print(f"Step 3: Found connection to region 2 at {connection_node}")
                break

            for neighbor in self.get_neighbors(current_tile[0], current_tile[1]):
                if neighbor not in visited3 and self.is_walkeable(neighbor[0], neighbor[1]):
                    temp_g = g_scores3[current_tile] + self.reward_map[neighbor]
                    if neighbor not in g_scores3 or temp_g < g_scores3[neighbor]:
                        origins3[neighbor] = current_tile
                        g_scores3[neighbor] = temp_g
                        f = temp_g + tools.manhattan_dist(end, neighbor)
                        heapq.heappush(heap3, (f, neighbor))

        if connection_node is None:
            connection_node = nodes_explored3[-1] if nodes_explored3 else periphery_start
            print(f"Step 3: Could not reach region 2, using closest node {connection_node}")

        print(f"Step 3: Explored {len(nodes_explored3)} nodes, connection at {connection_node}")
        self.displayExplored(nodes_explored1, nodes_explored2, nodes_explored3, color1=(255, 0, 0), color2=(128, 0, 128), color3=(0, 255, 255))
        self._flush()
        self._pending_flush = 0
        self.waitForKey()

        # Reconstruct paths
        print("Reconstructing paths...")
        path1 = self.returnPath(origins1, start, periphery_start)
        print(f"Path 1 length: {len(path1)}")
        path2 = self.returnPath(origins2, end, connection_node)
        print(f"Path 2 length: {len(path2)}")
        path3 = self.returnPath(origins3, periphery_start, connection_node)
        print(f"Path 3 length: {len(path3)}")

        # Reverse path2 since it goes from end to connection_node
        print("Reversing path 2...")
        path2.reverse()

        # Combine paths
        print("Combining paths...")
        full_path = path1[:-1] + path3 + path2
        print(f"Full path length: {len(full_path)}")

        print("Displaying complete path...")
        self.displayCompletePath(full_path, (0, 255, 0), (0, 255, 255), (0, 0, 255))

        self._last_nodes_explored = len(nodes_explored1) + len(nodes_explored2) + len(nodes_explored3)
        should_close = self.waitForKey(close_on_key=True)
        if should_close:
            sys.exit()

        print("Bidirectional A* completed")
        return full_path

    def solve(self, method):

        return method(self.start_node,self.end_node)

