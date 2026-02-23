#ifndef PATHFINDER_H
#define PATHFINDER_H

/* Include List */
#include <stdint.h>


/* Pathfinder API functions */
uint8_t findPath(uint8_t algorithm, void* _matrix, uint8_t nbrows, uint8_t nbcolumns);

#endif 