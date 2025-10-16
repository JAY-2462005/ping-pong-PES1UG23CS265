import pygame
import random

class Ball:
    def __init__(self, x, y, width, height, screen_width, screen_height, sound_manager=None):
        self.original_x = x
        self.original_y = y
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.velocity_x = random.choice([-8, 8])
        self.velocity_y = random.choice([-6, 6])
        self.sound_manager = sound_manager

    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)

    def move(self, player, ai):
        steps = max(abs(self.velocity_x), abs(self.velocity_y))
        if steps == 0:
            steps = 1
        step_x = self.velocity_x / steps
        step_y = self.velocity_y / steps

        for _ in range(int(steps)):
            self.x += step_x
            self.y += step_y

            # --- Wall collisions ---
            if self.y <= 0:
                self.y = 0
                self.velocity_y *= -1
                self.y += self.velocity_y * 0.1  # small offset to escape wall
                if self.sound_manager:
                    self.sound_manager.play("wall_bounce")

            elif self.y + self.height >= self.screen_height:
                self.y = self.screen_height - self.height
                self.velocity_y *= -1
                self.y += self.velocity_y * 0.1  # small offset to escape wall
                if self.sound_manager:
                    self.sound_manager.play("wall_bounce")

            # --- Paddle collisions ---
            ball_rect = self.rect()
            if ball_rect.colliderect(player.rect()):
                self.x = player.x + player.width
                self.velocity_x = abs(self.velocity_x)
                if self.sound_manager:
                    self.sound_manager.play("paddle_hit")

            elif ball_rect.colliderect(ai.rect()):
                self.x = ai.x - self.width
                self.velocity_x = -abs(self.velocity_x)
                if self.sound_manager:
                    self.sound_manager.play("paddle_hit")

    def reset(self):
        """Reset to center with randomized direction."""
        self.x = self.original_x
        self.y = self.original_y
        self.velocity_x = random.choice([-8, 8])
        self.velocity_y = random.choice([-6, 6])
