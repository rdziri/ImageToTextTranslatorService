import cv2
import pytesseract

import googletrans
from googletrans import *

from flask import Flask, flash, request, redirect, url_for, render_template
import urllib.request
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
 
UPLOAD_FOLDER = 'static/uploads/'
 
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
 
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

SUPPORTED_LANGUAGES = {
  "fr": "French",
  "de": "German",
  "es": "Spanish",
  "en": "English",
  "it": "Italian",
}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
     
def extractText(filenameParam):
    '''
        some code is removed for privacy
    '''
    return text

def translateText(inputText, destLanguage):
    '''
        some code is removed for privacy
    '''
    return translatedText.src, translatedText.dest, translatedText.text

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file selected')
        return redirect(request.url)
    if request.form['language']== '':
        flash('No language selected')
        return redirect(request.url)
    file = request.files['file']
    selectedLanguage = request.form['language']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        flash('Image successfully uploaded, its text is extracted and translated')
        
        extractedText = extractText(filename)
        print(extractedText)
        
        srcLanguage, destLanguage, translatedText = translateText(extractedText, selectedLanguage)
        print(translatedText)
            
        return render_template('index.html',srcLanguage=SUPPORTED_LANGUAGES[srcLanguage], destLanguage=SUPPORTED_LANGUAGES[destLanguage], extractedText=extractedText, translatedText=translatedText)
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)

@app.route('/translate', methods=['POST'])
def translate_image():
    if 'file' not in request.files:
        print('No file selected')
        return make_response(jsonify(error="No file selected"), 400)
    if request.form['language']== '':
        print('No language selected')
        return make_response(jsonify(error="No language selected"), 400)
    file = request.files['file']
    selectedLanguage = request.form['language']
    if file.filename == '':
        print('No image selected for uploading')
        return make_response(jsonify(error="No image to upload"), 400)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        print('Image successfully uploaded, its text is extracted and translated')

        extractedText = extractText(filename)
        print(extractedText)

        srcLanguage, destLanguage, translatedText = translateText(extractedText, selectedLanguage)
        print(translatedText)

        return make_response(jsonify(srcLanguage=SUPPORTED_LANGUAGES[srcLanguage], destLanguage=SUPPORTED_LANGUAGES[destLanguage], extractedText=extractedText, translatedText=translatedText), 200)

    else:
        print('Allowed image types are - png, jpg, jpeg, gif')
        return make_response(jsonify(error="Wrong file type"), 400)

@app.route('/display/<filename>')
def display_image(filename):
    return redirect(url_for('static', filename='uploads/' + filename), code=301)

if __name__ == "__main__":
    app.run("10.0.0.8", 8080)