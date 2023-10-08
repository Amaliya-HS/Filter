import cv2
import dlib
from scipy.spatial import distance as dist
from imutils import face_utils

video = cv2.VideoCapture(0)


model = "shape_predictor_68_face_landmarks.dat"
predictor = dlib.shape_predictor(model)
detector = dlib.get_frontal_face_detector()
 
def eye_aspect_ratio(eye):
	A = dist.euclidean(eye[1], eye[5])
	B = dist.euclidean(eye[2], eye[4])
	C = dist.euclidean(eye[0], eye[3])
	ear = (A + B) / (2.0 * C)
	return ear
  
def smile(mouth):
    A = dist.euclidean(mouth[3], mouth[9]) 
    B = dist.euclidean(mouth[2], mouth[10]) 
    C = dist.euclidean(mouth[4], mouth[8])
    L = (A+B+C)/3
    D = dist.euclidean(mouth[0], mouth[6])
    mar=(L/D)
    return mar

class VideoCameraDua(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        
    def __del__(self):
        self.video.release()
        
    def get_frame(self):
        ret, image = self.video.read()

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = detector(gray, 0)
        print("[INFO] loading facial landmark predictor...")
        (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
        (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
        (mStart, mEnd) = face_utils.FACIAL_LANDMARKS_IDXS["mouth"]
        EYE_AR_THRESH = 0.3
        TOTAL_MOUTH = 0
        TOTAL_EYE = 0

        i = 0
        for face in faces:
            shape = predictor(gray, face)
            i += 1
            pad = 10
 
            xeyeright = [shape.part(x).x for x in range(42, 47)]
            yeyeright = [shape.part(x).y for x in range(42, 47)]
            max_xer = max(xeyeright)
            min_xer = min(xeyeright)
            max_yer = max(yeyeright)
            min_yer = min(yeyeright)
            crop_eyer = image[min_yer - pad : max_yer + pad, min_xer - pad : max_xer + pad]
            
            xeyeleft = [shape.part(x).x for x in range(36, 41)]
            yeyeleft = [shape.part(x).y for x in range(36, 41)]
            max_xel = max(xeyeleft)
            min_xel = min(xeyeleft)
            max_yel = max(yeyeleft)
            min_yel = min(yeyeleft)
            crop_eyel = image[min_yel - pad : max_yel + pad, min_xel - pad : max_xel + pad]
            
            xmouthpoints = [shape.part(x).x for x in range(48, 67)]
            ymouthpoints = [shape.part(x).y for x in range(48, 67)]
            max_xm = max(xmouthpoints)
            min_xm = min(xmouthpoints)
            max_ym = max(ymouthpoints)
            min_ym = min(ymouthpoints)
            crop_mouth = image[min_ym - pad : max_ym + pad, min_xm - pad : max_xm + pad]
 
            shape = face_utils.shape_to_np(shape)
            leftEye = shape[lStart:lEnd]
            rightEye = shape[rStart:rEnd]
            leftEAR = eye_aspect_ratio(leftEye)
            rightEAR = eye_aspect_ratio(rightEye)
            ear = (leftEAR + rightEAR) / 2.0
            mouth = shape[mStart : mEnd]
            mar = smile(mouth)

            if ear < EYE_AR_THRESH:
                TOTAL_EYE = TOTAL_EYE + 1

                image[min_yer - pad : max_yer + pad, min_xer - pad : max_xer + pad] = cv2.resize(crop_mouth, (2 * pad + max_xer - min_xer, 2 * pad + max_yer - min_yer), interpolation = cv2.INTER_AREA)
                image[min_yel - pad : max_yel + pad, min_xel - pad : max_xel + pad] = cv2.resize(crop_mouth, (2 * pad + max_xel - min_xel, 2 * pad + max_yel - min_yel), interpolation = cv2.INTER_AREA)
            
            if mar <= .3 or mar > .38: 
                TOTAL_MOUTH = TOTAL_MOUTH + 1

                image[min_ym - pad : max_ym + pad, min_xm - pad : max_xm + pad] = cv2.resize(crop_eyer, (2 * pad + max_xm - min_xm, 2 * pad + max_ym - min_ym), interpolation = cv2.INTER_AREA)

            cv2.putText(image, "Blinks: {}".format(TOTAL_EYE), (500, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            cv2.putText(image, "EAR: {:.2f}".format(ear), (300, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            cv2.putText(image, "MAR: {}".format(mar), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()