import pygame
import sys
import copy
import heapq
import threading
import json
import os

SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
FPS = 60
BACKGROUND_COLOR = '#c0837f'

file_data_name = 'level_data.txt'

def create_file_data():
    import json
    data = {
        1: [
            True, 
            [ 
                ['green', 'green'], 
                ['green', 'green']
            ]
        ],
        2: [
            False,
            [
                ['pink', 'green', 'pink', 'green'], 
                ['green', 'pink', 'green', 'pink'], 
                []
            ]
        ],
        3: [
            False,
            [
                ['green', 'yellow'], 
                ['yellow', 'green'], 
                ['green', 'green'], 
                ['yellow', 'yellow']
            ]
        ],
        4: [
            False,
            [
                ['green', 'purple'], 
                ['red', 'red', 'green'], 
                ['purple', 'red', 'green'], 
                ['green', 'red'], 
                ['purple', 'purple']
            ]
        ],
        5: [
            False,
            [
                ['green', 'green', 'red', 'aqua'], 
                ['pink', 'purple', 'red', 'aqua'], 
                ['purple', 'red', 'pink', 'red'], 
                ['pink', 'green', 'aqua', 'purple'], 
                ['green', 'pink', 'aqua', 'purple'], 
                [],
                []
            ]
        ],
        6: [
            False,
            [
                ['purple', 'purple', 'purple', 'blue'], 
                ['purple', 'green', 'yellow', 'green'], 
                ['green', 'yellow', 'blue', 'yellow'], 
                ['yellow', 'blue', 'green', 'pink'], 
                ['blue', 'pink', 'pink', 'pink'], 
                [], 
                []
            ]
        ],
        7: [
            False,
            [
                ['pink', 'blue', 'pink', 'green'], 
                ['pink', 'green', 'blue', 'red'], 
                ['green', 'green', 'red', 'purple'], 
                ['red', 'red', 'blue', 'purple'], 
                ['pink', 'purple', 'blue', 'purple'], 
                [], 
                []
            ]
        ],
        8: [
            False,
            [
                ['grey', 'green', 'pink', 'red'], 
                ['grey', 'green', 'pink', 'purple'], 
                ['purple', 'pink', 'grey', 'pink'], 
                ['red', 'purple', 'purple', 'red'], 
                ['green', 'red', 'green', 'grey'], 
                [], 
                []
            ]
        ],
        9: [
            False,
            [
                ['grey', 'green', 'purple', 'purple'], 
                ['pink', 'red', 'grey', 'purple'], 
                ['red', 'green', 'green', 'pink'], 
                ['red', 'grey', 'grey', 'green'], 
                ['pink', 'red', 'purple', 'pink'], 
                [], 
                []
            ]
        ],
        10: [
            False,
            [
                ['red', 'green', 'pink', 'orange'], 
                ['purple', 'orange', 'red', 'orange'], 
                ['red', 'purple', 'pink', 'purple'], 
                ['green', 'pink', 'purple', 'green'], 
                ['red', 'green', 'orange', 'pink'], 
                [], 
                []
            ]
        ],
        11: [
            False,
            [
                ['green', 'green', 'pink', 'cyan'], 
                ['orange', 'orange', 'pink'], 
                ['purple', 'purple', 'orange', 'cyan'], 
                ['cyan'], 
                ['red', 'red', 'pink', 'red'], 
                ['pink', 'green', 'green', 'cyan'], 
                ['purple', 'purple', 'red', 'orange']
            ]
        ],
        12: [
            False,
            [
                ['green', 'purple', 'pink'], 
                ['orange', 'orange', 'red', 'purple'], 
                ['pink'], 
                ['blue', 'red', 'orange', 'green'], 
                ['red', 'red', 'blue', 'green'], 
                ['blue', 'blue', 'orange', 'green'], 
                ['purple', 'pink', 'pink', 'purple']
            ]
        ],
        13: [
            False,
            [
                ['red', 'pink', 'yellow', 'grey'], 
                ['blue', 'red', 'cyan', 'cyan'], 
                ['grey', 'grey', 'green', 'red'], 
                ['pink', 'yellow', 'yellow', 'green'], 
                ['blue', 'cyan', 'cyan', 'green'], 
                ['yellow', 'grey', 'pink', 'red'], 
                ['pink', 'blue', 'green', 'blue'], 
                [], 
                []
            ]
        ],
        14: [
            False,
            [
                ['grey', 'cyan', 'green', 'green'], 
                ['grey', 'blue', 'red', 'red'], 
                ['blue', 'green', 'red', 'grey'], 
                ['cyan', 'red', 'pink', 'yellow'], 
                ['yellow', 'yellow', 'grey', 'yellow'], 
                ['pink', 'pink', 'green', 'cyan'], 
                ['blue', 'pink', 'blue', 'cyan'], 
                [], 
                []
            ]
        ],
        15: [
            False,
            [
                ['grey', 'red', 'blue', 'yellow'], 
                ['purple', 'yellow', 'blue', 'grey'], 
                ['cyan', 'purple', 'grey', 'cyan'], 
                ['green', 'red', 'blue', 'cyan'], 
                ['purple', 'grey', 'yellow', 'red'], 
                ['yellow', 'green', 'green', 'cyan'], 
                ['blue', 'purple', 'green', 'red'], 
                [], 
                []
            ]
        ],
    }

    with open(file_data_name, 'w') as test_file:
        json.dump(data, test_file)

