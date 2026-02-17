from Maze_Solving import Maze
import pygame 

maze = Maze(100,99,(0,0),(99,98),)
print(maze.navigation_map)


print(maze.solve(maze.a_star))
print(maze.solve(maze.Dijkstra))

pygame.init()

window = pygame.display.set_mode((600, 480))

running = True

while(running):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pass

pygame.quit()

#print(maze.navigation_map)
#print(maze.reward_map)
