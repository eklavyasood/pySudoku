import sys
import pygame as pg
import functions
import boards

numberGrid = boards.numberGrid

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

# init selectedCell and solved status
selectedCell = None
solved = False

# main game loop
def gameLoop():
    global selectedCell, solved

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            elif event.type == pg.MOUSEBUTTONDOWN:
                selectedCell = functions.getCell(event.pos)

            elif event.type == pg.KEYDOWN and selectedCell:
                row, col = selectedCell

                if event.key == pg.K_0 or event.key == pg.K_KP0:
                    numberGrid[row][col] = 0

                if pg.K_1 <= event.key <= pg.K_9:
                    num = event.key - pg.K_0

                    if functions.isValidMove(numberGrid, row, col, num):
                        numberGrid[row][col] = num

                solved = functions.isSolved(numberGrid)
                # print(f"Solved: {solved}")

        functions.drawBG(screen)
        functions.drawNumbers(screen, font, numberGrid)
        functions.highlightCell(screen, selectedCell)
        if solved:
            functions.drawCongrats(screen, congratsFont)
        pg.display.flip()

# calling the game loop
gameLoop()
