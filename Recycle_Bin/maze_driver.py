import turtle as t
from Grid_Building import grid_template
from Recycle_Bin import maze_data_structure

grid = grid_template.grid(4, 4, cell_dim=30, border=40, bg_color='cyan', hide_grid=False)  # create a grid object
grid.build_grid()

maze_data = maze_data_structure.create_maze_data(grid.rows, grid.columns)
# print(maze_data)
# maze_create_solve.generate_maze(0,0)

t.done()