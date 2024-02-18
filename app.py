from dogFilter_app import process_image
from flask import Flask, render_template, Response, request, jsonify
import cv2
import base64

app = Flask(__name__)

@app.route('/process-image', methods=['POST'])
def process_image_route():
    # Terima data gambar dari klien
    image_data = request.data.decode('utf-8')

    # Proses gambar
    processed_image = process_image(image_data)

    # Konversi gambar yang diproses ke format yang bisa dikirim melalui JSON
    _, img_encoded = cv2.imencode('.jpg', processed_image)
    img_bytes = base64.b64encode(img_encoded).decode('utf-8')

    # Kirim gambar yang diproses sebagai respons JSON
    return jsonify({'processed_image': img_bytes})

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/index.html')
def index1():
    return render_template('index.html')

@app.route('/fungsiSatu.html')
def openkamera1():
    return render_template('fungsiSatu.html')

@app.route('/fungsiDua.html')
def openkamera2():
    return render_template('fungsiDua.html')

@app.route('/fungsiTiga.html')
def openkamera3():
    return render_template('fungsiTiga.html')

@app.route('/latihan.html')
def latihan():
    return render_template('latihan.html')

@app.route('/team.html')
def tim():
    return render_template('team.html')
