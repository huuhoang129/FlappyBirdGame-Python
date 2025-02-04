import pygame
import sys
import random
import numpy as np
import gym
from gym import spaces

class FlappyBirdEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        super(FlappyBirdEnv, self).__init__()
        # Initialize pygame
        pygame.init()
        pygame.mixer.pre_init(frequency=44100, size=16, channels=2, buffer=512)

        # Screen setup
        self.screen_width = 432
        self.screen_height = 748
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()

        # Load assets
        self.bg = pygame.transform.scale2x(pygame.image.load('assests/img/background-night.png'))
        self.floor = pygame.transform.scale2x(pygame.image.load('assests/img/floor.png'))
        self.floor_x_pos = 0

        # Bird setup
        self.bird_down = pygame.transform.scale2x(pygame.image.load('assests/img/yellowbird-downflap.png'))
        self.bird_mid = pygame.transform.scale2x(pygame.image.load('assests/img/yellowbird-midflap.png'))
        self.bird_up = pygame.transform.scale2x(pygame.image.load('assests/img/yellowbird-upflap.png'))
        self.bird_list = [self.bird_down, self.bird_mid, self.bird_up]
        self.bird_index = 0
        self.bird = self.bird_list[self.bird_index]
        self.bird_rect = self.bird.get_rect(center=(100, 374))

        # Pipe setup
        self.pipe_surface = pygame.transform.scale2x(pygame.image.load('assests/img/pipe-green.png'))
        self.pipe_list = []
        self.pipe_height = [250, 300, 350, 400, 450, 500]

        # Game variables
        self.gravity = 0.23
        self.bird_movement = 0
        self.game_active = True
        self.score = 0
        self.high_score = 0
        self.reward = 0
        self.done = False

        # Gym spaces
        self.action_space = spaces.Discrete(2)  # 0: Do nothing, 1: Flap
        self.observation_space = spaces.Box(
            low=0, high=255, shape=(self.screen_width, self.screen_height, 3), dtype=np.uint8
        )

    def reset(self):
        self.bird_rect.center = (100, 374)
        self.bird_movement = 0
        self.pipe_list.clear()
        self.score = 0
        self.reward = 0
        self.done = False
        state = self._get_state()
        return state

    def step(self, action):
        # Handle action
        if action == 1:
            self.bird_movement = -7

        # Apply gravity
        self.bird_movement += self.gravity
        self.bird_rect.centery += self.bird_movement

        # Move pipes
        self.pipe_list = self._move_pipes(self.pipe_list)

        # Check collisions
        self.done = self._check_collision()
        if self.done:
            self.reward = -1  # Negative reward for collision
        else:
            self.reward = 0.1  # Small reward for staying alive

        # Update score if bird passes pipes
        self._update_score()

        # Get state
        state = self._get_state()
        return state, self.reward, self.done, {}

    def render(self, mode='human'):
        self.screen.blit(self.bg, (0, 0))
        self.screen.blit(self.bird, self.bird_rect)
        self._draw_pipes(self.pipe_list)
        self._draw_floor()
        pygame.display.update()
        self.clock.tick(120)

    def close(self):
        pygame.quit()

    def _get_state(self):
        # Return current bird position and pipe positions as state
        return np.array([self.bird_rect.centery, self.bird_movement])

    def _move_pipes(self, pipes):
        for pipe in pipes:
            pipe.centerx -= 4
        return [pipe for pipe in pipes if pipe.right > 0]

    def _draw_pipes(self, pipes):
        for pipe in pipes:
            if pipe.bottom >= self.screen_height:
                self.screen.blit(self.pipe_surface, pipe)
            else:
                flip_pipe = pygame.transform.flip(self.pipe_surface, False, True)
                self.screen.blit(flip_pipe, pipe)

    def _check_collision(self):
        # Boundary collision
        if self.bird_rect.top <= -75 or self.bird_rect.bottom >= 640:
            return True

        # Pipe collision
        for pipe in self.pipe_list:
            if self.bird_rect.colliderect(pipe):
                return True
        return False

    def _draw_floor(self):
        self.screen.blit(self.floor, (self.floor_x_pos, 640))
        self.screen.blit(self.floor, (self.floor_x_pos + 432, 640))
        self.floor_x_pos -= 1
        if self.floor_x_pos < -432:
            self.floor_x_pos = 0

    def _update_score(self):
        for pipe in self.pipe_list:
            if pipe.centerx == self.bird_rect.centerx:
                self.score += 1

# Example usage
if __name__ == "__main__":
    env = FlappyBirdEnv()
    obs = env.reset()
    done = False

    while not done:
        action = env.action_space.sample()  # Random action
        obs, reward, done, info = env.step(action)
        env.render()

    env.close()
