import heapq
import matplotlib.pyplot as plt


class Mouse:
    def __init__(self, maze):
        """
        Initializes the Mouse with a reference to a Maze object.
        :param maze: A Maze object that the mouse will navigate.
        """
        self.maze = maze
        self.position = maze.start
        self.path = []
        self.visited = []

    @staticmethod
    def heuristic(a, b):
        """
        Calculate the Manhattan distance heuristic between two points.
        :param a: Tuple (x, y) as the current position.
        :param b: Tuple (x, y) as the goal position.
        :return: Manhattan distance between the two points.
        """
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def find_path(self):
        # First, lets initialize the variables of the algorithm
        # Priority queue in which the priority is set by the f(x) value (0) for the start
        open_set = []
        heapq.heappush(open_set, (0, self.maze.start))
        # Dictionary to store the nodes (pixels) that have already been visited. This will be
        # useful to apply backtracking and reconstruct the path.
        came_from = {}
        # g(x) dictionary
        g_score = {self.maze.start: 0}
        # f(x) dictionary, the first value should be the highest since h(x) is the highest
        # Remember: f(x) = g(x) + h(x)
        f_score = {self.maze.start: self.heuristic(self.maze.start, self.maze.goal)}

        while open_set:
            # We pop the highest priority neighbour
            current = heapq.heappop(open_set)[1]
            if current == self.maze.goal:
                # If we've alredy reached the goal, then we reconstruct the path
                self.reconstruct_path(came_from, current)
                return self.path, g_score
            for neighbour in self.maze.get_neighbors(*current):
                # We assume that the step cost from current to the neighbour is 1
                tentative_g_score = g_score[current] + 1
                """
                - CASE 1: The neighbour hasn't been visited yet. Then we must visit it and record it's g(x)
                - CASE 2: The neighbour, which has already been visited, has a g_score higher than the tentative_g_score
                          g(current) + 1: Is this new path a cheaper way to reach n than what we've found before?
                In a uniform-cost environment, the g_score serves as a measure of distance (in terms of steps) 
                from the start. When evaluating whether to update the path to a neighbor, the algorithm still checks 
                if the tentative_g_score is less than the g_score for that neighbor, as before. This ensures that if 
                there's a shorter path (in terms of the number of steps) to a neighbor, it will replace the longer 
                path.
                """
                if neighbour not in g_score or tentative_g_score < g_score[neighbour]:
                    # This path to neighbor is better than any previous one. Record it!
                    came_from[neighbour] = current
                    g_score[neighbour] = tentative_g_score
                    f_score[neighbour] = tentative_g_score + self.heuristic(neighbour, self.maze.goal)
                    heapq.heappush(open_set, (f_score[neighbour], neighbour))
        return None # No path was found

    def find_path_visited(self):
        open_set = []
        heapq.heappush(open_set, (0, self.maze.start))
        g_score = {self.maze.start: 0}
        f_score = {self.maze.start: self.heuristic(self.maze.start, self.maze.goal)}
        visited = []  # List to keep track of visited nodes

        while open_set:
            current = heapq.heappop(open_set)[1]
            visited.append(current)  # Record the visited node

            if current == self.maze.goal:
                # If the goal is reached, no need to continue. Return visited nodes.
                return visited

            for neighbour in self.maze.get_neighbors(*current):
                tentative_g_score = g_score[current] + 1
                if neighbour not in g_score or tentative_g_score < g_score[neighbour]:
                    g_score[neighbour] = tentative_g_score
                    f_score[neighbour] = tentative_g_score + self.heuristic(neighbour, self.maze.goal)
                    heapq.heappush(open_set, (f_score[neighbour], neighbour))

            yield visited  # Yield the current list of visited nodes

        return visited  # Return the visited list in case no path is found

    def reconstruct_path(self, came_from, current):
        """
        Reconstructs the path from the goal to the start using the came_from map.
        :param came_from: A dictionary holding the mapping of each node to its predecessor.
        :param current: The current position (goal position when reconstructing).
        """
        self.path = []
        while current in came_from:
            self.path.append(current)
            current = came_from[current]
        self.path.append(self.maze.start)  # Optional: include the start position
        self.path.reverse()  # The path is reconstructed from goal to start, so reverse it

    def move_to(self, position):
        """
        Moves the mouse to a new position.
        :param position: Tuple (x, y) representing the new position.
        """
        if position in self.path:
            self.position = position
        else:
            raise ValueError("The new position is not on the path!")

    def display_path(self, step=None, ax=None):
        """
        Displays the path that the mouse has found up to the current step using Matplotlib.
        :param ax: Matplotlib axes object to draw the path.
        :param step: The current step in the path to display up to. If None, display the full path.
        """

        if ax is None:
            fig, ax = plt.subplots()

        # Use the Maze's display method to draw the maze
        self.maze.display(ax=ax)

        # Overlay the path on the maze
        if step is not None and step <= len(self.path):
            path_section = self.path[:step]
        else:
            path_section = self.path

        # Convert the path into two lists of x and y coordinates for plotting
        xs, ys = zip(*path_section)
        ax.plot(ys, xs, "r-", linewidth=2)  # Reverse the order for Matplotlib
        ax.plot(ys[-1], xs[-1], "ro")  # Reverse the order for Matplotlib
        ax.set_aspect('equal')
        ax.axis('off')
