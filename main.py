import cv2
import numpy as np
from robot import *

if __name__ == '__main__':
    robot = Robot('/dev/ttyUSB0')
    robot.setup_motors((44, 42, 46), (50, 48, 8), max_power=0.5, k=7)
    robot.setup_camera(0)

    robot.camera.set_line_params(dt=0, work_pos=400, work_width=245, work_height=20, blur=13)
    callback = Callback(robot)
    robot.camera.track_line_auto(callback.follow_line)