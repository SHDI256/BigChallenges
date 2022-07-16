import face_recognition
import numpy as np
import psycopg2
import cv2


def get_connect():
    conn = psycopg2.connect(host='127.0.0.1', port='5432',
                            user='bot', password='1234', dbname='biometry_db')
    return conn


def get_all_db():
    with get_connect() as conn:
        cur = conn.cursor()
        query = f'''SELECT * FROM CRINGE_DB;'''
        cur.execute(query)
        return cur.fetchone()


def db_init():
    with get_connect() as conn:
        cur = conn.cursor()
        print("Opened database successfully")

        cur.execute("create extension if not exists CUBE;")
        # cur.execute("drop table if exists USER;")
        cur.execute('''CREATE TABLE USERS
              (ID        SERIAL PRIMARY KEY  NOT NULL,
              USERNAME   TEXT                NOT NULL,
              SEX        INT                 NOT NULL,
              AGE        INT                 NOT NULL,
              VEC_LOW    CUBE, 
              VEC_HIGH   CUBE
              );''')
        print("Table created successfully")

        conn.commit()


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


def face_add(username, age, sex, face_encodings):
    if len(face_encodings) > 0:
        with get_connect() as conn:
            cur = conn.cursor()
            query = f'''INSERT INTO USERS 
                   (USERNAME, AGE, SEX, VEC_LOW, VEC_HIGH) 
            VALUES (
            {username}, {age}, {sex},
            CUBE(array[{','.join(str(s) for s in face_encodings[0:64])}]), 
            CUBE(array[{','.join(str(s) for s in face_encodings[64:128])}]))'''
            cur.execute(query)
            conn.commit()


def face_find(detected_faces_encodings):
    with get_connect() as conn:
        cur = conn.cursor()
        for i, face_rect_encodings in enumerate(detected_faces_encodings):
            threshold = 0.6
            query = f'''SELECT ID FROM USERS WHERE 
            sqrt(power(CUBE(array[{','.join(str(s) for s in face_rect_encodings[0:64])}]) <-> VEC_LOW, 2) + 
            power(CUBE(array[{','.join(str(s) for s in face_rect_encodings[64:128])}]) <-> VEC_HIGH, 2)) 
            <= {threshold} ''' + \
                    f'''ORDER BY sqrt(
                    power(CUBE(array[{','.join(str(s) for s in face_rect_encodings[0:64])}]) <-> VEC_LOW, 2) + 
                    power(CUBE(array[{','.join(str(s) for s in face_rect_encodings[64:128])}]) <-> VEC_HIGH, 2));'''
            cur.execute(query)
            sol = cur.fetchone()
            return sol


if __name__ == '__main__':
    db_init()
