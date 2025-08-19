#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import time
from world import World
from school import School
from constants import *

def main():
    """メインゲームループ"""
    print("Fish School Simulator を開始します...")
    
    # 世界と群れを初期化
    world = World()
    school = School(DEFAULT_FISH_COUNT)
    
    try:
        # pygameを初期化
        world.initialize()
        print(f"画面サイズ: {world.width}x{world.height}")
        print(f"メダカの数: {school.get_fish_count()}")
        print("ゲーム開始！")
        
        # メインループ
        running = True
        frame_count = 0
        start_time = time.time()
        
        while running:
            # イベント処理
            event_result = world.handle_events()
            
            if event_result == False:
                running = False
            elif isinstance(event_result, tuple) and event_result[0] == "add_fish":
                # メダカを追加
                _, x, y = event_result
                school.add_fish(x, y)
                print(f"メダカを追加しました: ({x}, {y})")
            
            # 群れの更新
            school.update_all_fish()
            
            # 描画
            world.draw_background()
            school.draw_all_fish(world.screen)
            
            # 追加情報の描画
            world.draw_info(school)
            world.draw_vision_areas(school)
            world.draw_school_center(school)
            
            # 画面更新
            world.update_display()
            
            # フレームレート制御
            world.tick()
            
            # 統計情報
            frame_count += 1
            if frame_count % 60 == 0:  # 1秒ごと
                current_time = time.time()
                elapsed_time = current_time - start_time
                fps = world.get_fps()
                print(f"FPS: {fps:.1f}, 経過時間: {elapsed_time:.1f}秒, メダカ数: {school.get_fish_count()}")
        
        print("ゲーム終了")
        
    except KeyboardInterrupt:
        print("\nキーボード割り込みで終了")
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # クリーンアップ
        world.quit()
        print("プログラムを終了します")

if __name__ == "__main__":
    main()
