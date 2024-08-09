import turtle as t
import time
from itertools import cycle
from collections import deque
from grids_and_mazes.Grid_Building import grid_template
# from maze_generator import Generate
from grids_and_mazes.Mazes.maze_generator import Generate

class Solve:
    def __init__(self,maze_obj):
        self.maze = maze_obj
        self.maze_data = self.maze.walls_and_passages #Bring in data to represent all the walls and passages
        self.grid = self.maze.grid #Reference to the grid object

        ## print statements for debugging
        # print(self.maze.walls_and_passages)
        # print(self.grid)
        # print(self.maze.get_accessible_neighbors(0,0))

    def solve_DFS(self):
        t.color('black')
        t.up()
        step_count = 0
        colors = cycle(['red', 'green', 'blue', 'LightSalmon2'])

        ##start at cell (0,0)
        row, col = 0, 0
        t.goto(self.grid.grid_data_centers()[row][col][0], self.grid.grid_data_centers()[row][col][1])
        t.down()

        # Set up data to hold visited cells and the cells that are needed to be visited as well as a rule for stopping the maze search
        goal = (self.grid.rows - 1, self.grid.columns - 1)
        visited = [(0, 0)]
        need_to_visit = [(0, 0)]

        while need_to_visit:
            step_count += 1
            if goal in visited:
                print(f"Exit Found! in {step_count} moves")
                break

            row, col = need_to_visit.pop()
            # print('here')
            ##Get the accessible neighbor(s) of the current cell if they have not been visited yet
            # accessible_neighbors = maze_data_structure.get_accessible_neighbors(maze_data, row, col)
            accessible_neighbors = self.maze.get_accessible_neighbors(row, col)
            accessible_neighbors =  [n for n in accessible_neighbors if n not in visited]
            # print(accessible_neighbors)

            # If there are any accessible neighbors that have not been visited, draw a line to the next neighbor and mark it as visited
            if accessible_neighbors and accessible_neighbors[-1] not in visited:
                next_row, next_col = accessible_neighbors.pop()
                visited.append((next_row, next_col))
                t.goto(self.grid.grid_data_centers()[next_row][next_col][0], self.grid.grid_data_centers()[next_row][next_col][1])

                # If there is another neighbor (or more) to visit, we have multiple paths, add it to the need_to_visit list
                if accessible_neighbors:
                    for _ in accessible_neighbors:  # In the case where there is more then two paths, make sure to add ALL neighbors
                        need_to_visit.append(_)

            else:  # if no accessible neighbors backtrack and take the last location on the need_to_visit list
                if need_to_visit:  # ...as long as there is a cell that can be visited
                    # t.up()
                    next_row, next_col = need_to_visit.pop()
                    # t.color('red')
                    t.color(next(colors))
                    visited.append((next_row, next_col))
                    t.pensize(1)
                    t.goto(self.grid.grid_data_centers()[next_row][next_col][0],
                           self.grid.grid_data_centers()[next_row][next_col][1])
                    t.pensize(4)
                    t.down()
                else:
                    break

            # Make the next row equal to the current row for the next iteration
            # row, col = next_row, next_col
            need_to_visit.append((next_row, next_col))
            # print(need_to_visit, '%%')
            t.update()

    def solve_BFS(self):
        """Uses a BFS algorithm to search through a maze. The process is:
            1) Remove a cell from the beginning of the queue
            2) Visit the neighbors if they have not been visited yet and add them to the end of the queue
            3) add the neighbors to the visited set
            4) Add the path to the neignbors from the current cell as a key:value pair
            """
        t.color('black')
        t.up()

        ##start and end positions
        row, col = 0,0
        start = (row,col)
        end = (self.grid.rows-1, self.grid.columns-1)
        t.goto(self.grid.grid_data_centers()[row][col][0], self.grid.grid_data_centers()[row][col][1]) #Place pen at the start position
        # t.down()

        # Create a queue for BFS and a set to keep track of visited nodes
        queue = deque([start])
        visited = set([start])
        path = {start: None} #Use to keep track of path and retrace steps of solution
        # print(visited)

        while queue:

            # Dequeue a cell from the queue and set it as current cell
            current_cell = queue.popleft()
            row, col = current_cell[0], current_cell[1]
            # print(row, col)

            #Draw the path
            t.goto(self.grid.grid_data_centers()[row][col][0], self.grid.grid_data_centers()[row][col][1])
            t.dot(5, 'red')

            # Explore neighbors
            accessible_neighbors = self.maze.get_accessible_neighbors(row, col)
            accessible_neighbors = [n for n in accessible_neighbors if n not in visited]
            # print(accessible_neighbors)

            # If there is another neighbor (or more) to visit, we have multiple paths, add it to the need_to_visit list
            if accessible_neighbors:
                for _ in accessible_neighbors:  # In the case where there is more then two paths, make sure to add ALL neighbors
                    queue.append(_)
                    visited.add(_)
                    path[_] = current_cell
                    # print(path)


            # If we reach the end, reconstruct the path
            if current_cell == end:
                #Place a dot to mark end location
                t.goto(self.grid.grid_data_centers()[end[0]][end[1]][0], self.grid.grid_data_centers()[end[0]][end[1]][1])
                t.dot(7, 'blue')
                shortest_path = [] #Build the shortest path from start to finish
                #Grab the neigbor cell leading from the current cell in the path dictionary (as long as the path exists)
                while current_cell:
                    shortest_path.append(current_cell)
                    current_cell = path[current_cell]
                shortest_path.reverse() #reverse the path to go from start to finish
                # print(shortest_path, '**')

                #Draw the shortest path
                t.goto(self.grid.grid_data_centers()[start[0]][start[1]][0], self.grid.grid_data_centers()[start[0]][start[1]][1])
                time.sleep(0.5)
                for move in shortest_path:
                    trace_row, trace_col = move[0], move[1]
                    # print(trace_row, trace_col)
                    t.down()
                    t.goto(self.grid.grid_data_centers()[trace_row][trace_col][0], self.grid.grid_data_centers()[trace_row][trace_col][1])
                    # time.sleep(0.5)
                    t.update()
                return None

            # time.sleep(0.1)
            t.update()
        # return None

if __name__ == '__main__':
    grid = grid_template.grid(10, 10, cell_dim=15, border=40, bg_color='cyan', hide_grid=False) #Create grid objrct
    grid.build_grid()

    maze_generator =  Generate(grid) # Create object for maze generation
    # maze_generator.generate_maze_DFS(0,0) #Use DFS to generate a maze passing in the starting location
    maze_generator.generate_maze_kruskals() #Use Kruskals to generate a maze
    # print(maze_generator.walls_and_passages)

    solve = Solve(maze_generator) #Create object for maze solving (pass in the maze generator as parameters, the grid object is already part of the maze_generator object)
    solve.solve_DFS() #Solve using DFS
    solve.solve_BFS() #Solve Using BFS

    t.done()