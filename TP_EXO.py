from Maze_Solving import Maze
import pygame 



pygame.init()

window = pygame.display.set_mode((Maze.MAZE_DISPLAY_W, Maze.MAZE_DISPLAY_H))
running = True

maze = Maze(50,50,(0,0),(49,49),window=window)
print(maze.navigation_map)


print(maze.solve(maze.a_star))
print(maze.solve(maze.Dijkstra))

while(running):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip()


pygame.quit()

#print(maze.navigation_map)
#print(maze.reward_map)
