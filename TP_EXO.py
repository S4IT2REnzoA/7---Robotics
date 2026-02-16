from Maze_Solving import Maze



maze = Maze(10,8,(0,0),(9,7))
print(maze.navigation_map)


print(maze.solve(maze.a_star))


#print(maze.navigation_map)
#print(maze.reward_map)
