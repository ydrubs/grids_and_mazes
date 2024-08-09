""""
Generate an nxm grid using Turtle Graphics.The following data can be retrieved for any generated grid via the method calls:
 - grid_data_centers - returns the center point of each cell in the grid relative to Turtles screen coordiantes
 - get_cell_boundaries_all - a list containing the following information for each cell:
        1. The boundaries of each cell in terms of Turtles coordinates: cell_left,cell_right, cell_upper, cell_lower
        2 . The (row, column) index of each cell starting with (1,1)
        3. A single integer reference for each cell starting with 1 and counting across the row.
  - get_cell_boundaries_single - Accepts a one-referenced (1,1) row and column parameter and returns the boundaries of the cell as described in 1. above
  - get_neighbors - Accepts a zero-referenced (0,0) row and column parameter and returns a list of the (row, column) coordinates of all the neighbors (up, down, left right)
    ...also returns the direction of each neighbor relative to the row,column in the parameter
"""

import turtle as t
from copy import deepcopy
class grid:
    def __init__(self, columns = 10, rows = 10, cell_dim = 20, border = 40, bg_color = 'lightgreen', hide_grid = False, line_color = 'black', line_thickness_vert = 1, line_thickness_hor=1):
        #Set screen variables
        self.columns = columns
        self.rows = rows
        self.cell_dim = cell_dim
        self.border = border
        self.bg_color = bg_color
        self.hide_grid = hide_grid
        self.line_color = line_color

        self.screen_width = self.columns*self.cell_dim+2*self.border
        self.screen_height = self.rows*self.cell_dim+2*self.border
        self.max_X = self.screen_width//2
        self.min_X = -(self.screen_width//2)
        self.max_Y = self.screen_height//2
        self.min_Y = -(self.screen_height//2)
        self.screen_setup(self.bg_color)

        self.line_thickness_vert = line_thickness_vert #Use this to (optionally) change the vertical and horizontal line thickness' independently
        self.line_thickness_hor = line_thickness_hor

        self.grid_array_data = [[0 for i in range(self.columns)] for j in range(self.rows)] #Array to hold info from ind. cells

    #
# #Set up screen
    def screen_setup(self, bg_color = 'lightgreen'):
        t.Screen()
        t.setup(self.screen_width,self.screen_height)
        t.hideturtle()
        t.tracer(False)
        t.bgcolor(bg_color)
    #
    #Draw vertical lines  based on variables
    def vertical_lines(self):
        """Generate the vertical lines of the grid"""
        t.color(self.line_color)
        if self.hide_grid == True:
            t.color(self.bg_color)
        t.pensize(self.line_thickness_vert)
        t.up()
        v_line_count = 0 #Prevents Python from making extra vertical lines for some dimensions
        for i in range (self.min_X+self.border, self.max_X-self.cell_dim, self.cell_dim):
            t.goto(i, self.min_Y+self.border)
            t.down()
            t.goto(i, self.max_Y-self.border)
            t.up()
            v_line_count +=1
            if v_line_count == self.columns + 1:
                break

    #Draw horizonal lines
    def horizontal_lines(self):
        """Generate the vertical lines of the grid"""
        if self.hide_grid == True:
            t.color(self.bg_color)
        t.pensize(self.line_thickness_hor)
        t.up()
        for i in range(self.min_Y+self.border, self.max_Y-self.border+1, self.cell_dim):
            t.goto(self.min_X+self.border, i)
            t.down()
            t.goto(self.max_X-self.border, i)
            t.up()

    def build_grid(self):
        self.vertical_lines()
        self.horizontal_lines()

    def grid_data_centers(self):
        """Return the center point of each cell"""
        cell_number = 1
        grid_array_center = deepcopy(self.grid_array_data)
        for valueY, i in enumerate(self.grid_array_data):
            for valueX, j in enumerate(i):
                x = self.min_X + self.border + (self.cell_dim*(valueX)) + self.cell_dim*0.5
                y = self.max_Y - self.border - (self.cell_dim*(valueY)) - self.cell_dim*0.5
                # print(i,j)
                j = (int(x),int(y), cell_number)
                grid_array_center[valueY][valueX] = j
                cell_number+=1

        return grid_array_center

    def get_cell_boundaries_all(self):
        """Returns the edges of each cell in an x1,x2,y1,y2 form along with the (row,column) and id number of the cell."""
        grid_data = self.grid_data_centers()
        cell_number = 0

        for valueX, i in enumerate(grid_data):
            for valueY, j in enumerate(i):
                boundary = self.get_cell_boundaries_single(valueX+1, valueY+1)
                # print(boundary)
                cell_number+=1
                grid_data[valueX][valueY] = (boundary, (valueX+1,valueY+1), cell_number)

        return grid_data

    def get_cell_boundaries_single(self, column, row):
        """Returns the boundaries of a cell with the specified row and column"""
        #If our grid is not square, we need to adjust in order to check the 'extra dimensions' of the grid
        not_square_grid = abs(self.rows-self.columns)
        if row <= self.rows+not_square_grid and column <= self.columns+not_square_grid and row > 0 and column > 0:
            #First calculate the center of the cell
            x = self.min_X + self.border + (self.cell_dim*(row-1)) + self.cell_dim*0.5
            y = self.max_Y - self.border - (self.cell_dim*(column-1)) - self.cell_dim*0.5
            # print(i,j)
            j = (x,y)

            #Then get the boundaries
            cell_left = j[0] - self.cell_dim*0.5
            cell_right = j[0] + self.cell_dim*0.5
            cell_upper = j[1] + self.cell_dim*0.5
            cell_lower = j[1] - self.cell_dim*0.5

            cell_boundaries = [cell_left,cell_right, cell_upper, cell_lower]

            return cell_boundaries

        else:
            return None

    def get_neighbors(self, row, column):
        """Get the row, column coordinates of all the neighbors of a given cell"""
        current_cell = row,column
        #Neighbor cells row,column
        leftX, leftY = current_cell[0], current_cell[1]-1
        rightX, rightY = current_cell[0], current_cell[1]+1
        upX, upY = current_cell[0]-1, current_cell[1]
        downX, downY = current_cell[0]+1, current_cell[1]

        #Create list of possible neighbor coordinates (including cells in the edge of map that need to be sifted out)
        possible_neighbors = [(leftX,leftY, 'left'), (rightX,rightY, 'right'), (upX,upY, 'up'), (downX,downY, 'down')]

        neighbor_coordiantes = []
        ##If a cell is on the edge of a map and does not have a neighbor in respective direction delete it from list of possible coordinates
        for neighbor in possible_neighbors:
            # print(neighbor, '**')
            if (neighbor[0] > -1 and neighbor[0] <=self.rows-1) and (neighbor[1] > -1 and neighbor[1] <=self.columns-1):
                neighbor_coordiantes.append(neighbor)

        return neighbor_coordiantes

    def get_connections_all(self):
        """Returns all possible pairs of cells that are neighbors (as tuple pairs)"""
        cells = []
        for x in range(self.columns):
            for y in range(self.rows):
                if x < self.columns - 1:
                    cells.append(((x, y), (x + 1, y)))
                if y < self.rows - 1:
                    cells.append(((x, y), (x, y + 1)))
        return cells

#
if __name__ == '__main__':
    grid = grid(3,3,30, line_color='red')
    grid.build_grid()
    print(grid.get_neighbors(0,0))
    print(grid.get_cell_boundaries_single(1,1))
    print(grid.get_cell_boundaries_single(1,1))
    print(grid.get_connections_all())
#     #Run functions
#     screen_setup()
#     vertical_lines()
#     horizontal_lines()
#     print(place_dot(3,4,'purple'))
#     print(place_dot(7,8,'red'))
#
    t.done()

