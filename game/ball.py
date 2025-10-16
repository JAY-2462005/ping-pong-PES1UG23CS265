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

            # --- Wall collisions (top & bottom) ---
            if self.y <= 0:
                self.y = 0
                self.velocity_y *= -1
                if self.sound_manager:
                    self.sound_manager.play("wall_bounce")

            elif self.y + self.height >= self.screen_height:
                self.y = self.screen_height - self.height
                self.velocity_y *= -1
                if self.sound_manager:
                    self.sound_manager.play("wall_bounce")

            # --- Paddle collisions (player left, ai right) ---
            ball_rect = self.rect()
            player_rect = player.rect()
            ai_rect = ai.rect()

            # Player paddle
            if ball_rect.colliderect(player_rect):
                self.x = player.x + player.width  # move ball outside paddle
                self.velocity_x = abs(self.velocity_x)

                # adjust vertical direction based on hit location
                offset = (self.y + self.height / 2) - (player.y + player.height / 2)
                self.velocity_y += offset * 0.15
                self._clamp_velocity()

                if self.sound_manager:
                    self.sound_manager.play("paddle_hit")

            # AI paddle
            elif ball_rect.colliderect(ai_rect):
                self.x = ai.x - self.width
                self.velocity_x = -abs(self.velocity_x)

                # adjust vertical direction based on hit location
                offset = (self.y + self.height / 2) - (ai.y + ai.height / 2)
                self.velocity_y += offset * 0.15
                self._clamp_velocity()

                if self.sound_manager:
                    self.sound_manager.play("paddle_hit")

            # --- Small position correction ---
            # Push the ball slightly away from walls to prevent "sticking"
            if self.y <= 0:
                self.y = 0.5
            elif self.y + self.height >= self.screen_height:
                self.y = self.screen_height - self.height - 0.5

    def _clamp_velocity(self):
        """Keep ball speed within reasonable bounds."""
        max_speed = 10
        if self.velocity_y > max_speed:
            self.velocity_y = max_speed
        elif self.velocity_y < -max_speed:
            self.velocity_y = -max_speed

    def reset(self):
        """Reset to center with randomized direction."""
        self.x = self.original_x
        self.y = self.original_y
        self.velocity_x = random.choice([-8, 8])
        self.velocity_y = random.choice([-6, 6])
