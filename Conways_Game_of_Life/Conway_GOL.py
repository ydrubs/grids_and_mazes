import copy
import random
import Conway_GOL_patterns

from grids_and_mazes.Grid_Building import grid_template
import turtle as t

new_grid = grid_template.grid(50,50,10, hide_grid=False, line_color='black')
# new_grid.line_thickness_vert = 5
# new_grid.line_thickness_hor = 2
new_grid.build_grid()

# print('The center of each grid is at:')
# print(new_grid.grid_data_centers())
#
# print("The boundaries of each cell are at:")
# print(new_grid.get_cell_boundaries_all())
#
# print("The boundaries of the cell with the row, column given is:")
# print(new_grid.get_cell_boundaries_single(2,2))
next_step_array = [[0 for i in range(new_grid.columns)] for j in range(new_grid.rows)]


def random_shade():
    global next_step_array
    next_step_array = [[random.randint(0,1) for i in range(new_grid.columns)] for j in range(new_grid.rows)]
    next_step_shade()

def apply_pattern(row = 5, column=5, color = 'purple'):
    # injection_array = Conway_GOL_patterns.glider()
    # injection_array = Conway_GOL_patterns.penta()
    # injection_array = Conway_GOL_patterns.diehard()
    # injection_array = Conway_GOL_patterns.heavy_sapceship()
    # injection_array = Conway_GOL_patterns.minimal()
    # injection_array = Conway_GOL_patterns.beautiful()
    injection_array = Conway_GOL_patterns.three_by_three()
    # injection_array = Conway_GOL_patterns.beautiful2()
    # injection_array = Conway_GOL_patterns.inf_loop()

    # Define the starting row and column where you want to inject the array
    start_row = (len(next_step_array)//2)-(len(injection_array)//2)
    start_col = (len(next_step_array)//2)-(len(injection_array)//2)
    # start_row = row
    # start_col = column
    # Iterate over the injection_array and write its elements into next_step_array
    for i in range(len(injection_array)):
        for j in range(len(injection_array[0])):
            next_step_array[start_row + i][start_col + j] = injection_array[i][j]

    next_step_shade(color)

def make_live(row, column):
    """Turn a dead cell to a live cell in the array of cells"""
    new_grid.grid_array_data[row][column] = 1
    # print(new_grid.grid_array_data)

def get_neighbors(row, column):
    """Gets the neighbors boundaries of a cell with given row and column."""
    ##TESTING - Suppose current cell is (2,2)
    current_cell = row,column
    #Neighbor cells row,column
    leftX, leftY = current_cell[0], current_cell[1]-1
    rightX, rightY = current_cell[0], current_cell[1]+1
    upX, upY = current_cell[0]-1, current_cell[1]
    downX, downY = current_cell[0]+1, current_cell[1]
    left_upX, left_upY = current_cell[0]-1, current_cell[1]-1
    left_downX, left_downY = current_cell[0]+1, current_cell[1]-1
    right_upX, right_upY = current_cell[0]-1, current_cell[1]+1
    right_downX, right_downY = current_cell[0]+1, current_cell[1]+1

    #Create list of possible neighbor coordinates (including cells in the edge of map that need to be sifted out)
    possible_neighbors = [(leftX,leftY), (rightX,rightY), (upX,upY), (downX,downY),
                 (left_upX, left_upY), (left_downX,left_downY),(right_upX,right_upY), (right_downX,right_downY)]

    neighbor_coordiantes = []
    ##If a cell is on the edge of a map and does not have a neighbor in respective direction delete it from list of possible coordinates
    for neighbor in possible_neighbors:
        # print(neighbor, '**')
        if (neighbor[0] > 0 and neighbor[0] <=new_grid.rows) and (neighbor[1] > 0 and neighbor[1] <=new_grid.columns):
            neighbor_coordiantes.append(neighbor)

    #Create list of boundaries for all neighbors
    neighbor_boundaries = []
    for neighbor in neighbor_coordiantes:
        new_neighbor = new_grid.get_cell_boundaries_single(neighbor[0], neighbor[1])
        neighbor_boundaries.append(new_neighbor)

    # print(neighbor_boundaries, '\n', neighbor_coordiantes)
    # print(new_grid.get_cell_boundaries_single(left_upX,left_upY))
    # print(new_grid.get_cell_boundaries_single(1,1))
    return neighbor_coordiantes

def check_cell_state(row, column):
    """Check whether a cell with given row and column is alive or dead"""
    return new_grid.grid_array_data[row][column]

def shade_cell_click(x,y):
    """Click into a cell to make it alive"""
    cell_border = 0
    for i in new_grid.get_cell_boundaries_all():
        # print(i)
        for j in i:
            # print(j)
            if (y<j[0][2] and y>=j[0][3]) and (x>j[0][0] and x<=j[0][1]):
                t.goto(j[0][0]+cell_border, j[0][2]-cell_border)
                t.begin_fill()
                t.goto(j[0][0]+cell_border, j[0][3]+cell_border)
                t.goto(j[0][1]-cell_border, j[0][3]+cell_border)
                t.goto(j[0][1]-cell_border, j[0][2]-cell_border)
                t.end_fill()
                make_live(j[1][0]-1,j[1][1]-1)

def next_step_state(color = 'purple'):
    """
    Starting point for computing and displaying iterations.
    1) Loop through each cell in the grid
    2) Get the coordinates of all the neighbor cells
    3) Count the number of live numbers for each cell
    4) Call a function the applies Conways rules for the cell to determine cell shading in the next step
    5) Call a function that shades the grid for the next iteration
    """
    #Start by redrawing the grid
    t.clear()
    new_grid.build_grid()
    #Get the state of the current cell
    for i in range(new_grid.rows):
        for j in range(new_grid.columns):
            current_cell_state = check_cell_state(i,j)
            # print(current_cell_state)

            #Get the coordinates of all possible neighbors
            neighbors = get_neighbors(i+1,j+1)
            # print('**',neighbors)

            #...then check all of their states (dead or alive)
            live_neighbors = 0
            for neighbor in neighbors:
                state = check_cell_state(neighbor[0]-1, neighbor[1]-1)
                # print(state)
                if state == 1:
                    live_neighbors +=1
            # print(live_neighbors, '**')

            next_step_rules(i, j, current_cell_state, live_neighbors)
    next_step_shade(color)


def next_step_rules(row, column, state, neighbors):
    """Take the current cell and number of live neighbors and create an array for shading the cells during the next step
    by applying Conway's rules"""
        ##1. Any live cell with fewer than two live neighbors dies, as if by underpopulation.
    # print('$$$$$', new_grid.grid_array_data)
    if state == 1:
        if neighbors < 2:
            next_step_array[row][column]= 0
        elif neighbors == 2 or neighbors == 3:
            next_step_array[row][column] = 1
        elif neighbors > 3:
            next_step_array[row][column] = 0
    if state == 0:
        if neighbors == 3:
            next_step_array[row][column] = 1
        else:
          next_step_array[row][column] = 0
    # print('!!!!', next_step_array, row, column)

def next_step_shade(color):
    #Start by making a deep copy of the states of the current iteration in order to use for next iteration
    t.color(color)
    new_grid.grid_array_data = copy.deepcopy(next_step_array)
    cell_border = 0
    for x, row in enumerate (next_step_array):
        for y, cell in enumerate (row):
            if cell == 1:
                # print(cell, '#@!')
                # print(next_step_array, x,y)
                selected_cell = new_grid.get_cell_boundaries_single(x+1, y+1)
                # print(selected_cell)
                t.goto(selected_cell[0]+cell_border, selected_cell[2]-cell_border)
                t.begin_fill()
                t.goto(selected_cell[0]+cell_border, selected_cell[3]+cell_border)
                t.goto(selected_cell[1]-cell_border, selected_cell[3]+cell_border)
                t.goto(selected_cell[1]-cell_border, selected_cell[2]-cell_border)
                t.end_fill()
    t.update()

# get_neighbors(1,1)

# apply_pattern()
t.listen()
t.onscreenclick(shade_cell_click)
t.onkeypress(next_step_state, 'space')

apply_pattern() #Apply a predefined pattern (defined in the method)

# random_shade() # Randomly initial orientation

#Define number of generations to run-through
for i in range(1000):
    next_step_state()
    # time.sleep(0.1)
t.done()

"""To do:
1) Use the reference here in order to create some initial configurations: 
https://github.com/marcpaulo15/game_of_life/blob/main/seed_patterns.yml
...Done

2) Detect oscillators """
