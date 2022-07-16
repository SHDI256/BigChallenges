from generator_pictures import generator
import cv2

for i in generator():
    cv2.imshow('frame', i)
