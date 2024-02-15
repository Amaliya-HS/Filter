import cv2
import cv2
import math
import dlib
from imutils import face_utils, rotate_bound
from imutils.video import VideoStream

def draw_sprite(frame, sprite, x_offset, y_offset):
    (h, w) = (sprite.shape[0], sprite.shape[1])
    (imgH, imgW) = (frame.shape[0], frame.shape[1])

    if y_offset + h >= imgH:  
        sprite = sprite[0 : imgH - y_offset, :, :]

    if x_offset + w >= imgW:  
        sprite = sprite[:, 0 : imgW - x_offset, :]

    if x_offset < 0: 
        sprite = sprite[:, abs(x_offset) : :, :]
        w = sprite.shape[1]
        x_offset = 0

    for c in range(3):
        frame[y_offset : y_offset + h, x_offset : x_offset + w, c] = sprite[:, :, c] * (
            sprite[:, :, 3] / 255.0
        ) + frame[y_offset : y_offset + h, x_offset : x_offset + w, c] * (
            1.0 - sprite[:, :, 3] / 255.0
        )
    return frame

def adjust_sprite2head(sprite, head_width, head_ypos, ontop=True):
    (h_sprite, w_sprite) = (sprite.shape[0], sprite.shape[1])
    factor = 1.0 * head_width / w_sprite
    sprite = cv2.resize(
        sprite, (0, 0), fx=factor, fy=factor
    ) 
    (h_sprite, w_sprite) = (sprite.shape[0], sprite.shape[1])

    y_orig = (
        head_ypos - h_sprite if ontop else head_ypos
    )  
    if (
        y_orig < 0
    ):  
        sprite = sprite[abs(y_orig) : :, :, :]  
        y_orig = 0 
    return (sprite, y_orig)

def apply_sprite(image, path2sprite, w, x, y, angle, ontop=True):
    sprite = cv2.imread(path2sprite, -1)
    sprite = rotate_bound(sprite, angle)
    (sprite, y_final) = adjust_sprite2head(sprite, w, y, ontop)
    image = draw_sprite(image, sprite, x, y_final)

def calculate_inclination(point1, point2):
    x1, x2, y1, y2 = point1[0], point2[0], point1[1], point2[1]
    incl = 180 / math.pi * math.atan((float(y2 - y1)) / (x2 - x1))
    return incl

def calculate_boundbox(list_coordinates):
    x = min(list_coordinates[:, 0])
    y = min(list_coordinates[:, 1])
    w = max(list_coordinates[:, 0]) - x
    h = max(list_coordinates[:, 1]) - y
    return (x, y, w, h)

def get_face_boundbox(points, face_part):
    if face_part == 5:
        (x, y, w, h) = calculate_boundbox(points[29:36])
    elif face_part == 6:
        (x, y, w, h) = calculate_boundbox(points[48:68])
    return (x, y, w, h)

class VideoCameraSatu(object):
    def __init__(self, ip_camera):
        self.video = VideoStream(src=ip_camera).start()

    def __del__(self):
        self.video.stop()
        
    def get_frame(self):
        image = self.video.read()
    
        print("[INFO] loading facial landmark predictor...")
        model = "shape_predictor_68_face_landmarks.dat"
        predictor = dlib.shape_predictor(model)
    
        detector = dlib.get_frontal_face_detector()
                
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = detector(gray, 0)
    
        for face in faces:
            (x, y, w, h) = (face.left(), face.top(), face.width(), face.height())
    
            shape = predictor(gray, face)
            shape = face_utils.shape_to_np(shape)
            incl = calculate_inclination(shape[17], shape[26])
            is_mouth_open = (shape[66][1] - shape[62][1]) >= 10 
            (x0, y0, w0, h0) = get_face_boundbox(shape, 6) 
    
            (x3, y3, w3, h3) = get_face_boundbox(shape, 5)  
            apply_sprite(image, "static/gambar/dogs_nose.png", w3, x3, y3, incl, ontop=False)
            apply_sprite(image, "static/gambar/dog_ears.png", w, x, y, incl) 
    
            if is_mouth_open:
                apply_sprite(image, "static/gambar/dogs_tongue.png", w0, x0, y0, incl, ontop=False)
    
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()
