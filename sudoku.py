import random
import numpy as np
import pygame
import time


# Function to check if a number can be safely placed in the grid
def is_safe(grid, row, col, num):
    n = len(grid)
    # Check row, column, and block constraints
    for x in range(n):
        if grid[row][x] == num or grid[x][col] == num:
            return False

    box_size = int(n ** 0.5)
    box_row = row - row % box_size
    box_col = col - col % box_size

    for i in range(box_row, box_row + box_size):
        for j in range(box_col, box_col + box_size):
            if grid[i][j] == num:
                return False
    return True


# Function to generate Sudoku grid with random pre-filled numbers
def generate_sudoku(n, num_given):
    grid = np.zeros((n, n), dtype=int)

    # Randomly place numbers following Sudoku rules
    for _ in range(num_given):
        while True:
            row, col = random.randint(0, n - 1), random.randint(0, n - 1)
            num = random.randint(1, n)
            if grid[row][col] == 0 and is_safe(grid, row, col, num):
                grid[row][col] = num
                break

    return grid


# Backtracking solver function with step-by-step visualization
def solve_sudoku(grid, n):
    empty = find_empty(grid)
    if not empty:
        yield grid
        return
    row, col = empty

    for num in range(1, n + 1):
        if is_safe(grid, row, col, num):
            grid[row][col] = num
            yield from solve_sudoku(grid, n)  # Yield intermediate steps recursively
            grid[row][col] = 0  # Backtrack if the number doesn't work

    return


# Function to find the next empty cell
def find_empty(grid):
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 0:
                return (i, j)
    return None


# Pygame visualization for solving Sudoku
def visualize_sudoku(grid_gen, n):
    pygame.init()
    screen_size = 600
    screen = pygame.display.set_mode((screen_size, screen_size))
    pygame.display.set_caption('Sudoku Solver')

    font = pygame.font.SysFont(None, 40)
    box_size = screen_size // n

    def draw_grid(grid):
        screen.fill((255, 255, 255))
        for i in range(n):
            for j in range(n):
                value = grid[i][j]
                if value != 0:
                    text = font.render(str(value), True, (0, 0, 0))
                    screen.blit(text, (j * box_size + box_size // 3, i * box_size + box_size // 3))

        # Draw grid lines
        for i in range(n + 1):
            width = 5 if i % int(n ** 0.5) == 0 else 1
            pygame.draw.line(screen, (0, 0, 0), (i * box_size, 0), (i * box_size, screen_size), width)
            pygame.draw.line(screen, (0, 0, 0), (0, i * box_size), (screen_size, i * box_size), width)
        pygame.display.update()

    # Start visualizing the solving process
    for new_grid in grid_gen:
        draw_grid(new_grid)
        time.sleep(0.1)  # Adjust speed of the animation

    # Hold the final screen for a few seconds
    time.sleep(5)
    pygame.quit()

if __name__ == "__main__":
    n = 9  # For a standard Sudoku, n=9
    num_given = 20  # Number of pre-filled cells

    # Generate the Sudoku grid
    grid = generate_sudoku(n, num_given)

    # Solve the Sudoku and visualize the process
    solver = solve_sudoku(grid, n)
    visualize_sudoku(solver, n)
