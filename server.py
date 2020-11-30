from flask import Flask, render_template, redirect, url_for, request, session, flash, jsonify, Response
from flask_httpauth import HTTPDigestAuth
from werkzeug.security import generate_password_hash, check_password_hash
import numpy as np
import cv2
import time
import random
from camera import Camera

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hello'
auth = HTTPDigestAuth()

vc = cv2.VideoCapture(0)

users = {
    "admin": "admin"
}

endpoint = {
	"x" : 0,
	"y" : 0,
	"z" : 0
}

# 'user' : auth.username()

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@auth.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None
 
@app.route('/')
@auth.login_required
def index():
    return render_template("index.html")

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
		return jsonify({'type' : stype, 'image' : 'http://localhost:5000/latest_image', \
		 'time' : round(time.time())})
	elif stype == 'gps':
		return jsonify({'type' : stype, 'x' : round(random.uniform(59.0, 60.0), 4), \
			'y' : round(random.uniform(30.0, 31.0), 4), \
			'z' : round(random.uniform(1.0, 20.0), 2), 'time' : round(time.time())})

# @app.route('/logout', methods=['GET', 'POST'])
# @auth.login_required
# def logout():
#     auth.username = None

if __name__ == "__main__":
	app.run(debug=True, host='0.0.0.0', threaded=True)