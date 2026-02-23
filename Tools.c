#include "Tools.h"

/* Private Definitions */
uint8_t currentRow(uint16_t cellid, uint8_t nbcols);
uint8_t currentColumn(uint16_t cellid, uint8_t nbcols);

uint8_t isInBounds(uint16_t cellid, uint8_t nbrows, uint8_t nbcols)
{
    uint8_t isInBounds = 0;

    uint8_t currentrow = currentRow(cellid, nbcols);
    uint8_t currentcol = currentColumn(cellid, nbcols);

    //uint8_t invalidId = (currentrow < 0) || (currentcol < 0);
    uint8_t notInBounds = (currentrow >= nbrows) || (currentcol >= nbcols);

    //isInBounds = !(invalidId || notInBounds); // Only in bounds if NOT(0 OR 0) 
    isInBounds = !(notInBounds); 

    return isInBounds;
}
uint8_t isFree(uint16_t cellid, void *_matrix, uint8_t nbrows, uint8_t nbcols)
{
    uint8_t isFree = 0;
    uint8_t *matrix = (uint8_t *)_matrix;

    if(isInBounds(cellid, nbrows, nbcols))
    {
        isFree = !(*(matrix + cellid)); // Obstacle = 1, free = 0 = !1 
    } 
    else
    {
        isFree = 0; // 0 by default if not in bounds for safety 
    }

    return isFree;
}

// A cell's id is simply its address from the first cell
// if represented as a flat array (which every table is)
uint8_t computeId(uint8_t currentrow, uint8_t currentcol, uint8_t nbcols)
{
    uint8_t id = 0;

    id = currentrow * nbcols + currentcol; 

    return id;
}
// Getting the row back from a cell Id
uint8_t currentRow(uint16_t cellid, uint8_t nbcols)
{
    uint8_t currentRow = 0;

    currentRow = cellid / nbcols; 

    return currentRow;
}
// Getting the column back from a cell Id
uint8_t currentColumn(uint16_t cellid, uint8_t nbcols)
{
    uint8_t currentColumn = 0;

    currentColumn = cellid % nbcols; 

    return currentColumn;
}