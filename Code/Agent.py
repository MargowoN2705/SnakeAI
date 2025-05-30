import torch
import random
import numpy as np
from collections import deque
from Game import SnakeGameAI, Direction
from Model import Q_Net,Q_Trainer
import matplotlib.pyplot as plt
from IPython import display


class Agent:

    def __init__(self):
        self.MAX_MEMORY = 100_000
        self.LR = 0.001
        self.BATCH_SIZE = 1000

        self.number_of_games = 0
        self.epsilon = 0
        self.gamma = 0.9  # discount rate
        self.memory = deque(maxlen=self.MAX_MEMORY)
        self.model = Q_Net(11,256,3)

        self.trainer = Q_Trainer(self.model,lr=self.LR,gamma=self.gamma)

    def get_state(self, game):
        head = game.snake[0]
        x, y = head

        point_l = (x - game.BOX_SIZE, y)
        point_r = (x + game.BOX_SIZE, y)
        point_u = (x, y - game.BOX_SIZE)
        point_d = (x, y + game.BOX_SIZE)

        dir_l = game.direction == Direction.LEFT
        dir_r = game.direction == Direction.RIGHT
        dir_u = game.direction == Direction.UP
        dir_d = game.direction == Direction.DOWN

        state = [
            # Danger straight
            (dir_r and game.is_collision(point_r)) or
            (dir_l and game.is_collision(point_l)) or
            (dir_u and game.is_collision(point_u)) or
            (dir_d and game.is_collision(point_d)),

            # Danger right
            (dir_u and game.is_collision(point_r)) or
            (dir_d and game.is_collision(point_l)) or
            (dir_l and game.is_collision(point_u)) or
            (dir_r and game.is_collision(point_d)),

            # Danger left
            (dir_d and game.is_collision(point_r)) or
            (dir_u and game.is_collision(point_l)) or
            (dir_r and game.is_collision(point_u)) or
            (dir_l and game.is_collision(point_d)),

            # Move direction
            dir_l,
            dir_r,
            dir_u,
            dir_d,

            # Food location
            game.food[0] < x,  # food is left
            game.food[0] > x,  # food is right
            game.food[1] < y,  # food is up
            game.food[1] > y   # food is down
        ]

        return np.array(state, dtype=int)

    def remember(self, state, action, reward, next_state, game_over):
        self.memory.append((state, action, reward, next_state, game_over))

    def train_long_memory(self):
        if len(self.memory) > self.BATCH_SIZE:
            mini_sample = random.sample(self.memory, self.BATCH_SIZE)
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, game_overs = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, game_overs)

    def train_short_memory(self, state, action, reward, next_state, game_over):
        self.trainer.train_step(state, action, reward, next_state, game_over)

    def get_action(self, state):
        self.epsilon = 90 - self.number_of_games
        final_move = [0, 0, 0]
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 2)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1

        return final_move


def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record_score = 0
    agent = Agent()
    game = SnakeGameAI()

    while True:
        state_old = agent.get_state(game)
        final_move = agent.get_action(state_old)
        game_over, score, reward = game.play_step(final_move)
        state_new = agent.get_state(game)

        agent.train_short_memory(state_old, final_move, reward, state_new, game_over)
        agent.remember(state_old, final_move, reward, state_new, game_over)

        if game_over:
            game.reset()
            agent.number_of_games += 1
            agent.train_long_memory()

            if score > record_score:
                record_score = score
                agent.model.save()

            print(f'Game: {agent.number_of_games}, Score: {score}, Record: {record_score}')
            plot()
