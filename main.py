from core.config import *

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption(NAME)
clock = pygame.time.Clock()

icon = pygame.image.load(IMG_ROLE_HAPPY_PATH)
pygame.display.set_icon(icon)

pygame.mixer.music.load(MUSIC_BGM_PATH)
pygame.mixer.music.play(-1)

manager = StateManager(STATE_LIST)
manager.set_state("home")

while manager.running:
    dt = clock.tick(FPS) / 1000
    events = pygame.event.get()

    manager.handle_events(events)
    manager.update(dt)
    manager.draw(screen)
    pygame.display.flip()

pygame.quit()
