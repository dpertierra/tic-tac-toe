import pygame
import os
from grid import Grid

os.environ['SDL_VIDEO_WINDOW_POS'] = '400,100'

screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Tic-Tac-Toe")
icon = pygame.image.load("res/tic-tac-toe-icon_32x32.png")
pygame.display.set_icon(icon)

grid = Grid()
running = True
player = 'X'


def getCell(position):
    out = [0, 0]
    out[0] = position[0] // 200
    out[1] = position[1] // 200
    return out


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and not grid.game_over:
            if pygame.mouse.get_pressed(3)[0]:
                pos = pygame.mouse.get_pos()
                cell = getCell(pos)
                grid.getMouse(cell[0], cell[1], player)
                if grid.switch_player:
                    if player == 'X':
                        player = 'O'
                    else:
                        player = 'X'
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and grid.game_over:
                grid.clearGrid()
                grid.game_over = False
            elif event.key == pygame.K_ESCAPE:
                running = False

    screen.fill((0, 0, 0))
    grid.draw(screen)
    if grid.game_over:
        grid.drawWinningLine(screen)
        grid.renderResultmsg(screen)
    pygame.display.flip()
