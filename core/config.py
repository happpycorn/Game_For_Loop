from core.constants import *
from core.game_state import StateManager
from scenes.home import HomeScene
from scenes.game import GameScene
from scenes.info import InfoScene

STATE_LIST = [
    ["home", HomeScene],
    ["game", GameScene],
    ["info", InfoScene],
]