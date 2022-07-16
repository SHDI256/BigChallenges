from utils import face_add, faces_encodings_from_frame
import cv2

video_capture = cv2.VideoCapture(4)

if __name__ == "__main__":
    while True:
        ret, frame = video_capture.read()
        faces = faces_encodings_from_frame(frame, 1, 1)
        if len(faces) < 1:
            print('Ti gde?')      
        elif len(faces) > 1:
            print('eto perebor')
        elif ret:
            face_add('123', 33, 0, faces[0])
            print('Add face!')
            break
        else:
            print(ret)

        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
