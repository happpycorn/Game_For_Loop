from core.constants import *
from core.ui_components import Button

class InfoScene:
    def __init__(self, manager):
        self.manager = manager
        self.default_font = pygame.font.SysFont(None, DEFAULT_FONT_SIZE)

        self.buttons = {
            "exit": Button(CLOSE_BUTTON_PATH, (740, 20), 40, 40)
        }

        self.info_img = pygame.image.load(IMG_INFO_PATH).convert_alpha()

    def enter(self, data):
        print("Entered Info Scene")

    def update(self, dt):
        pass

    def draw(self, screen):
        screen.fill(COLOR_BACK_GROUND)
        screen.blit(self.info_img, (50, 50))
        for btn in self.buttons.values(): btn.draw(screen)

    def handle_events(self, events):
        for event in events:
            if self.buttons["exit"].is_clicked(event):
                self.manager.set_state("home")
