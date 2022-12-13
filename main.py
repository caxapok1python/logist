import cv2
import numpy as np
from robot import *

if __name__ == '__main__':
    robot = Robot('/dev/ttyUSB0')
    robot.setup_motors((44, 42, 5), (50, 48, 6), max_power=0.25, k=5)
    robot.setup_camera(0)

    robot.camera.set_line_params(dt=130, work_pos=300, work_width=400, work_height=20, blur=13)
    callback = Callback(robot)
    robot.camera.track_line(callback.follow_line)
