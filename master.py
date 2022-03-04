import time
import threading

STEERING_SERVO_CHANNEL = 7
PWM_FREQUENCY = 60
MAX_DUTY_CYCLE = 0xffff
STEERING_SERVO_MIN_PULSE = 0.001
STEERING_SERVO_MAX_PULSE = 0.002
DRIVE_POWER_MIN_PULSE = 0.001
DRIVE_POWER_MAX_PULSE = 0.002
DRIVE_POWER_CHANNEL = 6
DRIVE_POWER_FREQ = 60


class MobilePlatform:
    def __init__(self, steering_angle_range=(-45, 45), mock_pwm_output=True):
        self.steering_angle_min = steering_angle_range[0]
        self.steering_angle_max = steering_angle_range[1]
        if not mock_pwm_output:
            import busio
            import board
            import adafruit_pca9685
            # self.gpio = GPIO
            self.i2c = busio.I2C(board.SCL, board.SDA)
            self.pca = adafruit_pca9685.PCA9685(self.i2c)
            self.pca.frequency = 60
            self.steering_servo_pwm = self.pca.channels[STEERING_SERVO_CHANNEL]
            # self.steering_servo_pwm.start(0.0015 * STEERING_SERVO_FREQ)
            self.drive_power_pwm = self.pca.channels[DRIVE_POWER_CHANNEL]
            # self.drive_power_pwm.start(0.0015 * DRIVE_POWER_FREQ)
        self.mock_pwm_output = mock_pwm_output
        self.drive_power = 0
        self.steering_angle = 0
        self.lidar_readings = []
        self.battery_voltage = None
        self.raw_acc = None
        self.raw_gyro = None
        self.orientation = None
        self.real_position = None
        self.slam_position = None
        self.map = []
        self.camera_angle = None

    def set_steering_angle(self, angle):
        self.steering_angle = angle
        if angle<self.steering_angle_min or angle > self.steering_angle_max:
            raise ValueError('invalid angle')
        pulse_duration = STEERING_SERVO_MIN_PULSE + \
                         (STEERING_SERVO_MAX_PULSE - STEERING_SERVO_MIN_PULSE) * \
                         (angle - self.steering_angle_min)/(self.steering_angle_max - self.steering_angle_min)
        duty_cycle = pulse_duration * PWM_FREQUENCY * MAX_DUTY_CYCLE
        print(f'SENDING PWM SIGNAL TO STEERING SIGNAL DUTY_CYCLE {duty_cycle}')
        if not self.mock_pwm_output:
            self.steering_servo_pwm.duty_cycle = int(duty_cycle)

    def set_drive_power(self, power):
        if abs(power) > 1:
            raise ValueError('Power must be in range (-1, 1)')
        self.drive_power = power
        pulse_duration = DRIVE_POWER_MIN_PULSE + \
                         (DRIVE_POWER_MAX_PULSE - DRIVE_POWER_MIN_PULSE) * (power/2 + 0.5)
        duty_cycle = pulse_duration * PWM_FREQUENCY * MAX_DUTY_CYCLE
        print(f'SENDING PWM SIGNAL TO DRIVE MOTOR DUTY_CYCLE {duty_cycle}')
        if not self.mock_pwm_output:
            self.drive_power_pwm.duty_cycle = int(duty_cycle)

    def __del__(self):
        if not self.mock_pwm_output:
            print('deiniting')
            self.pca.deinit()

    def arm(self):
        self.set_drive_power(0)
        time.sleep(2)