class Game:
    def __init__(self):
        pygame.init()

        pygame.mixer.init()
        # Load and play background music
        pygame.mixer.music.load('assets/bgm.mp3')
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
        self.is_music_playing = True

        if not os.path.isfile(file_data_name):
            create_file_data()
        else:
            with open(file_data_name, 'r') as file:
                content = file.read()
                if not content:
                   create_file_data()
    
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        
        self.gameStateManager = GameStateManager('start', self)
        self.level_failed = LevelFailed(self.screen, self.gameStateManager)
        self.level_completed = LevelCompleted(self.screen, self.gameStateManager)
        self.game_completed = GameCompleted(self.screen, self.gameStateManager)
        self.game_play = GamePlay(self.screen, self.gameStateManager)
        self.start = Start(self.screen, self.gameStateManager)
        self.level = Level(self.screen, self.gameStateManager)
        self.rule = Rule(self.screen, self.gameStateManager)

        self.state = {
            'level_failed': self.level_failed,
            'level_completed': self.level_completed,
            'game_play': self.game_play,
            'start': self.start,
            'level': self.level,
            'rule': self.rule,
            'game_completed':self.game_completed
        }
    
    def set_puzzle(self):
        self.game_play.init_game()
    
    def reset_levels_list(self):
        self.level.init_buttons()

    def run(self):
        while True:
            if self.is_music_playing:
                volume_button_surf = pygame.image.load('assets/volumeopen.png')
                volume_button_surf = pygame.transform.scale(volume_button_surf, (50,50))
                volume_button_rect = volume_button_surf.get_frect(bottomright=(SCREEN_WIDTH-10,SCREEN_HEIGHT-10))
            else:
                volume_button_surf = pygame.image.load('assets/volumemute.png')
                volume_button_surf = pygame.transform.scale(volume_button_surf, (50,50))
                volume_button_rect = volume_button_surf.get_frect(bottomright=(SCREEN_WIDTH-10,SCREEN_HEIGHT-10))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if self.gameStateManager.get_state() == 'game_play':
                    if self.game_play.move_list and event.type == self.game_play.ai_step_timer:
                        self.game_play.ai_step()

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
                    mouse_pos = pygame.mouse.get_pos()
                    if volume_button_rect.collidepoint(mouse_pos):
                        self.is_music_playing = not self.is_music_playing
                        if self.is_music_playing:
                            pygame.mixer.music.unpause()
                        else:
                            pygame.mixer.music.pause()


            self.state[self.gameStateManager.get_state()].run()

            self.screen.blit(volume_button_surf, volume_button_rect)
            pygame.display.update()
            self.clock.tick(FPS)

