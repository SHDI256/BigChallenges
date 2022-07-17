from processing.data_processing import Serializer
import cv2

video_capture = cv2.VideoCapture(4)

cmp = Serializer()

if __name__ == "__main__":
    while True:
        ret, frame = video_capture.read()

        cmp.add_user('Gleb', 0, 16, frame)

        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
