import pygame
import logging
import time
from constants import *
from utils import log_world_event, log_performance

class World:
    def __init__(self, width=SCREEN_WIDTH, height=SCREEN_HEIGHT):
        self.width = width
        self.height = height
        self.screen = None
        self.clock = None
        self.font = None
        self.background_color = BLACK
        self.world_id = id(self)  # 世界のユニークID
        self.logger = logging.getLogger('FishSimulator.World')
        
        # パラメータ調整用
        self.separation_weight = SEPARATION_WEIGHT
        self.alignment_weight = ALIGNMENT_WEIGHT
        self.cohesion_weight = COHESION_WEIGHT
        self.random_weight = RANDOM_WEIGHT
        self.inertia_weight = INERTIA_WEIGHT
        
        # UI表示用
        self.show_info = True
        self.show_vision = False
        
        # 統計情報
        self.frame_count = 0
        self.start_time = None
        
        self.logger.info(f"World {self.world_id} created with size {width}x{height}")
    
    def initialize(self):
        """pygameを初期化"""
        start_time = time.time()
        
        try:
            pygame.init()
            self.screen = pygame.display.set_mode((self.width, self.height))
            pygame.display.set_caption("Fish School Simulator")
            self.clock = pygame.time.Clock()
            self.font = pygame.font.Font(None, 24)
            
            duration = time.time() - start_time
            log_performance("Pygame initialization", duration)
            self.logger.info(f"Pygame initialized successfully in {duration:.4f}s")
            
            self.start_time = time.time()
            log_world_event("INITIALIZED", f"Screen size: {self.width}x{self.height}")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize pygame: {e}")
            raise
    
    def handle_events(self):
        """イベントを処理"""
        start_time = time.time()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.logger.info("Quit event received")
                log_world_event("QUIT", "Window close requested")
                return False
            
            elif event.type == pygame.KEYDOWN:
                self._handle_keydown_event(event)
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                result = self._handle_mouse_event(event)
                if result:
                    return result
        
        duration = time.time() - start_time
        log_performance("Event handling", duration)
        return True
    
    def _handle_keydown_event(self, event):
        """キーダウンイベントを処理"""
        if event.key == pygame.K_ESCAPE:
            self.logger.info("Escape key pressed")
            log_world_event("ESCAPE", "Escape key pressed")
            return False
        elif event.key == pygame.K_i:
            self.show_info = not self.show_info
            self.logger.info(f"Info display toggled: {self.show_info}")
            log_world_event("TOGGLE_INFO", f"Info display: {self.show_info}")
        # 視界表示切り替え (V)
        elif event.key == pygame.K_v:
            self.show_vision = not self.show_vision
            self.logger.info(f"Vision display toggled: {self.show_vision}")
            log_world_event("TOGGLE_VISION", f"Vision display: {self.show_vision}")
        # 分離パラメータ (Q/W)
        elif event.key == pygame.K_q:
            self.separation_weight = max(0, self.separation_weight - 0.1)
            self.logger.info(f"Separation weight decreased to {self.separation_weight:.1f}")
            log_world_event("PARAMETER_CHANGE", f"Separation weight: {self.separation_weight:.1f}")
        elif event.key == pygame.K_w:
            self.separation_weight += 0.1
            self.logger.info(f"Separation weight increased to {self.separation_weight:.1f}")
            log_world_event("PARAMETER_CHANGE", f"Separation weight: {self.separation_weight:.1f}")
        # 整列パラメータ (A/S)
        elif event.key == pygame.K_a:
            self.alignment_weight = max(0, self.alignment_weight - 0.1)
            self.logger.info(f"Alignment weight decreased to {self.alignment_weight:.1f}")
            log_world_event("PARAMETER_CHANGE", f"Alignment weight: {self.alignment_weight:.1f}")
        elif event.key == pygame.K_s:
            self.alignment_weight += 0.1
            self.logger.info(f"Alignment weight increased to {self.alignment_weight:.1f}")
            log_world_event("PARAMETER_CHANGE", f"Alignment weight: {self.alignment_weight:.1f}")
        # 結合パラメータ (Z/X)
        elif event.key == pygame.K_z:
            self.cohesion_weight = max(0, self.cohesion_weight - 0.1)
            self.logger.info(f"Cohesion weight decreased to {self.cohesion_weight:.1f}")
            log_world_event("PARAMETER_CHANGE", f"Cohesion weight: {self.cohesion_weight:.1f}")
        elif event.key == pygame.K_x:
            self.cohesion_weight += 0.1
            self.logger.info(f"Cohesion weight increased to {self.cohesion_weight:.1f}")
            log_world_event("PARAMETER_CHANGE", f"Cohesion weight: {self.cohesion_weight:.1f}")
        # ランダムパラメータ (C/B)
        elif event.key == pygame.K_c:
            self.random_weight = max(0, self.random_weight - 0.05)
            self.logger.info(f"Random weight decreased to {self.random_weight:.2f}")
            log_world_event("PARAMETER_CHANGE", f"Random weight: {self.random_weight:.2f}")
        elif event.key == pygame.K_b:
            self.random_weight += 0.05
            self.logger.info(f"Random weight increased to {self.random_weight:.2f}")
            log_world_event("PARAMETER_CHANGE", f"Random weight: {self.random_weight:.2f}")
        # 慣性パラメータ (D/F)
        elif event.key == pygame.K_d:
            self.inertia_weight = max(0, self.inertia_weight - 0.1)
            self.logger.info(f"Inertia weight decreased to {self.inertia_weight:.1f}")
            log_world_event("PARAMETER_CHANGE", f"Inertia weight: {self.inertia_weight:.1f}")
        elif event.key == pygame.K_f:
            self.inertia_weight += 0.1
            self.logger.info(f"Inertia weight increased to {self.inertia_weight:.1f}")
            log_world_event("PARAMETER_CHANGE", f"Inertia weight: {self.inertia_weight:.1f}")
        # リセット機能 (R)
        elif event.key == pygame.K_r:
            self.separation_weight = SEPARATION_WEIGHT
            self.alignment_weight = ALIGNMENT_WEIGHT
            self.cohesion_weight = COHESION_WEIGHT
            self.random_weight = RANDOM_WEIGHT
            self.inertia_weight = INERTIA_WEIGHT
            self.logger.info("Parameters reset to default values")
            log_world_event("PARAMETER_RESET", "All parameters reset to default")
    
    def _handle_mouse_event(self, event):
        """マウスイベントを処理"""
        if event.button == 1:  # 左クリック
            x, y = event.pos
            self.logger.info(f"Mouse click at position ({x}, {y})")
            log_world_event("MOUSE_CLICK", f"Position: ({x}, {y})")
            return ("add_fish", x, y)
        return None
    
    def draw_background(self):
        """背景を描画"""
        start_time = time.time()
        self.screen.fill(self.background_color)
        duration = time.time() - start_time
        log_performance("Background drawing", duration)
    
    def draw_info(self, school):
        """情報を描画"""
        if not self.show_info:
            return
        
        start_time = time.time()
        
        # 基本情報
        info_lines = [
            f"Fish Count: {school.get_fish_count()}",
            f"School Density: {school.get_school_density():.3f}",
            "",
            "Parameters:",
            f"Separation: {self.separation_weight:.1f} (Q/W)",
            f"Alignment: {self.alignment_weight:.1f} (A/S)",
            f"Cohesion: {self.cohesion_weight:.1f} (Z/X)",
            f"Random: {self.random_weight:.2f} (C/B)",
            f"Inertia: {self.inertia_weight:.1f} (D/F)",
            "",
            "Controls:",
            "I - Toggle Info",
            "V - Toggle Vision",
            "R - Reset Parameters",
            "Mouse - Add Fish",
            "ESC - Quit"
        ]
        
        y_offset = 10
        for line in info_lines:
            if line:
                text_surface = self.font.render(line, True, WHITE)
                self.screen.blit(text_surface, (10, y_offset))
            y_offset += 20
        
        duration = time.time() - start_time
        log_performance("Info drawing", duration)
    
    def draw_vision_areas(self, school):
        """視界範囲を描画（前方のマスをざっくり表示）"""
        if not self.show_vision:
            return
        
        start_time = time.time()
        
        for fish in school.get_all_fish():
            fish_x, fish_y = fish.get_position()
            dx, dy = fish.get_direction()
            
            # 方向を8方向に正規化
            if abs(dx) > abs(dy):
                direction_x = 1 if dx > 0 else -1
                direction_y = 0
            elif abs(dy) > abs(dx):
                direction_x = 0
                direction_y = 1 if dy > 0 else -1
            else:
                direction_x = 1 if dx > 0 else -1
                direction_y = 1 if dy > 0 else -1
            
            # 前方のマスを小さな点で表示
            for distance in range(1, min(VISION_RANGE, 20) + 1):  # 表示は20マスまでに制限
                # 前方
                check_x = fish_x + direction_x * distance
                check_y = fish_y + direction_y * distance
                pygame.draw.circle(self.screen, GREEN, (int(check_x), int(check_y)), 1)
                
                # 斜め前（左右）も表示
                if direction_x != 0 and direction_y != 0:
                    check_left_x = fish_x + direction_x * distance
                    check_left_y = fish_y
                    check_right_x = fish_x
                    check_right_y = fish_y + direction_y * distance
                elif direction_x != 0:
                    check_left_x = fish_x + direction_x * distance
                    check_left_y = fish_y - distance
                    check_right_x = fish_x + direction_x * distance
                    check_right_y = fish_y + distance
                else:
                    check_left_x = fish_x - distance
                    check_left_y = fish_y + direction_y * distance
                    check_right_x = fish_x + distance
                    check_right_y = fish_y + direction_y * distance
                
                pygame.draw.circle(self.screen, GREEN, (int(check_left_x), int(check_left_y)), 1)
                pygame.draw.circle(self.screen, GREEN, (int(check_right_x), int(check_right_y)), 1)
        
        duration = time.time() - start_time
        log_performance("Vision areas drawing", duration)
    
    def draw_school_center(self, school):
        """群れの中心を描画"""
        start_time = time.time()
        
        center_x, center_y = school.get_school_center()
        pygame.draw.circle(self.screen, RED, (int(center_x), int(center_y)), 5)
        
        duration = time.time() - start_time
        log_performance("School center drawing", duration)
    
    def update_display(self):
        """画面を更新"""
        start_time = time.time()
        pygame.display.flip()
        duration = time.time() - start_time
        log_performance("Display update", duration)
        
        self.frame_count += 1
        if self.frame_count % 60 == 0:  # 1秒ごと
            self._log_performance_stats()
    
    def _log_performance_stats(self):
        """パフォーマンス統計をログに記録"""
        if self.start_time:
            elapsed_time = time.time() - self.start_time
            fps = self.get_fps()
            self.logger.info(f"Performance: FPS={fps:.1f}, Frames={self.frame_count}, Elapsed={elapsed_time:.1f}s")
            log_world_event("PERFORMANCE", f"FPS={fps:.1f}, Frames={self.frame_count}")
    
    def get_fps(self):
        """FPSを取得"""
        return self.clock.get_fps()
    
    def tick(self):
        """フレームレートを制御"""
        self.clock.tick(FPS)
    
    def quit(self):
        """pygameを終了"""
        self.logger.info("Quitting pygame")
        log_world_event("QUIT", "Pygame shutdown")
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
        old_params = self.get_parameters()
        
        self.separation_weight = params.get('separation_weight', self.separation_weight)
        self.alignment_weight = params.get('alignment_weight', self.alignment_weight)
        self.cohesion_weight = params.get('cohesion_weight', self.cohesion_weight)
        self.random_weight = params.get('random_weight', self.random_weight)
        self.inertia_weight = params.get('inertia_weight', self.inertia_weight)
        
        self.logger.info(f"Parameters updated: {params}")
        log_world_event("PARAMETERS_SET", f"New parameters: {params}")
    
    def get_world_statistics(self):
        """世界の統計情報を取得"""
        if self.start_time:
            elapsed_time = time.time() - self.start_time
        else:
            elapsed_time = 0
        
        stats = {
            'frame_count': self.frame_count,
            'elapsed_time': elapsed_time,
            'fps': self.get_fps(),
            'parameters': self.get_parameters(),
            'display_settings': {
                'show_info': self.show_info,
                'show_vision': self.show_vision
            }
        }
        
        self.logger.debug(f"World statistics: {stats}")
        return stats
