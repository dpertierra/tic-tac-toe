import pygame
import os
import socket
import threading
from grid import Grid

os.environ['SDL_VIDEO_WINDOW_POS'] = '400,100'

screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Tic-Tac-Toe Server")

grid = Grid()
turn = True

# Socket Constants
HOST = '127.0.0.1'
PORT = 65432
connection_established = False
conn, addr = None, None

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((HOST, PORT))
sock.listen(1)


# Create a separate thread to send and receive data to not block the execution while waiting for a connection
def createThread(target):
    thread = threading.Thread(target=target)
    thread.daemon = True
    thread.start()


def receiveData():
    global turn
    while True:
        data = conn.recv(1024).decode()
        data = data.split('-')
        x, y = int(data[0]), int(data[1])
        if data[2] == 'yourturn':
            turn = True
        if data[3] == 'False':
            grid.game_over = True
        if grid.getCellValue(x, y) == 0:
            grid.setCellValue(x, y, data[4])
        print(data)


def waitingForConnection():
    global connection_established, conn, addr
    conn, addr = sock.accept()  # waiting for connection, it will stop the process until it gets a connection
    print('Client is connected')
    connection_established = True
    receiveData()


createThread(waitingForConnection)


def getCell(position):
    x = position[0] // 200
    y = position[1] // 200
    return x, y


def main():
    global turn
    player = 'X'
    playing = 'True'
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and connection_established:
                if turn:  # and not grid.game_over:
                    if pygame.mouse.get_pressed(3)[0]:
                        pos = pygame.mouse.get_pos()
                        cell_x, cell_y = getCell(pos)
                        grid.getMouse(cell_x, cell_y, player)
                        if grid.game_over:
                            playing = 'False'
                        send_data = f'{cell_x}-{cell_y}-yourturn-{playing}-{player}'.encode()
                        conn.send(send_data)
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
        pygame.display.flip()


if __name__ == '__main__':
    main()
