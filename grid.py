import os
import pygame
from pygame.locals import *
from constants import *

pygame.font.init()
x_img = pygame.image.load("res/X.png")
o_img = pygame.image.load("res/O.png")
clock_img = pygame.image.load("res/clock.png")


class Grid:
    def __init__(self):
        self.grid_lines = [((0, 300), (600, 300)),  # First Horizontal Line
                           ((0, 500), (600, 500)),  # Second Horizontal Line
                           ((200, 100), (200, 700)),  # First Vertical Line
                           ((400, 100), (400, 700))  # Second Vertical Line
                           ]
        self.switch_player = True  # Used for local 1v1
        self.grid = [[0 for _ in range(3)] for _ in range(3)]
        self.game_over = False
        self.winning_line = None
        self.result = None
        self.font = pygame.font.Font(os.path.join("res", "font", "font.otf"), 50)

    def getCellValue(self, x, y):
        return self.grid[y][x]

    def setCellValue(self, x, y, value):
        self.grid[y][x] = value
        if self.isWinner(value):
            print(value, 'Won!\nPress the SpaceBar to play again')
            self.game_over = True
            self.result = f'{value} won!\nPress the SpaceBar\nto play again'
        elif self.isGridFull():
            print("It's a tie!\nPress the SpaceBar to play again")
            self.game_over = True
            self.result = "It's a tie!\nPress the SpaceBar\nto play again"

    def getMouse(self, x, y, player):
        if self.getCellValue(x, y) == 0:
            self.setCellValue(x, y, player)
            if self.isWinner(player):
                print(player, 'Won!\nPress the SpaceBar to play again')
                self.game_over = True
                self.result = f'{player} won!\nPress the SpaceBar\nto play again'
            elif self.isGridFull():
                print("It's a tie!\nPress the SpaceBar to play again")
                self.game_over = True
                self.result = "It's a tie!\nPress the SpaceBar\nto play again"
        else:
            self.switch_player = False

    def draw(self, screen):
        for line in self.grid_lines:
            pygame.draw.line(screen, (200, 200, 200), line[0], line[1], 2)
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if self.getCellValue(x, y) == 'X':
                    screen.blit(x_img, (x * 200 + 13, y * 200 + 113))
                elif self.getCellValue(x, y) == 'O':
                    screen.blit(o_img, (x * 200 + 13, y * 200 + 113))

    def drawWinningLine(self, screen):
        if self.winning_line is not None:
            pygame.draw.line(screen, (50, 205, 50), self.winning_line[0], self.winning_line[1], 10)

    def isWinner(self, player):
        if self.grid[0][0] == player and self.grid[1][0] == player and self.grid[2][0] == player:
            self.getWinningPosition(0)  # Vertical 1
            return True
        elif self.grid[0][1] == player and self.grid[1][1] == player and self.grid[2][1] == player:
            self.getWinningPosition(1)  # Vertical 2
            return True
        elif self.grid[0][2] == player and self.grid[1][2] == player and self.grid[2][2] == player:
            self.getWinningPosition(2)  # Vertical 3
            return True
        elif self.grid[0][0] == player and self.grid[0][1] == player and self.grid[0][2] == player:
            self.getWinningPosition(3)  # Horizontal Superior
            return True
        elif self.grid[1][0] == player and self.grid[1][1] == player and self.grid[1][2] == player:
            self.getWinningPosition(4)  # Horizontal central
            return True
        elif self.grid[2][0] == player and self.grid[2][1] == player and self.grid[2][2] == player:
            self.getWinningPosition(5)  # Horizontal inferior
            return True
        elif self.grid[0][0] == player and self.grid[1][1] == player and self.grid[2][2] == player:
            self.getWinningPosition(6)  # Diagonal principal
            return True
        elif self.grid[2][0] == player and self.grid[1][1] == player and self.grid[0][2] == player:
            self.getWinningPosition(7)  # Diagonal Secundaria
            return True
        else:
            return False

    def isGridFull(self):
        for row in self.grid:
            for value in row:
                if value == 0:
                    return False
        return True

    def clearGrid(self):
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                self.setCellValue(x, y, 0)

    def printGrid(self):
        for row in self.grid:
            print(row)

    def getWinningPosition(self, line):
        if line == 0:  # Vertical 1
            self.winning_line = [(100, 100), (100, 700)]
        elif line == 1:  # Vertical 2
            self.winning_line = [(300, 100), (300, 700)]
        elif line == 2:  # Vertical 3
            self.winning_line = [(500, 100), (500, 700)]
        elif line == 3:  # Horizontal 1
            self.winning_line = [(0, 200), (600, 200)]
        elif line == 4:  # Horizontal 2
            self.winning_line = [(0, 400), (600, 400)]
        elif line == 5:  # Horizontal 3
            self.winning_line = [(0, 600), (600, 600)]
        elif line == 6:  # Diagonal Principal
            self.winning_line = [(0, 100), (600, 700)]
        elif line == 7:  # Diagonal secundaria
            self.winning_line = [(600, 100), (0, 700)]

    def renderResultmsg(self, screen):
        texts = self.result.split('\n')
        if 'won' in texts[0]:
            self.renderMsg(screen, (240, 300), WHITE, texts[0])
        else:
            self.renderMsg(screen, (230, 300), WHITE, texts[0])
        self.renderMsg(screen, (110, 350), WHITE, texts[1])
        self.renderMsg(screen, (165, 400), WHITE, texts[2])

    def renderMsg(self, screen, position, color, text):
        text_surface = self.font.render(text, False, color)
        screen.blit(text_surface, position)
