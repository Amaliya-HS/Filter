from dogFilter_app import get_frame
from flask import Flask, render_template, Response, request, jsonify

app = Flask(__name__)

@app.route('/filter-one', methods=['POST'])
def process_filter_one():
    image_data = request.get_data()
    image_array = np.frombuffer(image_data, dtype=np.uint8)
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    processed_image = get_frame(image)
    processed_image_list = processed_image.tolist()
    return jsonify({'processed_image': processed_image_list})

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
