import pygame
import random

# 설정값
S_WIDTH, S_HEIGHT = 800, 700
G_WIDTH, G_HEIGHT = 300, 600  # 실제 게임판 크기 (10x20 칸)
BLOCK_SIZE = 30
TOP_LEFT_X = (S_WIDTH - G_WIDTH) // 2
TOP_LEFT_Y = S_HEIGHT - G_HEIGHT - 50

# 모양 정의 (7가지 테트로미노)
S = [['.....', '.....', '..00.', '.00..', '.....'], ['.....', '..0..', '..00.', '...0.', '.....']]
Z = [['.....', '.....', '.00..', '..00.', '.....'], ['.....', '..0..', '.00..', '.0...', '.....']]
I = [['..0..', '..0..', '..0..', '..0..', '.....'], ['.....', '0000.', '.....', '.....', '.....']]
O = [['.....', '.....', '.00..', '.00..', '.....']]
J = [['.....', '.0...', '.000.', '.....', '.....'], ['.....', '..00.', '..0..', '..0..', '.....'], ['.....', '.....', '.000.', '...0.', '.....'], ['.....', '..0..', '..0..', '.00..', '.....']]
L = [['.....', '...0.', '.000.', '.....', '.....'], ['.....', '..0..', '..0..', '..00.', '.....'], ['.....', '.....', '.000.', '.0...', '.....'], ['.....', '.00..', '..0..', '..0..', '.....']]
T = [['.....', '..0..', '.000.', '.....', '.....'], ['.....', '..0..', '..00.', '..0..', '.....'], ['.....', '.....', '.000.', '..0..', '.....'], ['.....', '..0..', '.00..', '..0..', '.....']]

SHAPES = [S, Z, I, O, J, L, T]
SHAPE_COLORS = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]

def draw_score(surface, score):
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render(f'Score: {score}', 1, (255,255,255))
    sx = TOP_LEFT_X + G_WIDTH + 50
    sy = TOP_LEFT_Y + 50
    surface.blit(label, (sx, sy))

def draw_next_shape(shape, surface):
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Next Shape', 1, (255,255,255))
    sx = TOP_LEFT_X + G_WIDTH + 50
    sy = TOP_LEFT_Y + G_HEIGHT/2 - 100
    format = shape.shape[shape.rotation % len(shape.shape)]
    for i, line in enumerate(format):
        for j, column in enumerate(line):
            if column == '0':
                pygame.draw.rect(surface, shape.color, (sx + j*30, sy + i*30, 30, 30), 0)
    surface.blit(label, (sx + 10, sy - 30))

def draw_score(surface, score):
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render(f'Score: {score}', 1, (255,255,255))
    sx = TOP_LEFT_X + G_WIDTH + 50
    sy = TOP_LEFT_Y + 50
    surface.blit(label, (sx, sy))

class Piece:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = SHAPE_COLORS[SHAPES.index(shape)]
        self.rotation = 0

def create_grid(locked_pos={}):
    grid = [[(0,0,0) for _ in range(10)] for _ in range(20)]
    for y in range(20):
        for x in range(10):
            if (x, y) in locked_pos:
                grid[y][x] = locked_pos[(x, y)]
    return grid

def convert_shape_format(piece):
    positions = []
    format = piece.shape[piece.rotation % len(piece.shape)]
    for i, line in enumerate(format):
        for j, column in enumerate(line):
            if column == '0':
                positions.append((piece.x + j, piece.y + i))
    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)
    return positions

def valid_space(piece, grid):
    accepted_pos = [[(x, y) for x in range(10) if grid[y][x] == (0,0,0)] for y in range(20)]
    accepted_pos = [x for item in accepted_pos for x in item]
    formatted = convert_shape_format(piece)
    for pos in formatted:
        if pos not in accepted_pos:
            if pos[1] > -1:
                return False
    return True

def clear_rows(grid, locked):
    inc = 0
    for i in range(len(grid)-1, -1, -1):
        row = grid[i]
        if (0,0,0) not in row:
            inc += 1
            ind = i
            for j in range(len(row)):
                try: del locked[(j, i)]
                except: continue
    if inc > 0:
        for key in sorted(list(locked.keys()), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)
    return inc

def draw_window(surface, grid):
    surface.fill((0,0,0))
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            pygame.draw.rect(surface, grid[y][x], (TOP_LEFT_X + x*BLOCK_SIZE, TOP_LEFT_Y + y*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)
    pygame.draw.rect(surface, (255,0,0), (TOP_LEFT_X, TOP_LEFT_Y, G_WIDTH, G_HEIGHT), 4)

def main():
    locked_positions = {}
    grid = create_grid(locked_positions)
    change_piece = False
    run = True
    current_piece = Piece(5, 0, random.choice(SHAPES))
    next_piece = Piece(5, 0, random.choice(SHAPES))
    clock = pygame.time.Clock()
    fall_time = 0
    
    # 1. 점수 변수 초기화
    score = 0 

    while run:
        fall_speed = 0.27
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        clock.tick()

        if fall_time / 1000 >= fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not valid_space(current_piece, grid) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid): current_piece.x += 1
                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid): current_piece.x -= 1
                if event.key == pygame.K_UP:
                    current_piece.rotation += 1
                    if not valid_space(current_piece, grid): current_piece.rotation -= 1
                if event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not valid_space(current_piece, grid): current_piece.y -= 1
                if event.key == pygame.K_SPACE:
                    while valid_space(current_piece, grid):
                        current_piece.y += 1
                    current_piece.y -= 1

        shape_pos = convert_shape_format(current_piece)
        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1: grid[y][x] = current_piece.color

        if change_piece:
            for pos in shape_pos:
                locked_positions[(pos[0], pos[1])] = current_piece.color
            current_piece = next_piece
            next_piece = Piece(5, 0, random.choice(SHAPES))
            change_piece = False
            
            # 2. 줄이 지워질 때 점수 누적 (1줄당 10점)
            rows_cleared = clear_rows(grid, locked_positions)
            score += rows_cleared * 10 

        # 3. 화면 그리기 (기존 그리기에 점수 그리기 추가)
        draw_window(win, grid)
        draw_score(win, score) # 이 줄이 점수를 화면에 그려줍니다.
        
        pygame.display.update()

        if any(y < 0 for (x, y) in locked_positions):
            run = False

    pygame.display.quit()
    