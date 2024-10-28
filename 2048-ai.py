import random
import math
import sys

# Optional Numba import for JIT compilation
try:
    from numba import njit
    NUMBA_AVAILABLE = True
except ImportError:
    NUMBA_AVAILABLE = False

# Heuristic functions used to evaluate the game board

def empty_tile_heuristic(grid):
    """
    Counts the number of empty tiles on the board.
    Encourages the AI to keep the board open to allow more moves.
    """
    return sum(row.count(0) for row in grid)

def smoothness_heuristic(grid):
    """
    Measures the smoothness of the grid.
    A smooth grid has similar tile values close to each other,
    which helps in merging tiles.
    """
    smoothness = 0
    for x in range(4):
        for y in range(4):
            if grid[x][y]:
                value = math.log2(grid[x][y])
                for direction in [(1, 0), (0, 1)]:  # Right and down
                    dx, dy = direction
                    nx, ny = x + dx, y + dy
                    while 0 <= nx < 4 and 0 <= ny < 4:
                        if grid[nx][ny]:
                            target_value = math.log2(grid[nx][ny])
                            smoothness -= abs(value - target_value)
                            break
                        nx += dx
                        ny += dy
    return smoothness

def monotonicity_heuristic(grid):
    """
    Measures how monotonic the grid is (i.e., whether the tiles are ordered).
    Encourages the AI to keep the tiles in order to facilitate merging.
    """
    totals = [0, 0, 0, 0]  # up, down, left, right

    # Left/right direction
    for x in range(4):
        current_row = grid[x]
        for i in range(3):
            current = math.log2(current_row[i]) if current_row[i] else 0
            next = math.log2(current_row[i + 1]) if current_row[i + 1] else 0
            if current > next:
                totals[0] += next - current
            elif next > current:
                totals[1] += current - next

    # Up/down direction
    for y in range(4):
        current_column = [grid[x][y] for x in range(4)]
        for i in range(3):
            current = math.log2(current_column[i]) if current_column[i] else 0
            next = math.log2(current_column[i + 1]) if current_column[i + 1] else 0
            if current > next:
                totals[2] += next - current
            elif next > current:
                totals[3] += current - next

    # Return the maximum monotonicity score
    return max(totals[0], totals[1]) + max(totals[2], totals[3])

def max_tile_heuristic(grid):
    """
    Encourages the AI to focus on achieving higher tiles.
    """
    return math.log2(max(max(row) for row in grid)) if max(max(row) for row in grid) else 0

def combined_heuristic(grid):
    """
    Combines multiple heuristics into a single evaluation score.
    """
    empty_weight = 2.7
    max_tile_weight = 1.0
    smoothness_weight = 0.1
    monotonicity_weight = 1.0

    return (empty_weight * empty_tile_heuristic(grid) +
            max_tile_weight * max_tile_heuristic(grid) +
            smoothness_weight * smoothness_heuristic(grid) +
            monotonicity_weight * monotonicity_heuristic(grid))

# Core game logic functions

def initialize_game():
    """
    Initializes the game board with two random tiles.
    """
    grid = [[0]*4 for _ in range(4)]
    add_random_tile(grid)
    add_random_tile(grid)
    return grid

def add_random_tile(grid):
    """
    Adds a random tile (2 or 4) to a random empty cell on the board.
    """
    empty_cells = [(r, c) for r in range(4) for c in range(4) if grid[r][c] == 0]
    if empty_cells:
        row, col = random.choice(empty_cells)
        grid[row][col] = 2 if random.random() < 0.9 else 4

def game_over(grid):
    """
    Checks if no more moves are possible.
    """
    if any(0 in row for row in grid):
        return False
    for x in range(4):
        for y in range(4):
            if x + 1 < 4 and grid[x][y] == grid[x + 1][y]:
                return False
            if y + 1 < 4 and grid[x][y] == grid[x][y + 1]:
                return False
    return True

def get_possible_moves(grid):
    """
    Returns a list of possible moves and their resulting grids.
    """
    moves = []
    for direction in ['up', 'down', 'left', 'right']:
        new_grid = move(grid, direction)
        if new_grid != grid:
            moves.append((direction, new_grid))
    return moves

def move(grid, direction):
    """
    Performs a move in the specified direction.
    """
    if direction == 'up':
        grid_rotated = rotate(grid)
        merged_grid = merge_left(grid_rotated)
        grid = rotate(merged_grid, -1)
    elif direction == 'down':
        grid_rotated = rotate(grid, -1)
        merged_grid = merge_left(grid_rotated)
        grid = rotate(merged_grid)
    elif direction == 'left':
        grid = merge_left(grid)
    elif direction == 'right':
        grid_reversed = reverse(grid)
        merged_grid = merge_left(grid_reversed)
        grid = reverse(merged_grid)
    return grid

