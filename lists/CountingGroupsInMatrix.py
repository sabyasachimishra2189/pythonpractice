'''
def main():
    visited [] # array to keep track of visited cell
    num_islands = 0 # start with zero
    for each row, col in matrix
          num_island += get_number_of_islands(matrix, row, col) #return 1 if it is an island
return num_island
def get_number_of_islands(matrix, row, col, visited):
    check if row and col is out of bound of the matrix
    check if we already visited the cell with row, col
    check if the cell is 0
    => return 0

    mark the cell as visited in the visited array
    recursive call get_number_of_islands() on each adjacent cell
    return 1
    
    ref geekforgeeks

'''

def get_number_of_islands(binaryMatrix):
    rows = len(binaryMatrix)
    cols = len(binaryMatrix[0])
    # you can use Set if you like
    # or change the content of binaryMatrix as it is visited
    visited = [[0 for col in range(cols)] for r in range(rows)]
    number_of_island = 0
    for row in range(rows):
        for col in range(cols):
            number_of_island += get_island(binaryMatrix, row, col, visited)
    return number_of_island


# get a continuous island
def get_island(binaryMatrix, row, col, visited):
    if not is_valid(binaryMatrix, row, col) or visited[row][col] == 1 or binaryMatrix[row][col] == 0:
        return 0

    # mark as visited
    visited[row][col] = 1
    get_island(binaryMatrix, row, col + 1, visited)
    get_island(binaryMatrix, row, col - 1, visited)
    get_island(binaryMatrix, row + 1, col, visited)
    get_island(binaryMatrix, row - 1, col, visited)
    return 1


def is_valid(binaryMatrix, row, col):
    rows = len(binaryMatrix)
    cols = len(binaryMatrix[0])
    return row >= 0 and row < rows and col >= 0 and col < cols


binaryMatrix = [ [0,    1,    0,    1,    0],
                         [0,    0,    1,    1,    1],
                         [1,    0,    0,    1,    0],
                         [0,    1,    1,    0,    0],
                         [1,    0,    1,    0,    1] ]


print(get_number_of_islands(binaryMatrix))
