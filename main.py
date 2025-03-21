import csv
import cv2
import numpy as np
import datetime
import time
import RPi.GPIO as GPIO
from ultralytics import YOLO
import supervision as sv
from picamera2 import Picamera2

# Setup GPIO
LOCK_PIN = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(LOCK_PIN, GPIO.OUT)

picam2 = Picamera2()
picam2.preview_configuration.main.size = (640, 480)
picam2.preview_configuration.main.format = "RGB888"
picam2.configure("preview")
picam2.start()

model = YOLO("yolov8n.pt")
box_annotator = sv.BoxAnnotator(thickness=2)
GPIO.output(LOCK_PIN, GPIO.LOW)
print("Door is initially UNLOCKED.")

def is_holiday():
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    try:
        with open('holidays.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if today == row[0]:
                    print(f"Today is a holiday: {row[1]}")
                    return True
    except Exception as e:
        print(f"Error reading holiday file: {e}")
    return False

def lock_door():
    GPIO.output(LOCK_PIN, GPIO.HIGH)
    print("🔒 Door Locked")

def unlock_door():
    GPIO.output(LOCK_PIN, GPIO.LOW)
    print("🔓 Door Unlocked")

def count_people(detections):
    return sum(1 for class_id in detections.class_id if class_id == 0)

process_started = False
lock_initiated = False

try:
    while True:
        current_time = datetime.datetime.now().time()

        if current_time.hour == 6 and current_time.minute == 0 and not is_holiday():
            print("🔓 Unlocking at 6 AM.")
            unlock_door()
            process_started = False
            lock_initiated = False

        if current_time.hour == 17 and current_time.minute >= 0 and not process_started:
            print("🚀 Process started at 5 PM.")
            process_started = True

        if current_time.hour >= 17 and not lock_initiated:
            frame = picam2.capture_array()
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

            result = model(frame_rgb, agnostic_nms=True)[0]
            detections = sv.Detections(
                xyxy=result.boxes.xyxy.cpu().numpy(),
                confidence=result.boxes.conf.cpu().numpy(),
                class_id=result.boxes.cls.cpu().numpy().astype(int)
            )
            people_count = count_people(detections)
            print(f"People in the room: {people_count}")

            if current_time.hour == 17 and current_time.minute >= 15:
                if people_count == 0:
                    print("🔒 No one detected. LOCKING the door.")
                    lock_door()
                else:
                    print("🔓 People detected. UNLOCKING the door.")
                    unlock_door()

                lock_initiated = True

        time.sleep(30)

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    cv2.destroyAllWindows()
    picam2.close()
    GPIO.cleanup()
