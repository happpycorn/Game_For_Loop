from core.constants import *
from core.ui_components import Button
from core.ui_components import Pause
from core.ui_components import Text
from core.game_state import StateManager

class HomeScene:
    def __init__(self, manager: StateManager):
        self.manager = manager

        self.buttons = {
            "pause": Button(PAUSE_BUTTON_PATH, (20, 20), 40, 40),
            "info": Button(INFO_BUTTON_PATH, (80, 20), 40, 40),
            "start": Button(START_BUTTON_PATH, (340, 450), 120, 40),
            "left": Button(LEFT_BUTTON_PATH, (200, 380), 40, 40),
            "right": Button(RIGHT_BUTTON_PATH, (560, 380), 40, 40),
        }

        self.texts = {
            "stage_count": Text("--", (400, 320)),
            "stage_name": Text("--", (400, 400))
        }

        self.pause = Pause(manager, self)

        self.title = pygame.image.load(IMG_TITLE_PATH).convert_alpha()

    def enter(self, data):
        print("Entered Home Scene")
        self.is_pause = False

    def update(self, dt):
        self.texts["stage_count"].text = f"Stage {str(self.manager.map_manager.current_map["num"])}"
        self.texts["stage_name"].text = str(self.manager.map_manager.current_map["name"])

    def draw(self, screen):
        screen.fill(COLOR_BACK_GROUND)

        screen.blit(self.title, (100, 0))

        for btn in self.buttons.values(): btn.draw(screen)
        for txt in self.texts.values(): txt.draw(screen)
        if self.is_pause: self.pause.draw(screen)


    def handle_events(self, events):
        if self.is_pause: self.pause.handle_events(events)

        for event in events:
            if self.buttons["info"].is_clicked(event): self.manager.set_state("info")

            if self.buttons["start"].is_clicked(event): self.manager.set_state("game")
            
            if self.buttons["pause"].is_clicked(event): self.is_pause = not self.is_pause
            
            if self.buttons["left"].is_clicked(event): self.manager.map_manager.last_map()

            if self.buttons["right"].is_clicked(event): self.manager.map_manager.next_map()