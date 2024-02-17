from dogFilter_app import VideoCameraSatu
from mataMulut_app import VideoCameraDua
from zoomIn_zoomOut_app import VideoCameraTiga
from flask import Flask, render_template, Response, request

app = Flask(__name__)

def genFrame(video_camera):
    while True:
        frame = video_camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n'+frame
               +b'\r\n\r\n')

def get_ip_and_port():
    ip_address = "0.0.0.0"
    port = request.environ['SERVER_PORT']
    return ip_address, port

@app.route('/fungsiSatu')
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

@app.route('/fungsiSatu.html')
def openkamera1():
    ip_address, port = get_ip_and_port()
    return render_template('fungsiSatu.html', ip=ip_address, port=port)

@app.route('/fungsiDua.html')
def openkamera2():
    ip_address, port = get_ip_and_port()
    return render_template('fungsiDua.html', ip=ip_address, port=port)

@app.route('/fungsiTiga.html')
def openkamera3():
    ip_address, port = get_ip_and_port()
    return render_template('fungsiTiga.html', ip=ip_address, port=port)

