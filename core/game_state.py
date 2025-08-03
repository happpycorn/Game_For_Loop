from core.constants import *
from core.map_manager import MapManager

class StateManager:
    def __init__(self, state_list=[]):
        self.states = {}
        for name, state in state_list: self.states[name] = state(self)

        self.current_state = None
        self.running = True
        self.map_manager = MapManager()

    def set_state(self, name, data=None):
        self.current_state = self.states[name]
        self.current_state.enter(data)

    def update(self, dt):
        if not self.current_state: return
        self.current_state.update(dt)

    def draw(self, screen):
        if not self.current_state: return
        self.current_state.draw(screen)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT: self.running = False
    
        if not self.current_state: return
        self.current_state.handle_events(events)
