import random
import pygame


class Cell:
    def __init__(self, alive, x, y):
        self.alive = bool(alive)
        self.y = int(y)
        self.x = int(x)
        self.neighbor = None

    def get_alive_neighbor(self, board):
        neighbor = []
        (x, y) = (self.x, self.y)
        for alive_cell in board.alive_cells:
            if alive_cell in [
                (x, y + 1),
                (x, y - 1),
                (x + 1, y),
                (x - 1, y),
                (x + 1, y + 1),
                (x + 1, y - 1),
                (x - 1, y + 1),
                (x - 1, y - 1),
            ]:
                neighbor.append(1)
        self.neighbor = neighbor
        return neighbor

    def set_status(self, board):
        neighbors = self.get_alive_neighbor(board)
        sum_neighbor = sum(neighbors)
        if self.alive:
            if sum_neighbor < 2 or sum_neighbor > 3:
                self.alive = False
            else:
                pass
        if not self.alive:
            if sum_neighbor == 3:
                self.alive = True
        return self


class Board:
    def __init__(self, width, height, block_size, range_threshold=20):
        self.width = int(width)
        self.height = int(height)
        self.block_size = block_size
        self.alive_cells = []
        # self.alive_cells = self.generate_random_tuples()
        self.alive_color = (0, 100, 0)
        self.dead_color = (0, 0, 0)
        self.range_threshold = range_threshold

    def generate_random_tuples(self):
        """
        Randomly populates the board
        """
        screen_height = self.height / self.block_size
        screen_width = self.width / self.block_size
        alive_cells = round(screen_width * screen_height * 0.4)
        random_tuples = [
            (
                random.randint(0, round(screen_width)),
                random.randint(0, round(screen_height)),
            )
            for _ in range(alive_cells)
        ]
        return random_tuples

    def get_peripheral_dead_cells(self):
        """
        Takes the alive_cells list and returns a set of peripheral
        dead cells.
        """
        peripheral_dead_cells = set()
        for alive_cell in self.alive_cells:
            (x, y) = (alive_cell[0], alive_cell[1])
            if (x, y + 1) not in self.alive_cells:
                peripheral_dead_cells.add((x, y + 1))
            if (x, y - 1) not in self.alive_cells:
                peripheral_dead_cells.add((x, y - 1))
            if (x + 1, y) not in self.alive_cells:
                peripheral_dead_cells.add((x + 1, y))
            if (x - 1, y) not in self.alive_cells:
                peripheral_dead_cells.add((x - 1, y))
            if (x + 1, y + 1) not in self.alive_cells:
                peripheral_dead_cells.add((x + 1, y + 1))
            if (x + 1, y - 1) not in self.alive_cells:
                peripheral_dead_cells.add((x + 1, y - 1))
            if (x - 1, y + 1) not in self.alive_cells:
                peripheral_dead_cells.add((x - 1, y + 1))
            if (x - 1, y - 1) not in self.alive_cells:
                peripheral_dead_cells.add((x - 1, y - 1))
        return peripheral_dead_cells

    def rise_from_death(self):
        """
        Takes the peripheral dead cells and updates it
        based on its life status.
        """
        peripheral_dead_cells = self.get_peripheral_dead_cells()
        updated_peripheral_dead_cells = set()
        for dead_cell in peripheral_dead_cells:
            cell = Cell(0, dead_cell[0], dead_cell[1])
            cell.set_status(board=self)
            updated_peripheral_dead_cells.add(cell)
        return updated_peripheral_dead_cells

    def within_range(self, cell):
        """
            Locate out of range cells
            within a certain threshold
            -> Take a moment to think about this "[x,y]_boundaries - 1"
        """
        x_boundaries = round(self.width / self.block_size + self.range_threshold)
        y_boundaries = round(self.height / self.block_size + self.range_threshold)
        print(x_boundaries, y_boundaries)
        if 0 <= cell.x <= x_boundaries - 1 and 0 <= cell.y <= y_boundaries - 1:
            return True
        else:
            return False

    def next_turn_dead_cells(self):
        """
        Generates the resurrected cells' coordinates based on
        the updated peripheral dead cells which may contain
        alive cells
        """
        updated_peripheral_dead_cells = self.rise_from_death()
        resurrected_cells = []
        for updated_peripheral_dead_cell in updated_peripheral_dead_cells:
            if updated_peripheral_dead_cell.alive and self.within_range(cell=updated_peripheral_dead_cell):
                resurrected_cells.append(
                    (updated_peripheral_dead_cell.x, updated_peripheral_dead_cell.y)
                )
        return resurrected_cells

    def next_turn_alive_cells(self):
        """
        Generate the surviving cells list based on
        the board current alive cells which may contain
        dead cells
        """
        alive_cell_copy = list(self.alive_cells)
        survived_cells = []
        for alive_cell_coordinate in alive_cell_copy:
            # update status of alive cells
            alive_cell = Cell(1, alive_cell_coordinate[0], alive_cell_coordinate[1])
            updated_cell = alive_cell.set_status(board=self)
            if updated_cell.alive and self.within_range(cell=updated_cell):
                survived_cells.append((updated_cell.x, updated_cell.y))
        return survived_cells

    def next_turn(self):
        """
        update the value of the board's alive_cells
        """
        # self.print_out_of_range_cells()
        resurrected_cells = self.next_turn_dead_cells()
        survived_cells = self.next_turn_alive_cells()
        self.alive_cells = survived_cells + resurrected_cells

    def print_out_of_range_cells(self):
        """
        For tests purposes
        """
        for alive_cell in self.alive_cells:
            cell = Cell(1, alive_cell[0], alive_cell[1])
            print((cell.x, cell.y), self.within_range(cell))
        print("---")

    def draw_board(self, screen):
        block_size = self.block_size
        for x in range(0, self.width, block_size):
            for y in range(0, self.height, block_size):
                rect = pygame.Rect(x, y, block_size, block_size)
                pygame.draw.rect(screen, (200, 200, 200), rect, 1)
                surface = pygame.Surface((block_size - 1, block_size - 1))
                if (x / block_size, y / block_size) in self.alive_cells:
                    surface.fill(self.alive_color)
                else:
                    surface.fill(self.dead_color)
                screen.blit(surface, rect)


# block_size = 20
# width = 30
# height = 20
# board = Board(block_size * width, block_size * height, block_size, range_threshold=0)
# cell = Cell(1, -1, -1)
# print(board.within_range(cell))
# print(board.range_threshold)


