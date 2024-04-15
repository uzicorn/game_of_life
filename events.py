import pygame
import math

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
                    if (x, y) in alive_cells_copy:
                        alive_cells_copy.remove((x, y))
                    else:
                        alive_cells_copy.append((x, y))
            elif event.type == pygame.KEYDOWN:
                # Pause the game
                if event.key == pygame.K_SPACE:
                    settings.paused = not settings.paused
                # Clear all cells
                if event.key == pygame.K_BACKSPACE:
                    self.board.alive_cells.clear()
                # Print the board as a list
                if event.key == pygame.K_p:
                    print(self.board.alive_cells)
                # Reset the board to a specific initialisation
                if event.key == pygame.K_r:
                    # self.board.alive_cells = self.board.generate_random_tuples()
                    self.board.alive_cells = [(0, 2), (1, 2), (2, 2), (2, 1), (1, 0), (1, 10), (2, 10), (3, 10), (3, 11), (2, 12)]
