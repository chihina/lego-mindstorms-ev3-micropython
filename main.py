#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

# For interval time
import time 
from time import strftime
from time import gmtime

# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.

# 色判定メソッド (1:red, 2:green, 3:blue)
def color_checker(color_sensor):
    
    # ex. (x, y, z) 0-100 の反射値を出す
    rgb_num_list = list(map(int, color_sensor.rgb()))
    print(rgb_num_list)

    max_num = max(rgb_num_list)
    max_idx = rgb_num_list.index(max_num) + 1

    return max_idx

# 色判定メソッド (1:red, 2:green, 3:blue, 4:オレンジ, 5:空, 6:怪しいのでパス)
def color_checker_fukaya(color_sensor):
    
    # ex. (x, y, z) 0-100 の反射値を出す
    rgb_num_list = list(map(int, color_sensor.rgb()))
    r_num, g_num, b_num = map(int, rgb_num_list)
    print(rgb_num_list, end=":")

    # ---------------------------色判定部-----------------------------------------
    # 反射値が大きいときはオレンジに近い?
    if (r_num+g_num+b_num) > 35:
        print("Orange")
        return 4
        
    if r_num >= 3 and g_num <= 2 and b_num <= 1:
        print("Red")
        return 1
    elif r_num == 1 and g_num == 0 and b_num == 0:
        print("Red")
        return 1
    elif r_num <= 2 and g_num >= 2 and b_num <= 1:
        print("Green")
        return 2
    elif r_num <= 1 and g_num <= 2 and b_num >= 2:
        print("Blue")
        return 3
    elif max(rgb_num_list) == 1 and not max(rgb_num_list) == 0:
        print("pass (Blue)")
        # return 6
        return 3
    else:
        print("Empty")
        return 5
    # ---------------------------色判定部-----------------------------------------

# 落としたい時の40度回転(ゆっくり回転)
def motor_forty_degree_late(motor):
    motor.run_angle(50, 38, Stop.BRAKE)

# 落としたくない時の40度回転(早く回転)
def motor_forty_degree_slow(motor):
    motor.run_angle(300, 38, Stop.BRAKE)

# 落としたくない時の60度回転(早く回転)
def motor_sixty_degree_fast(motor):
    # print("Rotate 60 degrees")
    motor.run_angle(600, 32, Stop.BRAKE)

# Empty empty 用
def motor_empty_degree_fast(motor):
    # print("Rotate 60 degrees")
    motor.run_angle(600, 22, Stop.BRAKE)

# 5度回転
def five_degree_lotate(motor):
    # print("Rotate 5 degree")
    motor.run_angle(600, 5, Stop.BRAKE)

# 10度回転
def ten_degree_lotate(motor):
    motor.run_angle(400, 10, Stop.BRAKE)

# ボール全排出用の関数(デバッグ用)
def departure_ball(motor):
    motor.run_angle(100, 360, Stop.BRAKE)

# メイン関数
def main():

    print("Exe main function")
    
    # ev3 のインスタンスを生成する
    ev3 = EV3Brick()

    # 選別開始のアラームを鳴らす
    ev3.speaker.beep()

    # モーターとカラーセンサのインスタンスを生成
    motor = Motor(port=Port.A)
    color_sensor = ColorSensor(port=Port.S1)

    # 正解のビー玉の順番を与える (1:red, 2:green, 3:blue)
    color_list = [1, 3, 2, 3, 2, 1, 2, 1, 3]
    
    # 埋まっているかどうかのフラグを保存するリスト
    box_flag_list = [True for _ in range(9)]
    
    while True:        
        # すべての場所が False (=0) になれば ループを抜ける
        if sum(box_flag_list) == 0:
            break
        
        # それぞれの場所について考える
        for box_idx, box_flag in enumerate(box_flag_list):
            
            # 最初に埋まっていない場所なら
            if box_flag:

                # 次に来てほしい色を取得
                true_color = color_list[box_idx]

                # 判定した色を取得
                jud_color = color_checker(color_sensor)

                # もし, 排出したい色ならば
                if jud_color == true_color:

                    # 埋まっている場所を False にする
                    box_flag_list[box_idx] = False
                    
                    # モーターを 40度回転(落としたい時)
                    motor_forty_degree_late(motor)
                    
                    # インターバル 1秒
                    time.sleep(1)

                # ちがうならパス
                else:
                    # モーター 40度回転(落としたくない時)
                    motor_forty_degree_fast(motor)

                    # インターバル 1秒
                    time.sleep(1)
                break

    # 仕分け終了のアラーム
    ev3.speaker.beep()

