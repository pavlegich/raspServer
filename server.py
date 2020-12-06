from flask import Flask, render_template, redirect, url_for, request, session, flash, jsonify, Response
from flask_httpauth import HTTPDigestAuth
from werkzeug.security import generate_password_hash, check_password_hash
import time
import random
# from camera_pi import Camera
import numpy as np
import cv2
import threading

# faceCascade = cv2.CascadeClassifier('Cascades/haarcascade_frontalface_default.xml')

# ip_address = "192.168.43.210"
ip_address = "192.168.1.102"
app = Flask(__name__)
app.config['SECRET_KEY'] = 'hello'
auth = HTTPDigestAuth()
x1 = 60.03143
y1 = 30.36020

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
	"x" : 59.972919,
	"y" : 30.302309,
	"z" : 0
}

UAV2 = {
	
	"x" : 59.822621,
	"y" : 30.347212,
	"x1" : round(random.uniform(60.03158, 60.03160), 5),
	"y1" : round(random.uniform(30.36010, 30.36011), 5),
	"x2" : round(random.uniform(60.03161, 60.03163), 5),
	"y2" : round(random.uniform(30.36012, 30.36014), 5),
	"x3" : round(random.uniform(60.03164, 60.03167), 5),
	"y3" : round(random.uniform(30.36013, 30.36015), 5)
}

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

# 'user' : auth.username()

# def setInterval(func,time):
#     e = threading.Event()
#     while not e.wait(time):
#         func()


def gen_img(camera):
	frame = camera.get_frame()
	yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def gen(camera):
	while True:
		frame = camera.get_frame()
		yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
@auth.login_required
def video_feed():
	return Response(gen(Camera()), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/image')
@auth.login_required
def image():
	return Response(gen_img(Camera()), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/latest_image')
@auth.login_required
def latest_image():
	return render_template("latest_image.html")

@app.route('/status', methods=["GET"])
@auth.login_required
def status():
    return jsonify({'x' : round(random.uniform(59.0, 60.0), 4), \
			'y' : round(random.uniform(30.0, 31.0), 4), \
			'z' : round(random.uniform(1.0, 20.0), 2), \
			'state' : 1, 'time' : round(time.time())})

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
		endpoint["x"] = request.form["endX"]
		endpoint["y"] = request.form["endY"]
		endpoint["z"] = request.form["endZ"]
		return redirect(url_for("index"))
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

@auth.login_required
def get_gps():
	UAV["x"] = 59.972919
	UAV["y"] = 30.302309
	UAV["z"] = 15
	return 1

# @app.route('/logout', methods=['GET', 'POST'])
# @auth.login_required
# def logout():
#     auth.username = None

# @app.route('/map')
# @auth.login_required
# def map():
# 	return render_template("map.html")

@app.route('/')
@auth.login_required
def index():
    return render_template("index.html", UAV = UAV, UAV2 = UAV2, UAV3 = UAV3)

if __name__ == "__main__":
	app.run(debug=True, host='0.0.0.0', threaded=True)