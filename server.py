from flask import Flask, render_template, redirect, url_for, request, session, flash, jsonify, Response
from flask_httpauth import HTTPDigestAuth
from werkzeug.security import generate_password_hash, check_password_hash
import time, datetime, random, threading
from camera_pi import Camera
from pymavlink import mavutil

# faceCascade = cv2.CascadeClassifier('Cascades/haarcascade_frontalface_default.xml')

# ip_address = "192.168.43.210"
ip_address = "192.168.1.103"
app = Flask(__name__)
app.config['SECRET_KEY'] = 'hello'
auth = HTTPDigestAuth()
x1 = 60.03143
y1 = 30.36020

vehicle = mavutil.mavlink_connection("/dev/ttyACM0", baud=115200)

# vehicle = mavutil.mavlink_connection('udpin:0.0.0.0:14550')

users = {
    "admin": "admin"
}

@auth.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None

endpoint = {
	"x" : 0,
	"y" : 0,
	"z" : 0
}

UAV = {
	'x' : 0,
	'y' : 0,
	'z' : 0
}

UAV2 = []

UAV3 = {
	"x" : 60.03143,
	"y" : 30.3613,
	# "x2" : 60.03153,
	# "y2" : 30.36151,
	# "x3" : 60.0316,
	# "y3" : 30.36172,
	# "x4" : 60.03159,
	# "y4" : 30.36191
	"x1" : round(random.uniform(x1, x1+0.00002), 5),
	"y1" : round(random.uniform(y1, y1+0.00002), 5),
	"x2" : round(random.uniform(x1+0.00002, x1+0.00004), 5),
	"y2" : round(random.uniform(y1+0.00004, y1+0.00006), 5),
	"x3" : round(random.uniform(x1+0.00004, x1+0.00006), 5),
	"y3" : round(random.uniform(y1+0.00006, y1+0.00008), 5)
}

def gen_img(camera):
	frame = camera.get_frame()
	yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def gen(camera):
	while True:
		frame = camera.get_frame()
		yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/arm', methods=["POST"])
@auth.login_required
def arm():
	status = False
	vehicle.arducopter_arm()
	armed = vehicle.motors_armed()
	if armed: status = True
	return jsonify({'status' : status})

@app.route('/disarm', methods=["POST"])
@auth.login_required
def disarm():
	status = False
	vehicle.arducopter_disarm()
	armed = vehicle.motors_armed()
	if (not armed): status = True
	return jsonify({'status' : status})

@app.route('/get_gps', methods=["GET"])
@auth.login_required
def get_gps():
	x = random.uniform(59.973982, 59.973478)
	y = random.uniform(30.298140, 30.300297)
	z = random.uniform(15.0, 17.0)
	if len(UAV2)<6:
		UAV2.append([x, y])
	else:
		UAV2.pop(0)
		UAV2.append([x, y])
	UAV2e = np.array(UAV2)
	j = 5
	step = np.diff(x[j-5:j+2]).mean()
	x_extra = np.array([x[j]+step,x[j]+step*2,x[j]+step*3])
	spl = splrep(x[j-5:j+2:2], y[j-5:j+2:2], k=1)
	y_extra = splev(x_extra, spl)
	main = {'x' : x, 'y' : y, 'z' : z, \
		'state' : 1, 'time' : datetime.datetime.now()}
	UAV2_extra = {'x1' : x_extra[0], 'y1' : y_extra[0],\
	'x2' : x_extra[1], 'y2' : y_extra[1], 'x3' : x_extra[2], 'y3' : y_extra[2]}
	data = [main, UAV2_extra]
	return jsonify(GPS_data = data)

@app.route('/get_gps3', methods=["GET"])
@auth.login_required
def get_gps3():
	return jsonify({'x' : random.uniform(59.974933, 59.974471), \
			'y' : random.uniform(30.297115, 30.299476), \
			'z' : round(random.uniform(15.0, 17.0), 2), \
			'state' : 1, 'time' : datetime.datetime.now()})


@app.route('/video_feed', methods=["GET"])
@auth.login_required
def video_feed():
	return Response(gen(Camera()), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/image', methods=["GET"])
@auth.login_required
def image():
	return Response(gen_img(Camera()), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/latest_image', methods=["GET"])
@auth.login_required
def latest_image():
	return render_template("latest_image.html")

@app.route('/status', methods=["GET"])
@auth.login_required
def status():
	try:
		state = 1
		vehicle.wait_heartbeat()
		lat = vehicle.messages["GPS_RAW_INT"].lat*1e-7
		lon = vehicle.messages["GPS_RAW_INT"].lon*1e-7
		alt = vehicle.messages["GPS_RAW_INT"].alt*1e-3
		sv = vehicle.messages['GPS_RAW_INT'].satellites_visible
		if (sv == 0):
			state = -1
		elif (sv<7 or (abs(lat-UAV['x'])>0.000038 or abs(lon-UAV['y'])>0.000078 \
		 or abs(alt-UAV['z'])>5)):
			state = 0
		UAV['x'] = lat
		UAV['y'] = lon
		UAV['z'] = alt
		return jsonify({'x' : UAV['x'], \
			'y' : UAV['y'], \
			'z' : UAV['z'], \
			'state' : state, 'time' : datetime.datetime.now()})
	except:
		return jsonify({'x' : UAV['x'], \
			'y' : UAV['y'], \
			'z' : UAV['z'], \
			'state' : -1, 'time' : datetime.datetime.now()})

@app.route('/manual_drive', methods=["GET"])
@auth.login_required
def manual_drive():
    return jsonify({'up' : True, 'down' : False})

@app.route('/getendpoint', methods=["GET"])
@auth.login_required
def getendpoint():
    return jsonify({'x' : endpoint["x"], 'y' : endpoint["y"], 'z' : endpoint["z"]})

@app.route('/setendpoint', methods=["GET", "POST"])
@auth.login_required
def setendpoint():
	if request.method == "POST":
		endpoint["x"] = request.values["setX"]
		endpoint["y"] = request.values["setY"]
		endpoint["z"] = request.values["setZ"]
		return jsonify({'status' : 'OK'})
	else:
		return render_template("setendpoint.html")

@app.route('/sensor', methods=["GET"])
@auth.login_required
def sensor():
	stype = request.args.get('type')
	if stype == 'camera':
		return jsonify({'type' : stype, 'image' : 'http://' + ip_address + ':5000/latest_image', \
		 'time' : round(time.time()) })
	elif stype == 'gps':
		return jsonify({'type' : stype, 'x' : round(random.uniform(59.0, 60.0), 4), \
			'y' : round(random.uniform(30.0, 31.0), 4), \
			'z' : round(random.uniform(1.0, 20.0), 2), 'time' : round(time.time())})


@app.route('/game')
@auth.login_required
def game():
    return render_template("game.html")

# @app.route('/logout', methods=['GET', 'POST'])
# @auth.login_required
# def logout():
#     auth.username = None

@app.route('/')
@auth.login_required
def index():
    return render_template("index.html", UAV2 = UAV2, UAV3 = UAV3)

if __name__ == "__main__":
	app.run(debug=True, host='0.0.0.0', threaded=True)