from typing import Tuple

from .hardware import *
from .software import *


class Robot:
    def __init__(self, serial='/dev/ttyUSB0'):
        self.camera = None
        self.chassis = None
        self.right = None
        self.left = None
        self.board = pyfirmata.ArduinoMega(serial)
        print("Communication Successfully started")

    def setup_motors(self, left: Tuple[int, int, int], right: Tuple[int, int, int], max_power=0.5, k=1.0):
        self.left = Motor(self.board, *left)
        self.right = Motor(self.board, *right)
        self.chassis = Chassis(self.left, self.right, max_power, k)

    def setup_camera(self, camera_number=0):
        self.camera = Camera(camera_number)

    def stop(self):
        self.chassis.set_power(0, 0)
        self.camera.stop()


class PID:
    def __init__(self, kp, ki, kd, dt=1.0):
        self.dt = dt
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.err = 0
        self.last_err = self.err
        self.sum_err = self.err
        self.derr = 0
        self.setpoint = 0
        self.min = -20
        self.max = 20

    def in_range(self, out):
        return max(min(self.max, out), self.min)

    def regulator(self, val):
        self.err = self.setpoint - val
        self.sum_err += self.err * self.dt
        self.derr = (self.err - self.last_err) / self.dt

        self.last_err = self.err

        out = self.kp * self.err + self.ki * self.sum_err + self.kd * self.derr
        print(f'\n{out}\n')
        return self.in_range(out)


class Callback:
    def __init__(self, robot: Robot):
        self.robot = robot
        self.pid = PID(0.0, 0.0, 0.0, 1.0)

    def calculate_angle(self, line_center):
        alc = (0 + int((self.robot.camera.width - self.robot.camera.work_width) / 2) + line_center[0],
               self.robot.camera.work_pos + line_center[1])
        dx = 640 // 2 - alc[0]
        dy = 480 - alc[1]
        # dx, dy = (self.robot.camera.work_width // 2 - line_center[0], self.robot.camera.work_height)
        return float(np.degrees(atan2(dx, dy)))

    def configurate_pid(self, kp=0.0, ki=0.0, kd=0.0, dt=1.0):
        self.pid.setpoint = 0
        self.pid.kp = kp
        self.pid.ki = ki
        self.pid.kd = kd
        self.pid.dt = dt
        self.pid.min = self.robot.chassis.statpower
        self.pid.max = self.robot.chassis.statpower

    def follow_line(self, *args):
        angle = self.calculate_angle(*args)
        delta = abs(self.pid.regulator(val=angle))
        print(self.pid.err)

        left = self.robot.chassis.statpower
        right = self.robot.chassis.statpower

        if angle == 0:
            left = 0
            right = 0
        elif angle < 0:
            right -= delta
        elif angle > 0:
            left -= delta

        self.robot.chassis.set_power(left, right)

        print(angle)
        print(delta)
        print(*list(map(lambda x: round(x, 2), (left, right))))
        # self.robot.chassis.direction(angle)