# メイン関数(バージョン2)
def main_two():

    # ev3 のインスタンスを生成する
    ev3 = EV3Brick()

    # 選別開始のアラームを鳴らす
    ev3.speaker.beep()

    # モーターとカラーセンサのインスタンスを生成
    motor = Motor(port=Port.A)
    color_sensor = ColorSensor(port=Port.S4)

    # 正解のビー玉の順番を与える (1:red, 2:green, 3:blue)
    color_list = [1, 3, 2, 3, 2, 1, 2, 1, 3]

    # 埋まっているかどうかのフラグを保存するリスト
    box_flag_list = [True for _ in range(9)]
    
    # 同じ色を連続で判定する問題用フラグ
    same_color_var = 0

    # 最初にある程度回しておく
    motor.run_angle(50, 160, Stop.BRAKE)

    while True:        
        print(box_flag_list)

        # すべての場所が False (=0) になれば ループを抜ける
        if sum(box_flag_list) == 1:
            departure_ball(motor)
            break
        
        five_degree_lotate(motor)
        time.sleep(0.6)

        # それぞれの場所について考える
        for box_idx, box_flag in enumerate(box_flag_list):
            
            # 最初に埋まっていない場所なら
            if box_flag:

                # 次に来てほしい色を取得
                true_color = color_list[box_idx]

                # 判定した色を取得
                jud_color = color_checker_fukaya(color_sensor)
                
                # もし連続で同じ色を判定したら
                if same_color_var == jud_color and jud_color in [1, 2, 3]:
                    # time.sleep(0.2)
                    pass

                # 2回数連続 empty なら
                elif same_color_var == jud_color and jud_color == 5:
                    print("Empty empty !!!")
                    motor_empty_degree_fast(motor)

                # もし, 排出したい色ならば
                elif jud_color == true_color:
                    # 該当の場所を False にする
                    box_flag_list[box_idx] = False

                    # パス対策
                    for _ in range(3):
                        five_degree_lotate(motor)

                    # 落としたらリセット
                    same_color_var = 0

                # 判定がオレンジなら
                elif jud_color == 4:
                    # time.sleep(0.2)
                    pass

                # 判定が空なら
                elif jud_color == 5:
                    # time.sleep(0.2)
                    pass
                
                # 怪しい判定ならパスする
                elif jud_color == 6:
                    # モーター 60度回転(落としたくない時)
                    motor_sixty_degree_fast(motor)

                    # インターバル 1秒
                    time.sleep(0.5)

                # 落としたくない色がきたら
                else:
                    # モーター 60度回転(落としたくない時)
                    motor_sixty_degree_fast(motor)

                    # インターバル 1秒
                    time.sleep(0.5)

                    # 回転させたらリセット
                    same_color_var = 0

                    break

                same_color_var = jud_color

                break

    # 仕分け終了のアラーム
    ev3.speaker.beep()

if __name__ == "__main__":

    # 選別開始のアラーム
    print("Start !!")

    # 開始時間の記録
    start_time = time.time()

    # ev3 のインスタンスを生成
    ev3 = EV3Brick()

    # 選別の開始のアラーム
    ev3.speaker.beep()

    # モーターとカラーセンサのインスタンスを生成
    motor = Motor(port=Port.A)
    color_sensor = ColorSensor(port=Port.S4)

    # 深谷ver
    main_two()

    # departure_ball(motor)
    
    # 選別終了のアラーム
    print("Finish !!")
    ev3.speaker.play_file(SoundFile.GOOD_JOB)

    print(strftime("%H:%M:%S", gmtime(time.time() - start_time)))