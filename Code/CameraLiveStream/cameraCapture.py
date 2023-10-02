import cv2

# change your IP
cap = cv2.VideoCapture('http://192.168.1.54:8080/video')



while(cap.isOpened()):

    ret, frame = cap.read()

    try:
        cv2.imshow('temp', cv2.resize(frame, (432, 768)))

        key = cv2.waitKey(1)
        if key == ord('q'):
            break
    except cv2.error:
        print("Stream ended...")
        break

        
cap.release()
cv2.destroyAllWindows()