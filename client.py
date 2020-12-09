import pygame
import os
import socket
import threading
from grid import Grid
from constants import *

os.environ['SDL_VIDEO_WINDOW_POS'] = '1000,100'

screen = pygame.display.set_mode((600, 700))
pygame.display.set_caption("Tic-Tac-Toe")
icon = pygame.image.load("res/tic-tac-toe-icon_32x32.png")
pygame.display.set_icon(icon)

grid = Grid()

turn = False


# Create a separate thread to send and receive data to not block the execution while waiting for a connection
def createThread(target):
    thread = threading.Thread(target=target)
    thread.daemon = True
    thread.start()


# Socket Constants
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

current_player = 'O'
game_time = "00:00"


# noinspection DuplicatedCode
def receiveData():
    global turn, current_player, game_time
    while True:
        data = sock.recv(1024).decode()
        data = data.split('-')
        x, y = int(data[0]), int(data[1])
        if data[2] == 'yourturn':
            turn = True
        if data[3] == 'False':
            grid.game_over = True
        if grid.getCellValue(x, y) == 0:
            grid.setCellValue(x, y, data[4])
        current_player = data[4]
        print(data)


createThread(receiveData)


def getCell(position):
    x = position[0] // 200
    y = (position[1] - 100) // 200
    return x, y


def main():
    pygame.init()
    game_start_time = pygame.time.get_ticks()
    clock_img = pygame.image.load("res/clock.png")
    player = 'O'
    other_player = 'X'
    running = True
    playing = 'True'
    while running:
        global turn
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and not grid.game_over:
                if turn:
                    if pygame.mouse.get_pressed(3)[0]:
                        pos = pygame.mouse.get_pos()
                        if pos[1] >= 100:
                            cell_x, cell_y = getCell(pos)
                            grid.getMouse(cell_x, cell_y, player)
                            if grid.game_over:
                                playing = 'False'
                            send_data = f'{cell_x}-{cell_y}-yourturn-{playing}-{player}'.encode()
                            sock.send(send_data)
                            turn = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and grid.game_over:
                    grid.clearGrid()
                    grid.game_over = False
                    playing = 'True'
                elif event.key == pygame.K_ESCAPE:
                    running = False

        screen.fill((0, 0, 0))
        grid.draw(screen)
        if grid.game_over:
            grid.drawWinningLine(screen)
            grid.renderResultmsg(screen)
            grid.renderMsg(screen, (470, 30), (255, 255, 255), game_time)
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

            screen.blit(clock_img, (380, 30))
            if turn:
                message = f"{player}'s turn"
                grid.renderMsg(screen, (30, 30), PLAYER_COLOR[player], message)
            else:
                message = f"{other_player}'s turn"
                grid.renderMsg(screen, (30, 30), PLAYER_COLOR[other_player], message)
        pygame.display.flip()


if __name__ == '__main__':
    main()
