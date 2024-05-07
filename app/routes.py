from flask import render_template, request, session
from app import app
import os, random
import game_functions

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/mentee')
def mentee():
    return render_template('mentee.html')


emotions = ['joy', 'sadness', 'anger', 'fear', 'surprise', 'contentment', 'jealousy', 'disgust']
images_used = []
images_per_game = 3
sesja = {"counter": 0, "score": 0}
correct_emotion = ""

@app.route('/game', methods=['GET', 'POST'])
def game():
    global correct_emotion
    if request.method == 'POST':
        user_answer = request.form.get('user_answer')
        #correct_emotion = request.form.get('correct_emotion')
        if user_answer == correct_emotion:
            sesja['score'] += 1
        sesja['counter'] += 1  # Zwiększ wartość counter o 1 za każdym razem, gdy formularz zostanie wysłany

        if sesja['counter'] >= images_per_game:
            return render_template('wynik.html', score=sesja["score"], total_images=images_per_game, emotion = correct_emotion, user=user_answer)
       
    if sesja['counter'] < images_per_game: 
        while True:
            random_image = game_functions.get_random_image()
            if random_image not in images_used:
                images_used.append(random_image)
                break
        image_path = f'img/{random_image}'
        fourth_option = random_image.split("_")[0]
        while True:
            random_emotions = random.sample(emotions, 3)
            if fourth_option not in random_emotions:
                break

        random_emotions.append(fourth_option)
        correct_emotion = fourth_option
        #random.shuffle(random_emotions)
        return render_template('game.html', image_path=image_path, emotions=random_emotions, correct_emotion=fourth_option, score=sesja["score"], counter=sesja["counter"])

