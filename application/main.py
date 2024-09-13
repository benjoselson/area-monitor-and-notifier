import os
import datetime
import time
import cv2
import numpy as np

from pathlib import Path
from application.filefuncs import empty_smsnums
from number_gui import main_gui
from ultralytics import YOLO

from deep_sort_realtime.deepsort_tracker import DeepSort
from threading import Thread

# flag to mainly control background thread
KEEP_RUNNING = True

# load the pre-trained YOLOv8n model
os.chdir(r"C:\Users\Ben User\PycharmProjects\marycariolayolo\application")
model_path = Path('../resources/yolov8n.pt')
model = YOLO(model_path)
tracker = DeepSort(max_age=10)

CONFIDENCE_THRESHOLD = 0.8
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

person_still_exists = False
roi_selected = False
person_exists = False
miss_counter = 0


def detect(cap, vidroi):
    # Use global keyword to change these global variables from inside the function
    global person_exists
    global miss_counter
    global roi_selected
    global person_still_exists

    start = datetime.datetime.now()

    ret, frame = cap.read()
    if not ret:
        raise Exception("Problem getting input from video source")

    if not roi_selected:  # make the entire frame the roi
        height, width = frame.shape[:2]
        top_left_frame = (0, 0)
        bottom_left_frame = (0, height - 1)
        bottom_right_frame = (width - 1, height - 1)
        top_right_frame = (width - 1, 0)
        vidroi = [(top_left_frame), (bottom_left_frame), (bottom_right_frame), (top_right_frame)]
    else:  # roi already established
        pass

    detections = model(frame, verbose=False)[0]

    # initialize the list of bounding boxes and confidences
    results = []

    # loop over the detections
    for data in detections.boxes.data.tolist():
        confidence = data[4]
        if float(confidence) < CONFIDENCE_THRESHOLD:
            person_exists = False
            continue
        else:  # if confidence is greater than threshold, get bounding box and label
            xmin, ymin, xmax, ymax = int(data[0]), int(data[1]), int(data[2]), int(data[3])
            class_id = int(data[5])
            # add the bounding box (x, y, w, h), confidence and class id to the results list
            results.append([[xmin, ymin, xmax - xmin, ymax - ymin], confidence, class_id])

    # update tracker with the new detections
    tracks = tracker.update_tracks(results, frame=frame)
    # loop over the tracks
    for track in tracks:
        # if track is not confirmed ignore the track. If track is confirmed get the track id and the bounding box
        if not track.is_confirmed:
            continue
        else:
            ltrb = track.to_ltrb()

            xmin, ymin, xmax, ymax = int(ltrb[0]), int(
                ltrb[1]), int(ltrb[2]), int(ltrb[3])

            cx = int(xmin + xmax) // 2
            cy = int(ymin + ymax) // 2

            # check if circle overlaps with the out-of-bounds box
            results = cv2.pointPolygonTest(np.array(vidroi, np.int32), (cx, cy), False)
            # draw the bounding box
            cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), GREEN, 2)
            # draw the circle in the middle of the bounding box for out of bounds detection
            cv2.circle(frame, (cx, cy), 50, (255, 0, 255), -1)

            if results >= 0:  # If the person is in the area label them and set variable
                cv2.putText(frame, 'person out of bounds', (xmin, ymin), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 0, 0), 1)
                person_exists = True
            else:
                person_exists = False
            # draw visual out-of-bounds box
            cv2.polylines(frame, [np.array(vidroi, np.int32)], True, (255, 0, 0), 2)

    # Compute performance
    end = datetime.datetime.now()
    frame_process_time = (end - start).total_seconds()
    frame_process_stat = f"Time to process 1 frame: {frame_process_time * 1000:.0f} milliseconds"
    fps_stat = f"fps: {1 / frame_process_time:.2f}"
    cv2.putText(frame, frame_process_stat, (15, 95), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    cv2.putText(frame, fps_stat, (15, 115), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    return frame


def correct_info():
    states = [None, None, None, None]
    corrected_state = True
    false_count = 0
    true_count = 0
    for idx, item in enumerate(states):
        states[idx] = person_exists
        time.sleep(0.16)
    for state in states:
        if state is False:
            false_count += 1
        else:
            true_count += 1
    if true_count > 0:
        corrected_state = True
    else:
        corrected_state = False
    return corrected_state


def messenger():
    global KEEP_RUNNING
    # global person_exists
    person_still_there = False
    while KEEP_RUNNING:
        time.sleep(0.5)
        correct_state = correct_info()
        if correct_state == True and person_still_there == False:  # Person just entered the zone. Send SMS and set person_still_there to True
            print('sending sms')
            person_still_there = True
            # sms_client()
        elif correct_state == False and person_still_there == True:  # Person just left the zone. Set person_still_there to False
            person_still_there = False

        elif correct_state == True and person_still_there == True:  # Person is still in zone and already sent sms. Do Nothing
            continue

        elif correct_state == False and person_still_there == False:  # Nothing happened. Do Nothing
            continue


def main():
    global KEEP_RUNNING
    global roi_selected

    yoloroi = None
    message_thread = Thread(target=messenger)
    message_thread.daemon = True

    main_gui()
    vid_cap = cv2.VideoCapture(0)
    message_thread.start()

    while KEEP_RUNNING:
        frame = detect(cap=vid_cap, vidroi=yoloroi)
        cv2.imshow("Frame", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            empty_smsnums()
            KEEP_RUNNING = False
            message_thread.join()
            cv2.destroyAllWindows()
            print('closing main')

        if key == ord('c'):
            print('c')
            ROI = cv2.selectROI("Selection", frame, True, False, True)
            print("Area Selection: -x = {}, -y = {}, -w = {},"
                  " -h = {}".format(ROI[0], ROI[1], ROI[2], ROI[3]))
            roi_x = ROI[0]
            roi_y = ROI[1]
            roi_w = ROI[2]
            roi_h = ROI[3]

            cv2.rectangle(frame, (roi_x, roi_y),
                          (roi_x + roi_w, roi_y + roi_h), (0, 0, 255), 2)
            top_x = roi_x
            top_y = roi_y
            bottom_x = roi_x + roi_w
            bottom_y = roi_y + roi_h

            top_left = (top_x, top_y)
            bottom_left = (top_x, bottom_y)
            bottom_right = (bottom_x, bottom_y)
            top_right = (bottom_x, top_y)

            yoloroi = [(top_left), (bottom_left), (bottom_right), (top_right)]
            roi_selected = True
            print('yoloroi')
            print(yoloroi)
            time.sleep(1)
            cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
