from flask import render_template, request, Response, redirect, url_for
from app import app
from patryk.live_functions import get_frames, get_gaze
import cv2
import random, os
from . import game_functions
from transformers import pipeline

camera = cv2.VideoCapture(0)
text_classifier = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", return_all_scores=True)

emotions = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']
images_used = []
images_per_game = 3
sesja = {"counter": 0, "score": 0}

sesja_audio = {"counter": 0, "score": 0}

emotions = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']
images_used = []
images_per_game = 3

sesja = {"counter": 0, "score": 0}
sesja_audio = {"counter": 0, "score": 0}

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/guardian')
def guardian():
    return render_template("guardian.html")

@app.route('/add_jpg', methods=['GET', 'POST'])
def add_jpg():
    if request.method == 'POST':
        if 'image' not in request.files:
            return redirect(request.url)
        image = request.files['image']
        if image.filename == '':
            return redirect(request.url)
        if image:
            label = request.form['label']
            filename = image.filename
            if os.path.exists(f"app/static/img/{label}_1.jpg"):
                i = 1
                while os.path.exists(f"app/static/img/{label}_{i}.jpg"):
                    i += 1
                filename = f"{label}_{i}.jpg"
            else:
                filename = f"{label}_1.jpg"
            image.save(os.path.join("app", "static", "img", filename))
            return redirect(url_for('add_jpg'))
    return render_template("add_jpg.html", emotions=emotions)


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

@app.route('/mentee/live/eyecontact/score')
def mentee_live_eyecontact_score():
    with open('app/static/texts/gaze.txt', 'r') as file:
        loaded_value = file.readline().strip()
    return render_template('mentee_live_eyes_score.html', score=loaded_value)

@app.route('/mentee/live/textclassification', methods=['GET', 'POST'])
def mentee_live_textclassification():
    if request.method == 'POST':
        user_input = request.form.get('user_input')
        results = text_classifier(user_input)
        max_score = 0
        max_label = ""
        for entry in results[0]:
            if entry['score'] > max_score:
                max_score = entry['score']
                max_label = entry['label']
        result_text = f"The most probable emotion is {max_label} with a score of {max_score*100:.2f}%"
        return render_template('mentee_live_textclassification.html', user_input=f"Your text: {user_input}", results=result_text)
    return render_template('mentee_live_textclassification.html')

@app.route('/game_menu')
def game_menu():
    return render_template('game_menu.html')


emotions = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']
images_used = []
images_per_game = 3
sesja = {"counter": 0, "score": 0}

sesja_audio = {"counter": 0, "score": 0}

@app.route('/game', methods=['GET', 'POST'])
def game():
    global sesja
    global correct_emotion

    if sesja_audio['counter'] >= images_per_game:
        return redirect(url_for('new_game')) 

    if request.method == 'POST':
        user_answer = request.form.get('user_answer')
        if user_answer == correct_emotion:
            sesja['score'] += 1
        sesja['counter'] += 1

        if sesja['counter'] >= images_per_game:
            return render_template('wynik.html', score=sesja["score"], total_images=images_per_game, emotion=correct_emotion, user=user_answer)

    if sesja['counter'] < images_per_game:
        random_thing = game_functions.get_random_image("img")
        while random_thing in images_used:
            random_thing = game_functions.get_random_image("img")
        images_used.append(random_thing)
        
        image_path = f'img/{random_thing}'
        fourth_option = random_thing.split("_")[0]
        while True:
            random_emotions = random.sample(emotions, 3)
            if fourth_option not in random_emotions:
                random_emotions.append(fourth_option)
                break
        random.shuffle(random_emotions)

        correct_emotion = fourth_option
        return render_template('game.html', image_path=image_path, emotions=random_emotions, correct_emotion=fourth_option, score=sesja["score"], counter=sesja["counter"])

@app.route('/new_game')
def new_game():
    global sesja
    global correct_emotion
    sesja = {"counter": 0, "score": 0}
    correct_emotion = ""
    return redirect(url_for('game'))


@app.route('/audio', methods=['GET', 'POST'])
def audio():
    global sesja_audio
    global correct_emotion

    if sesja_audio['counter'] >= images_per_game:
        return redirect(url_for('new_audio')) 

    if request.method == 'POST':
        user_answer = request.form.get('user_answer')
        if user_answer == correct_emotion:
            sesja_audio['score'] += 1
        sesja_audio['counter'] += 1

        if sesja_audio['counter'] >= images_per_game:
            return render_template('wynik.html', score=sesja_audio["score"], total_images=images_per_game, emotion=correct_emotion, user=user_answer)

    if sesja_audio['counter'] < images_per_game:
        random_thing = game_functions.get_random_image("sounds")
        while random_thing in images_used:
            random_thing = game_functions.get_random_image("sounds")
        images_used.append(random_thing)
        
        image_path = f'sounds/{random_thing}'
        fourth_option = random_thing.split(".")[0]
        while True:
            random_emotions = random.sample(emotions, 3)
            if fourth_option not in random_emotions:
                random_emotions.append(fourth_option)
                break
        random.shuffle(random_emotions)

        correct_emotion = fourth_option
        return render_template('audio.html', audio_path=image_path, emotions=random_emotions, correct_emotion=fourth_option, score=sesja_audio["score"], counter=sesja_audio["counter"])

@app.route('/new_audio')
def new_audio():
    global sesja_audio
    global correct_emotion
    sesja_audio = {"counter": 0, "score": 0}
    correct_emotion = ""
    return redirect(url_for('audio'))

