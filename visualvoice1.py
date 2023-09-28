import cv2
import numpy as np
from PIL import Image
from google.cloud import vision
from google.cloud import translate
from gtts import gTTS
import moviepy.editor as mp
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"projectocr-399718-616bacd8b14e.json"

# Initialize Google Cloud Vision and Translation clients
vision_client = vision.ImageAnnotatorClient()
translate_client = translate.TranslationServiceClient()

# Function to extract text from an image using Google Cloud Vision
def process_image(image_path):
    with open(image_path, 'rb') as image_file:
        content = image_file.read()
    
    image = vision.Image(content=content)
    response = vision_client.text_detection(image=image)
    texts = response.text_annotations
    
    if texts:
        return texts[0].description
    else:
        return None

# Function to translate text to the desired language
def translate_text(text, target_language):
    parent = f"projects/projectocr-399718"
    response = translate_client.translate_text(
        parent=parent,
        contents=[text],
        target_language_code=target_language,
    )
    translation = response.translations[0].translated_text
    return translation

# Function to generate audio from translated text
def text_to_speech(text, language):
    tts = gTTS(text, lang=language)
    tts.save("static/output.mp3")

# Function to create a video from an image and audio
def create_video(image_path, audio_path, video_output_path):
    audio = mp.AudioFileClip(audio_path)
    img = Image.open(image_path)
    img_duration = audio.duration

    video = mp.ImageClip(np.array(img))
    video = video.set_duration(img_duration)
    video = video.set_audio(audio)
    
    # Set the frames per second (fps) for the video (e.g., 24 fps)
    video.fps = 24

    video.write_videofile(video_output_path, codec='libx264')
