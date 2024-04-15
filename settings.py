import pygame
import math


class Settings:
    def __init__(self, board):
        self.screen = pygame.display.set_mode((board.width, board.height))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Pygame Airflow UI ")
        self.paused = True