def merge_left(grid):
    """
    Merges the grid to the left.
    """
    new_grid = []
    for row in grid:
        new_row = [tile for tile in row if tile != 0]
        i = 0
        while i < len(new_row) - 1:
            if new_row[i] == new_row[i + 1]:
                new_row[i] *= 2
                del new_row[i + 1]
                new_row.append(0)  # Ensure the row remains of length 4
            i += 1
        new_row += [0] * (4 - len(new_row))
        new_grid.append(new_row)
    return new_grid

def reverse(grid):
    """
    Reverses each row in the grid.
    """
    return [row[::-1] for row in grid]

def rotate(grid, times=1):
    """
    Rotates the grid 90 degrees clockwise (times > 0) or counter-clockwise (times < 0).
    """
    times = times % 4
    for _ in range(times):
        grid = [list(row) for row in zip(*grid[::-1])]
    return grid

# Transposition table for memoization
transposition_table = {}

# Optional Numba JIT compilation
def expectimax(grid, depth, player_turn, max_depth=3):
    """
    The expectimax algorithm implementation with memoization.
    """
    grid_tuple = tuple(tuple(row) for row in grid)
    if (grid_tuple, depth, player_turn) in transposition_table:
        return transposition_table[(grid_tuple, depth, player_turn)]

    if depth == max_depth or game_over(grid):
        score = combined_heuristic(grid)
        transposition_table[(grid_tuple, depth, player_turn)] = (score, None)
        return score, None

    if player_turn:
        # Maximizing player (AI)
        max_score = -float('inf')
        best_direction = None
        for direction, new_grid in get_possible_moves(grid):
            score, _ = expectimax(new_grid, depth + 1, False, max_depth)
            if score > max_score:
                max_score = score
                best_direction = direction
        transposition_table[(grid_tuple, depth, player_turn)] = (max_score, best_direction)
        return max_score, best_direction
    else:
        # Chance nodes (random tile addition)
        score = 0
        empty_cells = [(r, c) for r in range(4) for c in range(4) if grid[r][c] == 0]
        if not empty_cells:
            score = combined_heuristic(grid)
            transposition_table[(grid_tuple, depth, player_turn)] = (score, None)
            return score, None

        total_tiles = len(empty_cells)
        probabilities = [0.9, 0.1]
        tile_values = [2, 4]
        for cell in empty_cells:
            r, c = cell
            for value, probability in zip(tile_values, probabilities):
                grid_new = [row[:] for row in grid]
                grid_new[r][c] = value
                tile_score, _ = expectimax(grid_new, depth + 1, True, max_depth)
                score += (probability / total_tiles) * tile_score

        transposition_table[(grid_tuple, depth, player_turn)] = (score, None)
        return score, None

# Game simulation function

def play_game():
    """
    Simulates a game using the expectimax algorithm to choose moves.
    """
    global transposition_table
    transposition_table = {}  # Reset the transposition table for each game
    grid = initialize_game()
    moves_made = 0
    move_limit = 1000
    max_depth = 3  # Reduced depth for faster runtime

    print("Initial game board:")
    for row in grid:
        print(row)
    print("-" * 20)

    while not game_over(grid) and moves_made < move_limit:
        # Get the best move using expectimax
        _, best_direction = expectimax(grid, depth=0, player_turn=True, max_depth=max_depth)

        if best_direction is None:
            break  # No more moves, game over

        grid = move(grid, best_direction)
        add_random_tile(grid)
        moves_made += 1

        # Print the game board after each move
        print(f"Move {moves_made}: {best_direction}")
        for row in grid:
            print(row)
        print("-" * 20)

    print("Final Board:")
    for row in grid:
        print(row)

    max_tile = max(max(row) for row in grid)
    return max_tile

# Start and automate multiple game runs

if __name__ == "__main__":
    print("\n")  # Empty line before output
    num_runs = 20  # Number of times to run the game
    highest_tile = 0  # Track the highest tile across runs
    scores = []  # Store scores of each run

    for i in range(num_runs):
        print(f"Run {i + 1}:")
        max_tile = play_game()
        scores.append(max_tile)
        highest_tile = max(highest_tile, max_tile)  # Update highest tile if needed
        print(f"Max Tile Reached: {max_tile}")
        print("=" * 30)  # Separator between runs

    # Clear separation of final results
    print("\n" + "=" * 30)
    print("Scores from each run:")
    for i, score in enumerate(scores):
        print(f"Run {i + 1}: Max Tile = {score}")

    print(f"\nHighest Tile Reached After {num_runs} Runs: {highest_tile}")
    print("\n")  # Empty line after output
