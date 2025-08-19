import pygame
from constants import *

class World:
    def __init__(self, width=SCREEN_WIDTH, height=SCREEN_HEIGHT):
        self.width = width
        self.height = height
        self.screen = None
        self.clock = None
        self.font = None
        self.background_color = BLACK
        
        # パラメータ調整用
        self.separation_weight = SEPARATION_WEIGHT
        self.alignment_weight = ALIGNMENT_WEIGHT
        self.cohesion_weight = COHESION_WEIGHT
        self.random_weight = RANDOM_WEIGHT
        self.inertia_weight = INERTIA_WEIGHT
        
        # UI表示用
        self.show_info = True
        self.show_vision = False
    
    def initialize(self):
        """pygameを初期化"""
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Fish School Simulator")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)
    
    def handle_events(self):
        """イベントを処理"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_i:
                    self.show_info = not self.show_info
                elif event.key == pygame.K_v:
                    self.show_vision = not self.show_vision
                elif event.key == pygame.K_1:
                    self.separation_weight = max(0, self.separation_weight - 0.1)
                elif event.key == pygame.K_2:
                    self.separation_weight += 0.1
                elif event.key == pygame.K_3:
                    self.alignment_weight = max(0, self.alignment_weight - 0.1)
                elif event.key == pygame.K_4:
                    self.alignment_weight += 0.1
                elif event.key == pygame.K_5:
                    self.cohesion_weight = max(0, self.cohesion_weight - 0.1)
                elif event.key == pygame.K_6:
                    self.cohesion_weight += 0.1
                elif event.key == pygame.K_7:
                    self.random_weight = max(0, self.random_weight - 0.05)
                elif event.key == pygame.K_8:
                    self.random_weight += 0.05
                elif event.key == pygame.K_9:
                    self.inertia_weight = max(0, self.inertia_weight - 0.1)
                elif event.key == pygame.K_0:
                    self.inertia_weight += 0.1
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # 左クリック
                    # クリックした位置にメダカを追加
                    x, y = event.pos
                    return ("add_fish", x, y)
        
        return True
    
    def draw_background(self):
        """背景を描画"""
        self.screen.fill(self.background_color)
    
    def draw_info(self, school):
        """情報を描画"""
        if not self.show_info:
            return
        
        # 基本情報
        info_lines = [
            f"Fish Count: {school.get_fish_count()}",
            f"School Density: {school.get_school_density():.3f}",
            f"Separation: {self.separation_weight:.1f} (1/2)",
            f"Alignment: {self.alignment_weight:.1f} (3/4)",
            f"Cohesion: {self.cohesion_weight:.1f} (5/6)",
            f"Random: {self.random_weight:.2f} (7/8)",
            f"Inertia: {self.inertia_weight:.1f} (9/0)",
            "",
            "Controls:",
            "I - Toggle Info",
            "V - Toggle Vision",
            "Mouse - Add Fish",
            "ESC - Quit"
        ]
        
        y_offset = 10
        for line in info_lines:
            if line:
                text_surface = self.font.render(line, True, WHITE)
                self.screen.blit(text_surface, (10, y_offset))
            y_offset += 20
    
    def draw_vision_areas(self, school):
        """視界範囲を描画"""
        if not self.show_vision:
            return
        
        for fish in school.get_all_fish():
            vision_coords = fish.get_vision_area()
            for coord in vision_coords:
                x, y = coord
                # 視界範囲を小さな点で表示
                pygame.draw.circle(self.screen, GREEN, (x, y), 2)
    
    def draw_school_center(self, school):
        """群れの中心を描画"""
        center_x, center_y = school.get_school_center()
        pygame.draw.circle(self.screen, RED, (int(center_x), int(center_y)), 5)
    
    def update_display(self):
        """画面を更新"""
        pygame.display.flip()
    
    def get_fps(self):
        """FPSを取得"""
        return self.clock.get_fps()
    
    def tick(self):
        """フレームレートを制御"""
        self.clock.tick(FPS)
    
    def quit(self):
        """pygameを終了"""
        pygame.quit()
    
    def get_parameters(self):
        """現在のパラメータを取得"""
        return {
            'separation_weight': self.separation_weight,
            'alignment_weight': self.alignment_weight,
            'cohesion_weight': self.cohesion_weight,
            'random_weight': self.random_weight,
            'inertia_weight': self.inertia_weight
        }
    
    def set_parameters(self, params):
        """パラメータを設定"""
        self.separation_weight = params.get('separation_weight', self.separation_weight)
        self.alignment_weight = params.get('alignment_weight', self.alignment_weight)
        self.cohesion_weight = params.get('cohesion_weight', self.cohesion_weight)
        self.random_weight = params.get('random_weight', self.random_weight)
        self.inertia_weight = params.get('inertia_weight', self.inertia_weight)
