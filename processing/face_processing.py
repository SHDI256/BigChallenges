from processing.db_processing import add_user, search_by_face
import face_recognition
import numpy as np
import cv2


def faces_encodings_from_frame(frame, fx=1, fy=1):
    small_frame = cv2.resize(frame, (0, 0), fx=fx, fy=fy)
    rgb_small_frame = small_frame[:, :, ::-1]
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
    return face_encodings


def face_recognition_from_list(face_encodings, list_faces_encodings):
    face_names = []
    for face_encoding in face_encodings:
        print(face_encoding.shape)
        matches = face_recognition.compare_faces(list_faces_encodings, face_encoding)
        name = -1

        face_distances = face_recognition.face_distance(list_faces_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = best_match_index

        face_names.append(name)


def face_add(username, age, sex, img, before_values):
    face = faces_encodings_from_frame(img)
    print(face)
    if len(face) != 1:
        print('Error col face')
        return
    print(face)
    add_user(username, age, sex, face[0], before_values)


def face_find(detected_faces_encodings):
    return search_by_face(detected_faces_encodings)
