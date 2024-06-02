# functions for the board
import pygame as pg

# draw black background and white grid
def drawBG(screen):
    screen.fill(pg.Color("black"))
    pg.draw.rect(screen, pg.Color("purple"), pg.Rect(15, 15, 720, 720), 10)
    i = 1
    while (i * 80) < 720:
        lineWidth = 5 if i % 3 > 0 else 10
        pg.draw.line(screen, pg.Color("purple"), pg.Vector2((i * 80) + 15, 15), pg.Vector2((i * 80) + 15, 735), lineWidth)
        pg.draw.line(screen, pg.Color("purple"), pg.Vector2(15, (i * 80) + 15), pg.Vector2(735, (i * 80) + 15), lineWidth)
        i += 1

# draw the numbers to fill the grid
def drawNumbers(screen, font, numberGrid):
    row = 0
    offset = 40

    while row < 9:
        col = 0

        while col < 9:
            output = numberGrid[row][col] if numberGrid[row][col] != 0 else ' '

            nText = font.render(str(output), True, pg.Color('white'))
            screen.blit(nText, pg.Vector2((col * 80) + offset + 5, (row * 80) + offset - 2))

            col += 1

        row += 1

# highlight whatever cell that user has clicked on
def highlightCell(screen, selectedCell):
    if selectedCell:
        row, col = selectedCell
        pg.draw.rect(screen, pg.Color("yellow"), pg.Rect(col * 80 + 15, row * 80 + 15, 80, 80), 5)

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
def drawCongrats(screen, congratsFont):
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
