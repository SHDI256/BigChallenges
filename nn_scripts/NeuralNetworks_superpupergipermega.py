import face_recognition
import cv2
import numpy as np
from time import time
import mediapipe as mp
import math

from client_api import Transfer
from vars import HOST

transfer = Transfer(HOST)


class Detector:
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.mp_face_mesh = mp.solutions.face_mesh
        self.mp_face_detection = mp.solutions.face_detection

        # head rotate
        self.last_dir_rotate = 'nothing'

        # hand face
        self.hand_on_face = False

        # hand with phone
        self.last_phone_time = time()
        self.phone_in_hand = False
        self.alarm = False

        # frequent breath
        self.count_frequent_breath = 0
        self.now_open = False
        self.now_nervous = False
        self.start_open = 0
        self.start_nervous = 0

        # eye detection
        self.distances_iris_x = []
        self.distances_iris_y = []
        self.last_eye = 'open'

    def update_points(self, image):
        with self.mp_pose.Pose(
                static_image_mode=True,
                model_complexity=0,
                enable_segmentation=True,
                min_detection_confidence=0.5) as pose:
            # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            self.points_body = pose.process(image)
        with self.mp_face_mesh.FaceMesh(
                static_image_mode=True,
                max_num_faces=1,
                refine_landmarks=True,
                min_detection_confidence=0.5) as face_mesh:
            self.points_face = face_mesh.process(image)

    def head_rotate(self):
        try:
            nose = self.points_body.pose_landmarks.landmark[0].x
            right_eye = self.points_body.pose_landmarks.landmark[7].x
            left_eye = self.points_body.pose_landmarks.landmark[8].x
            # print(last)
            if right_eye - nose < 0 and self.last != 'left':
                self.last = 'left'
                return True
            elif left_eye - nose > 0 and self.last != 'right':
                self.last = 'right'
                return True
            elif left_eye - nose <= 0 and right_eye - nose >= 0:
                self.last = 'nothing'
                return False
            return False
        except:
            return False

    def hand_face(self):
        try:
            right_hand = self.points_body.pose_landmarks.landmark[20].y  # чем ниже правая рука, тем больше
            right_hand_x = self.points_body.pose_landmarks.landmark[20].x
            shoulder = self.points_body.pose_landmarks.landmark[11].y
            right_ear_x = self.points_body.pose_landmarks.landmark[8].x
            left_ear_x = self.points_body.pose_landmarks.landmark[7].x
            if right_hand < shoulder and (right_hand_x > right_ear_x and right_hand_x < left_ear_x):
                return True
                # hand_on_face = True
                # self.count_hand_face += 1
            else:
                left_hand_x = self.points_body.pose_landmarks.landmark[19].x
                if left_hand_x < shoulder and (left_hand_x > right_ear_x and left_hand_x < left_ear_x):
                    return True
                    # hand_on_face = True
                    # self.count_hand_face += 1
                else:
                    return False
                    # hand_on_face = False
        except:
            return False

    def hand_with_phone(self):
        try:
            right_hand = self.points_body.pose_landmarks.landmark[20].y  # чем ниже правая рука, тем больше
            right_hand_x = self.points_body.pose_landmarks.landmark[20].x
            shoulder = self.points_body.pose_landmarks.landmark[11].y
            right_ear_x = self.points_body.pose_landmarks.landmark[8].x
            left_ear_x = self.points_body.pose_landmarks.landmark[7].x
            if right_hand < shoulder and (right_hand_x < right_ear_x or right_hand_x > left_ear_x):
                return True
                # if not self.phone_in_hand:
                # self.phone_in_hand = True
                # self.last_phone_time = time()
            else:
                left_hand = self.points_body.pose_landmarks.landmark[19].y  # чем ниже левая рука, тем больше
                left_hand_x = self.points_body.pose_landmarks.landmark[19].x
                if left_hand < shoulder and (left_hand_x < right_ear_x or left_hand_x > left_ear_x):
                    return True
                else:
                    return False
        except AttributeError:
            return False

    def frequent_breath(self):
        try:
            face_size_y = abs(
                self.points_face.multi_face_landmarks[0].landmark[10].y -
                self.points_face.multi_face_landmarks[0].landmark[
                    102].y)
            up_mouth = self.points_face.multi_face_landmarks[0].landmark[0].y
            down_mouth = self.points_face.multi_face_landmarks[0].landmark[17].y

            num = abs(up_mouth - down_mouth) / face_size_y * 100
            mas = [False, False]
            if num < 13:
                mas[0] = True
                # self.now_nervous = True
                # self.now_open = False
                # self.start_nervous = time()
            elif num > 30:
                mas[1] = True
                # self.now_open = True
                # self.now_nervous = False
                # self.start_open = time()
            # elif num >= 13 and num <= 30:
            # self.now_nervous = False
            # self.now_open = False
            return mas
        except:
            return [False, False]

    def eye_detection(self):
        try:
            mas = [False, False]

            face_size_y = abs(
                self.points_face.multi_face_landmarks[0].landmark[10].y -
                self.points_face.multi_face_landmarks[0].landmark[102].y)
            left_eye_y = abs(self.points_face.multi_face_landmarks[0].landmark[374].y -
                             self.points_face.multi_face_landmarks[0].landmark[386].y) / face_size_y * 100
            mas[0] = left_eye_y < 6

            x_iris = (self.points_face.multi_face_landmarks[0].landmark[468].x -
                      self.points_face.multi_face_landmarks[0].landmark[130].x) / (
                             self.points_face.multi_face_landmarks[0].landmark[157].x -
                             self.points_face.multi_face_landmarks[0].landmark[130].x)
            y_iris = (self.points_face.multi_face_landmarks[0].landmark[468].y -
                      self.points_face.multi_face_landmarks[0].landmark[472].y) / (
                             self.points_face.multi_face_landmarks[0].landmark[472].y -
                             self.points_face.multi_face_landmarks[0].landmark[470].y)

            self.distances_iris_x.append(x_iris)
            self.distances_iris_y.append(y_iris)

            if len(self.distances_iris_x) > 100:
                distances_iris_x = self.distances_iris_x[-100:]
            if len(self.distances_iris_x) < 20:
                return mas

            # print(distances_iris_y[-2], distances_iris_y[-1])
            speed_x = abs(self.distances_iris_x[-2] - self.distances_iris_x[-1])
            speed_y = abs(self.distances_iris_y[-2] - self.distances_iris_y[-1])
            speed = math.sqrt(speed_x ** 2 + speed_y ** 2)
            mas[1] = speed > 0.07
            return mas
        except:
            return mas

    def correcting_clothes(self):
        try:
            right_shoulder = self.points_body.pose_landmarks.landmark[12].x
            right_shoulder_y = self.points_body.pose_landmarks.landmark[12].y
            left_shoulder = self.points_body.pose_landmarks.landmark[11].x
            left_shoulder_y = self.points_body.pose_landmarks.landmark[11].y
            middle = right_shoulder + (left_shoulder - right_shoulder) / 2
            middle_y = right_shoulder_y + abs(right_shoulder_y - left_shoulder_y) / 2
            right_hand = self.points_body.pose_landmarks.landmark[20].x
            right_hand_y = self.points_body.pose_landmarks.landmark[20].y
            if (abs(middle - right_hand) < 0.05) and (abs(middle_y - right_hand_y) < 0.06):
                return True
            else:
                left_hand = self.points_body.pose_landmarks.landmark[19].x
                left_hand_y = self.points_body.pose_landmarks.landmark[19].y
                if (abs(middle - left_hand) < 0.05) and (abs(middle_y - left_hand_y) < 0.06):
                    return True
                else:
                    return False
        except:
            return False

    def check_distance(self, image, depth_image):
        try:
            with self.mp_face_detection.FaceDetection(
                    model_selection=1, min_detection_confidence=0.5) as face_detection:
                results = face_detection.process(image)
                middle_x = results.detections[0].location_data.relative_bounding_box.xmin + (
                        results.detections[0].location_data.relative_bounding_box.width / 2)
                middle_y = results.detections[0].location_data.relative_bounding_box.ymin + (
                        results.detections[0].location_data.relative_bounding_box.height / 2)
                dist = depth_image.get_distance(320, 180)
                return dist
        except:
            return 500

