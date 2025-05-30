import pygame
from enum import Enum
import random

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

    def _place_food(self):

        x = random.randint(0, (self.w - self.BOX_SIZE) // self.BOX_SIZE) * self.BOX_SIZE
        y = random.randint(0, (self.h - self.BOX_SIZE) // self.BOX_SIZE) * self.BOX_SIZE
        self.food = (x, y)
        if self.food in self.snake:
            self._place_food()

    def play_step(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and self.direction != Direction.RIGHT:
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT and self.direction != Direction.LEFT:
                    self.direction = Direction.RIGHT
                elif event.key == pygame.K_UP and self.direction != Direction.DOWN:
                    self.direction = Direction.UP
                elif event.key == pygame.K_DOWN and self.direction != Direction.UP:
                    self.direction = Direction.DOWN

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


        if self.head == self.food:
            self.score += 1
            self._place_food()
        else:
            self.snake.pop()  # Usuń ogon, jeśli nie zjadł


        if (x < 0 or x >= self.w or y < 0 or y >= self.h or self.head in self.snake[1:]):
            return True


        self._update_ui()
        self.clock.tick(self.SPEED)
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


