from core.constants import *
from core.ui_components import Button
from core.ui_components import Pause
from core.ui_components import Text
from core.ui_components import Finish
from core.game_state import StateManager
from core.role_control import RoleControler

class GameScene:
    def __init__(self, manager: StateManager):
        self.manager = manager
        self.default_font = pygame.font.SysFont(None, DEFAULT_FONT_SIZE)

        self.buttons = {
            "pause": Button(PAUSE_BUTTON_PATH, (20, 20), 40, 40)
        }

        self.texts = {
            "move_count": Text("--", (80, 30), center=False)
        }

        self.pause = Pause(manager, self)
        self.finish = Finish(manager, self)
        self.role = RoleControler(manager, self)

    def enter(self, data):
        print("Entered Game Scene")
        self.is_pause = False
        self.is_anime = False
        self.manager.map_manager.enter(data)
        self.role.enter(data)
        self.move_count = 0
        self.is_finish = False

    def update(self, dt):
        self.role.update(dt)
        self.finish.update(dt)
        self.texts["move_count"].text = f"MOVE {self.move_count}"

    def draw(self, screen):
        screen.fill((30, 30, 30))
        self.manager.map_manager.draw(screen)
        self.role.draw(screen)
        for btn in self.buttons.values(): btn.draw(screen)
        for txt in self.texts.values(): txt.draw(screen)
        if self.is_pause: self.pause.draw(screen)
        if self.is_finish: self.finish.draw(screen)

    def handle_events(self, events):
        if self.is_finish:
            self.finish.handle_events(events)
            return

        if self.is_pause: self.pause.handle_events(events)

        if self.is_anime: return

        self.role.handle_events(events)

        for event in events:
            if self.buttons["pause"].is_clicked(event):
                self.is_pause = not self.is_pause
