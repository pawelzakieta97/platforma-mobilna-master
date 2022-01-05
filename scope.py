import datetime
import time
import csv
from gpiozero import Button
button = Button(17)
from master import MobilePlatform
import time

if __name__ == '__main__':
    pm = MobilePlatform(mock_pwm_output=False)
    # pm.set_drive_power(0.0)
    pm.set_steering_angle(0)
    time.sleep(2)
    pm.set_steering_angle(15)
    data = []
    prev_val = 0
    prev_check = datetime.datetime.now().timestamp()
    with open('output1.csv', 'w+') as output_file:
        writer = csv.writer(output_file)
        writer.writerow(['ts', 'state'])
        while True:
            if button.is_pressed != prev_val:
                if prev_val:
                    writer.writerow([prev_check, 0])
                else:
                    writer.writerow([prev_check, 1])
                prev_val = button.is_pressed
                if prev_val:
                    writer.writerow([datetime.datetime.now().timestamp(), 0])
                else:
                    writer.writerow([datetime.datetime.now().timestamp(), 1])
            prev_check = datetime.datetime.now().timestamp()