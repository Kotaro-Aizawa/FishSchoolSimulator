#!/usr/bin/env python3
"""
配置リセット機能のテストスクリプト
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from school import School
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

def test_reset_positions():
    """メダカの位置リセット機能をテスト"""
    print("=== メダカ配置リセット機能テスト ===")
    
    # 群れを作成
    school = School(5)  # 5匹のメダカで小さくテスト
    
    print("初期位置:")
    initial_positions = []
    for i, fish in enumerate(school.fish_list):
        pos = (fish.x, fish.y)
        initial_positions.append(pos)
        print(f"  メダカ{i+1}: {pos}")
    
    print("\n位置をリセット中...")
    school.reset_fish_positions()
    
    print("リセット後の位置:")
    reset_positions = []
    for i, fish in enumerate(school.fish_list):
        pos = (fish.x, fish.y)
        reset_positions.append(pos)
        print(f"  メダカ{i+1}: {pos}")
    
    # 位置が変わったかチェック
    positions_changed = 0
    for i, (initial, reset) in enumerate(zip(initial_positions, reset_positions)):
        if initial != reset:
            positions_changed += 1
    
    print(f"\n結果:")
    print(f"  変更された位置: {positions_changed}/{len(initial_positions)}")
    print(f"  テスト結果: {'成功' if positions_changed > 0 else '失敗'}")
    
    # 位置が画面内に収まっているかチェック
    all_in_bounds = True
    for i, fish in enumerate(school.fish_list):
        if not (0 <= fish.x < SCREEN_WIDTH and 0 <= fish.y < SCREEN_HEIGHT):
            print(f"  警告: メダカ{i+1}が画面外に配置されました: ({fish.x}, {fish.y})")
            all_in_bounds = False
    
    if all_in_bounds:
        print("  全てのメダカが画面内に正しく配置されました")
    
    return positions_changed > 0 and all_in_bounds

if __name__ == "__main__":
    success = test_reset_positions()
    print(f"\n最終結果: {'テスト成功' if success else 'テスト失敗'}")
    sys.exit(0 if success else 1)
