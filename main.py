#!/usr/bin/env pybricks-micropython

'''
    Author: Chihiro Nakatani
    E-mail: sd18064@toyota-ti.ac.jp
    December 19th, 2020
    This script is used for "Creativity Development Seminar"
'''

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

import time 
from time import strftime
from time import gmtime

# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.

def color_checker(color_sensor):
     """This function is color checker to choose a correct color marble.

    Check color labels by using lego color sensor.
    The color sensor is very sensitive so that we need to use it in the same light condtion.

    Parameters
    ----------
    color_sensor : Color sensor instance
        This is a color sensor instance.

    Returns
    -------
    Color number
        1:Red, 2:Green, 3:Blue, 4:Orange, 5:Empty, 6:Pass
        Pass label means that the check is suspicious.
    """

    r_num, g_num, b_num = map(int, color_sensor.rgb())
    print(rgb_num_list, end=":")

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
        print("Blue")
        return 3
    else:
        print("Empty")
        return 5

def rotate_thirty_degrees_fast(motor):
    """This function is used to rotate a gear 30 degrees.

    We use this function when we don’t want to drop a marble which checked by color sensor.
    The motor has several degrees error. We need to think about it.

    Parameters
    ----------
    motor : Motor instance
        This is a motor instance.
    """
    motor.run_angle(600, 32, Stop.BRAKE)

def rotate_twenty_degrees_fast(motor):
    """This function is used to rotate a gear 20 degrees.

    We use this function when we want to skip the empty box in a gear.
    By using this function, We improved speed. 
    The motor has several degrees error. We need to think about it.

    Parameters
    ----------
    motor : Motor instance
        This is a motor instance.
    """
    motor.run_angle(600, 22, Stop.BRAKE)

def rotate_five_degrees_fast(motor):
    """This function is used to rotate a gear 5 degrees.

    We use this function when we want to drop a marble which checked by color sensor.
    The motor has several degrees error. We need to think about it.

    Parameters
    ----------
    motor : Motor instance
        This is a motor instance.
    """
    motor.run_angle(600, 5, Stop.BRAKE)

def drop_all_marbles(motor):
    """This function is used to drop all marbles.

    We use this function when we droped a marble into the 8th box.
    We don't need to check the last marble. By using this function, We improved speed. 

    Parameters
    ----------
    motor : Motor instance
        This is a motor instance.
    """
    motor.run_angle(100, 360, Stop.BRAKE)

def fill_marbles_into_gear(motor):
    """This function is used to rotate 160 degrees gear.

    We use this function when we start program.
    By using this function, We improved speed. 

    Parameters
    ----------
    motor : Motor instance
        This is a motor instance.
    """
    motor.run_angle(50, 160, Stop.BRAKE)

def main():
    """This is a main function of the script.

    We archied a high performance by calling this function which is refined.

    """
    
    # Generate connection with lego mindstorms
    ev3 = EV3Brick()
    ev3.speaker.beep()
    motor = Motor(port=Port.A)
    color_sensor = ColorSensor(port=Port.S4)

    # Define the list of color order which we should sort
    color_list = [1, 3, 2, 3, 2, 1, 2, 1, 3]

    # Define the list of flags whether each box include a marble or not  
    box_flag_list = [True for _ in range(9)]
    
    # Define a variable to save the previous checked color
    same_color_var = 0

    # Rotate 160 degrees gear
    fill_marbles_into_gear(motor)

    while True:        

        # Get out of the loop when we drop a marble into 8th box
        if sum(box_flag_list) == 1:
            departure_ball(motor)
            break
        
        # Rotate 5 degrees gear and sleep few second
        rotate_five_degrees_fast(motor)
        time.sleep(0.6)

        # Get the color label of the box we want to fill
        box_idx = box_flag_list.index(True)
        true_color = color_list[box_idx]
        checked_color = color_checker(color_sensor)
        
        # If the checked color is the same as the previous decision, we skip it.
        if same_color_var == checked_color and checked_color in [1, 2, 3]:
            pass

        # If we check empty twice in the row, rotate about 22 degrees
        elif same_color_var == checked_color and checked_color == 5:
            rotate_twenty_degrees_fast(motor)

        # If the checked color is the correct color, we drop the marble in the box
        elif checked_color == true_color:
            box_flag_list[box_idx] = False

            for _ in range(3):
                rotate_five_degrees_fast(motor)

            # reset a saved color label
            same_color_var = 0

        # If the checked color is orange, we skip it
        elif checked_color == 4:
            pass

        # If the checked color is empty, we skip it
        elif checked_color == 5:
            pass
        
        # If the checked color is suspecious, we don't drop it
        elif checked_color == 6:
            rotate_thirty_degrees_fast(motor)
            time.sleep(0.5)

        # If the checked color is color we don't expect, rotate 60 degrees gear in fast
        else:
            rotate_thirty_degrees_fast(motor)
            time.sleep(0.5)

            # reset a saved color label
            same_color_var = 0

        # save the color label checked in this iteration for next iteration
        same_color_var = checked_color

if __name__ == "__main__":

    # Save the start time
    start_time = time.time()

    # Generate instance of EV3
    ev3 = EV3Brick()

    # Start alert
    print("Start !!")
    ev3.speaker.beep()

    # Start a main function
    main()
    
    # finish alert 
    print("Finish !!")
    ev3.speaker.play_file(SoundFile.GOOD_JOB)

    # output the time we used to sort marbles
    print(strftime("%H:%M:%S", gmtime(time.time() - start_time)))