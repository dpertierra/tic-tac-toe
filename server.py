import pygame
import socket
import os
import threading
from grid import Grid

os.environ['SDL_VIDEO_WINDOW_POS'] = '400,100'

surface = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Tic-Tac-Toe")

# Socket Constants
HOST = '127.0.0.1'
PORT = 65432
connection_established = False
conn, addr = None, None

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen(2)


# Create a separate thread to send and receive data to not block the execution while waiting for a connection
def createThread(target):
    thread = threading.Thread(target=target)
    thread.daemon = True
    thread.start()


def waitingForConnection():
    global connection_established, conn, addr
    conn, addr = sock.accept()  # waiting for connection, it will stop the process until it gets a connection
    print('Client is connected')
    connection_established = True
    receiveData()


def receiveData():
    pass


createThread(waitingForConnection)

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
        if event.type == pygame.MOUSEBUTTONDOWN and connection_established and not grid.game_over:
            if pygame.mouse.get_pressed(3)[0]:
                pos = pygame.mouse.get_pos()
                cellX, cellY = getCell(pos)
                grid.getMouse(cellX, cellY, player)
                send_data = f'{cellX}-{cellY}'.encode()
                conn.send(send_data)
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
