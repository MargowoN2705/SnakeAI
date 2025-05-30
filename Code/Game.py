import pygame
from enum import Enum  # <-- poprawione

class Direction(Enum):  # <-- przykład użycia
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

class SnakeGameAI:

    def __init__(self, h=480, w=640):
        pygame.init()
        self.h = h
        self.w = w

        self.BOX_SIZE = 20
        self.SPEED = 20

        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake AI')
        self.clock = pygame.time.Clock()

        self.direction = Direction.RIGHT  # Domyślny kierunek

        # Początkowa pozycja głowy węża
        x = self.w // 2
        y = self.h // 2
        self.snake = [(x, y),
                      (x - self.BOX_SIZE, y),
                      (x - 2 * self.BOX_SIZE, y)]

        self.head = self.snake[0]

        self.score = 0
        self.food = None
        self._place_food()

    def _place_food(self):
        import random
        x = random.randint(0, (self.w - self.BOX_SIZE) // self.BOX_SIZE) * self.BOX_SIZE
        y = random.randint(0, (self.h - self.BOX_SIZE) // self.BOX_SIZE) * self.BOX_SIZE
        self.food = (x, y)
        if self.food in self.snake:
            self._place_food()

