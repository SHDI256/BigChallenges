import face_recognition
from PIL import Image
import cv2
import os


video_capture = cv2.VideoCapture(4)


def face_split(image):
    faces = []
    face_locations = face_recognition.face_locations(image)
    for i, face_location in enumerate(face_locations):
        top, right, bottom, left = face_location
        face_image = image[top:bottom, left:right]
        faces.append(face_image)
    return faces


def face_encodings_frame():
    ret, frame = video_capture.read()
    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.2, fy=0.2)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    faces = face_split(rgb_small_frame)

    if len(faces) == 0:
        print("Error not face")
        return
    elif len(faces) > 1:
        print('Error cring face')
        return

    rgb_small_frame = faces[0]

    # Find all the faces and face encodings in the current frame of video
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
    return face_encodings


def face_detection_frame():
    pass


def main():
    face_split()


if __name__ == '__main__':
    main()