class LevelFailed:
    def __init__(self, display: pygame.surface.Surface, gameStateManager: 'GameStateManager'):
        self.display = display
        self.gameStateManager = gameStateManager
        self.title_font = pygame.font.Font('font/Arial.ttf', 100)
        self.button_font = pygame.font.Font('font/Arial.ttf', 50)

        #Title Setup
        self.level_completed_title_surf = self.title_font.render('Level Failed', False, '#EEEEEE')
        self.level_completed_title_rect = self.level_completed_title_surf.get_frect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/3))

        #Next Level Button Setup
        # self.next_level_text_surf = self.button_font.render('Reset', False, "#EEEEEE", "#A3C9AA")
        self.next_level_text_surf = pygame.image.load('assets/reset.png').convert_alpha()
        self.next_level_text_surf = pygame.transform.scale(self.next_level_text_surf, (50, 50))
        self.next_level_text_rect = self.next_level_text_surf.get_frect(center=(SCREEN_WIDTH/2-100, SCREEN_HEIGHT/2+100))

        #Home Button Setup
        # self.home_text_surf = self.button_font.render('Home', False, "#EEEEEE", "#A3C9AA", wraplength=200)
        self.home_text_surf = pygame.image.load('assets/home.png').convert_alpha()
        self.home_text_surf = pygame.transform.scale(self.home_text_surf, (50, 50))
        self.home_text_rect = self.home_text_surf.get_frect(center=(SCREEN_WIDTH/2+100, SCREEN_HEIGHT/2+100))
    
    def run(self):
        self.display.fill(BACKGROUND_COLOR)
        self.display.blit(self.level_completed_title_surf, self.level_completed_title_rect)
        self.display.blit(self.next_level_text_surf, self.next_level_text_rect)
        self.display.blit(self.home_text_surf, self.home_text_rect)
       
        mouses = pygame.mouse.get_just_pressed()
        if mouses[0]:
            mouse_pos = pygame.mouse.get_pos()
            if self.home_text_rect.collidepoint(mouse_pos):
                self.gameStateManager.set_state('start')
            if self.next_level_text_rect.collidepoint(mouse_pos):
                self.gameStateManager.set_puzzle(level_number=self.gameStateManager.level_number, puzzle=self.gameStateManager.puzzle)
                self.gameStateManager.set_state('game_play')

class LevelCompleted:
    def __init__(self, display: pygame.surface.Surface, gameStateManager: 'GameStateManager'):
        self.display = display
        self.gameStateManager = gameStateManager
        self.title_font = pygame.font.Font('font/Arial.ttf', 100)
        self.button_font = pygame.font.Font('font/Arial.ttf', 50)

        #Title Setup
        self.level_completed_title_surf = self.title_font.render('Level Completed', False, '#EEEEEE')
        self.level_completed_title_rect = self.level_completed_title_surf.get_frect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/3))

        #Next Level Button Setup
        # self.next_level_text = self.button_font.render('Next Level', False, "#EEEEEE", "#A3C9AA")
        self.next_level_text_surf = pygame.image.load('assets/next.png').convert_alpha()
        self.next_level_text_surf = pygame.transform.scale(self.next_level_text_surf, (50, 50))
        self.next_level_text_rect = self.next_level_text_surf.get_frect(center=(SCREEN_WIDTH/2-100, SCREEN_HEIGHT/2+100))

        #Home Button Setup
        # self.home_text_surf = self.button_font.render('Home', False, "#EEEEEE", "#A3C9AA", wraplength=200)
        self.home_text_surf = pygame.image.load('assets/home.png').convert_alpha()
        self.home_text_surf = pygame.transform.scale(self.home_text_surf, (50, 50))
        self.home_text_rect = self.home_text_surf.get_frect(center=(SCREEN_WIDTH/2+100, SCREEN_HEIGHT/2+100))
    
    def run(self):
        self.display.fill(BACKGROUND_COLOR)
        self.display.blit(self.level_completed_title_surf, self.level_completed_title_rect)
        self.display.blit(self.next_level_text_surf, self.next_level_text_rect)
        self.display.blit(self.home_text_surf, self.home_text_rect)
        
        mouses = pygame.mouse.get_just_pressed()
        if mouses[0]:
            mouse_pos = pygame.mouse.get_pos()
            if self.home_text_rect.collidepoint(mouse_pos):
                self.gameStateManager.set_state('start')
            if self.next_level_text_rect.collidepoint(mouse_pos):
                if self.gameStateManager.level_number == 15:
                    self.gameStateManager.set_state('game_completed')
                else:
                    self.gameStateManager.set_up_next_level()
                    self.gameStateManager.set_state('game_play')

