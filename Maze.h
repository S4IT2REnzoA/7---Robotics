#ifndef MAZE_H
#define MAZE_H

/* Include List */
#include <stddef.h>
#include <stdint.h>
// Needed for the seeded random number generation
#include <stdlib.h>
#include <time.h>

/* Pathfinder API functions */
uint8_t *generateMaze(uint8_t rows, uint8_t columns);

#endif