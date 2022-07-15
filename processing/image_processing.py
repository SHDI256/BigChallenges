from PIL import Image
import numpy as np
from io import BytesIO


def img_to_numpy(img):
    img = Image.open(img)
    img_np = np.asarray(img)

    return img_np


def numpy_to_bytes(img_np):
    np_bytes = BytesIO()
    np.save(np_bytes, img_np, allow_pickle=True)
    np_bytes = np_bytes.getvalue()

    return np_bytes


def img_to_bytes(img):
    img_np = img_to_numpy(img)
    bytes = numpy_to_bytes(img_np)

    return bytes


def numpy_to_img(np_bytes, path):
    img = Image.fromarray(np_bytes, 'RGB')
    img.save(path)


def bytes_to_numpy(bytes):
    np_bytes = BytesIO(bytes)
    np_bytes = np.load(np_bytes, allow_pickle=True)

    return np_bytes


def bytes_to_img(bytes, path):
    np_bytes = bytes_to_numpy(bytes)
    numpy_to_img(np_bytes, path)
