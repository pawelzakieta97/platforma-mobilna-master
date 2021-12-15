from master import MobilePlatform

if __name__ == '__main__':
    pm = MobilePlatform(mock_pwm_output=False)
    pm.set_drive_power(0.1)