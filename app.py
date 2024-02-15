from dogFilter_app import VideoCameraSatu
from mataMulut_app import VideoCameraDua
from zoomIn_zoomOut_app import VideoCameraTiga
from flask import Flask, render_template, Response, request
from flask_cors import CORS

app = Flask(__name__)

camera_info = None

@app.route('/camera-url', methods=['POST'])
def get_camera_url():
    data = request.json
    ip_address = data['ip']
    port = data['port']
    camera_url = f"http://{ip_address}:{port}/video_feed1"
    return camera_url

def genSatu():
    global camera_info
    if camera_info:
        camera = VideoCameraSatu(camera_info)
        while True:
            frame = camera.get_frame()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def genDua(mataMulut_app):
    while True:
        frame = mataMulut_app.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n'+frame
               +b'\r\n\r\n')
        
def genTiga(zoomIn_zoomOut_app):
    while True:
        frame = zoomIn_zoomOut_app.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n'+frame
               +b'\r\n\r\n')
        
@app.route('/video_feed1')
def video_feed1():
    return Response(genSatu(), mimetype='multipart/x-mixed-replace; boundary=frame')   

@app.route('/fungsiDua')
def video_feed2():
    return Response(genDua(VideoCameraDua()),
        mimetype='multipart/x-mixed-replace; boundary=frame')
    
@app.route('/fungsiTiga')
def video_feed3():
    return Response(genTiga(VideoCameraTiga()),
        mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/index.html')
def index1():
    return render_template('index.html')

@app.route('/fungsiSatu.html')
def index2():
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

CORS(app)

#if __name__ == '__main__':
#    app.run(debug=True, host='0.0.0.0')
