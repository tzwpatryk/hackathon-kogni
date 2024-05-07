from app import app
import os, random

def get_random_image(type):
    image_folder = os.path.join(app.root_path, 'static', type)
    images = os.listdir(image_folder)
    random_image = random.choice(images)
    return random_image
