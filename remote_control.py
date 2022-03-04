from flask import Flask, request

from master import MobilePlatform

app = Flask(__name__)

pm = MobilePlatform(mock_pwm_output=False)

@app.route('/')
def index():
  return "mobile platform remote control server online!"


@app.route('/drive-power', methods=['GET', 'POST'])
def drive_power():
    if request.method == 'POST':
        args = request.args
        pm.set_drive_power(float(args['power']))
        # ACTUALLY SET THE POWER
        return f"Setting drive power to {args['power']}"
    else:
        return str(pm.drive_power)

@app.route('/steering-angle', methods=['GET', 'POST'])
def steering_angle():
    if request.method == 'POST':
        args = request.args
        pm.set_steering_angle(float(args['angle']))
        # ACTUALLY SET THE POWER
        return f"Setting steering angle to {args['angle']}"
    else:
        return str(pm.steering_angle)


@app.route('/drive-power', methods=['POST'])
def set_drive_power():
    args = request.args
    return args

if __name__ == '__main__':
    pm.arm()
    app.debug = True
    app.run(host="0.0.0.0")