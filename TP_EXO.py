from Maze_Solving import Maze
import pygame
import networkx as nx



pygame.init()

window = pygame.display.set_mode((Maze.MAZE_DISPLAY_W, Maze.MAZE_DISPLAY_H))
running = True


H, W = 500, 500
maze = Maze(H, W, (0, 0), (H-1, W-1), window=window)
print(maze.navigation_map)


#print(maze.solve(maze.a_star))
print(maze.solve(maze.Dijkstra_Bi_Simple))

while(running):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip()


pygame.quit()

#print(maze.navigation_map)
#print(maze.reward_map)
