from flask import Flask, render_template, Response, request
from dogFilter_app import VideoCameraSatu
from mataMulut_app import VideoCameraDua
from zoomIn_zoomOut_app import VideoCameraTiga

app = Flask(__name__)

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/fungsiSatu')
def video_feed1():
    gunicorn_ip = request.host.split(':')[0]
    return Response(gen(VideoCameraSatu("https://{gunicorn_ip}/fungsiSatu")), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/fungsiDua')
def video_feed2():
    return Response(gen(VideoCameraDua()), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/fungsiTiga')
def video_feed3():
    return Response(gen(VideoCameraTiga()), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/index.html')
def index1():
    return render_template('index.html')

@app.route('/fungsiSatu.html')
def fungsiSatu():
    return render_template('fungsiSatu.html')

@app.route('/fungsiDua.html')
def fungsiDua():
    return render_template('fungsiDua.html')

@app.route('/fungsiTiga.html')
def fungsiTiga():
    return render_template('fungsiTiga.html')

@app.route('/latihan.html')
def latihan():
    return render_template('latihan.html')

@app.route('/team.html')
def tim():
    return render_template('team.html')
