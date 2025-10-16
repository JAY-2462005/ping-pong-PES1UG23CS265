import pygame
import math
from .paddle import Paddle
from .ball import Ball
from .sound_manager import SoundManager

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100

        # Sound manager
        self.sound_manager = SoundManager()

        # Entities
        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ball = Ball(width // 2, height // 2, 10, 10, width, height, self.sound_manager)

        # Scoring
        self.player_score = 0
        self.ai_score = 0
        self.font = pygame.font.SysFont("Arial", 30)
        self.large_font = pygame.font.SysFont("Arial", 60)

        # Win config
        self.best_of = 5
        self.winning_score = self._best_of_to_target(self.best_of)

        # Game state
        self.game_over = False
        self.winner = None
        self.game_over_timer = 0
        self.menu_shown = False
        self.menu_delay_ms = 2000

    def _best_of_to_target(self, best_of):
        return math.floor(best_of / 2) + 1

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.KEYDOWN and self.game_over and self.menu_shown:
                if event.key == pygame.K_3:
                    self.start_new_match(best_of=3)
                elif event.key == pygame.K_5:
                    self.start_new_match(best_of=5)
                elif event.key == pygame.K_7:
                    self.start_new_match(best_of=7)
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    raise SystemExit
                elif event.key == pygame.K_SPACE:
                    self.start_new_match(best_of=self.best_of)

    def handle_input(self):
        if self.game_over:
            return
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.move(-10, self.height)
        if keys[pygame.K_s]:
            self.player.move(10, self.height)

    def update(self):
        if self.game_over:
            now = pygame.time.get_ticks()
            if not self.menu_shown and now - self.game_over_timer >= self.menu_delay_ms:
                self.menu_shown = True
            return

        self.ball.move(self.player, self.ai)

        # Scoring logic
        if self.ball.x <= 0:
            self.ai_score += 1
            if self.sound_manager:
                self.sound_manager.play("score")
            self.ball.reset()

        elif self.ball.x + self.ball.width >= self.width:
            self.player_score += 1
            if self.sound_manager:
                self.sound_manager.play("score")
            self.ball.reset()

        # AI tracking
        self.ai.auto_track(self.ball, self.height)

        # Game end
        if self.player_score >= self.winning_score:
            self.end_game("Player Wins!")
        elif self.ai_score >= self.winning_score:
            self.end_game("AI Wins!")

    def end_game(self, winner_text):
        self.game_over = True
        self.winner = winner_text
        self.game_over_timer = pygame.time.get_ticks()
        self.menu_shown = False

    def start_new_match(self, best_of=5):
        if best_of not in (3, 5, 7):
            best_of = 5
        self.best_of = best_of
        self.winning_score = self._best_of_to_target(best_of)
        self.player_score = 0
        self.ai_score = 0
        self.player.y = self.height // 2 - self.player.height // 2
        self.ai.y = self.height // 2 - self.ai.height // 2
        self.ball.reset()
        self.game_over = False
        self.winner = None
        self.menu_shown = False
        self.game_over_timer = 0

    def render(self, screen):
        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())
        pygame.draw.ellipse(screen, WHITE, self.ball.rect())
        pygame.draw.aaline(screen, WHITE, (self.width // 2, 0), (self.width // 2, self.height))

        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width // 4, 20))
        screen.blit(ai_text, (self.width * 3 // 4, 20))

        if self.game_over:
            self.show_game_over(screen)

    def show_game_over(self, screen):
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 120))
        screen.blit(overlay, (0, 0))

        message = self.large_font.render(self.winner, True, WHITE)
        msg_rect = message.get_rect(center=(self.width // 2, self.height // 2 - 80))
        screen.blit(message, msg_rect)

        sub = self.font.render("Match ended. Showing options shortly...", True, WHITE)
        sub_rect = sub.get_rect(center=(self.width // 2, self.height // 2 - 40))
        screen.blit(sub, sub_rect)

        if self.menu_shown:
            self._render_menu(screen)

    def _render_menu(self, screen):
        lines = [
            "Play again:",
            "Press 3 → Best of 3",
            "Press 5 → Best of 5",
            "Press 7 → Best of 7",
            "Press SPACE → Replay same best-of",
            "Press ESC → Exit"
        ]
        gap = 36
        start_y = self.height // 2
        for i, text in enumerate(lines):
            font = self.font if i > 0 else self.large_font
            rendered = font.render(text, True, WHITE)
            rect = rendered.get_rect(center=(self.width // 2, start_y + i * gap))
            screen.blit(rendered, rect)
