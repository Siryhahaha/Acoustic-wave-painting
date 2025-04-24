#按下空格可以截图，保存.bmp文件在本目录下层bmp文件夹(esc退出)

import cv2

cap = cv2.VideoCapture(0)

prtsc_num = 1
while cap.isOpened():
    success, image = cap.read()
    if not success:
        continue
    cv2.imshow("Cap", image)

    key = cv2.waitKey(5) & 0xFF
    if key == 27:  # 按 ESC 退出
        break
    elif key == 32:
        cv2.imwrite(f"bmp/prtsc{prtsc_num}.bmp", image)
        prtsc_num = prtsc_num + 1

cap.release()
cv2.destroyAllWindows()
