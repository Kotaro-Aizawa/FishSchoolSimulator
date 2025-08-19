import random
import math
from fish import Fish
from constants import *

class School:
    def __init__(self, fish_count=DEFAULT_FISH_COUNT):
        self.fish_list = []
        self.fish_count = fish_count
        self.initialize_fish()
    
    def initialize_fish(self):
        """メダカを初期化"""
        for _ in range(self.fish_count):
            x = random.randint(0, SCREEN_WIDTH - 1)
            y = random.randint(0, SCREEN_HEIGHT - 1)
            fish = Fish(x, y)
            self.fish_list.append(fish)
    
    def get_nearby_fish(self, fish, max_distance=50):
        """指定されたメダカの近くにいるメダカを取得"""
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
        
        return nearby_fish
    
    def get_fish_in_vision(self, fish):
        """メダカの視界範囲内のメダカを取得"""
        vision_coords = fish.get_vision_area()
        fish_in_vision = []
        
        for other_fish in self.fish_list:
            if other_fish != fish:
                other_pos = other_fish.get_position()
                if other_pos in vision_coords:
                    fish_in_vision.append(other_fish)
        
        return fish_in_vision
    
    def update_all_fish(self):
        """全てのメダカを更新"""
        for fish in self.fish_list:
            # 視界範囲内のメダカを取得
            nearby_fish = self.get_fish_in_vision(fish)
            
            # メダカを更新
            fish.update(nearby_fish)
    
    def add_fish(self, x=None, y=None):
        """新しいメダカを追加"""
        if x is None:
            x = random.randint(0, SCREEN_WIDTH - 1)
        if y is None:
            y = random.randint(0, SCREEN_HEIGHT - 1)
        
        fish = Fish(x, y)
        self.fish_list.append(fish)
        self.fish_count += 1
    
    def remove_fish(self, fish):
        """メダカを削除"""
        if fish in self.fish_list:
            self.fish_list.remove(fish)
            self.fish_count -= 1
    
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
        for fish in self.fish_list:
            fish.draw(screen)
    
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
