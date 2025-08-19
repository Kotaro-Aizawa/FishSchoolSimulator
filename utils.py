import math
import random
import logging
import time
from constants import *

# ログ設定
def setup_logging():
    """ログ設定を初期化"""
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('fish_simulator.log', encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger('FishSimulator')

def log_fish_behavior(fish_id, behavior_type, details):
    """メダカの行動をログに記録"""
    logger = logging.getLogger('FishSimulator.Fish')
    logger.debug(f"Fish {fish_id}: {behavior_type} - {details}")

def log_school_state(school_id, fish_count, density, center):
    """群れの状態をログに記録"""
    logger = logging.getLogger('FishSimulator.School')
    logger.info(f"School {school_id}: Count={fish_count}, Density={density:.3f}, Center={center}")

def log_world_event(event_type, details):
    """世界イベントをログに記録"""
    logger = logging.getLogger('FishSimulator.World')
    logger.info(f"World Event: {event_type} - {details}")

def log_performance(operation, duration):
    """パフォーマンス情報をログに記録"""
    logger = logging.getLogger('FishSimulator.Performance')
    logger.debug(f"Performance: {operation} took {duration:.4f}s")

def distance_between_points(x1, y1, x2, y2):
    """2点間の距離を計算"""
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def distance_in_torus(x1, y1, x2, y2, width, height):
    """トーラス状の世界での2点間の最短距離を計算"""
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    
    # トーラス状の世界での最短距離
    dx = min(dx, width - dx)
    dy = min(dy, height - dy)
    
    return math.sqrt(dx**2 + dy**2)

def normalize_vector(dx, dy):
    """ベクトルを正規化"""
    length = math.sqrt(dx**2 + dy**2)
    if length > 0:
        return dx / length, dy / length
    return 0, 0

def limit_vector(dx, dy, max_length):
    """ベクトルの長さを制限"""
    length = math.sqrt(dx**2 + dy**2)
    if length > max_length:
        return normalize_vector(dx, dy)[0] * max_length, normalize_vector(dx, dy)[1] * max_length
    return dx, dy

def wrap_position(x, y, width, height):
    """位置をトーラス状の世界に収める"""
    x = x % width
    y = y % height
    return x, y

def get_random_direction():
    """ランダムな方向ベクトルを取得"""
    angle = random.uniform(0, 2 * math.pi)
    return math.cos(angle), math.sin(angle)

def get_direction_from_angle(angle):
    """角度から方向ベクトルを取得"""
    return math.cos(angle), math.sin(angle)

def get_angle_from_direction(dx, dy):
    """方向ベクトルから角度を取得"""
    return math.atan2(dy, dx)

def rotate_vector(dx, dy, angle):
    """ベクトルを回転"""
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)
    new_dx = dx * cos_a - dy * sin_a
    new_dy = dx * sin_a + dy * cos_a
    return new_dx, new_dy

def clamp(value, min_val, max_val):
    """値を範囲内に制限"""
    return max(min_val, min(max_val, value))

def lerp(a, b, t):
    """線形補間"""
    return a + (b - a) * t

def smooth_step(t):
    """スムーズステップ関数"""
    return t * t * (3 - 2 * t)

def get_nearest_fish(fish, fish_list, max_distance=None):
    """最も近いメダカを取得"""
    if not fish_list:
        return None
    
    nearest_fish = None
    min_distance = float('inf')
    
    for other_fish in fish_list:
        if other_fish != fish:
            dist = distance_in_torus(
                fish.x, fish.y, 
                other_fish.x, other_fish.y, 
                SCREEN_WIDTH, SCREEN_HEIGHT
            )
            
            if max_distance is None or dist <= max_distance:
                if dist < min_distance:
                    min_distance = dist
                    nearest_fish = other_fish
    
    return nearest_fish

def calculate_school_center(fish_list):
    """群れの中心を計算"""
    if not fish_list:
        return SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
    
    avg_x = sum(fish.x for fish in fish_list) / len(fish_list)
    avg_y = sum(fish.y for fish in fish_list) / len(fish_list)
    
    return avg_x, avg_y

def calculate_school_density(fish_list):
    """群れの密度を計算"""
    if len(fish_list) < 2:
        return 0
    
    center_x, center_y = calculate_school_center(fish_list)
    
    total_distance = 0
    for fish in fish_list:
        dist = distance_between_points(fish.x, fish.y, center_x, center_y)
        total_distance += dist
    
    avg_distance = total_distance / len(fish_list)
    
    # 密度は距離の逆数
    density = 1.0 / (avg_distance + 1)
    
    return density
