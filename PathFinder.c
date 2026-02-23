#include "PathFinder.h"

/* Private Definitions */
uint8_t dijkstra_search(void* _matrix, uint8_t nbrows, uint8_t nbcolumns);
uint8_t astar_search(void* _matrix, uint8_t nbrows, uint8_t nbcolumns);

// Pathfinding function wrapper
uint8_t findPath(uint8_t algorithm, void* _matrix, uint8_t nbrows, uint8_t nbcolumns)
{
    uint8_t pathExists = 0;
    
    // Calling one or the other pathfinding algorithms
    // Make more solid by calling function pointer 
    // and changing what gets called at init stage
    if (algorithm) // 1 => Dijkstra
    {
        pathExists = dijkstra_search(_matrix, nbrows, nbcolumns);
    }
    else // 0 => Astar 
    {
        pathExists = astar_search(_matrix, nbrows, nbcolumns);
    }


    return pathExists;
}

// Pathfinding functions 
// Dijkstra 
uint8_t dijkstra_search(void* _matrix, uint8_t nbrows, uint8_t nbcolumns) 
{
    uint8_t pathExists = 0;
 
    uint8_t *matrix = (uint8_t *)_matrix;


    return pathExists;
}
// Astar 
uint8_t astar_search(void* _matrix, uint8_t nbrows, uint8_t nbcolumns)
{
    uint8_t pathExists = 0;

   uint8_t *matrix = (uint8_t *)_matrix;


    return pathExists;
}
