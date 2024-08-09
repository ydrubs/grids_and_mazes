import turtle as t
from Grid_Building import grid_template
from Mazes.maze_generator import Generate

"""Creates a grid object:
    parameters (required):
        - Number of columns, number of rows
    parameters (optional)
        - cell_dim - default is 
    """
grid = grid_template.grid(40, 40, cell_dim=10, border=30, bg_color='cyan', hide_grid=False)  # create a grid object

#Specifiy thickness of vert and hor lines in the grid (needs to be the same for the maze function to look consistant.
grid.line_thickness_hor = 1
grid.line_thickness_vert = 1
grid.build_grid()

print(grid.grid_array_data) #Creates a 2D array of zeros representing all the possible cells in the array

#Get grid data
cell_centers_points = grid.grid_data_centers()
cell_boundaries = grid.get_cell_boundaries_all()
cell_boundaries_cell = grid.get_cell_boundaries_single(1,1)
neighbors = grid.get_neighbors(0,0)

print(cell_boundaries_cell)
print(cell_boundaries)
print(neighbors)

#Generate a maze
walls_and_passage_data = maze_data_structure.create_maze_data(grid.rows, grid.columns)
print(walls_and_passage_data)
# maze_reimplamented_.generate_maze(0,0, grid, walls_and_passage_data)

#Solve Maze
# maze_reimplamented_.solve_DFS(walls_and_passage_data)
# maze_reimplamented_.solve_BFS(walls_and_passage_data)

t.done()
