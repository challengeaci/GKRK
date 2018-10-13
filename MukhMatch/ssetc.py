import cv2

def scan():
    detector = cv2.CascadeClassifier(r'haarcascade_frontalface_default.xml')
    sampleNum = 0
    # id = 55
    cap = cv2.VideoCapture(0)
    while (True):
        ret, img = cap.read()
        # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = detector.detectMultiScale(img, 1.3, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

            sampleNum = sampleNum + 1
            cv2.imwrite("scan.jpg", img[y:y + h+25, x:x + w+25])
            cv2.waitKey(100)
        cv2.imshow('frame', img)
        cv2.waitKey(1)
        if (sampleNum > 10):
            break

    cap.release()
    cv2.destroyAllWindows()
