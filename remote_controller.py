import requests
import keyboard  # using module keyboard
import time

mobile_platform_url = 'http://192.168.247.61:5000'

forward_speed = 0.2
backwards_speed = -0.3
idle_speed = 0
left_angle = 13
right_angle = -27
idle_angle = -7

last_power_signal=None
last_steering_signal=None
if __name__ == '__main__':
    try:
        while True:  # making a loop
            if keyboard.is_pressed('w'):
                if last_power_signal != 'w':
                    requests.post(mobile_platform_url + '/drive-power', params={'power': forward_speed})
                    last_power_signal = 'w'
            elif keyboard.is_pressed('s'):
                if last_power_signal != 's':
                    requests.post(mobile_platform_url + '/drive-power', params={'power': backwards_speed})
                    last_power_signal = 's'
            else:
                if last_power_signal is not None:
                    requests.post(mobile_platform_url + '/drive-power', params={'power': idle_speed})
                    last_power_signal = None

            if keyboard.is_pressed('a'):
                if last_steering_signal != 'a':
                    requests.post(mobile_platform_url + '/steering-angle', params={'angle': left_angle})
                    last_steering_signal = 'a'
            elif keyboard.is_pressed('d'):
                if last_steering_signal != 'd':
                    requests.post(mobile_platform_url + '/steering-angle', params={'angle': right_angle})
                    last_steering_signal = 'd'
            else:
                if last_steering_signal is not None:
                    requests.post(mobile_platform_url + '/steering-angle', params={'angle': idle_angle})
                    last_steering_signal = None

            time.sleep(0.01)
    except Exception as e:
        print(e)
        requests.post(mobile_platform_url + '/drive-power', params={'power': idle_speed})
        requests.post(mobile_platform_url + '/steering-angle', params={'angle': idle_angle})