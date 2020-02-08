

import dlib
import numpy as np
import cv2
import os


path_read = "data/images/faces_for_test/"
img = cv2.imread(path_read+"test_faces_3.jpg")


path_save = "data/images/faces_separated/"


# Delete old images
def clear_images():
    imgs = os.listdir(path_save)

    for img in imgs:
        os.remove(path_save + img)

    print("clean finish", '\n')


clear_images()



detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('data/dlib/shape_predictor_68_face_landmarks.dat')
faces = detector(img, 1)

print("人脸数 / faces in all:", len(faces), '\n')

for num, face in enumerate(faces):


    pos_start = tuple([face.left(), face.top()])
    pos_end = tuple([face.right(), face.bottom()])


    height = face.bottom()-face.top()
    width = face.right()-face.left()


    img_blank = np.zeros((height, width, 3), np.uint8)

    for i in range(height):
        for j in range(width):
                img_blank[i][j] = img[face.top()+i][face.left()+j]




    print("Save into:", path_save+"img_face_"+str(num+1)+".jpg")
    cv2.imwrite(path_save+"img_face_"+str(num+1)+".jpg", img_blank)

