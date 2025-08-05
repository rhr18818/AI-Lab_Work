import time
from collections import deque
import heapq

class EightPuzzle:
    """
    Represents the 8-puzzle board and its core functionalities.
    States are represented as tuples of tuples to be hashable.
    """
    def __init__(self, initial_state_list, goal_state_list=None):
        self.initial_state = self.state_to_tuple(initial_state_list)
        if goal_state_list:
            self.goal_state = self.state_to_tuple(goal_state_list)
        else:
            self.goal_state = ((1, 2, 3), (4, 5, 6), (7, 8, 0))
        self.size = 3
        # Pre-calculate goal positions for the heuristic for efficiency
        self.goal_positions = {tile: (r, c) for r, row in enumerate(self.goal_state) for c, tile in enumerate(row)}


    def state_to_tuple(self, state_list):
        """Converts a list of lists to a tuple of tuples."""
        return tuple(tuple(row) for row in state_list)

    def find_blank(self, state):
        """Finds the (row, col) position of the blank tile (0)."""
        for r in range(self.size):
            for c in range(self.size):
                if state[r][c] == 0:
                    return r, c
        return None

    def get_neighbors(self, state):
        """Returns a list of all valid neighbor states."""
        neighbors = []
        blank_row, blank_col = self.find_blank(state)
        
        # Possible moves: (dr, dc) for Up, Down, Left, Right
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        for dr, dc in moves:
            new_row, new_col = blank_row + dr, blank_col + dc
            
            if 0 <= new_row < self.size and 0 <= new_col < self.size:
                new_state_list = [list(row) for row in state]
                new_state_list[blank_row][blank_col] = new_state_list[new_row][new_col]
                new_state_list[new_row][new_col] = 0
                neighbors.append(self.state_to_tuple(new_state_list))
        
        return neighbors

    def manhattan_distance(self, state):
        """Calculates the Manhattan distance heuristic for a given state."""
        distance = 0
        for r in range(self.size):
            for c in range(self.size):
                tile = state[r][c]
                if tile != 0:
                    goal_r, goal_c = self.goal_positions[tile]
                    distance += abs(r - goal_r) + abs(c - goal_c)
        return distance

class BruteForceSearch:
    """Implements Brute-Force Search using Breadth-First Search (BFS)."""
    def __init__(self, puzzle):
        self.puzzle = puzzle
        
    def solve(self):
        start_time = time.time()
        # Queue stores tuples of (state, path_list)
        queue = deque([(self.puzzle.initial_state, [])])
        visited = {self.puzzle.initial_state}
        nodes_explored = 0

        while queue:
            current_state, path = queue.popleft()
            nodes_explored += 1
            
            if current_state == self.puzzle.goal_state:
                end_time = time.time()
                return {
                    'path': path,
                    'steps': len(path),
                    'nodes_explored': nodes_explored,
                    'time_taken': end_time - start_time,
                }
            
            for neighbor in self.puzzle.get_neighbors(current_state):
                if neighbor not in visited:
                    visited.add(neighbor)
                    new_path = path + [neighbor]
                    queue.append((neighbor, new_path))
        
        return None # No solution found

class HeuristicSearch:
    """Implements Heuristic Search using Best-First Search."""
    def __init__(self, puzzle):
        self.puzzle = puzzle

    def solve(self):
        start_time = time.time()
        h_initial = self.puzzle.manhattan_distance(self.puzzle.initial_state)
        # Priority queue stores (heuristic_value, state, path)
        p_queue = [(h_initial, self.puzzle.initial_state, [])]
        visited = {self.puzzle.initial_state}
        nodes_explored = 0

        while p_queue:
            _, current_state, path = heapq.heappop(p_queue)
            nodes_explored += 1

            if current_state == self.puzzle.goal_state:
                end_time = time.time()
                return {
                    'path': path,
                    'steps': len(path),
                    'nodes_explored': nodes_explored,
                    'time_taken': end_time - start_time,
                }

            for neighbor in self.puzzle.get_neighbors(current_state):
                if neighbor not in visited:
                    visited.add(neighbor)
                    h_neighbor = self.puzzle.manhattan_distance(neighbor)
                    new_path = path + [neighbor]
                    heapq.heappush(p_queue, (h_neighbor, neighbor, new_path))

        return None # No solution found