detector = Detector()

count_frame = 0
start_time = time()

if __name__ == '__main__':

    nataly_image = face_recognition.load_image_file("/home/user/Desktop/BIgChallenges/gleb/gallery/nataly_0.jpg")
    nataly_face_encoding = face_recognition.face_encodings(nataly_image)[0]

    # Load a second sample picture and learn how to recognize it.
    gleb_image = face_recognition.load_image_file("/home/user/Desktop/BIgChallenges/gleb/gallery/gleb_0.jpg")
    gleb_face_encoding = face_recognition.face_encodings(gleb_image)[0]

    andrei_image = face_recognition.load_image_file("/home/user/Desktop/BIgChallenges/gleb/gallery/Andrei_0.jpg")
    andrei_face_encoding = face_recognition.face_encodings(andrei_image)[0]

    daniil_image = face_recognition.load_image_file("/home/user/Desktop/BIgChallenges/gleb/gallery/daniil_0.jpg")
    daniil_face_encoding = face_recognition.face_encodings(daniil_image)[0]

    andrei_antonovic_image = face_recognition.load_image_file(
        "/home/user/Desktop/BIgChallenges/gleb/gallery/Andrei_1.jpg")
    andrei_antonovic_face_encoding = face_recognition.face_encodings(andrei_antonovic_image)[0]

    # Create arrays of known face encodings and their names
    known_face_encodings = [
        nataly_face_encoding,
        gleb_face_encoding,
        andrei_antonovic_face_encoding
    ]
    known_face_names = [
        "Natali",
        "Gleb",
        "Andrei Antonovich"
    ]

    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []

    cap = cv2.VideoCapture('/home/user/Downloads/video4.mp4')
    cap.set(cv2.CAP_PROP_FPS, 25)

    while cap.isOpened():
        # Grab a single frame of video
        '''frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        depth = frames.get_depth_frame()'''
        _, color_frame = cap.read()
        image = np.asanyarray(color_frame)
        print(image.shape)
        images = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        if count_frame % 3 == 0:
            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(image, (0, 0), fx=0.25, fy=0.25)

            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = small_frame[:, :, ::-1]

            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                print(face_encoding)
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"

                # # If a match was found in known_face_encodings, just use the first one.
                # if True in matches:
                #     first_match_index = matches.index(True)
                #     name = known_face_names[first_match_index]

                # Or instead, use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]

                face_names.append(name)

        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(image, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(image, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(image, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # # Display the resulting image
        cv2.imshow('Video', image)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        image = images

        if count_frame % 1 == 0:
            detector.update_points(image)
            print('Detecting point')

            mas = detector.frequent_breath() + [detector.hand_with_phone(), detector.hand_face(),
                                                detector.head_rotate()] + detector.eye_detection() + [
                      detector.correcting_clothes()]
            try:
                transfer.open()
                print('Tranfer was open')
                transfer.trans_data_bool(mas)
                transfer.close()
                print(mas)
            except:
                try:
                    print('EXCEPT!')
                    transfer = Transfer(HOST)
                except:
                    print("Disconnected")

        try:
            print(2)
            transfer.open()
            print(3)
            transfer.trans_img(cv2.resize(image, (320, 180)))
            transfer.close()
        except:
            try:
                print('Except')
                transfer = Transfer(HOST)
            except:
                print("Disconnected")

        count_frame += 1
