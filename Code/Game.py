import pygame
from enum import Enum
import random
import numpy as np

class Direction(Enum):
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

        self.reset()

    def reset(self):
        self.direction = Direction.RIGHT

        x = self.w // 2
        y = self.h // 2
        self.snake = [(x, y),
                      (x - self.BOX_SIZE, y),
                      (x - 2 * self.BOX_SIZE, y)]

        self.head = self.snake[0]

        self.score = 0
        self.food = None
        self._place_food()

        self.frame_iteration = 0

    def _place_food(self):
        x = random.randint(0, (self.w - self.BOX_SIZE) // self.BOX_SIZE) * self.BOX_SIZE
        y = random.randint(0, (self.h - self.BOX_SIZE) // self.BOX_SIZE) * self.BOX_SIZE
        self.food = (x, y)
        if self.food in self.snake:
            self._place_food()

    def play_step(self, action):
        self.frame_iteration += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock_wise.index(self.direction)

        if np.array_equal(action, [1, 0, 0]):
            new_dir = clock_wise[idx]  # prosto
        elif np.array_equal(action, [0, 1, 0]):
            new_dir = clock_wise[(idx + 1) % 4]  # w prawo (obrót o 90 stopni)
        else:  # [0, 0, 1]
            new_dir = clock_wise[(idx - 1) % 4]  # w lewo (obrót o 90 stopni)

        self.direction = new_dir

        x, y = self.head
        if self.direction == Direction.RIGHT:
            x += self.BOX_SIZE
        elif self.direction == Direction.LEFT:
            x -= self.BOX_SIZE
        elif self.direction == Direction.DOWN:
            y += self.BOX_SIZE
        elif self.direction == Direction.UP:
            y -= self.BOX_SIZE

        self.head = (x, y)
        self.snake.insert(0, self.head)

        reward = 0
        game_over = False

        if self.is_collision() or self.frame_iteration > 100 * len(self.snake):
            game_over = True
            reward = -10
            return game_over, self.score, reward

        if self.head == self.food:
            self.score += 1
            self._place_food()
            reward = 10
        else:
            self.snake.pop()

        self._update_ui()
        self.clock.tick(self.SPEED)

        return game_over, self.score, reward

    def is_collision(self, pt=None):
        if pt is None:
            pt = self.head
        x, y = pt
        if x < 0 or x >= self.w or y < 0 or y >= self.h:
            return True
        if pt in self.snake[1:]:
            return True
        return False

    def _update_ui(self):
        white = (255, 255, 255)
        green = (0, 255, 0)
        red = (200, 0, 0)
        black = (0, 0, 0)

        self.display.fill(black)

        for pt in self.snake:
            pygame.draw.rect(self.display, green, pygame.Rect(pt[0], pt[1], self.BOX_SIZE, self.BOX_SIZE))

        pygame.draw.rect(self.display, red, pygame.Rect(self.food[0], self.food[1], self.BOX_SIZE, self.BOX_SIZE))

        font = pygame.font.SysFont('arial', 25)
        text = font.render("Score: " + str(self.score), True, white)
        self.display.blit(text, [10, 10])
        pygame.display.flip()



