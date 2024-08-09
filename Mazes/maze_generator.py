from math import ceil
import turtle as t
import random
from grids_and_mazes.Grid_Building import grid_template
from grids_and_mazes.Algorithms import Union_Find_Kruskals

class Generate:
    def __init__(self, grid_obj):
        self.grid = grid_obj
        self.walls_and_passages = self.create_maze_data(self.grid.rows, self.grid.columns)

    def create_maze_data(self, rows, columns):
        """Take in number of rows and columns and return the data structure representing walls and openings"""
        array = [[1 for i in range((columns * 2) + 1)] for j in range((rows * 2) + 1)]  # Initially everything is a wall
        for i in range(1, len(array), 2):  # ..Then create openings to represent cell locations
            # print(walls_and_passages[i])
            for j in range(1, len(array[i]), 2):
                array[i][j] = 0
        return array

    def remove_wall(self, dir, row, col):
        t.pensize(4)
        t.color(self.grid.bg_color)
        row, col = row + 1, col + 1
        # t.tracer(1)

        ##Bottom wall of a cell remove
        if dir == 'down':
            t.up()
            t.color(self.grid.bg_color)
            remove_wall = self.grid.get_cell_boundaries_single(row, col)
            t.goto(remove_wall[0] + self.grid.line_thickness_hor + 1, remove_wall[3])
            t.down()
            t.goto(remove_wall[1] - self.grid.line_thickness_hor - 1, remove_wall[3])
            ##Update the array holding the passage data
            self.make_passage(dir, row - 1, col - 1)
            t.update()

        # Top wall remove
        if dir == 'up':
            t.up()
            t.color(self.grid.bg_color)
            remove_wall = self.grid.get_cell_boundaries_single(row, col)
            t.goto(remove_wall[0] + self.grid.line_thickness_hor + 1, remove_wall[2])
            t.down()
            t.goto(remove_wall[1] - self.grid.line_thickness_hor - 1, remove_wall[2])
            self.make_passage(dir, row - 1, col - 1)
            t.update()

        # Left Wall Remove
        if dir == 'left':
            t.up()
            t.color(self.grid.bg_color)
            remove_wall = self.grid.get_cell_boundaries_single(row, col)
            t.goto(remove_wall[0], remove_wall[2] - 2)
            t.down()
            t.goto(remove_wall[0], remove_wall[3] + 2)
            self.make_passage(dir, row - 1, col - 1)
            t.update()

        if dir == 'right':
            # Right wall Remove
            t.up()
            t.color(self.grid.bg_color)
            remove_wall = self.grid.get_cell_boundaries_single(row, col)
            t.goto(remove_wall[1], remove_wall[2] - self.grid.line_thickness_hor - 1)
            t.down()
            t.goto(remove_wall[1], remove_wall[3] + self.grid.line_thickness_hor + 1)
            self.make_passage(dir, row - 1, col - 1)
            t.update()

    def make_passage(self, direction, row, col):
        """Create passageways between two cells by removing walls in the data structure (replace 1 with 0)"""
        # Start at current cell
        # change a 1 to a zero depending on where the wall is relative to current cell
        ##Example with cell at row 2, column 2 or  (1,1) in array structure
        ##Define location relative to row and column

        row = 2 * row + 1
        col = 2 * col + 1
        # current_cell = '#'
        # walls_and_passages[row][col] = current_cell
        dir = ((row - 1), (row + 1), (col + 1), (col - 1))  # top, bottom, right, left
        current_cell = self.walls_and_passages[row][col]

        if direction == 'up':
            # Remove top wall
            self.walls_and_passages[dir[0]][col] = 0
        if direction == 'left':
            # remove left wall
            self.walls_and_passages[row][dir[3]] = 0
        if direction == 'down':
            # Remove bottom wall
            self.walls_and_passages[dir[1]][col] = 0
        # Remove right wall
        if direction == 'right':
            self.walls_and_passages[row][dir[2]] = 0

    def generate_maze_DFS(self, row, col):
        """Use a randomized DFS Algorithm to generate a maze """
        ###Start at 0,0
        ###Get all the possible neighbors
        ###Choose a random neighbor
        ###Remove the wall between them if there is one
        ###Go on to the next neigbor and do the same

        walls_removed = {}  # Keep track of what wall was removed relative to the current cell (not used but might be useful for new features later)

        # Create a start and end position opening
        self.remove_wall('up', row, col)
        self.make_passage('up', row, col)
        self.remove_wall('left', self.grid.rows - 1, self.grid.columns - 1)
        self.make_passage('left', self.grid.rows - 1, self.grid.columns - 1)
        self.remove_wall('down', self.grid.rows - 1, self.grid.columns - 1)
        self.make_passage('down', self.grid.rows - 1, self.grid.columns - 1)

        # set the start position
        self.grid.grid_array_data[row][col] = 1

        # Set the end position
        end_row, end_col = self.grid.rows - 1, self.grid.columns - 1
        self.grid.grid_array_data[end_row][end_col] = 1

        # Create a stack to keep track of visited cells
        stack = [(row, col)]

        # Generate the maze using Depth-First Search algorithm
        while stack:
            # for i in range(200):
            current_row, current_col = stack[-1]
            # print(stack, current_row)

            # Find all neighbors of current cell
            neighborhood = []
            neighbors = self.grid.get_neighbors(current_row, current_col)

            # Only keep unvisitied neighbors
            for n in neighbors:
                if self.grid.grid_array_data[n[0]][n[1]] == 0:
                    neighborhood.append(n)

            if neighborhood:
                # Choose a random neighbor
                chosen_neighbor = random.choice(neighborhood)

                # Remove the wall between current cell and chosen neighbor
                self.remove_wall(chosen_neighbor[2], current_row, current_col)
                walls_removed[current_row, current_col] = chosen_neighbor[2]

                # Mark the chosen neighbor as visited
                self.grid.grid_array_data[chosen_neighbor[0]][chosen_neighbor[1]] = 1

                # Add the chosen neighbor to the stack
                stack.append((chosen_neighbor[0], chosen_neighbor[1]))

            else:
                # Backtrack if there are no unvisited neighbors
                stack.pop()

    def generate_maze_kruskals(self):
        """Use Kruskals Algorithm to generate a maze"""
        # Total cells in the maze
        n = self.grid.rows * self.grid.columns

        # Disjoint set for union-find
        ds = Union_Find_Kruskals.DisjointSet(n)
        # print(maze_data)

        cell_data = self.grid.get_connections_all()
        random.shuffle(cell_data)
        # print(cell_data)

        ##TO DO: Break out into its own function for the start and end set
        # Create a start and end position opening
        self.remove_wall('up', 0, 0)
        self.make_passage('up', 0, 0)
        self.remove_wall('left', self.grid.rows - 1, self.grid.columns - 1)
        self.make_passage('left', self.grid.rows - 1, self.grid.columns - 1)
        self.remove_wall('down', self.grid.rows - 1, self.grid.columns - 1)
        self.make_passage('down', self.grid.rows - 1, self.grid.columns - 1)

        # Kruskal's algorithm
        for (cell1, cell2) in cell_data:
            x1, y1 = cell1
            x2, y2 = cell2
            idx1 = y1 * self.grid.columns + x1
            idx2 = y2 * self.grid.columns + x2
            # print(idx1,idx2, end='\n')

            if ds.find(idx1) != ds.find(idx2):  # Result of this check is whether the walls are part of the same set
                # print('--', ds.parent[idx1], ds.parent[idx2])
                ds.union(idx1, idx2)  # if not make them part of the same set
                # print('**', idx1,idx2)
                # print('parent: ', ds.parent)
                # print('rank: ', ds.rank)
                if x1 == x2:  # vertical wall
                    self.walls_and_passages[max(2 * y1, 2 * y2)][2 * x1 + 1] = 0
                else:  # horizontal wall
                    self.walls_and_passages[2 * y1 + 1][max(2 * x1, 2 * x2)] = 0

        # print(sorted(cell_data))
        # print(maze_data[1][2], maze_data[1][4])

        for x, i in enumerate(self.walls_and_passages):
            if x % 2 == 1:
                # print(i)
                for y, j in enumerate(i):
                    if y % 2 == 0:
                        # print(j)
                        if j == 0:
                            self.remove_wall('right', (x - 1) // 2, (y - 1) // 2)
                if x >= 3:
                    # print(i, '***')
                    for z, k in enumerate(i):
                        if z % 2 == 1:
                            if self.walls_and_passages[x - 1][z] == 0:
                                # print('here', x-1, z)
                                # remove_wall('up', x-1, z)
                                self.remove_wall('up', ((x - 1) // 2), (z - 1) // 2)

        return self.walls_and_passages

    def get_accessible_neighbors(self, row, col):
        row = 2 * row + 1
        col = 2 * col + 1
        dir = ((row - 1), (row + 1), (col + 1), (col - 1))  # top, bottom, right, left
        accessible_neighbors = []
        # print(maze)

        if self.walls_and_passages[dir[0]][col] == 0:  # Top is accessible
            accessible_neighbors.append((ceil((dir[0] - 2) / 2), ceil((col - 1) / 2)))

        if self.walls_and_passages[row][dir[3]] == 0:  # Left is accessible
            accessible_neighbors.append((ceil((row - 1) / 2), ceil((dir[3] - 2) / 2)))

        if self.walls_and_passages[dir[1]][col] == 0:  # Bottom is accessible
            accessible_neighbors.append((ceil((dir[1] - 1) / 2), ceil((col - 1) / 2)))

        if self.walls_and_passages[row][dir[2]] == 0:  # Right is accssible
            accessible_neighbors.append((ceil((row - 1) / 2), ceil((dir[2] - 1) / 2)))

        accessible_neighbors = [n for n in accessible_neighbors if n[0] > -1 and n[1] > -1]

        return accessible_neighbors

    def get_maze_data(self):
        return self.walls_and_passages

if __name__ == '__main__':
    grid = grid_template.grid(50,50, cell_dim=12, border=40, bg_color='cyan', hide_grid=False)  # create a grid object
    grid.build_grid()

    maze_generator = Generate(grid)  # Create object for maze generation

    # print(maze_generator.grid.rows)
    # print(maze_generator.get_maze_data())
    # maze_generator.remove_wall('left', 1, 1)

    # maze_generator.generate_maze_DFS(0, 0)
    maze_generator.generate_maze_kruskals()
    # print(maze_generator.get_maze_data())

    print(maze_generator.get_accessible_neighbors(0,0))

    t.done()
