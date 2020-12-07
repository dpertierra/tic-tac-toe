import pygame

x_img = pygame.image.load("res/X.png")
o_img = pygame.image.load("res/O.png")


class Grid:
    def __init__(self):
        self.grid_lines = [((0, 200), (600, 200)),  # First Horizontal Line
                           ((0, 400), (600, 400)),  # Second Horizontal Line
                           ((200, 0), (200, 600)),  # First Vertical Line
                           ((400, 0), (400, 600))  # Second Vertical Line
                           ]
        self.switch_player = True
        # Search Directions    N        NW        W        SW       S       SE      E       NE
        self.search_dirs = [(0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1)]
        self.grid = [[0 for _ in range(3)] for _ in range(3)]
        self.game_over = False
        self.winning_line = None
        self.surface = None

    def getCellValue(self, x, y):
        return self.grid[y][x]

    def setCellValue(self, x, y, value):
        self.grid[y][x] = value

    def getMouse(self, x, y, player):
        if self.getCellValue(x, y) == 0:
            print(y, x)
            self.switch_player = True
            if player == 'X':
                self.setCellValue(x, y, 'X')
            elif player == 'O':
                self.setCellValue(x, y, 'O')
            if self.isWinner(player):
                print(player, 'Won!\nPress the SpaceBar to play again')
                self.game_over = True
            elif self.isGridFull():
                print("It's a tie!\nPress the SpaceBar to play again")
                self.game_over = True
        else:
            self.switch_player = False

    def draw(self, surface):
        for line in self.grid_lines:
            pygame.draw.line(surface, (200, 200, 200), line[0], line[1], 2)
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if self.getCellValue(x, y) == 'X':
                    surface.blit(x_img, (x * 200 + 13, y * 200 + 13))
                elif self.getCellValue(x, y) == 'O':
                    surface.blit(o_img, (x * 200 + 13, y * 200 + 13))
        self.surface = surface

    def drawWinningLine(self, surface):
        if self.winning_line is not None:
            pygame.draw.line(surface, (50, 205, 50), self.winning_line[0], self.winning_line[1], 10)

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
        out = [(0, 0), (0, 0)]
        if line == 0:
            out = [(100, 0), (100, 600)]
        elif line == 1:
            out = [(300, 0), (300, 600)]
        elif line == 2:
            out = [(500, 0), (500, 600)]
        elif line == 3:
            out = [(0, 100), (600, 100)]
        elif line == 4:
            out = [(0, 300), (600, 300)]
        elif line == 5:
            out = [(0, 500), (600, 500)]
        elif line == 6:
            out = [(0, 0), (600, 600)]
        elif line == 7:
            out = [(600, 0), (0, 600)]
        self.winning_line = out