class GameCompleted:
    def __init__(self, display: pygame.surface.Surface, gameStateManager: 'GameStateManager'):
        self.display = display
        self.gameStateManager = gameStateManager
        self.title_font = pygame.font.Font('font/Arial.ttf', 100)
        self.title_font2 = pygame.font.Font('font/Arial.ttf', 50)

        #Title Setup
        self.level_completed_title_surf = self.title_font.render('Congratulation!!!', False, '#EEEEEE')
        self.level_completed_title_rect = self.level_completed_title_surf.get_frect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/3))
        
        self.level_completed_title_surf2 = self.title_font2.render('You are done with this game!', False, '#EEEEEE')
        self.level_completed_title_rect2 = self.level_completed_title_surf2.get_frect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/3+100))

        #Home Button Setup
        self.home_text_surf = pygame.image.load('assets/home.png').convert_alpha()
        self.home_text_surf = pygame.transform.scale(self.home_text_surf, (50, 50))
        self.home_text_rect = self.home_text_surf.get_frect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT/2+100))
    
    def run(self):
        self.display.fill(BACKGROUND_COLOR)
        self.display.blit(self.level_completed_title_surf, self.level_completed_title_rect)
        self.display.blit(self.level_completed_title_surf2, self.level_completed_title_rect2)
        self.display.blit(self.home_text_surf, self.home_text_rect)
        
        mouses = pygame.mouse.get_just_pressed()
        if mouses[0]:
            mouse_pos = pygame.mouse.get_pos()
            if self.home_text_rect.collidepoint(mouse_pos):
                self.gameStateManager.set_state('start')

