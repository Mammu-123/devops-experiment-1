3

import copy
import heapq

class PuzzleState:
    def __init__(self, board, parent=None, move="", cost=0):
        self.board = board
        self.parent = parent
        self.move = move
        self.cost = cost
        self.blank_pos = self.find_blank()
        self.hash = str(self.board)

    def find_blank(self):
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == 0:
                    return (i, j)

    def get_neighbors(self):
        neighbors = []
        i, j = self.blank_pos
        moves = [("Up", -1, 0), ("Down", 1, 0), ("Left", 0, -1), ("Right", 0, 1)]

        for move, dx, dy in moves:
            ni, nj = i + dx, j + dy
            if 0 <= ni < 3 and 0 <= nj < 3:
                new_board = copy.deepcopy(self.board)
                new_board[i][j], new_board[ni][nj] = new_board[ni][nj], new_board[i][j]
                neighbors.append(PuzzleState(new_board, self, move, self.cost + 1))
        return neighbors

    def __lt__(self, other):
        return self.cost < other.cost

def calculate_heuristic(state, goal_state):
    distance = 0
    for i in range(3):
        for j in range(3):
            val = state.board[i][j]
            if val != 0:
                goal_i, goal_j = (val - 1) // 3, (val - 1) % 3
                distance += abs(i - goal_i) + abs(j - goal_j)
    return distance

def a_star_search(start_state, goal_state):
    open_list = []
    heapq.heappush(open_list, (calculate_heuristic(start_state, goal_state), start_state))
    visited = set()

    while open_list:
        _, current = heapq.heappop(open_list)

        if current.board == goal_state.board:
            return reconstruct_path(current)

        visited.add(current.hash)
        for neighbor in current.get_neighbors():
            if neighbor.hash not in visited:
                total_cost = calculate_heuristic(neighbor, goal_state) + neighbor.cost
                heapq.heappush(open_list, (total_cost, neighbor))
    return None

def reconstruct_path(state):
    path = []
    while state:
        path.append((state.move, state.board))
        state = state.parent
    return path[::-1]

def print_solution(path):
    print(f"Total Moves: {len(path) - 1}\n")
    for move, board in path:
        if move:
            print(f"Move: {move}")
        for row in board:
            print(row)
        print()

# Example usage
if __name__ == "__main__":
    initial_board = [[1, 2, 3], [4, 0, 5], [6, 7, 8]]
    goal_board = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

    initial_state = PuzzleState(initial_board)
    goal_state = PuzzleState(goal_board)

    solution_path = a_star_search(initial_state, goal_state)

    if solution_path:
        print("Solution found!")
        print_solution(solution_path)
    else:
        print("No solution found.")