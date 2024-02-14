import pygame
import math


class Settings:
    def __init__(self, board):
        self.screen = pygame.display.set_mode((board.width, board.height))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Pygame Airflow UI ")
        self.paused = True


class Events:
    def __init__(self, board):
        self.board = board
        self.running = True

    def event_handler(self, settings):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # get mouse coordinates withing block
                    mouse_position = pygame.mouse.get_pos()
                    x, y = (
                        math.floor(mouse_position[0] / self.board.block_size),
                        math.floor(mouse_position[1] / self.board.block_size),
                    )
                    alive_cells_copy = self.board.alive_cells
                    if (x, y) == (0, 0):
                        self.board.alive_cells.clear()
                        settings.paused = not settings.paused
                    elif (x, y) in alive_cells_copy:
                        alive_cells_copy.remove((x, y))
                    else:
                        alive_cells_copy.append((x, y))
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    settings.paused = not settings.paused
