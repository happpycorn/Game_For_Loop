from core.constants import *

class Button:
    def __init__(self, image_path, position, w, h):
        self.original_image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.original_image, (w, h))

        self.rect = self.image.get_rect(topleft=position)

        self.click_sound = pygame.mixer.Sound(SOUND_CLICK_PATH)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def is_hovered(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered(event.pos):
            self.click_sound.play()
            return True
        return False

class Pause:
    COLOR_PAUSE_BACKGROUND = (70, 70, 70)
    COLOR_PAUSE_OUTLINE = (200, 200, 200)
    RECT_POS_X = 320
    RECT_POS_Y = 180
    RECT_SIZE_X = 160
    RECT_SIZE_Y = 240
    LINE_WIDTH = 3

    def __init__(self, manager, father):
        self.manager = manager
        self.father = father

        self.buttons = {
            "sound_up": Button(SOUND_UP_BUTTON_PATH, (340, 230), 55, 20),
            "sound_down": Button(SOUND_DOWN_BUTTON_PATH, (405, 230), 55, 20),
            "menu": Button(MENU_BUTTON_PATH, (340, 260), 120, 40),
            "reset": Button(RESET_BUTTON_PATH, (340, 310), 120, 40),
            "exit": Button(EXIT_BUTTON_PATH, (340,360), 120, 40)
        }

        self.pause_outline_img = pygame.image.load(resource_path("assets/images/Sound_Not_Work.png")).convert_alpha()

    def draw(self, screen):
        pygame.draw.rect(
            screen, self.COLOR_PAUSE_OUTLINE, 
            (self.RECT_POS_X-self.LINE_WIDTH, self.RECT_POS_Y-self.LINE_WIDTH, 
             self.RECT_SIZE_X+self.LINE_WIDTH*2, self.RECT_SIZE_Y+self.LINE_WIDTH*2),
            border_radius=20
        )
        pygame.draw.rect(
            screen, self.COLOR_PAUSE_BACKGROUND, 
            (self.RECT_POS_X, self.RECT_POS_Y, self.RECT_SIZE_X, self.RECT_SIZE_Y),
            border_radius=20
        )
        screen.blit(self.pause_outline_img, (340, 200))
        for btn in self.buttons.values(): btn.draw(screen)

    def handle_events(self, events):
        for event in events:
            if self.buttons["exit"].is_clicked(event):
                self.manager.running = False

            if self.buttons["reset"].is_clicked(event):
                self.manager.set_state("game")

            if self.buttons["menu"].is_clicked(event):
                self.manager.set_state("home")

            if self.buttons["sound_up"].is_clicked(event):
                pass

            if self.buttons["sound_down"].is_clicked(event):
                pass

class Finish:
    COLOR_BACKGROUND = (70, 70, 70)
    COLOR_OUTLINE = (200, 200, 200)
    RECT_POS_X = -10
    RECT_POS_Y = 180
    RECT_SIZE_X = 820
    RECT_SIZE_Y = 240
    LINE_WIDTH = 3

    def __init__(self, manager, father):
        self.manager = manager
        self.father = father

        self.buttons = {
            "again": Button(AGAIN_BUTTON_PATH, (340, 310), 120, 40),
            "next": Button(NEXT_BUTTON_PATH, (340,360), 120, 40)
        }

        self.texts = {
            "move_count": Text("--", (400, 230)),
            "best_record": Text("--", (400, 270))
        }

        self.bg_image1 = pygame.image.load(IMG_FINISH_1_PATH).convert_alpha()
        self.bg_image2 = pygame.image.load(IMG_FINISH_2_PATH).convert_alpha()
    
    def update(self, dx):
        self.texts["move_count"].text = f"Move Count: {self.father.move_count}"
        self.texts["best_record"].text = f"Best Record: {self.manager.map_manager.current_map['best_record']}"

    def draw(self, screen):
        pygame.draw.rect(
            screen, self.COLOR_OUTLINE, 
            (self.RECT_POS_X-self.LINE_WIDTH, self.RECT_POS_Y-self.LINE_WIDTH, 
             self.RECT_SIZE_X+self.LINE_WIDTH*2, self.RECT_SIZE_Y+self.LINE_WIDTH*2)
        )
        pygame.draw.rect(
            screen, self.COLOR_BACKGROUND, 
            (self.RECT_POS_X, self.RECT_POS_Y, self.RECT_SIZE_X, self.RECT_SIZE_Y)
        )

        scaled_image = pygame.transform.scale(self.bg_image1, (200, 200))
        screen.blit(scaled_image, (50, 200))
        scaled_image = pygame.transform.scale(self.bg_image2, (200, 200))
        screen.blit(scaled_image, (550, 200))
        
        for btn in self.buttons.values(): btn.draw(screen)
        for txt in self.texts.values(): txt.draw(screen)

    def handle_events(self, events):
        for event in events:
            if self.buttons["again"].is_clicked(event):
                self.manager.set_state("game")

            if self.buttons["next"].is_clicked(event):
                self.manager.map_manager.next_map()
                self.manager.set_state("game")
    
class Text:
    def __init__(self, text: str, pos: tuple, color=COLOR_WHITE, font=None, center=True) -> None:
        self.text = text
        self.color = color
        self.pos = pos
        self.center = center
        if font: self.font = font
        else: self.font = pygame.font.SysFont(None, DEFAULT_FONT_SIZE)
    
    def draw(self, screen) -> None:
        surface = self.font.render(self.text, True, self.color)
        if self.center: rect = surface.get_rect(center=self.pos)
        else: rect = surface.get_rect(topleft=self.pos)
        screen.blit(surface, rect)
    