import random
import math
import logging
import time
from fish import Fish
from constants import *
from utils import log_school_state, log_performance

class School:
    def __init__(self, fish_count=DEFAULT_FISH_COUNT):
        self.fish_list = []
        self.fish_count = fish_count
        self.school_id = id(self)  # 群れのユニークID
        self.logger = logging.getLogger('FishSimulator.School')
        
        self.logger.info(f"School {self.school_id} created with {fish_count} fish")
        self.initialize_fish()
    
    def initialize_fish(self):
        """メダカを初期化"""
        start_time = time.time()
        
        for i in range(self.fish_count):
            x = random.randint(0, SCREEN_WIDTH - 1)
            y = random.randint(0, SCREEN_HEIGHT - 1)
            fish = Fish(x, y)
            self.fish_list.append(fish)
            self.logger.debug(f"Fish {fish.id} added at position ({x}, {y})")
        
        duration = time.time() - start_time
        log_performance("School initialization", duration)
        self.logger.info(f"Initialized {self.fish_count} fish in {duration:.4f}s")
    
    def get_nearby_fish(self, fish, max_distance=50):
        """指定されたメダカの近くにいるメダカを取得"""
        start_time = time.time()
        nearby_fish = []
        
        for other_fish in self.fish_list:
            if other_fish != fish:
                # 距離を計算（トーラス状の世界を考慮）
                dx = abs(other_fish.x - fish.x)
                dy = abs(other_fish.y - fish.y)
                
                # トーラス状の世界での最短距離を計算
                dx = min(dx, SCREEN_WIDTH - dx)
                dy = min(dy, SCREEN_HEIGHT - dy)
                
                distance = math.sqrt(dx**2 + dy**2)
                
                if distance <= max_distance:
                    nearby_fish.append(other_fish)
        
        duration = time.time() - start_time
        log_performance(f"Get nearby fish for {fish.id}", duration)
        self.logger.debug(f"Fish {fish.id} has {len(nearby_fish)} nearby fish within {max_distance} distance")
        
        return nearby_fish
    
    def get_fish_in_vision(self, fish):
        """メダカの視界範囲内のメダカを取得"""
        start_time = time.time()
        vision_coords = fish.get_vision_area()
        fish_in_vision = []
        
        for other_fish in self.fish_list:
            if other_fish != fish:
                other_pos = other_fish.get_position()
                if other_pos in vision_coords:
                    fish_in_vision.append(other_fish)
        
        duration = time.time() - start_time
        log_performance(f"Get fish in vision for {fish.id}", duration)
        self.logger.debug(f"Fish {fish.id} sees {len(fish_in_vision)} fish in vision area")
        
        return fish_in_vision
    
    def update_all_fish(self):
        """全てのメダカを更新"""
        start_time = time.time()
        
        for fish in self.fish_list:
            # 視界範囲内のメダカを取得
            nearby_fish = self.get_fish_in_vision(fish)
            
            # メダカを更新
            fish.update(nearby_fish)
        
        duration = time.time() - start_time
        log_performance("Update all fish", duration)
        
        # 群れの状態をログに記録
        density = self.get_school_density()
        center = self.get_school_center()
        log_school_state(self.school_id, self.fish_count, density, center)
        
        self.logger.debug(f"Updated all {self.fish_count} fish in {duration:.4f}s")
    
    def add_fish(self, x=None, y=None):
        """新しいメダカを追加"""
        if x is None:
            x = random.randint(0, SCREEN_WIDTH - 1)
        if y is None:
            y = random.randint(0, SCREEN_HEIGHT - 1)
        
        fish = Fish(x, y)
        self.fish_list.append(fish)
        self.fish_count += 1
        
        self.logger.info(f"Added fish {fish.id} at position ({x}, {y}). Total fish: {self.fish_count}")
    
    def remove_fish(self, fish):
        """メダカを削除"""
        if fish in self.fish_list:
            self.fish_list.remove(fish)
            self.fish_count -= 1
            self.logger.info(f"Removed fish {fish.id}. Total fish: {self.fish_count}")
        else:
            self.logger.warning(f"Attempted to remove fish {fish.id} that is not in the school")
    
    def get_fish_count(self):
        """メダカの数を取得"""
        return self.fish_count
    
    def get_all_fish(self):
        """全てのメダカを取得"""
        return self.fish_list
    
    def get_fish_positions(self):
        """全てのメダカの位置を取得"""
        return [fish.get_position() for fish in self.fish_list]
    
    def get_fish_directions(self):
        """全てのメダカの方向を取得"""
        return [fish.get_direction() for fish in self.fish_list]
    
    def draw_all_fish(self, screen):
        """全てのメダカを描画"""
        start_time = time.time()
        
        for fish in self.fish_list:
            fish.draw(screen)
        
        duration = time.time() - start_time
        log_performance("Draw all fish", duration)
    
    def get_school_center(self):
        """群れの中心を計算"""
        if not self.fish_list:
            return (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        
        avg_x = sum(fish.x for fish in self.fish_list) / len(self.fish_list)
        avg_y = sum(fish.y for fish in self.fish_list) / len(self.fish_list)
        
        return (avg_x, avg_y)
    
    def get_school_density(self):
        """群れの密度を計算"""
        if not self.fish_list:
            return 0
        
        # 群れの中心を計算
        center_x, center_y = self.get_school_center()
        
        # 中心からの平均距離を計算
        total_distance = 0
        for fish in self.fish_list:
            dx = fish.x - center_x
            dy = fish.y - center_y
            distance = math.sqrt(dx**2 + dy**2)
            total_distance += distance
        
        avg_distance = total_distance / len(self.fish_list)
        
        # 密度は距離の逆数（距離が小さいほど密度が高い）
        density = 1.0 / (avg_distance + 1)  # +1でゼロ除算を防ぐ
        
        return density
    
    def get_school_statistics(self):
        """群れの統計情報を取得"""
        if not self.fish_list:
            return {
                'count': 0,
                'density': 0,
                'center': (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),
                'avg_energy': 0,
                'avg_age': 0,
                'gender_ratio': {'male': 0, 'female': 0}
            }
        
        # 基本統計
        total_energy = sum(fish.energy for fish in self.fish_list)
        total_age = sum(fish.age for fish in self.fish_list)
        male_count = sum(1 for fish in self.fish_list if fish.gender == 'male')
        female_count = len(self.fish_list) - male_count
        
        stats = {
            'count': self.fish_count,
            'density': self.get_school_density(),
            'center': self.get_school_center(),
            'avg_energy': total_energy / self.fish_count,
            'avg_age': total_age / self.fish_count,
            'gender_ratio': {
                'male': male_count / self.fish_count,
                'female': female_count / self.fish_count
            }
        }
        
        self.logger.debug(f"School statistics: {stats}")
        return stats
