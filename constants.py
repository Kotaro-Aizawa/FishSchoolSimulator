# 画面設定
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900
FPS = 60

# メダカ設定
DEFAULT_FISH_COUNT = 100
FISH_SIZE = 4
FISH_SPEED = 1

# 視界設定
VISION_RANGE = 1  # 前方・斜め前の3方向1マスずつ

# 群れ行動の重み（初期値）
SEPARATION_WEIGHT = 1.5
ALIGNMENT_WEIGHT = 1.0
COHESION_WEIGHT = 0.8
RANDOM_WEIGHT = 0.1
INERTIA_WEIGHT = 1.0

# 色設定
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 100, 255)
LIGHT_BLUE = (100, 150, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# 方向ベクトル（8方向）
DIRECTIONS = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1),           (0, 1),
    (1, -1),  (1, 0),  (1, 1)
]
