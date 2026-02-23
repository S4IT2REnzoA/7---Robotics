#include "Maze.h"


// We are looking to generate a maze, which is ultimately just 
// a matrix. This matrix will then be explored by the pathfinder
// API function, based on one or the other algorithm we implement 
uint8_t *generateMaze(uint8_t rows, uint8_t columns)
{   
    // Allocating the maze grid
    uint8_t (*maze)[columns] = malloc(rows * sizeof(*maze));
    // sizeof(*maze) is columns * sizeof(uint8_t)

    // For each cell, generating a random number 
    // 0 for free cell/ 1 for obstacle
    srand(time(NULL));  // seed random with current time
    // The aim of the seeding is to create a different number
    // at every run, time changing at each run makes it a good
    // simple seed

    for (uint8_t row = 0; row < rows; row++)
    {
        for (uint8_t column = 0; column < columns; column++)
        {
            maze[row][column] = (uint8_t)(rand() % 2); // random from 0 to 2 excl 
        }
    }

    return (uint8_t *)maze;
}
