from core.constants import *
import os

class MapManager:
    def __init__(self):
        self.current_map_index = 0
        self.map_list = self.load_maps_from_folder(MAP_FOLDER_PATH)
        self.map_count = len(self.map_list)
        self.draw_info = []

        self.tile_images = {
            "/" : pygame.image.load(IMG_SPACE_PATH).convert_alpha(),
            "#" : pygame.image.load(IMG_WALL_PATH).convert_alpha(),
            "." : pygame.image.load(IMG_EMPTY_PATH).convert_alpha(),
            "S" : pygame.image.load(IMG_EMPTY_PATH).convert_alpha(),
            "R" : pygame.image.load(IMG_RETURN_PATH).convert_alpha(),
            "E" : pygame.image.load(IMG_END_PATH).convert_alpha(),
            "CA": pygame.image.load(IMG_CONTRAL_A_PATH).convert_alpha(),
            "CB": pygame.image.load(IMG_CONTRAL_B_PATH).convert_alpha(),
            "D" : pygame.image.load(IMG_WALL_PATH).convert_alpha(),
        }
        self.default_image = pygame.image.load(IMG_SPACE_PATH).convert_alpha()
        
    def load_maps_from_folder(self, folder_path):
        maps = []
        for file_name in sorted(os.listdir(folder_path)):
            if file_name.endswith(".txt"):
                file_path = os.path.join(folder_path, file_name)
                maps.append(self.readMap(file_path))
        return maps

    def enter(self, data):
        self.cols = self.current_map["col"]
        self.rows = self.current_map["row"]
        tile_width = DRAW_SIZE_X // self.cols
        tile_height = DRAW_SIZE_Y // self.rows
        self.tile_size = min(tile_width, tile_height)
        self.is_door = True

        # 中心對齊的偏移
        self.offset_x = DRAW_MARGIN + (DRAW_SIZE_X - self.tile_size * (self.cols+1)) // 2
        self.offset_y = DRAW_MARGIN + (DRAW_SIZE_Y - self.tile_size * (self.rows+1)) // 2

        for w in self.current_map["walls"]: w["close"] = True

    def update(self, dt):
        pass

    def draw(self, screen):
        for r in range(self.rows):
            for c in range(self.cols):
                ch = self.current_map["data"][r][c]
                if ch == "C":
                    ch = "CA" if any(w["close"] for w in self.current_map["walls"]) else "CB"
                img = self.tile_images.get(ch, self.default_image)
                
                x = self.offset_x + c * self.tile_size
                y = self.offset_y + r * self.tile_size
                
                screen.blit(pygame.transform.scale(img, (self.tile_size, self.tile_size)), (x, y))

        for w in self.current_map["walls"]:
            wx = w["tx"] if w["close"] else w["fx"]
            wy = w["ty"] if w["close"] else w["fy"]
            x = self.offset_x + wx * self.tile_size
            y = self.offset_y + wy * self.tile_size
            w_px = self.tile_size * w["ww"]
            h_px = self.tile_size * w["wh"]

            # 繪製牆體圖片
            wall_image = pygame.transform.scale(self.tile_images["D"], (w_px, h_px))
            screen.blit(wall_image, (x, y))

    @property
    def current_map(self):
        return self.map_list[self.current_map_index]
    
    def current_pos(self, x, y):
        return self.map_list[self.current_map_index]["data"][y][x]

    def readMap(self, file_name) -> dict:
        with open(file_name, 'r') as f:
            lines = [line.strip() for line in f if line.strip()]  # 去除空白行和換行
        
        name = lines[0]
        n, r, c, y, x = map(int, lines[1].split())
        d = lines[2:r+2]

        padding = 5
        padded_width = c + padding * 2

        padded_d = [
            "/" * padding + row + "/" * padding
            for row in d
        ]

        full_d = (
            ["/" * padded_width] * padding +
            padded_d +
            ["/" * padded_width] * padding
        )

        walls = []
        for i in lines[r+2:]:
            ww, wh, ty, tx, fy, fx = map(int, i.split())
            walls.append({
                "wh": wh, "ww": ww,
                "ty": ty + padding, "tx": tx + padding,
                "fy": fy + padding, "fx": fx + padding,
                "close": True
            })
        
        return {
            "name": name,
            "num": n,
            "row": r + padding * 2,
            "col": c + padding * 2,
            "data": full_d,
            "start_point": (y + padding, x + padding),
            "walls": walls,
            "best_record": float("inf")
        }
    
    def next_map(self): self.current_map_index = (self.current_map_index + 1) % self.map_count

    def last_map(self): self.current_map_index = (self.current_map_index - 1) % self.map_count