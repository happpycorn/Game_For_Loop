# Import
import pygame
import os
import sys

def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base_path, relative_path)

# Value
NAME = "Game For Loop"
SCREEN_SIZE = (800, 600)
DRAW_MARGIN = 100
DRAW_SIZE_X = SCREEN_SIZE[0]-DRAW_MARGIN
DRAW_SIZE_Y = SCREEN_SIZE[1]-DRAW_MARGIN

DEFAULT_FONT_SIZE = 36
TITLE_FONT_SIZE = 72

FPS = 60

COLOR_BACK_GROUND = (30, 30, 30)
COLOR_WHITE = (255, 255, 255)

COLOR_SPACE = (30, 30, 30)
COLOR_EMPTY = (100, 100, 100)
COLOR_WALL = (200, 200, 200)

COLOR_START = (100, 100, 100)
COLOR_RETURN = (150, 150, 30)
COLOR_END = (150, 30, 30)

COLOR_ROLE = (30, 30, 150)

# Path
PAUSE_BUTTON_PATH = resource_path("assets/images/Setting_Button.png")
INFO_BUTTON_PATH = resource_path("assets/images/Info_Button.png")
CLOSE_BUTTON_PATH = resource_path("assets/images/Close_Button.png")

START_BUTTON_PATH = resource_path("assets/images/Start_Button.png")
LEFT_BUTTON_PATH = resource_path("assets/images/Left_Button.png")
RIGHT_BUTTON_PATH = resource_path("assets/images/Right_Button.png")

EXIT_BUTTON_PATH = resource_path("assets/images/Exit_Button.png")
MENU_BUTTON_PATH = resource_path("assets/images/Home_Button.png")
AGAIN_BUTTON_PATH = resource_path("assets/images/Again_Button.png")
CANCEL_BUTTON_PATH = resource_path("assets/images/Back_Button.png")
RESET_BUTTON_PATH = resource_path("assets/images/Reset_Button.png")
NEXT_BUTTON_PATH = resource_path("assets/images/NEXT_Button.png")

SOUND_UP_BUTTON_PATH = resource_path("assets/images/Sound_Up_Button.png")
SOUND_DOWN_BUTTON_PATH = resource_path("assets/images/Sound_Down_Button.png")

MAP_FOLDER_PATH = resource_path("assets/map")

IMG_SPACE_PATH = resource_path("assets/images/Space_Img.png")
IMG_EMPTY_PATH = resource_path("assets/images/Empty_Img.png")
IMG_WALL_PATH = resource_path("assets/images/Wall_Img.png")
IMG_END_PATH = resource_path("assets/images/Flag_Img.png")
IMG_RETURN_PATH = resource_path("assets/images/Return_Img.png")
IMG_CONTRAL_A_PATH = resource_path("assets/images/Control_A_Img.png")
IMG_CONTRAL_B_PATH = resource_path("assets/images/Control_B_Img.png")

IMG_ROLE_NORMAL_PATH = resource_path("assets/images/Role_Normal.png")
IMG_ROLE_HAPPY_PATH = resource_path("assets/images/Role_Happy.png")
IMG_ROLE_SCARED_PATH = resource_path("assets/images/Role_Scared.png")
IMG_ROLE_PUSH_PATH = resource_path("assets/images/Role_Push.png")

IMG_FINISH_1_PATH = resource_path("assets/images/Ending_Role.png")
IMG_FINISH_2_PATH = resource_path("assets/images/Ending_Flag.png")

IMG_TITLE_PATH = resource_path("assets/images/Title.png")
IMG_INFO_PATH = resource_path("assets/images/Info.png")

MUSIC_BGM_PATH = resource_path("assets/musics/Devonshire_Waltz_Andante.mp3")

SOUND_APPEAR_PATH = resource_path("assets/musics/appear.ogg")
SOUND_BIGGER_PATH = resource_path("assets/musics/bigger.ogg")
SOUND_BOOM_PATH = resource_path("assets/musics/boom.ogg")
SOUND_CLICK_PATH = resource_path("assets/musics/click.ogg")
SOUND_GET_FLAG_PATH = resource_path("assets/musics/get_flag.ogg")
SOUND_MOVE_PATH = resource_path("assets/musics/move.ogg")
SOUND_OPEN_DOOR_PATH = resource_path("assets/musics/open_door.ogg")