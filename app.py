from flask import Flask, render_template, request, redirect, url_for
from other_code import process_image, translate_text, text_to_speech, create_video

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('ocr_converter.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect('/')
    
    uploaded_file = request.files['file']
    if uploaded_file.filename == '':
        return redirect('/')
    
    uploaded_file.save('static/uploaded_image.jpg')
    return redirect('/convert')

@app.route('/convert', methods=['POST', 'GET'])
def convert():
    input_image_path = "static/uploaded_image.jpg"
    target_language = request.form.get('target_language', 'en')  # Default to English if not selected

    extracted_text = process_image(input_image_path)

    if extracted_text:
        translated_text = translate_text(extracted_text, target_language)
        text_to_speech(translated_text, target_language)
        create_video(input_image_path, "static/output.mp3", 'static/output.mp4')
        return render_template('conversion_result.html', video_path='static/output.mp4')

    return redirect('/')

if __name__ == '__main__':
    app.run()
