import pygame
import os
import socket
import threading
from grid import Grid

os.environ['SDL_VIDEO_WINDOW_POS'] = '400,100'

surface = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Tic-Tac-Toe")


# Create a separate thread to send and receive data to not block the execution while waiting for a connection
def createThread(target):
    thread = threading.Thread(target=target)
    thread.daemon = True
    thread.start()


# Socket Constants
HOST = '127.0.0.1'
PORT = 65432

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))


def receiveData():
    while True:
        data = sock.recv(1024).decode()
        print(data)


createThread(receiveData)

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

    surface.fill((0, 0, 0))
    grid.draw(surface)
    if grid.game_over:
        grid.drawWinningLine(surface)
    pygame.display.flip()
