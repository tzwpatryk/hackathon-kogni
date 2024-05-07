from flask import render_template, Response, request
from app import app
from patryk.live_functions import get_frames, get_gaze
import cv2

camera = cv2.VideoCapture(0)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/mentee')
def mentee():
    return render_template('mentee.html')

@app.route('/mentee/live')
def mentee_live():
    return render_template('mentee_live.html')

@app.route('/mentee/live/emotions')
def mentee_live_emotions(): 
    return Response(get_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/mentee/live/eyecontact')
def mentee_live_eyecontact():
    return render_template('mentee_live_eyes.html')

@app.route('/mentee/live/gaze')
def mentee_live_gaze():
    return Response(get_gaze(camera), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/requests',methods=['GET'])
def tasks():
    if request.method=='GET':
        app.logger.info('moj tekst')
        return render_template('mentee_live_eyes.html')
    return render_template('mentee_live_eyes.html')