class Rule:
    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager

        self.HEADER_FONT = pygame.font.Font("font/Arial.ttf", 90)
        self.TITLE_FONT = pygame.font.Font("font/Arial.ttf", 40)

        self.back_button_surf = pygame.image.load('assets/back.png')
        self.back_button_surf = pygame.transform.scale(self.back_button_surf, (50, 50))
        self.back_button_rect = self.back_button_surf.get_frect(topleft=(10,10))

        self.rules_text = [
            "• Mỗi ống chứa nhiều lớp nước ngẫu nhiên xếp chồng lên nhau.",
            "• Người chơi có thể rót nước từ một ống này sang một ống khác",
            "   theo các màu giống nhau.",
            "• Người chơi có thể chọn bất kỳ ống nào để đổ nước,",
            "   miễn là tuân theo quy tắc trên."
        ]
    def draw_text(self,text,font,color,pos):
        surface = font.render(text,True,color)
        rect = surface.get_rect(topleft = pos)
        self.display.blit(surface, rect)

    def run(self):
        self.display.fill(BACKGROUND_COLOR)
        self.display.blit(self.back_button_surf, self.back_button_rect)

        header_surf = self.HEADER_FONT.render("RULES", True, "black")
        header_rect = header_surf.get_rect(center=(SCREEN_WIDTH // 2, 80))
        
        self.display.blit(header_surf, header_rect)

        for i, line in enumerate(self.rules_text):
            self.draw_text(line, self.TITLE_FONT, "black", (80, 180 + i * 50))
        
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()
        
        if self.back_button_rect.collidepoint(mouse_pos) and mouse_click[0]:
            self.gameStateManager.set_state('start')

class Level:
    class LevelButton(pygame.sprite.Sprite):
        def __init__(self, number, rect, level, is_opened, puzzle):
            self.number = number
            self.rect = rect
            self.level = level
            self.is_opened = is_opened
            self.puzzle = puzzle
            self.image = pygame.image.load('assets/lock.png')
            self.image = pygame.transform.scale(self.image, (30, 30))

        def draw(self, screen: pygame.surface.Surface):
            pygame.draw.rect(screen, "lightgray", self.rect)
            self.level.draw_text_center(str(self.number), self.level.font, "black", self.rect)
            if not self.is_opened:
                screen.blit(self.image, self.rect)

    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager
        self.level_buttons = []

        self.back_button_surf = pygame.image.load('assets/back.png')
        self.back_button_surf = pygame.transform.scale(self.back_button_surf, (50, 50))
        self.back_button_rect = self.back_button_surf.get_frect(topleft=(10,10))

        self.init_buttons()
        
        self.font = pygame.font.Font(None, 40)

    def init_buttons(self):
        self.level_buttons = []
        button_size = 80
        padding = 30
        cols = 5
        rows = 3

        total_width = cols * button_size + (cols - 1) * padding
        total_height = rows * button_size + (rows - 1) * padding
        start_x = (SCREEN_WIDTH - total_width) // 2
        start_y = (SCREEN_HEIGHT - total_height) // 2
        
        with open(file_data_name) as test_file:
            self.level_data = json.load(test_file)

        num = 1
        for row in range(rows):
            for col in range(cols):
                x = start_x + col * (button_size + padding)
                y = start_y + row * (button_size + padding)
                rect = pygame.Rect(x, y, button_size, button_size)
                level = self.level_data.get(str(num))
                level_button = self.LevelButton(num, rect, self, level[0], level[1])
                self.level_buttons.append(level_button)
                num += 1

    def draw_text_center(self, text, font, color, rect):
        text_surf = font.render(text, True, color)
        text_rect = text_surf.get_rect(center=rect.center)
        self.display.blit(text_surf, text_rect)

    def run(self):
        self.display.fill(BACKGROUND_COLOR)
        self.display.blit(self.back_button_surf, self.back_button_rect)
        
        for level_button in self.level_buttons:
            level_button.draw(self.display)
            
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_just_pressed()

        if mouse_click[0]:
            for level_button in self.level_buttons:
                if level_button.rect.collidepoint(mouse_pos):
                    if level_button.is_opened:
                        self.gameStateManager.set_puzzle(level_button.puzzle, level_button.number)
                        self.gameStateManager.set_state('game_play')

        if self.back_button_rect.collidepoint(mouse_pos) and mouse_click[0]:
            self.gameStateManager.set_state('start')

class GamePlay:
    class Bottle(pygame.sprite.Sprite):
        def __init__(self, data):
            super().__init__()
            self.data = data
            self.rect = pygame.FRect(50, 50, 50, 170)
            self.is_choosen = False
            self.remaining_colors_number = len(data)
            self.is_locked = False
        
        def check_is_filled_with_right_color(self):
            if len(self.data) == 4 and all(color == self.data[0] for color in self.data):
                self.is_locked = True
            else:
                self.is_locked = False
        
        def draw(self, screen):
            if self.is_locked:
                pygame.draw.rect(screen, 'lightgray', self.rect, width=0)
            
            line_width = 3
            left = self.rect.left
            right = self.rect.right
            top = self.rect.top
            bottom = self.rect.bottom

            if self.is_choosen:
                border_color = 'white'
            else:
                border_color = 'black'

            pygame.draw.line(screen, border_color, (left, top), (left, bottom), line_width)
            pygame.draw.line(screen, border_color, (right, top), (right, bottom), line_width)
            pygame.draw.line(screen, border_color, (left, bottom), (right, bottom), line_width)

            if not len(self.data):
                return

            padding = 2
            inner_x = self.rect.x + padding
            inner_width = self.rect.width - 1.5 * padding
            layer_height = 40

            for i in range(len(self.data)):
                color = self.data[i]
                layer_rect = pygame.FRect(
                    inner_x,
                    self.rect.y + self.rect.height - padding/2 - (i + 1) * layer_height,
                    inner_width,
                    layer_height
                )
                pygame.draw.rect(screen, color, layer_rect, border_radius=0)

    def perform_move(self, state, from_idx, to_idx):
        new_state = copy.deepcopy(state)
        from_top_color = new_state[from_idx][-1]
        count = 1
        for k in range(len(new_state[from_idx]) - 2, -1, -1):
            if new_state[from_idx][k] == from_top_color:
                count += 1
            else:
                break
        space = 4 - len(new_state[to_idx])
        pourable = min(count, space)
        for _ in range(pourable):
            new_state[to_idx].append(new_state[from_idx].pop())

        return new_state

    def pour(self, bottle_from, bottle_to):
        if not bottle_from.data:
            return False  # Can't pour from an empty bottle

        if len(bottle_to.data) >= 4:
            return False  # Can't pour into a full bottle

        from_top_color = bottle_from.data[-1]

        # Count how many top layers are the same color
        count = 1
        for i in range(len(bottle_from.data) - 2, -1, -1):
            if bottle_from.data[i] == from_top_color:
                count += 1
            else:
                break

        # Determine how many layers we can actually pour into the target
        space_available = 4 - len(bottle_to.data)
        pourable = min(count, space_available)

        # Check color match or if empty
        if bottle_to.data and bottle_to.data[-1] != from_top_color:
            return False

        # Perform the pour
        for _ in range(pourable):
            bottle_to.data.append(bottle_from.data.pop())

        return True  # Pour successful
    
    def check_is_won(self):
        for bottle in self.list_bottle:
            if not bottle.data:
                continue

            if len(bottle.data) != 4:
                return False

            first_color = bottle.data[0]
            if any(color != first_color for color in bottle.data):
                return False
            
        return True

    def check_is_lost(self):
        for i in range(len(self.list_bottle)):
            for j in range(len(self.list_bottle)):
                if i == j:
                    continue

                from_bottle = self.list_bottle[i]
                to_bottle = self.list_bottle[j]

                if from_bottle.is_locked or to_bottle.is_locked:
                    continue

                if not from_bottle.data or len(to_bottle.data) >= 4:
                    continue

                from_top = from_bottle.data[-1]

                if not to_bottle.data or to_bottle.data[-1] == from_top:
                    return False
        return True

    def heuristic(self, state):
        cost = 0
        for bottle in state:
            if not bottle:
                continue
            top = bottle[-1]
            for color in reversed(bottle):
                if color != top:
                    cost += 1
        return cost
    
    def is_goal(self,state):
        for bottle in state:
            if not bottle:
                continue
            if len(bottle) != 4 or any(color != bottle[0] for color in bottle):
                return False
        return True

    def valid_pour(self,from_bottle, to_bottle):
        if not from_bottle or len(to_bottle) == 4:
            return False
        if not to_bottle:
            return True
        return to_bottle[-1] == from_bottle[-1]

    def do_pour(self,state, i, j):
        state = [b[:] for b in state]  # Deep copy
        from_bottle = state[i]
        to_bottle = state[j]

        color = from_bottle[-1]
        count = 0
        for k in range(len(from_bottle) - 1, -1, -1):
            if from_bottle[k] == color:
                count += 1
            else:
                break

        space = 4 - len(to_bottle)
        move = min(count, space)

        for _ in range(move):
            to_bottle.append(from_bottle.pop())

        return state

    def state_to_tuple(self,state):
        return tuple(tuple(bottle) for bottle in state)

    def solve_astar(self, start_state):
        heap = []
        visited = set()

        start = (self.heuristic(start_state), 0, start_state, [])
        heapq.heappush(heap, start)

        while heap:
            f, g, state, path = heapq.heappop(heap)
            state_id = self.state_to_tuple(state)

            if state_id in visited:
                continue
            visited.add(state_id)

            if self.is_goal(state):
                return path  # Return the move sequence

            for i in range(len(state)):
                for j in range(len(state)):
                    if i == j or not self.valid_pour(state[i], state[j]):
                        continue
                    new_state = self.do_pour(state, i, j)
                    new_path = path + [(i, j)]
                    heapq.heappush(heap, (g + 1 + self.heuristic(new_state), g + 1, new_state, new_path))

        return None  # No solution found

    def __init__(self, display:pygame.rect.Rect, gameStateManager:'GameStateManager'):
        self.display = display
        self.gameStateManager = gameStateManager
        self.selected_bottle = None

        #set up button
        self.text_font = pygame.font.Font('font/Arial.ttf',40)
        
        # self.auto_solve_button_surf = self.text_font.render("Auto Solve", False, 'white')
        self.auto_solve_button_surf = pygame.image.load('assets/aisolve.png').convert_alpha()
        self.auto_solve_button_surf = pygame.transform.scale(self.auto_solve_button_surf, (50, 50))
        self.auto_solve_button_rect = self.auto_solve_button_surf.get_frect(topright=(SCREEN_WIDTH-250, 50))

        # self.reset_button_surf = self.text_font.render("Reset", False, 'white')
        self.reset_button_surf = pygame.image.load('assets/reset.png').convert_alpha()
        self.reset_button_surf = pygame.transform.scale(self.reset_button_surf, (50, 50))
        self.reset_button_rect = self.reset_button_surf.get_frect(topright=(SCREEN_WIDTH-150, 50))

        # self.home_button_surf = self.text_font.render("Home", False, 'white')
        self.home_button_surf = pygame.image.load('assets/home.png').convert_alpha()
        self.home_button_surf = pygame.transform.scale(self.home_button_surf, (50, 50))
        self.home_button_rect = self.home_button_surf.get_frect(topright=(SCREEN_WIDTH-50, 50))

        self.level_number = 0
        #text
        self.level_title_surf = self.text_font.render(f"Level: {self.level_number}", False, 'white')
        self.level_title_rect = self.level_title_surf.get_frect(topleft=(50, 50))
       
        #bottles' positions set up
        self.BOTTLES_PER_ROW = 4
        self.BOTTLE_WIDTH = 50
        self.BOTTLE_HEIGHT = 170
        self.BOTTLE_SPACING_X = 100
        self.BOTTLE_SPACING_Y = 200

        self.is_ai_play = False

        self.init_game()

        #set up thread
        self.solver_thread = None
        self.solver_result = None
        self.is_solving = False


        #Set up for auto solver
        self.move_list = []
        self.move_index = 0
        self.ai_step_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.ai_step_timer, 200)
    
    def start_solver_thread(self, puzzle_data):
        def solve_task():
            self.solver_result = self.solve_astar(puzzle_data)
            self.is_solving = False
            print("SOLUTION FOUND:", self.solver_result)

        self.is_solving = True
        self.solver_thread = threading.Thread(target=solve_task)
        self.solver_thread.start()

    def init_game(self):
        self.level_number = self.gameStateManager.level_number
        #text
        self.level_title_surf = self.text_font.render(f"Level: {self.level_number}", False, 'white')
        self.level_title_rect = self.level_title_surf.get_frect(topleft=(50, 50))

        self.is_ai_play = False
        self.selected_bottle = None
        self.move_list = []
        self.move_index = 0

        self.list_bottle = []
        for puz in copy.deepcopy(self.gameStateManager.puzzle):
            bottle = self.Bottle(puz)
            self.list_bottle.append(bottle)

    def ai_step(self):
        if self.move_index < len(self.move_list):
            from_idx, to_idx = self.move_list[self.move_index]
            self.pour(self.list_bottle[from_idx], self.list_bottle[to_idx])
            self.move_index += 1

    def choose_bottle_logic(self, mouse_pos):
        clicked_bottle = None
        for bottle in self.list_bottle:
            if bottle.rect.collidepoint(mouse_pos):
                clicked_bottle = bottle
                break

        # Case 1: Clicked on empty space or locked bottle — cancel selection
        if clicked_bottle is None or clicked_bottle.is_locked:
            if self.selected_bottle is not None:
                self.selected_bottle.is_choosen = False
                self.selected_bottle = None
        else:
            # Case 2: First selection
            if self.selected_bottle is None:
                self.selected_bottle = clicked_bottle
                self.selected_bottle.is_choosen = True

            # Case 3: Second selection
            elif clicked_bottle != self.selected_bottle:
                if not clicked_bottle.is_locked:
                    self.pour(self.selected_bottle, clicked_bottle)
                    self.selected_bottle.check_is_filled_with_right_color()
                    clicked_bottle.check_is_filled_with_right_color()
                self.selected_bottle.is_choosen = False
                self.selected_bottle = None

            # Case 4: Clicked the same bottle again — unselect
            else:
                self.selected_bottle.is_choosen = False
                self.selected_bottle = None

    def run(self):
        self.display.fill(BACKGROUND_COLOR)
        self.display.blit(self.level_title_surf, self.level_title_rect)
        self.display.blit(self.reset_button_surf, self.reset_button_rect)
        self.display.blit(self.home_button_surf, self.home_button_rect)
        self.display.blit(self.auto_solve_button_surf, self.auto_solve_button_rect)

        mouses = pygame.mouse.get_just_pressed()
        if mouses[0]:
            mouse_pos = pygame.mouse.get_pos()
            if not self.is_ai_play:
                self.choose_bottle_logic(mouse_pos)

            if self.reset_button_rect.collidepoint(mouse_pos):
                self.init_game()
                pygame.display.update()

            if self.home_button_rect.collidepoint(mouse_pos):
                self.gameStateManager.set_state('start')
            
            if self.auto_solve_button_rect.collidepoint(mouse_pos) and not self.is_solving:
                self.is_ai_play = True
                puzzle_data = [bottle.data.copy() for bottle in self.list_bottle]
                self.start_solver_thread(puzzle_data)
        
        if mouses[1]:
            self.gameStateManager.set_state('level_failed')
                

        if self.solver_result is not None:
            self.move_list = self.solver_result
            self.solver_result = None

        self.BOTTLES_PER_ROW = max(len(self.list_bottle)//2+1, 4)
        for row in range((len(self.list_bottle) + self.BOTTLES_PER_ROW - 1) // self.BOTTLES_PER_ROW):
            start_index = row * self.BOTTLES_PER_ROW
            end_index = min(start_index + self.BOTTLES_PER_ROW, len(self.list_bottle))
            bottles_in_row = self.list_bottle[start_index:end_index]
            num_bottles = len(bottles_in_row)

            total_row_width = (num_bottles - 1) * self.BOTTLE_SPACING_X
            start_x = (SCREEN_WIDTH - total_row_width) // 2
            y = 200 + row * self.BOTTLE_SPACING_Y

            for col, bottle in enumerate(bottles_in_row):
                x = start_x + col * self.BOTTLE_SPACING_X
                bottle.rect.x = x
                bottle.rect.y = y
                bottle.check_is_filled_with_right_color()
                bottle.draw(self.display)
        

        if self.is_solving:
            colored_surf = pygame.Surface((200, 100))
            colored_surf.fill((0, 200, 255))
            colored_rect = colored_surf.get_frect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            colored_surf.set_alpha(128)
            colored_surf = colored_surf.convert_alpha()

            loading_surf = self.text_font.render("Solving...", False, 'white')
            loading_rect = loading_surf.get_frect(center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            
            self.display.blit(colored_surf, colored_rect)
            self.display.blit(loading_surf, loading_rect)

        if self.check_is_won():
            self.gameStateManager.set_state('level_completed')
            self.gameStateManager.open_next_level()
        elif self.check_is_won():
            self.gameStateManager.set_state('level_failed')

class Start:
    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager

        self.HEADER_FONT = pygame.font.Font("font/Arial.ttf", 150)
        self.TITLE_FONT = pygame.font.Font("font/Arial.ttf", 40)

        self.play_button = pygame.Rect(0,0,140,60)
        self.play_button.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

        self.rule_button = pygame.Rect(0,0,140,60)
        self.rule_button.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80)

    def draw_text(self, text, font, color, center):
        surface = font.render(text,True,color)
        rect = surface.get_rect(center = center)
        self.display.blit(surface,rect)
    
    def run(self):
        self.display.fill(BACKGROUND_COLOR)
        self.draw_text("SORTPUZ",self.HEADER_FONT, "white", (SCREEN_WIDTH // 2, 200))

        pygame.draw.rect(self.display,"black",self.play_button,border_radius=10)
        self.draw_text("Play",self.TITLE_FONT,"white", self.play_button.center)

        pygame.draw.rect(self.display, "black", self.rule_button, border_radius= 10)
        self.draw_text("Rule", self.TITLE_FONT,"white",self.rule_button.center)


        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        if self.play_button.collidepoint(mouse_pos) and mouse_click[0]:
            self.gameStateManager.set_state('level')
        if self.rule_button.collidepoint(mouse_pos) and mouse_click[0]:
            self.gameStateManager.set_state('rule')

class GameStateManager:
    def __init__(self, currentState, game:'Game'):
        self.currentState = currentState
        self.game = game
        self.puzzle = []
        self.level_number = 1
    
    def set_puzzle(self, puzzle, level_number):
        self.puzzle = puzzle
        self.level_number = level_number
        self.game.set_puzzle()
    
    def set_up_next_level(self):
        with open(file_data_name) as test_file:
            data = json.load(test_file)
        self.level_number = self.level_number + 1
        self.puzzle = data[str(self.level_number)][1]
        self.game.set_puzzle()
    
    def open_next_level(self):
        with open(file_data_name) as test_file:
            data = json.load(test_file)
        
        if self.level_number < 15:
            data[str(self.level_number+1)][0] = True

        with open(file_data_name, 'w') as test_file:
            json.dump(data, test_file)
        
        self.game.reset_levels_list()
    
    def get_state(self):
        return self.currentState

    def set_state(self, state):
        self.currentState = state

if __name__ == '__main__':
    game = Game()
    game.run()