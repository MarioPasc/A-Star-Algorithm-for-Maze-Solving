import matplotlib.pyplot as plt
import numpy as np


class Maze:
    def __init__(self, grid, start, goal):
        """
        Initializes the Maze with a given grid, start, and goal positions.
        :param grid: 2D list representing the maze layout (0 for open paths, 1 for walls)
        :param start: Tuple (x, y) for the starting position
        :param goal: Tuple (x, y) for the goal position
        """
        self.grid = grid
        self.start = start
        self.goal = goal

    def is_obstacle(self, x, y):
        """
        Checks if the cell at (x, y) is an obstacle.
        :param x: X-coordinate of the cell
        :param y: Y-coordinate of the cell
        :return: True if the cell is a wall (1), False otherwise
        """
        return self.grid[x][y] == 1

    def get_neighbors(self, x, y):
        """
        Returns the accessible neighboring cells of the given cell.
        :param x: X-coordinate of the cell
        :param y: Y-coordinate of the cell
        :return: List of tuples representing coordinates of neighboring cells
        """
        neighbors = []
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # Directions: up, down, left, right
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(self.grid) and 0 <= ny < len(self.grid[0]) and not self.is_obstacle(nx, ny):
                neighbors.append((nx, ny))
        return neighbors

    def display(self, ax=None):
        """
        Visualizes the maze using Matplotlib, adapted for FuncAnimation.
        :param ax: Matplotlib axes object to draw the maze. If None, a new figure and axes are created.
        """
        if ax is None:  # If ax is not provided, create a new figure and axes
            fig, ax = plt.subplots()

        # Convert the grid to a NumPy array for easier manipulation
        maze_array = np.array(self.grid)
        ax.imshow(maze_array, cmap='gray_r', interpolation='none')

        # Mark the start and goal positions
        # Make sure to switch the coordinates for plotting
        ax.plot(self.start[1], self.start[0], "bs")  # Switch to (y, x) for Matplotlib
        ax.plot(self.goal[1], self.goal[0], "gs")  # Switch to (y, x) for Matplotlib

        # Optionally set the aspect ratio of the plot to 'equal'
        ax.set_aspect('equal')

        # Turn off the axes labels
        ax.axis('off')


# Adapted from https://github.com/guofei9987/python-maze
class RandomMaze:
    def __init__(self, maze, point):
        # 每次只能上下左右试探
        self.step_set = np.array([[1, 0],
                                  [-1, 0],
                                  [0, 1],
                                  [0, -1]])
        self.maze = maze
        self.length, self.width = maze.shape
        self.init_maze()
        self.maze = self.find_next_step(self.maze, point)

    def init_maze(self):
        length, width = self.maze.shape
        maze_0 = np.zeros(shape=(length, width))
        maze_0[::2, ::2] = 1
        maze = np.where(self.maze < 0, self.maze, maze_0)
        self.maze = maze

    def find_next_step(self, maze, point):
        # 用递归实现深度优先搜索
        step_set = np.random.permutation(self.step_set)
        for next_step in step_set:
            next_point = point + next_step * 2
            x, y = next_point
            if 0 <= x < self.length and 0 <= y < self.width:  # 在格子内
                if maze[x, y] == 1:  # 如果还没打通，就打通
                    maze[x, y] = 2
                    maze[(point + next_step)[0], (point + next_step)[1]] = 2
                    maze = self.find_next_step(maze, next_point)  # 深度优先搜索
        # 全部遍历后，还是找不到，就是这个叶节点没有下一步了，返回即可
        return maze
