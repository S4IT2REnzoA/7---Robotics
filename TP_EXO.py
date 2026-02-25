from Maze_Solving import Maze
import pygame 



pygame.init()

window = pygame.display.set_mode((Maze.MAZE_DISPLAY_W, Maze.MAZE_DISPLAY_H))
running = True

maze = Maze(50,50,(0,0),(49,49),window=window,diagonal=False)
print(maze.navigation_map)

path_astar = maze.solve(maze.a_star)
path_dijkstra = maze.solve(maze.Dijkstra)

print(len(path_astar))
print(len(path_dijkstra))


while(running):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip()


pygame.quit()

#print(maze.navigation_map)
#print(maze.reward_map)
