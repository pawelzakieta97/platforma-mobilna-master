from master import MobilePlatform
import time

if __name__ == '__main__':
    pm = MobilePlatform(mock_pwm_output=False)
    pm.arm()
    # pm.set_drive_power(0.0)
    pm.set_steering_angle(-20)
    time.sleep(10)