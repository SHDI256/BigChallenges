from utils import face_find
import face_recognition
import numpy as np
import cv2

from time import time

from client_api import Transfer
from vars import HOST

from detector import Detector
import pyrealsense2 as rs

# Configure depth and color streams
pipeline = rs.pipeline()
config = rs.config()

# Get device product line for setting a supporting resolution
pipeline_wrapper = rs.pipeline_wrapper(pipeline)
pipeline_profile = config.resolve(pipeline_wrapper)
device = pipeline_profile.get_device()
device_product_line = str(device.get_info(rs.camera_info.product_line))

found_rgb = False
for s in device.sensors:
    if s.get_info(rs.camera_info.name) == 'RGB Camera':
        found_rgb = True
        break

if not found_rgb:
    print("The demo requires Depth camera with Color sensor")
    exit(0)

config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

if device_product_line == 'L500':
    config.enable_stream(rs.stream.color, 960, 540, rs.format.bgr8, 30)
else:
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# Start streaming
pipeline.start(config)

detector = Detector()

count_frame = 0
start_time = time()


if __name__ == '__main__':
    transfer = Transfer(HOST)

    while True:
        # Grab a single frame of video
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        depth = frames.get_depth_frame()
        image = np.asanyarray(color_frame.get_data())

        # Display the resulting image
        cv2.imshow('Video', image)
        transfer.open()
        transfer.trans_img(cv2.resize(cv2.cvtColor(image, cv2.COLOR_BGR2RGB), (320, 180)))
        transfer.close()

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        if count_frame % 5 == 0 and detector.check_distance(image, depth) < 3.5:
            small_frame = cv2.resize(image, (0, 0), fx=1, fy=1)
            rgb_small_frame = small_frame[:, :, ::-1]
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
            face = face_find(face_encodings)
            if not face:
                face = [-1]
            else:
                face = [face[0]]

            detector.update_points(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            mas = detector.frequent_breath() + [detector.hand_with_phone(), detector.hand_face(),
                                                detector.head_rotate()] + detector.eye_detection() + \
                  [detector.correcting_clothes()] + face

            print(mas)
            transfer.open()
            transfer.trans_data_int(mas)
            transfer.close()


    count_frame += 1

