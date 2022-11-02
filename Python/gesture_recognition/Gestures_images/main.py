import handtracking as ht
import cv2

cap = cv2.VideoCapture(1)
detector = ht.HandDetector()

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    success, img = detector.find_hands_2D(img, display_hands=True)
    if success:
        detector.draw_overlays(img)
    cv2.imshow("Image", img)
    cv2.waitKey(1)
