from evaluate import ffwd_live
import cv2

cap = cv2.VideoCapture(0)  # Capture video from camera

# Get the width and height of frame
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) + 0.5)
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) + 0.5)

count = 0
debug = False

while cap.isOpened():
    ret, frame = cap.read()
    if ret:

        frame = ffwd_live(frame, "/null", "ckpt/la_muse.ckpt")

        if debug:
            cv2.imwrite('out' + str(count) + '.png', frame)
        else:
            cv2.imshow('frame', frame)

        count += 1

    else:
        break

# Release everything if job is finished
cap.release()
cv2.destroyAllWindows()
