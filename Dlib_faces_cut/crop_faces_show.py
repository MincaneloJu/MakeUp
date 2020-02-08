
from imutils.face_utils import FaceAligner
import dlib
import numpy as np
import cv2

# Dlib
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('data/dlib/shape_predictor_68_face_landmarks.dat')
#----------------------------------------------------------------------





#----------------------------------------------------------------------
# 讀取圖像
path = "data/images/faces_for_test/"
img = cv2.imread(path+"image2.jpg")

# Dlib 檢測
faces = detector(img, 1)

print("人脸数 / faces in all:", len(faces), "\n")

# 記錄人臉矩陣大小
height_max = 0
width_sum = 0

# 計算要生成的圖片 img_blank 大小
for face in faces:
    print(face)

    # 計算矩形大小
    # (x,y), (宽度width, 高度height)
    pos_start = tuple([face.left(), face.top()])
    pos_end = tuple([face.right(), face.bottom()])

    # 計算矩形框大小
    height = face.bottom()-face.top()
    width = face.right()-face.left()

    # 處理寬度
    width_sum += width
    if width_sum <= 361:
        a = 361 - width_sum
        width_sum += a


    # 處理高度
    if height > height_max:
        height_max = height
    else:
        height_max = height_max

    if height_max <= 361:
        b = 361 - height_max
        height_max += b

# 繪製用來顯示人臉的圖像的大小
print("窗口大小 / The size of window:"
      , '\n', "高度 / height:", height_max
      , '\n', "宽度 / width: ", width_sum)

# 生成用來顯示的圖像
img_blank = np.zeros((height_max, width_sum, 3), np.uint8)

# 紀錄每次開始寫入人臉像素的寬度位置
blank_start = 0

# 將人臉填充到 img_blank
for face in faces:

    height = face.bottom()-face.top()
    #height += 50
    width = face.right()-face.left()
    #width += 50
    # aa = face.top()
    # bb = face.left()
    # aa -=100
    # bb -=100

    # 填充


    for i in range(height):
        for j in range(width):
                # img_blank[i][blank_start + j] = img[aa+ i][bb+ j]
                img_blank[i][blank_start+j] = img[face.top()+i][face.left()+j]
    # 調整圖像
    blank_start += width
cv2.namedWindow("img_faces")#, 2)
cv2.imshow("img_faces", img_blank)
cv2.waitKey(0)