#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import time
import logging
from world import World
from school import School
from constants import *
from utils import setup_logging, log_world_event, log_performance

def main():
    """メインゲームループ"""
    # ログ設定を初期化
    logger = setup_logging()
    logger.info("=== Fish School Simulator Starting ===")
    
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
        
        logger.info(f"Game started with {school.get_fish_count()} fish on {world.width}x{world.height} screen")
        log_world_event("GAME_START", f"Fish count: {school.get_fish_count()}")
        
        # メインループ
        running = True
        frame_count = 0
        start_time = time.time()
        last_stats_time = start_time
        
        while running:
            loop_start_time = time.time()
            
            # イベント処理
            event_result = world.handle_events()
            
            if event_result == False:
                logger.info("Game loop terminated by user")
                running = False
            elif isinstance(event_result, tuple) and event_result[0] == "add_fish":
                # メダカを追加
                _, x, y = event_result
                school.add_fish(x, y)
                print(f"メダカを追加しました: ({x}, {y})")
                logger.info(f"Fish added at position ({x}, {y})")
            elif isinstance(event_result, tuple) and event_result[0] == "reset_positions":
                # メダカの位置をリセット
                school.reset_fish_positions()
                print(f"メダカの位置をリセットしました: {school.get_fish_count()}匹")
                logger.info(f"Fish positions reset for {school.get_fish_count()} fish")
            
            # 群れの更新
            # Worldクラスから現在のパラメータを取得
            params = {
                'separation_weight': world.separation_weight,
                'alignment_weight': world.alignment_weight,
                'cohesion_weight': world.cohesion_weight,
                'random_weight': world.random_weight,
                'inertia_weight': world.inertia_weight,
                'fish_speed': world.fish_speed,
                'vision_range': world.vision_range
            }
            school.update_all_fish(params)
            
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
            current_time = time.time()
            
            # 1秒ごとに統計を出力
            if current_time - last_stats_time >= 1.0:
                elapsed_time = current_time - start_time
                fps = world.get_fps()
                fish_count = school.get_fish_count()
                
                print(f"FPS: {fps:.1f}, 経過時間: {elapsed_time:.1f}秒, メダカ数: {fish_count}")
                
                # 詳細な統計情報をログに記録
                school_stats = school.get_school_statistics()
                world_stats = world.get_world_statistics()
                
                logger.info(f"Frame {frame_count}: FPS={fps:.1f}, Fish={fish_count}, "
                           f"Density={school_stats['density']:.3f}, "
                           f"Avg Energy={school_stats['avg_energy']:.1f}")
                
                last_stats_time = current_time
            
            # ループ全体のパフォーマンスを記録
            loop_duration = time.time() - loop_start_time
            if frame_count % 60 == 0:  # 1秒ごと
                log_performance("Main game loop", loop_duration)
        
        # ゲーム終了時の統計
        total_time = time.time() - start_time
        final_stats = {
            'total_frames': frame_count,
            'total_time': total_time,
            'avg_fps': frame_count / total_time if total_time > 0 else 0,
            'final_fish_count': school.get_fish_count(),
            'school_stats': school.get_school_statistics(),
            'world_stats': world.get_world_statistics()
        }
        
        logger.info(f"Game ended. Final statistics: {final_stats}")
        log_world_event("GAME_END", f"Total frames: {frame_count}, Total time: {total_time:.1f}s")
        
        print("ゲーム終了")
        
    except KeyboardInterrupt:
        logger.warning("Game interrupted by keyboard")
        print("\nキーボード割り込みで終了")
    except Exception as e:
        logger.error(f"Unexpected error occurred: {e}", exc_info=True)
        print(f"エラーが発生しました: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # クリーンアップ
        try:
            world.quit()
            logger.info("Pygame shutdown completed")
        except Exception as e:
            logger.error(f"Error during pygame shutdown: {e}")
        
        logger.info("=== Fish School Simulator Shutdown Complete ===")
        print("プログラムを終了します")

if __name__ == "__main__":
    main()
