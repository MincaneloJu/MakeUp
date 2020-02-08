# 使用webcam 偵測多人/單人，並顯示偵測到的人臉；


import dlib
import cv2
import time

# 儲存截圖目錄
path_screenshots = "data/images/screenshots/"

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('data/dlib/shape_predictor_68_face_landmarks.dat')

# 創建CV2對象
cap = cv2.VideoCapture(0)

# 設置視頻參數，propId 設置的視頻參數，value 設置的參數值
cap.set(3, 960)

# 截圖 screenshots 的計數器
ss_cnt = 0

while cap.isOpened():
    flag, img_rd = cap.read()

    # 每帧數據延時 1ms，延時為 0 讀取的是靜態帧
    k = cv2.waitKey(1)

    # 取灰階
    img_gray = cv2.cvtColor(img_rd, cv2.COLOR_RGB2GRAY)

    # 人臉數
    faces = detector(img_gray, 0)

    # 要寫的字體
    font = cv2.FONT_HERSHEY_SIMPLEX

    # 按下 'q' 退出
    if k == ord('q'):
        break
    else:
        # 檢測到人臉
        if len(faces) != 0:
            # 紀錄每次開始寫入人像素的寬度位置
            faces_start_width = 0

            for face in faces:
                # 繪製矩形框
                cv2.rectangle(img_rd, tuple([face.left(), face.top()]), tuple([face.right(), face.bottom()]),
                              (0, 255, 255), 2)

                height = face.bottom() - face.top()
                width = face.right() - face.left()

                ### 進行人臉裁減 ###
                # 如果没有超出鏡頭邊界
                if (face.bottom() < 480) and (face.right() < 640) and \
                        ((face.top() + height) < 480) and ((face.left() + width) < 640):
                    # 填充
                    for i in range(height):
                        for j in range(width):
                            img_rd[i][faces_start_width + j] = \
                                img_rd[face.top() + i][face.left() + j]

                # 更新 faces_start_width 的座標
                faces_start_width += width

            cv2.putText(img_rd, "Faces in all: " + str(len(faces)), (20, 350), font, 0.8, (0, 0, 0), 1, cv2.LINE_AA)

        else:
            # 没有檢測到人臉
            cv2.putText(img_rd, "no face", (20, 350), font, 0.8, (0, 0, 0), 1, cv2.LINE_AA)

        # 添加说明
        img_rd = cv2.putText(img_rd, "Press 'S': Screen shot", (20, 400), font, 0.8, (255, 255, 255), 1, cv2.LINE_AA)
        img_rd = cv2.putText(img_rd, "Press 'Q': Quit", (20, 450), font, 0.8, (255, 255, 255), 1, cv2.LINE_AA)

    # 按下 's' 保存
    if k == ord('s'):
        ss_cnt += 1
        print(path_screenshots + "screenshot" + "_" + str(ss_cnt) + "_" + time.strftime("%Y-%m-%d-%H-%M-%S",
                                                                                        time.localtime()) + ".jpg")
        cv2.imwrite(path_screenshots + "screenshot" + "_" + str(ss_cnt) + "_" + time.strftime("%Y-%m-%d-%H-%M-%S",
                                                                                              time.localtime()) + ".jpg",
                    img_rd)

    cv2.namedWindow("camera", 1)
    cv2.imshow("camera", img_rd)

# 釋放webcam
cap.release()

# 删除建立的窗口
cv2.destroyAllWindows()
