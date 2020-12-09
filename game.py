import pygame
import os
from grid import Grid

os.environ['SDL_VIDEO_WINDOW_POS'] = '400,100'

screen = pygame.display.set_mode((600, 700))
pygame.display.set_caption("Tic-Tac-Toe")
icon = pygame.image.load("res/tic-tac-toe-icon_32x32.png")
pygame.display.set_icon(icon)

grid = Grid()
running = True
player = 'X'
pygame.init()
game_start_time = pygame.time.get_ticks()
game_time = "00:00"


def getCell(position):
    print(position)
    out = [0, 0]
    out[0] = position[0] // 200
    print(position[1] - 100)
    out[1] = (position[1] - 100) // 200
    print(out)
    return out


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and not grid.game_over:
            if pygame.mouse.get_pressed(3)[0]:
                pos = pygame.mouse.get_pos()
                if pos[1] >= 100:
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
                pygame.init()
                game_start_time = pygame.time.get_ticks()
            elif event.key == pygame.K_ESCAPE:
                running = False

    screen.fill((0, 0, 0))
    grid.draw(screen)
    if grid.game_over:
        grid.drawWinningLine(screen)
        grid.renderResultmsg(screen)
        grid.renderMsg(screen, (470, 30), (255, 255, 255), game_time)
        clock_img = pygame.image.load("res/clock.png")
        screen.blit(clock_img, (380, 30))
    else:
        seconds = (pygame.time.get_ticks() - game_start_time) // 1000
        minutes = 0
        if seconds > 60:
            minutes = seconds // 60
            seconds = seconds % 60
        elif seconds < 10:
            seconds = '0' + str(seconds)
        if minutes < 10:
            minutes = '0' + str(minutes)
        elapsed_time = f"{minutes}:{seconds}"
        game_time = elapsed_time
        grid.renderMsg(screen, (470, 30), (255, 255, 255), game_time)

        message = f"{player}'s turn"
        if player == 'X':
            grid.renderMsg(screen, (30, 30), (255, 0, 0), message)
        else:
            grid.renderMsg(screen, (30, 30), (0, 113, 188), message)
    pygame.display.flip()
