from dogFilter_app import VideoCameraSatu
from mataMulut_app import VideoCameraDua
from zoomIn_zoomOut_app import VideoCameraTiga
from flask import Flask, render_template, Response, request

app = Flask(__name__)

def genFrame(video_camera):
    while True:
        frame = video_camera
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def get_ip_and_port():
    ip_address = "0.0.0.0"
    port = request.environ['SERVER_PORT']
    return ip_address, port

@app.route('/video_feed1')
def video_feed1():
    ip_address, port = get_ip_and_port()
    return Response(genFrame(VideoCameraSatu(ip_address, port)),
                    mimetype='multipart/x-mixed-replace; boundary=frame')   

@app.route('/fungsiDua')
def video_feed2():
    ip_address, port = get_ip_and_port()
    return Response(genFrame(VideoCameraDua(ip_address, port)),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
    
@app.route('/fungsiTiga')
def video_feed3():
    ip_address, port = get_ip_and_port()
    return Response(genFrame(VideoCameraTiga(ip_address, port)),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/index.html')
def index1():
    return render_template('index.html')

@app.route('/fungsiSatu.html')
def openkamera1():
    ip, port = get_ip_and_port()
    return render_template('fungsiSatu.html', ip=ip, port=port)

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
