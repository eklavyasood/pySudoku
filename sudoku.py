import sys
import pygame as pg

pg.init() # init pygame
screenSize = 750, 750
screen = pg.display.set_mode(screenSize)
bgColor = 'black'
fgColor = 'purple'
textColor = 'white'
highlightColor = 'yellow'
fontSize = 60
font = pg.font.SysFont(None, fontSize)
congratsFont = pg.font.SysFont(None, 60)

# unsolved grid
# numberGrid = [
#     [4, 7, 3, 0, 0, 8, 6, 0, 1],
#     [0, 9, 0, 6, 1, 2, 4, 0, 0],
#     [2, 0, 1, 3, 0, 0, 9, 8, 0],
#     [7, 0, 0, 2, 0, 0, 8, 1, 0],
#     [9, 0, 4, 0, 8, 1, 0, 0, 2],
#     [0, 2, 0, 0, 0, 0, 0, 0, 9],
#     [0, 1, 9, 0, 0, 5, 2, 4, 0],
#     [3, 0, 0, 0, 2, 6, 0, 0, 0],
#     [0, 8, 2, 1, 0, 0, 7, 9, 0],
# ]

# solved grid for debugging
numberGrid = [
    [4, 7, 0, 5, 9, 8, 6, 2, 1],
    [8, 9, 5, 6, 1, 2, 4, 3, 7],
    [2, 6, 1, 3, 4, 7, 9, 8, 5],
    [7, 3, 6, 2, 5, 9, 8, 1, 4],
    [9, 5, 4, 7, 8, 1, 3, 6, 2],
    [1, 2, 8, 4, 6, 3, 5, 7, 9],
    [6, 1, 9, 8, 7, 5, 2, 4, 3],
    [3, 4, 7, 9, 2, 6, 1, 5, 8],
    [5, 8, 2, 1, 3, 4, 7, 9, 6],
]

# init selectedCell and solved status
selectedCell = None
solved = False

# draw black background and white grid
def drawBG():
    screen.fill(pg.Color(bgColor))
    pg.draw.rect(screen, pg.Color(fgColor), pg.Rect(15, 15, 720, 720), 10)
    i = 1
    while (i * 80) < 720:
        lineWidth = 5 if i % 3 > 0 else 10
        pg.draw.line(screen, pg.Color(fgColor), pg.Vector2((i * 80) + 15, 15), pg.Vector2((i * 80) + 15, 735), lineWidth)
        pg.draw.line(screen, pg.Color(fgColor), pg.Vector2(15, (i * 80) + 15), pg.Vector2(735, (i * 80) + 15), lineWidth)
        i += 1

# draw the numbers to fill the grid
def drawNumbers():
    row = 0
    offset = 40

    while row < 9:
        col = 0

        while col < 9:
            output = numberGrid[row][col] if numberGrid[row][col] != 0 else ' '

            nText = font.render(str(output), True, pg.Color(textColor))
            screen.blit(nText, pg.Vector2((col * 80) + offset + 5, (row * 80) + offset - 2))

            col += 1

        row += 1

# highlight whatever cell that user has clicked on
def highlightCell():
    if selectedCell:
        row, col = selectedCell
        pg.draw.rect(screen, pg.Color(highlightColor), pg.Rect(col * 80 + 15, row * 80 + 15, 80, 80), 5)

# get clicked cell's position
def getCell(pos):
    x, y = pos
    if 15 < x < 735 and 15 < y < 735:
        return ((y - 15) // 80, (x - 15) // 80)
    return None

# check move validity
def isValidMove(grid, row, col, num):
    for i in range(9):
        if grid[row][i] == num and i != col:
            return False
        if grid[i][col] == num and i != row:
            return False
    
    startRow, startCol = 3 * (row // 3), 3 * (col // 3)
    for i in range(startRow, startRow + 3):
        for j in range(startCol, startCol + 3):
            if grid[i][j] == num and (i, j) != (row, col):
                return False

    return True

# check solve status
def isSolved(grid):
    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:
                # print(f"Cell ({row}, {col} is empty)")
                return False
            if not isValidMove(grid, row, col, grid[row][col]):
                # print(f"Invalid move at cell ({row}, {col}) with value {grid[row][col]}")
                return False
    print("Puzzle solved")
    return True


# draw a congratulatory message when board is solved
def drawCongrats():
    congratsText = congratsFont.render("Congrats, you solved the board!", True, pg.Color('green'))
    congratsTextOutline = congratsFont.render("Congrats, you solved the board!", True, pg.Color('black'))  # Render text with black color for outline
    congratsRect = congratsText.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
    
    # Blit the text with outline
    screen.blit(congratsTextOutline, (congratsRect.x - 2, congratsRect.y - 2))  # Top-left
    screen.blit(congratsTextOutline, (congratsRect.x + 2, congratsRect.y + 2))  # Bottom-right
    screen.blit(congratsTextOutline, (congratsRect.x + 2, congratsRect.y - 2))  # Top-right
    screen.blit(congratsTextOutline, (congratsRect.x - 2, congratsRect.y + 2))  # Bottom-left
    
    # Blit the main text
    screen.blit(congratsText, congratsRect)

# main game loop
def gameLoop():
    global selectedCell, solved

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            elif event.type == pg.MOUSEBUTTONDOWN:
                selectedCell = getCell(event.pos)

            elif event.type == pg.KEYDOWN and selectedCell:
                row, col = selectedCell

                if event.key == pg.K_0 or event.key == pg.K_KP0:
                    numberGrid[row][col] = 0

                if pg.K_1 <= event.key <= pg.K_9:
                    num = event.key - pg.K_0

                    if isValidMove(numberGrid, row, col, num):
                        numberGrid[row][col] = num

                solved = isSolved(numberGrid)
                # print(f"Solved: {solved}")

        drawBG()
        drawNumbers()
        highlightCell()
        if solved:
            drawCongrats()
        pg.display.flip()

# calling the game loop
gameLoop()
