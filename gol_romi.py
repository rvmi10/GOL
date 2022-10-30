import sys
from typing import List, Tuple
import pygame
import time

rules = """G A M E  O F   L I F E 
Click on a box to turn it RED (alive).
Click on it again to turn it back to GREY (dead).
Press the SPACE key to Start and to Pause the loop. Quit the Game by closing the window.
The game loop goes by these following rules:
RULE 1: Any live cell with fewer than two live neighbours dies, as if by underpopulation.
RULE 2: Any live cell with two or three live neighbours lives on to the next generation.
RULE 3: Any live cell with more than three live neighbours dies, as if by overpopulation.
RULE 4: Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
"""
WIDTH = 800
ROWS = 20
SURFACE = pygame.display.set_mode((WIDTH, WIDTH))

GREY = (154, 154, 154)
RED = (255, 0, 0)

pygame.display.set_caption("Game of Life - Press Left Arrow for Rules")


class Node:
    # __init__ bezieht sich auf klasse
    def __init__(self, row: int, column: int, width: int):
        self.row = row

        self.column = column

        self.colour = GREY

        self.x = int(row * width)

        self.y = int(column * width)

    def __repr__(self) -> str:
        return (
            f"Row={self.row}\n"
            f"Column={self.column}\n"
            f"Colour={self.colour}\n"
            f"x={self.x}\n"
            f"y={self.y}"
        )

    def draw(self, surface: pygame.Surface):
        pygame.draw.rect(surface, self.colour, (self.x, self.y, WIDTH / 8, WIDTH / 8))


def make_grid(rows: int) -> List[List[Node]]:
    grid = []  # empty array

    gap = WIDTH // rows  # returns an int # WIDTH declareted l. 4

    for y in range(rows):

        grid.append([])

        for x in range(rows):
            node = Node(x, y, gap)

            # for every y (part in array) append Node(i, j, gap)
            grid[y].append(node)

    return grid  # [[Node x,y,z], [Node], [Node], ...]


def draw_grid(window: pygame.Surface, rows: int, width: int):
    gap = width // ROWS  # ROWS declareted in l. 5

    for x in range(rows):

        # 1 and 2, 1 where will draw (on window) and 2 which colour
        # 3 where will draw again but on in what place
        # 4 size of our line, from x,y to size of our window
        # 3 from left to 4 right
        pygame.draw.line(window, (0, 0, 0), (0, x * gap), (width, x * gap))  # sidewards

    for y in range(rows):
    #from top to bottom
        pygame.draw.line(window, (0, 0, 0), (y * gap, 0), (y * gap, width))  # upwards


# screen update for every tick
def update_display(window: pygame.Surface, grid: List[List[Node]], rows: int, width: int):
    for row in grid:
        for spot in row:
            spot.draw(window)

    draw_grid(window, rows, width)

    pygame.display.update()


# returns location (coordinates) of rows, columns
def find_node(pos: int, width: int) -> Tuple[int, int]:
    interval = width / ROWS

    y, x = pos

    rows = y // interval

    columns = x // interval

    return int(rows), int(columns)


def neighbour(tile: Node) -> List[List[Tuple[int, int]]]:
    col, row = tile.row, tile.column

    neighbours = [
        [row - 1, col - 1],  # bottom left
        [row - 1, col],  # bottom
        [row - 1, col + 1],  # bottom right
        [row, col - 1],  # left
        [row, col + 1],  # right
        [row + 1, col - 1],  # top left
        [row + 1, col],  # top
        [row + 1, col + 1],  # top right
    ]

    actual_neighbour = []

    for neighbour in neighbours:
        row, col = neighbour
        # row, col auf einmal neighbour zuordnen

        # actual neighbour condition / rule
        # if selected neighbour box is on the grid append to actual array
        if 0 <= row <= (ROWS - 1) and 0 <= col <= (ROWS - 1):
            actual_neighbour.append(neighbour)

    return actual_neighbour


def update_grid(grid: List[List[Node]]) -> List[Tuple[int, int, int]]:
    newgrid = []
    for row in grid:
        for tile in row:
            neighbours = neighbour(tile)
            count = 0
            for i in neighbours:
                row, col = i
                if grid[row][col].colour == RED:
                    count += 1

            if tile.colour == RED:
                if count == 2 or count == 3:  # RULE 2
                    newgrid.append(RED)
                else:  # RULE 1
                    newgrid.append(GREY)
            else:
                if count == 3:  # RULE 4
                    newgrid.append(RED)
                else:  # RULE 3
                    newgrid.append(GREY)

    return newgrid  # returns color for all boxes in the grid


def main(surface: pygame.Surface, width: int):
    grid = make_grid(ROWS)
    run = None

    while True:
        pygame.time.delay(50)  # stops cpu dying
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    run = True  # initiates game loop

            if event.type == pygame.MOUSEBUTTONDOWN: #changes colour on click
                pos = pygame.mouse.get_pos()
                row, col = find_node(pos, width)
                if grid[col][row].colour == GREY:
                    grid[col][row].colour = RED

                elif grid[col][row].colour == RED:
                    grid[col][row].colour = GREY

            if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        print(rules)
            while run:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            run = False



                newcolours = update_grid(grid)
                count = 0
                for i in range(0, len(grid[0])):
                    for j in range(0, len(grid[0])):
                        # "alle felder = update_grid function an dem index von count" / old to new
                        grid[i][j].colour = newcolours[count]
                        count += 1
                update_display(surface, grid, ROWS, width) #neues display
                time.sleep(1)  # no rush

            update_display(surface, grid, ROWS, width)
            continue


main(SURFACE, WIDTH)
