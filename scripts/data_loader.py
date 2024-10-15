import os
import numpy as np
from PIL import Image, ImageChops, ImageEnhance
from keras.utils import to_categorical
from sklearn.model_selection import train_test_split
from config import IMAGE_DIR, IMAGE_SIZE

def convert_to_ela_image(image_path, quality=90):
    """
    Converts image to ELA format
    """
    original_image = Image.open(image_path).convert('RGB')
    temp_filename = 'temp_file_name.jpg'
    ela_filename = 'temp_ela.png'

    original_image.save(temp_filename, 'JPEG', quality=quality)
    temp_image = Image.open(temp_filename)

    ela_image = ImageChops.difference(original_image, temp_image)
    extrema = ela_image.getextrema()
    
    max_diff = max([ex[1] for ex in extrema]) if extrema else 1
    scale = 255.0 / max_diff if max_diff > 0 else 1

    ela_image = ImageEnhance.Brightness(ela_image).enhance(scale)
    return ela_image

def prepare_image(image_path):
    """
    Prepares the image for training
    """
    return np.array(convert_to_ela_image(image_path).resize(IMAGE_SIZE)).flatten() / 255.0

def load_data():
    """
    Load image data and labels[1]
    """
    X, Y = [], []

    path = os.path.join(IMAGE_DIR, 'Au/')
    for dirname, _, filenames in os.walk(path):
        for filename in filenames:
            if filename.endswith(('jpg', 'png')):
                full_path = os.path.join(dirname, filename)
                X.append(prepare_image(full_path))
                Y.append(1)  

    """
    Load image data and labels[0]
    """
    path = os.path.join(IMAGE_DIR, 'Tp/')
    for dirname, _, filenames in os.walk(path):
        for filename in filenames:
            if filename.endswith(('jpg', 'png')):
                full_path = os.path.join(dirname, filename)
                X.append(prepare_image(full_path))
                Y.append(0) 

    X = np.array(X)
    Y = to_categorical(Y, 2) 
    X = X.reshape(-1, *IMAGE_SIZE, 3)

    return train_test_split(X, Y, test_size=0.2, random_state=5)
