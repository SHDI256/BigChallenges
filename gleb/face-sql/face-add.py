from face_processing import face_encodings_frame
import postgresql

# Load the image
image = face_encodings_frame()


db = postgresql.open('pq://user:pass@localhost:5434/db')
