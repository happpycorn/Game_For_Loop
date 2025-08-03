from core.constants import *
from core.game_state import StateManager
import math

class RoleControler:
    def __init__(self, manager: StateManager, father) -> None:
        self.manager = manager
        self.father = father

        self.role_anime = RoleAnime(self)

        self.appear_sound = pygame.mixer.Sound(SOUND_APPEAR_PATH)
        self.bigger_sound = pygame.mixer.Sound(SOUND_BIGGER_PATH)
        self.boom_sound = pygame.mixer.Sound(SOUND_BOOM_PATH)
        self.get_flag_sound = pygame.mixer.Sound(SOUND_GET_FLAG_PATH)
        self.move_sound = pygame.mixer.Sound(SOUND_MOVE_PATH)
        self.open_door_sound = pygame.mixer.Sound(SOUND_OPEN_DOOR_PATH)
    
    def enter(self, data):
        self.x = self.manager.map_manager.current_map["start_point"][0]
        self.y = self.manager.map_manager.current_map["start_point"][1]
        self.size = 1

        self.role_anime.enter(
            self.x, self.y, self.size,
            self.manager.map_manager.tile_size,
            self.manager.map_manager.offset_x,
            self.manager.map_manager.offset_y
        )

        self.move_dir = (0, 0)
        self.is_space = False

        self.is_anime = False

        self.appear_sound.play()
        
    def update(self, dt):
        map_data = self.manager.map_manager.current_map
        tiles = self.get_tiles(map_data, self.move_dir)
        if not tiles is None:
            self.move_judge(tiles, self.move_dir)

            if self.is_space and any(tile == "C" for row in tiles for tile in row):
                for w in map_data["walls"]: w["close"] = not w["close"]
                self.is_space = False
                self.open_door_sound.play()
                self.role_anime.control_anime()

        self.role_anime.update(dt)
            
    def get_tiles(self, map_data, move_dir):
        d = [["/"]*self.size for _ in range(self.size)]
        for dy in range(self.size):
            for dx in range(self.size):
                tx = self.x + move_dir[0] + dx - self.size//2
                ty = self.y + move_dir[1] + dy - self.size//2

                if not (0 <= tx < map_data["col"] and 0 <= ty < map_data["row"]):
                    return

                d[dy][dx] = map_data["data"][ty][tx]

                if any(self.is_colliding_wall((w, tx, ty)) for w in map_data["walls"]): d[dy][dx] = "#"
        return d
    
    def move_judge(self, tiles, move_dir):

        if any(tile == "#" for row in tiles for tile in row):
            return
        
        if any(tile == "E" for row in tiles for tile in row):
            self.x += move_dir[0]
            self.y += move_dir[1]
            if not self.father.is_finish:
                self.get_flag_sound.play()
            self.role_anime.is_animes["move"] = True
            self.father.is_finish = True
            self.move_dir = (0, 0)
            self.manager.map_manager.current_map["best_record"] = min(
                self.father.move_count, 
                self.manager.map_manager.current_map["best_record"]
            )
            return
        
        if any(tile == "R" for row in tiles for tile in row):
            self.size += 1
            self.bigger_sound.play()
            if self.size > 5: 
                # self.x += move_dir[0]
                # self.y += move_dir[1]
                if self.role_anime.boom_anime():
                    self.boom_sound.play()
                    print(1)
                    self.manager.set_state("game")
                return
            self.x = self.manager.map_manager.current_map["start_point"][0]
            self.y = self.manager.map_manager.current_map["start_point"][1]
            self.role_anime.is_animes["return"] = True
            return
        
        if self.size > 5: 
            # self.x += move_dir[0]
            # self.y += move_dir[1]
            if self.role_anime.boom_anime():
                self.manager.set_state("game")
            return
        
        if all(tile == "/" for row in tiles for tile in row):
            self.x += move_dir[0]
            self.y += move_dir[1]
            if self.role_anime.drop_anime():
                self.manager.set_state("game")
            return
        
        if any(move_dir): 
            self.x += move_dir[0]
            self.y += move_dir[1]
            self.father.move_count += 1
            self.role_anime.is_animes["move"] = True
            self.move_sound.play()
    
    def is_colliding_wall(self, wallinfo):
        wall, x, y = wallinfo

        wl = wall["tx"] if wall["close"] else wall["fx"]
        wr = wl + wall["ww"] - 1
        wt = wall["ty"] if wall["close"] else wall["fy"]
        wb = wt + wall["wh"] - 1

        return wl <= x <= wr and wt <= y <= wb

    def draw(self, screen):
        role_data = self.role_anime.get_role_data(self.x, self.y, self.size)
        scaled_image = pygame.transform.scale(role_data["img"], (role_data["w"], role_data["h"]))
        rotated_image = pygame.transform.rotate(scaled_image, role_data["angle"])
        new_rect = rotated_image.get_rect(center=(role_data["x"] + role_data["w"] // 2, role_data["y"] + role_data["h"] // 2))
        screen.blit(rotated_image, new_rect.topleft)

    def handle_events(self, events):
        self.move_dir = (0, 0)
        if self.role_anime.is_anime: return
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.move_dir = (-1, 0)
                elif event.key == pygame.K_RIGHT:
                    self.move_dir = (1, 0)
                elif event.key == pygame.K_UP:
                    self.move_dir = (0, -1)
                elif event.key == pygame.K_DOWN:
                    self.move_dir = (0, 1)
                elif event.key == pygame.K_SPACE:
                    self.is_space = True

class RoleAnime:
    ROLE_MOVE_SMOOTHING = 0.3
    ROLE_MOVE_SNAP = 0.01

    def __init__(self, father) -> None:
        self.father = father

        self.role_images = {
            "normal": pygame.image.load(IMG_ROLE_NORMAL_PATH).convert_alpha(),
            "happy" : pygame.image.load(IMG_ROLE_HAPPY_PATH).convert_alpha(),
            "scared": pygame.image.load(IMG_ROLE_SCARED_PATH).convert_alpha(),
            "push"  : pygame.image.load(IMG_ROLE_PUSH_PATH).convert_alpha(),
        }
    
    def enter(self, x, y, size, tile_size, offset_x, offset_y):
        self.draw_x = x
        self.draw_y = y
        self.size = size
        self.angle = 0

        self.tile_size = tile_size
        self.offset_x = offset_x
        self.offset_y = offset_y

        self.is_animes = {
            "move" : False,
            "return" : False,
            "control" : False,
            "drop1" : False,
            "drop2" : False,
            "drop3" : False,
            "boom1" : False,
            "boom2" : False,
        }

        self.img_anime_time = 0

        self.current_img = self.role_images["normal"]
    
    def update(self, dt):
        if self.is_animes["control"]:
            self.img_anime_time = max(self.img_anime_time-dt, 0)
            if self.img_anime_time == 0: 
                self.is_animes["control"] = False
                self.current_img = self.role_images["normal"]
        if self.is_animes["drop1"] and not self.is_animes["drop2"]:
            self.img_anime_time = max(self.img_anime_time-dt, 0)
            if self.img_anime_time == 0: 
                self.is_animes["drop2"] = True
                self.current_img = self.role_images["push"]
                self.img_anime_time = 2
        if self.is_animes["drop2"]:
            self.img_anime_time = max(self.img_anime_time-dt, 0)
            if self.img_anime_time == 0: 
                self.is_animes["drop3"] = True
                self.current_img = self.role_images["push"]
        if self.is_animes["boom1"]:
            self.img_anime_time = max(self.img_anime_time-dt, 0)
            print(self.is_animes["boom1"], self.is_animes["boom2"], self.img_anime_time)
            if self.img_anime_time == 0: 
                self.is_animes["boom2"] = True
                self.current_img = self.role_images["normal"]
    
    def control_anime(self):
        self.is_animes["control"] = True
        self.img_anime_time = 0.2
        self.current_img = self.role_images["push"]
    
    def drop_anime(self) -> bool:
        if self.is_animes["drop1"] and self.is_animes["drop2"] and self.is_animes["drop3"]:
            return True
        elif not self.is_animes["drop1"]:
            self.is_animes["drop1"] = True
            self.img_anime_time = 0.5
            self.current_img = self.role_images["scared"]
            self.is_animes["move"] = True
        return False
    
    def boom_anime(self) -> bool:
        print(self.is_animes["boom1"] and self.is_animes["boom2"])
        if self.is_animes["boom1"] and self.is_animes["boom2"]:
            return True
        elif not self.is_animes["boom1"]:
            self.is_animes["boom1"] = True
            self.img_anime_time = 1
            self.current_img = self.role_images["scared"]
            self.is_animes["move"] = True
        return False

    @property
    def is_anime(self): return any(i for i in self.is_animes.values())

    def get_role_data(self, x: int, y: int, size: int) -> dict:
        size_in_px = self.tile_size * self.size

        if self.is_animes["return"]:
            self.return_anime(x, y, size)

            size_in_px = self.tile_size * self.size
            draw_x, scale_x = self.get_axis_draw_info(x, self.draw_x, self.size, self.offset_x)
            draw_y, scale_y = self.get_axis_draw_info(y, self.draw_y, self.size, self.offset_y)
            draw_w = size_in_px * scale_x
            draw_h = size_in_px * scale_y

        elif self.is_animes["move"]: 
            self.move(x, y)
        
            draw_x, scale_x = self.get_axis_draw_info(x, self.draw_x, self.size, self.offset_x)
            draw_y, scale_y = self.get_axis_draw_info(y, self.draw_y, self.size, self.offset_y)
            draw_w = size_in_px * scale_x
            draw_h = size_in_px * scale_y
        
        elif self.is_animes["drop2"]:
            self.drop()

            draw_x = (self.draw_x - math.ceil(size) // 2) * self.tile_size + self.offset_x + (size-self.size)*self.tile_size/2
            draw_y = (self.draw_y - math.ceil(size) // 2) * self.tile_size + self.offset_y + (size-self.size)*self.tile_size/2
            draw_w = size_in_px
            draw_h = size_in_px

        elif self.is_animes["boom1"]:
            self.boom()

            draw_x = (self.draw_x - math.ceil(size) // 2) * self.tile_size + self.offset_x + (size-self.size)*self.tile_size/2
            draw_y = (self.draw_y - math.ceil(size) // 2) * self.tile_size + self.offset_y + (size-self.size)*self.tile_size/2
            draw_w = size_in_px
            draw_h = size_in_px
        
        else:
            draw_x, scale_x = self.get_axis_draw_info(x, self.draw_x, self.size, self.offset_x)
            draw_y, scale_y = self.get_axis_draw_info(y, self.draw_y, self.size, self.offset_y)
            draw_w = size_in_px * scale_x
            draw_h = size_in_px * scale_y

        return {
            "img" : self.current_img,
            "x" : draw_x, 
            "y" : draw_y, 
            "w" : draw_w, 
            "h" : draw_h,
            "angle" : self.angle,
        }

    def drop(self) -> None:
        self.angle += 10
        self.size *= 0.9

    def boom(self) -> None:
        self.size *= 1.1

    def move(self, x: int, y: int) -> None:
        self.draw_x = self.smooth_to(self.draw_x, x)
        self.draw_y = self.smooth_to(self.draw_y, y)

        if self.draw_x == x and self.draw_y == y:
            self.is_animes["move"] = False
    
    def return_anime(self, x: int, y: int, size: float) -> None:
        transpot_speed = 0.1
        self.draw_x = self.smooth_to(self.draw_x, x, transpot_speed)
        self.draw_y = self.smooth_to(self.draw_y, y, transpot_speed)
        self.size = self.smooth_to(self.size, size, transpot_speed)
        self.current_img = self.role_images["happy"]

        if self.draw_x == x and self.draw_y == y and self.size == size:
            self.is_animes["return"] = False
            self.current_img = self.role_images["normal"]

    def smooth_to(self, current, target, smoothing=ROLE_MOVE_SMOOTHING, snap=ROLE_MOVE_SNAP):
        current += (target - current) * smoothing
        if abs(current - target) < snap:
            return target
        return current
    
    def get_axis_draw_info(self, target: float, current: float, size: float, offset: float) -> tuple[float, float]:
        delta = min(abs(target - current), 1.0)
        scale = 1 - abs(delta - 0.5) * 2
        visual_scale = 1.0 + (0.5 * scale / size)

        draw_pos = (current - math.ceil(size) // 2) * self.tile_size + offset
        return draw_pos, visual_scale