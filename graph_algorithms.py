"""
Standalone graph algorithm implementations that work directly on NetworkX graphs.
No Maze class dependency — algorithms and visualization are self-contained.
"""

import heapq
import numpy as np
import pygame


def dijkstra_bi_simple_nx(G, start, end, viz=None):
    """
    Bidirectional Dijkstra on NetworkX graph — mirrors Dijkstra_Bi_Simple logic.

    Args:
        G: NetworkX graph
        start: start node ID
        end: end node ID
        viz: optional GraphVisualizer for display (if None, no visualization)

    Returns:
        (path, nodes_explored_total) where:
        - path is list of nodes from start to end
        - nodes_explored_total is count of unique nodes expanded
    """

    # Calculate exploration target (explore ~25% of graph from each end)
    total_nodes = len(G.nodes())
    target_explore_count = max(100, total_nodes // 4)

    if viz:
        viz.displayBlankGraph()

    # ===== Step 1: Dijkstra from start =====
    heap1 = []
    g_scores1 = {start: 0}
    origins1 = {}
    nodes_explored1 = []
    visited1 = set()
    periphery_start = None
    heapq.heappush(heap1, (0, start))

    while heap1 and len(nodes_explored1) < target_explore_count:
        current_cost, current_node = heapq.heappop(heap1)

        if current_node in visited1:
            continue

        visited1.add(current_node)
        nodes_explored1.append(current_node)
        periphery_start = current_node

        for neighbor in G.neighbors(current_node):
            if neighbor not in visited1:
                # Get edge weight (default to 1 if not specified)
                edge_weight = G[current_node][neighbor].get('weight', 1)
                temp_g = g_scores1[current_node] + edge_weight

                if neighbor not in g_scores1 or temp_g < g_scores1[neighbor]:
                    origins1[neighbor] = current_node
                    g_scores1[neighbor] = temp_g
                    heapq.heappush(heap1, (temp_g, neighbor))

    if viz:
        viz.displayExplored(nodes_explored1, color1=(255, 0, 0))
        viz.waitForKey()

    # ===== Step 2: Dijkstra from end =====
    heap2 = []
    g_scores2 = {end: 0}
    origins2 = {}
    nodes_explored2 = []
    visited2 = set()
    periphery_end = None
    heapq.heappush(heap2, (0, end))

    while heap2 and len(nodes_explored2) < target_explore_count:
        current_cost, current_node = heapq.heappop(heap2)

        if current_node in visited2:
            continue

        visited2.add(current_node)
        nodes_explored2.append(current_node)
        periphery_end = current_node

        for neighbor in G.neighbors(current_node):
            if neighbor not in visited2:
                edge_weight = G[current_node][neighbor].get('weight', 1)
                temp_g = g_scores2[current_node] + edge_weight

                if neighbor not in g_scores2 or temp_g < g_scores2[neighbor]:
                    origins2[neighbor] = current_node
                    g_scores2[neighbor] = temp_g
                    heapq.heappush(heap2, (temp_g, neighbor))

    if viz:
        viz.displayExplored(nodes_explored1, nodes_explored2, color1=(255, 0, 0), color2=(128, 0, 128))
        viz.waitForKey()

    # ===== Step 3: Dijkstra from periphery_start to find connection =====
    explored2_set = set(nodes_explored2)
    heap3 = []
    g_scores3 = {periphery_start: 0}
    origins3 = {}
    nodes_explored3 = []
    visited3 = set()
    connection_node = None
    heapq.heappush(heap3, (0, periphery_start))

    while heap3 and connection_node is None:
        current_cost, current_node = heapq.heappop(heap3)

        if current_node in visited3:
            continue

        visited3.add(current_node)
        nodes_explored3.append(current_node)

        # Check if we reached a node from region 2
        if current_node in explored2_set:
            connection_node = current_node
            break

        for neighbor in G.neighbors(current_node):
            if neighbor not in visited3:
                edge_weight = G[current_node][neighbor].get('weight', 1)
                temp_g = g_scores3[current_node] + edge_weight

                if neighbor not in g_scores3 or temp_g < g_scores3[neighbor]:
                    origins3[neighbor] = current_node
                    g_scores3[neighbor] = temp_g
                    heapq.heappush(heap3, (temp_g, neighbor))

    # Fallback if no connection found
    if connection_node is None:
        connection_node = nodes_explored3[-1] if nodes_explored3 else periphery_start

    if viz:
        viz.displayExplored(nodes_explored1, nodes_explored2, nodes_explored3,
                           color1=(255, 0, 0), color2=(128, 0, 128), color3=(0, 255, 255))
        viz.waitForKey()

    # ===== Path reconstruction =====
    def reconstruct_path(origins, start, end):
        """Reconstruct path from origins dict."""
        if end == start:
            return [start]
        if end not in origins:
            return [start, end]  # Fallback

        path = [end]
        previous = origins[end]
        path.append(previous)
        while previous != start:
            if previous not in origins:
                break
            previous = origins[previous]
            path.append(previous)
        path.reverse()
        return path

    path1 = reconstruct_path(origins1, start, periphery_start)
    path2 = reconstruct_path(origins2, end, connection_node)
    path3 = reconstruct_path(origins3, periphery_start, connection_node)

    # Reverse path2 since it goes from end to connection_node
    path2.reverse()

    # Combine paths
    full_path = path1[:-1] + path3 + path2

    if viz:
        viz.displayPath(full_path)
        viz.waitForKey(close_on_key=True)

    # Count total nodes explored
    total_nodes_explored = len(nodes_explored1) + len(nodes_explored2) + len(nodes_explored3)

    return full_path, total_nodes_explored


class GraphVisualizer:
    """
    Visualizer for NetworkX graphs with pygame.
    Mirrors Maze display methods but for arbitrary graph topologies.
    """

    DISPLAY_H = 800
    DISPLAY_W = 800
    COLOR_WALL = (50, 50, 50)  # Dark grey for background
    COLOR_WALKABLE = (200, 200, 200)  # Light grey
    COLOR_EDGE = (100, 100, 100)  # Grey edges
    COLOR_NODE = (200, 200, 200)  # Light grey nodes
    COLOR_EXPLORED_1 = (255, 0, 0)  # Red
    COLOR_EXPLORED_2 = (128, 0, 128)  # Purple
    COLOR_EXPLORED_3 = (0, 255, 255)  # Cyan
    COLOR_PATH = (0, 255, 0)  # Green
    NODE_RADIUS = 3

    def __init__(self, G, positions, window):
        """
        Args:
            G: NetworkX graph
            positions: dict {node: (x, y)} with coordinates in [0, 1]
            window: pygame display surface (or 0 for no display)
        """
        self.G = G
        self.positions = positions
        self.window = window
        self.node_to_pixel = {}

        # Normalize positions from [0, 1] to pixel coordinates
        for node, (x, y) in positions.items():
            px = int(x * self.DISPLAY_W)
            py = int(y * self.DISPLAY_H)
            self.node_to_pixel[node] = (px, py)

        # Create pixel array
        self.pixel_array = np.zeros((self.DISPLAY_H, self.DISPLAY_W, 3), dtype=np.uint8)
        if self.window:
            self._cell_surface = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))
            self._pending_flush = 0

        self.last_explored = set()

    def _flush(self):
        """Blit pixel_array to pygame window."""
        if not self.window:
            return
        pygame.surfarray.blit_array(
            self._cell_surface,
            self.pixel_array.transpose(1, 0, 2)
        )
        self.window.blit(self._cell_surface, (0, 0))
        pygame.display.flip()

    def displayBlankGraph(self):
        """Clear display and draw edges and nodes."""
        if not self.window:
            return

        # Clear to dark background
        self.pixel_array[:] = self.COLOR_WALL

        # Draw edges as thin lines first
        for u, v in self.G.edges():
            if u in self.node_to_pixel and v in self.node_to_pixel:
                x1, y1 = self.node_to_pixel[u]
                x2, y2 = self.node_to_pixel[v]
                self._draw_line(x1, y1, x2, y2, self.COLOR_EDGE)

        # Draw nodes on top of edges (so they're visible)
        for node, (px, py) in self.node_to_pixel.items():
            self._draw_circle(px, py, self.NODE_RADIUS, self.COLOR_NODE)

        self._flush()
        self.last_explored = set()

    def displayExplored(self, explored1, explored2=None, explored3=None,
                       color1=None, color2=None, color3=None):
        """Display explored nodes with up to 3 colors."""
        if not self.window:
            return

        color1 = color1 or self.COLOR_EXPLORED_1
        color2 = color2 or self.COLOR_EXPLORED_2
        color3 = color3 or self.COLOR_EXPLORED_3

        explored1_set = set(explored1)
        explored2_set = set(explored2) if explored2 else set()
        explored3_set = set(explored3) if explored3 else set()

        overlap = explored1_set & explored2_set
        only_1 = explored1_set - overlap
        only_2 = explored2_set - overlap
        only_3 = explored3_set - explored1_set - explored2_set

        # Draw regions in order
        for group, color in [(only_1, color1), (only_2, color2),
                             (overlap, color3), (only_3, (0, 255, 255))]:
            for node in group:
                if node in self.node_to_pixel:
                    px, py = self.node_to_pixel[node]
                    self._draw_circle(px, py, self.NODE_RADIUS + 1, color)

        self._flush()
        self._pending_flush = 0

    def displayPath(self, path):
        """Highlight path nodes in green."""
        if not self.window:
            return

        for node in path:
            if node in self.node_to_pixel:
                px, py = self.node_to_pixel[node]
                self._draw_circle(px, py, self.NODE_RADIUS + 2, self.COLOR_PATH)

        self._flush()
        self._pending_flush = 0

    def waitForKey(self, close_on_key=False):
        """Wait for spacebar or window close."""
        if not self.window:
            return False

        print("waitForKey: Press SPACEBAR to continue...")
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        waiting = False
                        if close_on_key:
                            return True
                if event.type == pygame.QUIT:
                    waiting = False
                    return True
        return False

    def _draw_circle(self, cx, cy, radius, color):
        """Draw filled circle on pixel_array."""
        for dy in range(-radius, radius + 1):
            for dx in range(-radius, radius + 1):
                if dx*dx + dy*dy <= radius*radius:
                    x, y = cx + dx, cy + dy
                    if 0 <= x < self.DISPLAY_W and 0 <= y < self.DISPLAY_H:
                        self.pixel_array[y, x] = color

    def _draw_line(self, x1, y1, x2, y2, color):
        """Draw line using Bresenham algorithm."""
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy

        x, y = x1, y1
        while True:
            if 0 <= x < self.DISPLAY_W and 0 <= y < self.DISPLAY_H:
                self.pixel_array[y, x] = color
            if x == x2 and y == y2:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x += sx
            if e2 < dx:
                err += dx
                y += sy
