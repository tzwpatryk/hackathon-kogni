from flask import render_template, request, session, Response, redirect, url_for
from app import app
import os, random
from . import game_functions
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
        return redirect(url_for('new_game'))  # Przekierowanie do rozpoczęcia nowej gry

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
        fourth_option = random_thing.split(".")[0]
        random_emotions = random.sample(emotions, 3)
        random_emotions.append(fourth_option)
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
        return redirect(url_for('new_audio'))  # Przekierowanie do rozpoczęcia nowej gry

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
        random_emotions = random.sample(emotions, 3)
        random_emotions.append(fourth_option)
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