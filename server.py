from flask import Flask, render_template, redirect, url_for, request, session, flash, jsonify, Response
from flask_httpauth import HTTPDigestAuth
from werkzeug.security import generate_password_hash, check_password_hash
import time, datetime, random, threading
import numpy as np
from camera_pi import Camera
from pymavlink import mavutil
from scipy.interpolate import splrep, splev

# faceCascade = cv2.CascadeClassifier('Cascades/haarcascade_frontalface_default.xml')

ip_address = "192.168.43.7"

# ip = ['192.168.43.112','192.168.43.132']
# login = [['admin','admin'],['admin','admin']]

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hello'
auth = HTTPDigestAuth()

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
	"lat" : None,
	"lon" : None,
	"alt" : None
}

myUAV = {
	'lat' : 0,
	'lon' : 0,
	'alt' : 0
}

UAV = [[[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]],[[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]]]

def gen_img(camera):
	frame = camera.get_frame()
	yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def gen(camera):
	while True:
		frame = camera.get_frame()
		yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

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

@app.route('/arm', methods=["POST"])
@auth.login_required
def arm():
	status = False
	vehicle.arducopter_arm()
	# vehicle.motors_armed_wait()
	armed = vehicle.motors_armed()
	if armed: status = True
	return jsonify({'status' : status})

@app.route('/disarm', methods=["POST"])
@auth.login_required
def disarm():
	status = False
	vehicle.arducopter_disarm()
	# vehicle.motors_disarmed_wait()
	armed = vehicle.motors_armed()
	if (not armed): status = True
	return jsonify({'status' : status})

@app.route('/get_gps', methods=["POST"])
@auth.login_required
def get_gps():
	i = int(request.values["UAVnum"])
	if i == 0:
		x = random.uniform(59.973982, 59.973478)
		y = random.uniform(30.298140, 30.300297)
		z = random.uniform(15.0, 17.0)
	else:
		x = random.uniform(59.974933, 59.974471)
		y = random.uniform(30.297115, 30.299476)
		z = random.uniform(20.0, 30.0)

	# url = 'http://' + ip[i] + ':5000/status'
	# auth = HTTPDigestAuth(login[i][0], login[i][1])
	# r = requests.get(url = url, auth = auth)
	# data = r.json()

	# x = data['lat']
	# y = data['lon']
	# z = data['alt']

	UAV[i].pop(0)
	UAV[i].append([x, y])
	UAVe = np.array(UAV[i])

	j = len(UAVe) - 1
	lat = np.array(UAVe[:,0])
	lon = np.array(UAVe[:,1])
	lon_sort = np.sort(lon)

	step = np.diff(lon[(j-5):(j+2)]).mean()
	lon_extra = np.array([lon[j]+step,lon[j]+step*2,lon[j]+step*3])
	spl = splrep(lon_sort[(j-5):(j+2):2], lat[(j-5):(j+2):2], k=1)
	lat_extra = splev(lon_extra, spl)

	return jsonify({'x' : x, 'y' : y, 'z' : z, \
		'state' : 1, 'time' : datetime.datetime.now(), \
		'lat1' : lat_extra[0], 'lon1' : lon_extra[0], \
		'lat2' : lat_extra[1], 'lon2' : lon_extra[1], \
		'lat3' : lat_extra[2], 'lon3' : lon_extra[2]})

@app.route('/status', methods=["GET"])
# @auth.login_required
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
		elif (sv<7 or (abs(lat-myUAV['lat'])>0.000038 or abs(lon-myUAV['lon'])>0.000078 \
		 or abs(alt-myUAV['alt'])>5)):
			state = 0
		myUAV['lat'] = lat
		myUAV['lon'] = lon
		myUAV['alt'] = alt
		return jsonify({'lat' : myUAV['lat'], 'lon' : myUAV['lon'], 'alt' : myUAV['alt'], \
			'state' : state, 'time' : datetime.datetime.now()})
	except:
		return jsonify({'lat' : myUAV['lat'], 'lon' : myUAV['lon'], \
			'alt' : myUAV['alt'], \
			'state' : -1, 'time' : datetime.datetime.now()})

@app.route('/manual_drive', methods=["GET"])
@auth.login_required
def manual_drive():
    return jsonify({'up' : True, 'down' : False})

@app.route('/getendpoint', methods=["GET"])
@auth.login_required
def getendpoint():
    return jsonify({'lat' : endpoint["lat"], 'lon' : endpoint["lon"], 'alt' : endpoint["alt"]})

@app.route('/setendpoint', methods=["GET", "POST"])
@auth.login_required
def setendpoint():
	if request.method == "POST":
		endpoint["lat"] = request.values["setX"]
		endpoint["lon"] = request.values["setY"]
		endpoint["alt"] = request.values["setZ"]
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
		return jsonify({'type' : stype, 'lat' : myUAV['lat'], 'lon' : myUAV['lon'], \
			'alt' : myUAV['alt'], 'time' : datetime.datetime.now()})

@app.route('/game')
@auth.login_required
def game():
    return render_template("game.html")

@app.route('/')
@auth.login_required
def index():
    return render_template("index.html")

if __name__ == "__main__":
	app.run(debug=True, host='0.0.0.0', threaded=True)