import cv2
import numpy as np
from robot import *

if __name__ == '__main__':
    robot = Robot('/dev/ttyUSB0')
    robot.setup_motors((44, 42, 6), (50, 48, 5), max_power=0.3, k=9)
    robot.setup_camera(0)

    robot.camera.set_line_params(dt=100, work_pos=400, work_width=500, work_height=20, blur=13)
    callback = Callback(robot)
    robot.camera.track_line_auto(callback.follow_line)
