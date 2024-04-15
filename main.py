import pygame
import sys
from models import Board
from settings import Settings
from events import Events


def main(width, height, block_size):
    # Board
    board = Board(block_size * width, block_size * height, block_size, range_threshold=10)
    # Settings
    settings = Settings(board)
    # Events
    events = Events(board=board)
    # ----------- Game loop -----------
    # running = True
    while events.running:
        # Event handling
        events.event_handler(settings)
        if settings.paused:  # game paused
            board.draw_board(screen=settings.screen)
            pygame.display.update()
        else:  # game runs
            board.draw_board(screen=settings.screen)
            # ---
            board.next_turn()
            # ---
            pygame.display.update()
            settings.clock.tick(10)
    # -----------
    # Quit Pygame
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main(20, 15, 40)

