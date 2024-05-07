from flask import render_template, Response
from app import app
from patryk.live_functions import get_frames

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/mentee')
def mentee():
    return render_template('mentee.html')

@app.route('/mentee/live')
def mentee_live():
    return Response(get_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')