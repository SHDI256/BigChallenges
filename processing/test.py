from processing.data_processing import Serializer
from processing.db_processing import search_by_id

import cv2


cmp = Serializer()

if __name__ == "__main__":
    id = 1
    while search_by_id(id):
        print(search_by_id(id))
        id += 1