class AStarSearch:
    """Implements the A* Search algorithm."""
    def __init__(self, puzzle):
        self.puzzle = puzzle

    def solve(self):
        start_time = time.time()
        g_cost = 0
        h_cost = self.puzzle.manhattan_distance(self.puzzle.initial_state)
        f_cost = g_cost + h_cost
        
        # Priority queue stores (f_cost, g_cost, state, path)
        p_queue = [(f_cost, g_cost, self.puzzle.initial_state, [])]
        
        # visited stores the minimum g_cost found so far for a state
        visited = {self.puzzle.initial_state: 0}
        nodes_explored = 0
        
        while p_queue:
            _, g_val, current_state, path = heapq.heappop(p_queue)
            nodes_explored += 1

            # If we've found a better path already, skip
            if g_val > visited[current_state]:
                continue

            if current_state == self.puzzle.goal_state:
                end_time = time.time()
                return {
                    'path': path,
                    'steps': len(path),
                    'nodes_explored': nodes_explored,
                    'time_taken': end_time - start_time,
                }

            for neighbor in self.puzzle.get_neighbors(current_state):
                new_g_val = g_val + 1
                if neighbor not in visited or new_g_val < visited[neighbor]:
                    visited[neighbor] = new_g_val
                    h_neighbor = self.puzzle.manhattan_distance(neighbor)
                    f_neighbor = new_g_val + h_neighbor
                    new_path = path + [neighbor]
                    heapq.heappush(p_queue, (f_neighbor, new_g_val, neighbor, new_path))
                    
        return None # No solution found

if __name__ == '__main__':
    # Define an initial state for testing
    #initial = [[2, 8, 3], [1, 6, 4], [7, 0, 5]]
    
    initial = [[1, 2, 3], [4, 0, 5], [7, 8, 6]]

    #goal = [[1, 2, 3], [8, 0, 4], [7, 6, 5]] # A different goal to show flexibility

    puzzle = EightPuzzle(initial_state_list=initial)

    # --- 1. Brute-Force (BFS) ---
    print("--- Solving with Brute-Force Search (BFS) ---")
    bfs_solver = BruteForceSearch(puzzle)
    bfs_result = bfs_solver.solve()
    if bfs_result:
        print(f"Solution found in {bfs_result['steps']} steps.")
        print(f"Nodes explored: {bfs_result['nodes_explored']}")
        print(f"Time taken: {bfs_result['time_taken']:.4f} seconds\n")
    else:
        print("No solution found.\n")

    # --- 2. Heuristic Search (Best-First) ---
    print("--- Solving with Heuristic Search (Best-First) ---")
    heuristic_solver = HeuristicSearch(puzzle)
    heuristic_result = heuristic_solver.solve()
    if heuristic_result:
        print(f"Solution found in {heuristic_result['steps']} steps.")
        print(f"Nodes explored: {heuristic_result['nodes_explored']}")
        print(f"Time taken: {heuristic_result['time_taken']:.4f} seconds\n")
    else:
        print("No solution found.\n")
        
    # --- 3. A* Search ---
    print("--- Solving with A* Search ---")
    astar_solver = AStarSearch(puzzle)
    astar_result = astar_solver.solve()
    if astar_result:
        print(f"Solution found in {astar_result['steps']} steps.")
        print(f"Nodes explored: {astar_result['nodes_explored']}")
        print(f"Time taken: {astar_result['time_taken']:.4f} seconds\n")
    else:
        print("No solution found.\n")
