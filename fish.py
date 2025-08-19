import random
import math
import numpy as np
import logging
import time
from constants import *
from utils import log_fish_behavior

class Fish:
    def __init__(self, x, y, dx=0, dy=0):
        self.x = x
        self.y = y
        self.dx = dx if dx != 0 else random.choice([-1, 0, 1])
        self.dy = dy if dy != 0 else random.choice([-1, 0, 1])
        self.energy = 100
        self.age = 0
        self.gender = random.choice(['male', 'female'])
        self.id = id(self)  # ユニークID
        
        # 方向を正規化
        self._normalize_direction()
        
        # ログ出力
        log_fish_behavior(self.id, "CREATED", f"Position=({x}, {y}), Direction=({self.dx:.2f}, {self.dy:.2f}), Gender={self.gender}")
    
    def _normalize_direction(self):
        """方向ベクトルを正規化する"""
        length = math.sqrt(self.dx**2 + self.dy**2)
        if length > 0:
            self.dx /= length
            self.dy /= length
            log_fish_behavior(self.id, "NORMALIZE", f"Direction normalized to ({self.dx:.2f}, {self.dy:.2f})")
    
    def get_position(self):
        """現在位置を返す"""
        return (self.x, self.y)
    
    def get_direction(self):
        """現在の方向を返す"""
        return (self.dx, self.dy)
    
    def get_vision_area(self):
        """視界範囲の座標を返す（前方・斜め前の3方向）"""
        vision_coords = []
        
        # 現在の方向に基づいて前方・斜め前の3方向を計算
        if self.dx == 0 and self.dy == 0:
            # 方向が未設定の場合はランダムに設定
            self.dx = random.choice([-1, 0, 1])
            self.dy = random.choice([-1, 0, 1])
            self._normalize_direction()
            log_fish_behavior(self.id, "RANDOM_DIRECTION", f"Set random direction to ({self.dx:.2f}, {self.dy:.2f})")
        
        # 前方
        front_x = int(self.x + self.dx * VISION_RANGE)
        front_y = int(self.y + self.dy * VISION_RANGE)
        vision_coords.append((front_x, front_y))
        
        # 斜め前（左）
        left_x = int(self.x + (self.dx - self.dy) * VISION_RANGE)
        left_y = int(self.y + (self.dy + self.dx) * VISION_RANGE)
        vision_coords.append((left_x, left_y))
        
        # 斜め前（右）
        right_x = int(self.x + (self.dx + self.dy) * VISION_RANGE)
        right_y = int(self.y + (self.dy - self.dx) * VISION_RANGE)
        vision_coords.append((right_x, right_y))
        
        log_fish_behavior(self.id, "VISION_AREA", f"Vision coords: {vision_coords}")
        return vision_coords
    
    def calculate_separation(self, nearby_fish):
        """分離行動を計算"""
        if not nearby_fish:
            log_fish_behavior(self.id, "SEPARATION", "No nearby fish")
            return 0, 0
        
        separation_x = 0
        separation_y = 0
        
        for fish in nearby_fish:
            # 距離を計算
            dx = self.x - fish.x
            dy = self.y - fish.y
            distance = math.sqrt(dx**2 + dy**2)
            
            if distance > 0:
                # 距離が近いほど強い分離力
                force = 1.0 / distance
                separation_x += dx * force
                separation_y += dy * force
        
        log_fish_behavior(self.id, "SEPARATION", f"Force=({separation_x:.2f}, {separation_y:.2f}), Nearby={len(nearby_fish)}")
        return separation_x, separation_y
    
    def calculate_alignment(self, nearby_fish):
        """整列行動を計算"""
        if not nearby_fish:
            log_fish_behavior(self.id, "ALIGNMENT", "No nearby fish")
            return 0, 0
        
        avg_dx = sum(fish.dx for fish in nearby_fish) / len(nearby_fish)
        avg_dy = sum(fish.dy for fish in nearby_fish) / len(nearby_fish)
        
        log_fish_behavior(self.id, "ALIGNMENT", f"Average direction=({avg_dx:.2f}, {avg_dy:.2f}), Nearby={len(nearby_fish)}")
        return avg_dx, avg_dy
    
    def calculate_cohesion(self, nearby_fish):
        """結合行動を計算"""
        if not nearby_fish:
            log_fish_behavior(self.id, "COHESION", "No nearby fish")
            return 0, 0
        
        # 群れの中心を計算
        center_x = sum(fish.x for fish in nearby_fish) / len(nearby_fish)
        center_y = sum(fish.y for fish in nearby_fish) / len(nearby_fish)
        
        # 中心に向かう方向
        cohesion_x = center_x - self.x
        cohesion_y = center_y - self.y
        
        log_fish_behavior(self.id, "COHESION", f"Center=({center_x:.1f}, {center_y:.1f}), Force=({cohesion_x:.2f}, {cohesion_y:.2f})")
        return cohesion_x, cohesion_y
    
    def update(self, nearby_fish):
        """メダカの状態を更新"""
        start_time = time.time()
        
        # 群れ行動を計算
        sep_x, sep_y = self.calculate_separation(nearby_fish)
        align_x, align_y = self.calculate_alignment(nearby_fish)
        coh_x, coh_y = self.calculate_cohesion(nearby_fish)
        
        # 重み付けで合成
        new_dx = (sep_x * SEPARATION_WEIGHT + 
                 align_x * ALIGNMENT_WEIGHT + 
                 coh_x * COHESION_WEIGHT + 
                 random.uniform(-1, 1) * RANDOM_WEIGHT +
                 self.dx * INERTIA_WEIGHT)
        
        new_dy = (sep_y * SEPARATION_WEIGHT + 
                 align_y * ALIGNMENT_WEIGHT + 
                 coh_y * COHESION_WEIGHT + 
                 random.uniform(-1, 1) * RANDOM_WEIGHT +
                 self.dy * INERTIA_WEIGHT)
        
        # 方向を正規化
        length = math.sqrt(new_dx**2 + new_dy**2)
        if length > 0:
            self.dx = new_dx / length
            self.dy = new_dy / length
        
        # 移動前の位置を記録
        old_x, old_y = self.x, self.y
        
        # 移動
        self.x += self.dx * FISH_SPEED
        self.y += self.dy * FISH_SPEED
        
        # 境界処理（トーラス状の世界）
        if self.x < 0 or self.x >= SCREEN_WIDTH or self.y < 0 or self.y >= SCREEN_HEIGHT:
            self.x = self.x % SCREEN_WIDTH
            self.y = self.y % SCREEN_HEIGHT
            log_fish_behavior(self.id, "BOUNDARY_WRAP", f"Wrapped from ({old_x:.1f}, {old_y:.1f}) to ({self.x:.1f}, {self.y:.1f})")
        
        # 年齢と体力の更新
        self.age += 1
        self.energy = max(0, self.energy - 0.1)
        
        # ログ出力
        duration = time.time() - start_time
        log_fish_behavior(self.id, "UPDATE", f"Position=({self.x:.1f}, {self.y:.1f}), Direction=({self.dx:.2f}, {self.dy:.2f}), Age={self.age}, Energy={self.energy:.1f}, Duration={duration:.4f}s")
    
    def draw(self, screen):
        """メダカを描画"""
        import pygame
        
        # メダカの色（性別によって少し変える）
        color = LIGHT_BLUE if self.gender == 'male' else BLUE
        
        # メダカの位置
        pos_x = int(self.x)
        pos_y = int(self.y)
        
        # メダカの向きに基づいて三角形を描画
        if self.dx != 0 or self.dy != 0:
            # 方向ベクトルを正規化
            length = math.sqrt(self.dx**2 + self.dy**2)
            if length > 0:
                dx_norm = self.dx / length
                dy_norm = self.dy / length
                
                # 三角形の頂点を計算
                tip_x = pos_x + dx_norm * FISH_SIZE
                tip_y = pos_y + dy_norm * FISH_SIZE
                
                # 三角形の底辺の点
                perp_x = -dy_norm * FISH_SIZE * 0.5
                perp_y = dx_norm * FISH_SIZE * 0.5
                
                left_x = pos_x + perp_x
                left_y = pos_y + perp_y
                right_x = pos_x - perp_x
                right_y = pos_y - perp_y
                
                # 三角形を描画
                pygame.draw.polygon(screen, color, [
                    (tip_x, tip_y),
                    (left_x, left_y),
                    (right_x, right_y)
                ])
        else:
            # 方向が未設定の場合は円で描画
            pygame.draw.circle(screen, color, (pos_x, pos_y), FISH_SIZE)
