import pygame
from game.game_engine import GameEngine

pygame.init()

WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong - Pygame Version")

BLACK = (0, 0, 0)
clock = pygame.time.Clock()
FPS = 60

engine = GameEngine(WIDTH, HEIGHT)

def main():
    running = True
    while running:
        # Collect events once and pass to engine
        events = pygame.event.get()

        # Allow engine to process QUIT event and menu key presses (will raise SystemExit)
        engine.handle_events(events)

        # Fill background
        SCREEN.fill(BLACK)

        # Continuous input (movement)
        engine.handle_input()

        # Update game state
        engine.update()

        # Render everything
        engine.render(SCREEN)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
