import cv2
import numpy as np
from robot import *
import argparse

kp = 1.0
ki = 0.0
kd = 0.0
dt = 1.0

if __name__ == '__main__':
    # parser = argparse.ArgumentParser()
    # parser.add_argument("--power", type=int, default=0.25, help="Maximum power")

    robot = Robot('/dev/ttyUSB0')
    robot.setup_motors((50, 48, 6), (44, 42, 5), max_power=0.25)
    robot.setup_camera(0)

    robot.camera.set_line_params(dt=100, work_pos=190, work_width=350, work_height=20, blur=13)
    callback = Callback(robot)
    callback.configurate_pid(kp, ki, kd, dt)
    robot.camera.track_line_auto(callback.follow_line)
