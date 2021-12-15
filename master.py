STEERING_SERVO_PIN = 35
STEERING_SERVO_FREQ = 100
STEERING_SERVO_MIN_PULSE = 0.001
STEERING_SERVO_MAX_PULSE = 0.002
DRIVE_POWER_PIN = 12
DRIVE_POWER_FREQ = 1000


class MobilePlatform:
    def __init__(self, steering_angle_range=(-45, 45), mock_pwm_output=True):
        self.steering_angle_min = steering_angle_range[0]
        self.steering_angle_max = steering_angle_range[1]
        if not mock_pwm_output:
            import GPIO
            GPIO.setwarnings(False)  # disable warnings
            GPIO.setmode(GPIO.BOARD)  # set pin numbering system
            GPIO.setup(STEERING_SERVO_PIN, GPIO.OUT)
            GPIO.setup(DRIVE_POWER_PIN, GPIO.OUT)
            self.steering_servo_pwm = GPIO.PWM(STEERING_SERVO_PIN, STEERING_SERVO_FREQ)
            self.steering_servo_pwm.start(0.0015 * STEERING_SERVO_FREQ)
            self.drive_power_pwm = GPIO.PWM(DRIVE_POWER_PIN, DRIVE_POWER_FREQ)
            self.drive_power_pwm.start(0)
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
                         (angle - self.steering_angle_min)/(self.steering_angle_max - self.steering_angle_max)
        duty_cycle = pulse_duration * STEERING_SERVO_FREQ
        print('SENDING PWM SIGNAL TO STEERING SIGNAL ')
        if not self.mock_pwm_output:
            self.steering_servo_pwm.ChangeDutyCycle(duty_cycle)

    def set_drive_power(self, power):
        self.drive_power = power
        print('SENDING PWM SIGNAL TO STEERING SIGNAL ')
        if not self.mock_pwm_output:
            self.steering_servo_pwm.ChangeDutyCycle(power)

    def __del__(self):
        if not self.mock_pwm_output:
            self.steering_servo_pwm.stop()
            self.drive_power_pwm.stop()