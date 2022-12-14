import cv2
import numpy as np
from robot import *
import argparse

kp = 0.01
ki = 0.0
kd = 0.0
dt = 1.0

if __name__ == '__main__':
    # parser = argparse.ArgumentParser()
    # parser.add_argument("--power", type=int, default=0.25, help="Maximum power")

    robot = Robot('/dev/ttyUSB0')
    robot.setup_motors((44, 42, 5), (50, 48, 6), max_power=0.25)
    robot.setup_camera(0)

    robot.camera.set_line_params(dt=130, work_pos=30, work_width=500, work_height=20, blur=13)
    callback = Callback(robot)
    callback.configurate_pid(kp, ki, kd, dt)


    # robot.camera.track_line_auto(callback.follow_line)
    robot.camera.track_line(callback.follow_line)
