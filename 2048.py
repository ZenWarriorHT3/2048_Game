import pygame
import random

# Initialize pygame
pygame.init()

# Game settings
SIZE = 4  # 4x4 grid
WIDTH, HEIGHT = 400, 400  # Screen size
CELL_SIZE = WIDTH // SIZE  # Size of each cell
FONT = pygame.font.SysFont('Arial', 40)

# Define colors
BACKGROUND_COLOR = (187, 173, 160)
EMPTY_CELL_COLOR = (205, 193, 180)
COLORS = {
    2: (238, 228, 218), 4: (237, 224, 200), 8: (242, 177, 121),
    16: (245, 149, 99), 32: (246, 124, 95), 64: (246, 94, 59),
    128: (237, 207, 114), 256: (237, 204, 97), 512: (237, 200, 80),
    1024: (237, 197, 63), 2048: (237, 194, 46)
}

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048 Game")

# Game logic
def init_game():
    grid = [[0] * SIZE for _ in range(SIZE)]
    add_random_tile(grid)
    add_random_tile(grid)
    return grid

def add_random_tile(grid):
    empty_cells = [(r, c) for r in range(SIZE) for c in range(SIZE) if grid[r][c] == 0]
    if empty_cells:
        r, c = random.choice(empty_cells)
        grid[r][c] = 4 if random.random() < 0.1 else 2

def move_row_left(row):
    new_row = [i for i in row if i != 0]
    new_row += [0] * (SIZE - len(new_row))
    for i in range(SIZE - 1):
        if new_row[i] == new_row[i + 1] and new_row[i] != 0:
            new_row[i] *= 2
            new_row[i + 1] = 0
    new_row = [i for i in new_row if i != 0]
    new_row += [0] * (SIZE - len(new_row))
    return new_row

def rotate_grid(grid):
    return [list(row) for row in zip(*grid[::-1])]

def move_left(grid):
    return [move_row_left(row) for row in grid]

def move_right(grid):
    return [move_row_left(row[::-1])[::-1] for row in grid]

def move_up(grid):
    grid = rotate_grid(grid)
    grid = move_right(grid)
    grid = rotate_grid(grid)
    grid = rotate_grid(grid)
    grid = rotate_grid(grid)
    return grid

def move_down(grid):
    grid = rotate_grid(grid)
    grid = move_left(grid)
    grid = rotate_grid(grid)
    grid = rotate_grid(grid)
    grid = rotate_grid(grid)
    return grid

def is_game_over(grid):
    for row in grid:
        if 0 in row:
            return False
    for r in range(SIZE):
        for c in range(SIZE - 1):
            if grid[r][c] == grid[r][c + 1]:
                return False
            if grid[c][r] == grid[c + 1][r]:
                return False
    return True

def draw_grid(grid):
    screen.fill(BACKGROUND_COLOR)
    for r in range(SIZE):
        for c in range(SIZE):
            value = grid[r][c]
            color = COLORS.get(value, EMPTY_CELL_COLOR)
            pygame.draw.rect(screen, color, (c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            if value != 0:
                text_surface = FONT.render(str(value), True, (0, 0, 0))
                text_rect = text_surface.get_rect(center=(c * CELL_SIZE + CELL_SIZE // 2, r * CELL_SIZE + CELL_SIZE // 2))
                screen.blit(text_surface, text_rect)
    pygame.display.update()

def handle_swipe(direction, grid):
    if direction == "left":
        new_grid = move_left(grid)
    elif direction == "right":
        new_grid = move_right(grid)
    elif direction == "up":
        new_grid = move_up(grid)
    elif direction == "down":
        new_grid = move_down(grid)
    
    if new_grid != grid:
        add_random_tile(new_grid)
    return new_grid

# Touchscreen event handler (simulated via mouse)
def detect_swipe(start_pos, end_pos):
    x_diff = end_pos[0] - start_pos[0]
    y_diff = end_pos[1] - start_pos[1]
    if abs(x_diff) > abs(y_diff):
        return "left" if x_diff < 0 else "right"
    else:
        return "up" if y_diff < 0 else "down"

# Main game loop
def main():
    grid = init_game()
    draw_grid(grid)
    running = True
    start_pos = None

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                start_pos = event.pos
            elif event.type == pygame.MOUSEBUTTONUP and start_pos:
                end_pos = event.pos
                direction = detect_swipe(start_pos, end_pos)
                grid = handle_swipe(direction, grid)
                draw_grid(grid)
                if is_game_over(grid):
                    print("Game Over")
                    running = False

    pygame.quit()

if __name__ == "__main__":
    main()
