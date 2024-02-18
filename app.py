from dogFilter_app import VideoCameraSatu
from mataMulut_app import VideoCameraDua
from zoomIn_zoomOut_app import VideoCameraTiga
from flask import Flask, render_template, Response, request

app = Flask(__name__)

def genFrame(video_camera):
    while True:
        frame = video_camera.get_frame()
        if frame is None:
            continue
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n'+frame
               +b'\r\n\r\n')


Tidak, frame data yang diterima dari <canvas> dan dikirim ke Flask dalam bentuk data URL (base64) tidak dapat langsung digunakan sebagai parameter untuk cv2.VideoCapture. Anda perlu mengonversi data URL kembali menjadi gambar atau video yang dapat diproses oleh OpenCV.

Berikut adalah langkah-langkah untuk mengonversi data URL kembali menjadi gambar yang dapat digunakan dengan OpenCV:

Di Flask, terima data URL, lalu lakukan dekoding base64 dan simpan gambar ke file sementara.
Gunakan file gambar tersebut sebagai input untuk cv2.VideoCapture.
Berikut adalah contoh implementasinya:

python
Copy code
from flask import Flask, request
import base64
import cv2
import numpy as np
import os

app = Flask(__name__)

@app.route('/send-frame', methods=['POST'])
def receive_camera_url():
    frame_data = request.json['frame']
    img_data = frame_data.split(',')[1]
    img_bytes = base64.b64decode(img_data)
    with open('temp_frame.jpg', 'wb') as f:
        f.write(img_bytes)
    return f

@app.route('/fungsiSatu')
def video_feed1():
    gunicorn_ip = receive_camera_url()
    return Response(genFrame(VideoCameraSatu(gunicorn_ip)),
                    mimetype='multipart/x-mixed-replace; boundary=frame')   

@app.route('/fungsiDua')
def video_feed2():
    gunicorn_ip = receive_camera_url()
    return Response(genFrame(VideoCameraDua(gunicorn_ip)),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
    
@app.route('/fungsiTiga')
def video_feed3():
    gunicorn_ip = receive_camera_url()
    return Response(genFrame(VideoCameraTiga(gunicorn_ip)),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/index.html')
def index1():
    return render_template('index.html')

@app.route('/fungsiSatu.html')
def openkamera1():
    gunicorn_ip = request.host.split(':')[0]
    return render_template('fungsiSatu.html', ip=gunicorn_ip)

@app.route('/fungsiDua.html')
def openkamera2():
    gunicorn_ip = request.host.split(':')[0]
    return render_template('fungsiDua.html', ip=gunicorn_ip)

@app.route('/fungsiTiga.html')
def openkamera3():
    gunicorn_ip = request.host.split(':')[0]
    return render_template('fungsiTiga.html', ip=gunicorn_ip)

@app.route('/latihan.html')
def latihan():
    return render_template('latihan.html')

@app.route('/team.html')
def tim():
    return render_template('team.html')
