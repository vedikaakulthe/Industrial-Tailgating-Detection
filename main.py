!pip install ultralytics opencv-python-headless
!wget https://github.com/intel-iot-devkit/sample-videos/raw/master/people-detection.mp4 -O cctv_feed.mp4

import cv2
import numpy as np
import time
import requests
from ultralytics import YOLO

# ---------------------------------------------------------
# 1. TELEGRAM BOT CONFIGURATION
# ---------------------------------------------------------
# ⚠️ REPLACE THESE WITH YOUR ACTUAL DETAILS BEFORE RUNNING
BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN_HERE" 
CHAT_ID = "YOUR_CHAT_ID_HERE" 

# Cooldown timer to prevent spamming messages
last_alert_time = 0
COOLDOWN_SECONDS = 10 

def send_telegram_alert(frame, message):
    """Saves the frame and sends it via Telegram Bot"""
    cv2.imwrite("intruder_alert.jpg", frame)
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    with open("intruder_alert.jpg", "rb") as photo:
        data = {"chat_id": CHAT_ID, "caption": message}
        files = {"photo": photo}
        try:
            response = requests.post(url, data=data, files=files)
            if response.status_code == 200:
                print("✅ Telegram Alert Sent Successfully!")
            else:
                print(f"❌ Failed to send alert: {response.text}")
        except Exception as e:
            print(f"Error sending message: {e}")

# ---------------------------------------------------------
# 2. YOLO & VIDEO SETUP
# ---------------------------------------------------------
print("Loading AI Model...")
model = YOLO('yolov8n.pt')

input_video_path = "cctv_feed.mp4"
output_video_path = "tailgating_final_demo.mp4"

cap = cv2.VideoCapture(input_video_path)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv2.CAP_PROP_FPS))

out = cv2.VideoWriter(output_video_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

# Define Polygon Zone (Mapped to Kutch Copper Gate Perspective)
POLYGON_ZONE = np.array([[100, 350], [550, 350], [450, 150], [200, 150]], np.int32)

print("Starting Security System with Live Telegram Alerts...")

# ---------------------------------------------------------
# 3. MAIN PROCESSING LOOP
# ---------------------------------------------------------
while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    # Run object tracking
    results = model.track(frame, persist=True, classes=[0], verbose=False)
    persons_in_zone = 0

    # Draw the Restricted Polygon Zone
    cv2.polylines(frame, [POLYGON_ZONE], isClosed=True, color=(255, 255, 0), thickness=2)
    cv2.putText(frame, "SECURE ZONE", (200, 140), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)

    if results[0].boxes.id is not None:
        boxes = results[0].boxes.xyxy.cpu().numpy()
        track_ids = results[0].boxes.id.cpu().numpy()

        for box, track_id in zip(boxes, track_ids):
            x1, y1, x2, y2 = map(int, box)
            
            # Find center of feet
            cx, cy = int((x1 + x2) / 2), int(y2) 

            # Check if feet are inside the polygon
            is_inside = cv2.pointPolygonTest(POLYGON_ZONE, (cx, cy), False)

            if is_inside >= 0:
                persons_in_zone += 1
                color = (0, 0, 255) # Red for Inside
            else:
                color = (0, 255, 0) # Green for Outside

            # Draw Bounding Box, ID, and Center Dot
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            cv2.circle(frame, (cx, cy), 6, color, -1)
            cv2.putText(frame, f"ID: {int(track_id)}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    # ---------------------------------------------------------
    # 4. TAILGATING ALERT & TELEGRAM TRIGGER
    # ---------------------------------------------------------
    if persons_in_zone > 1:
        # Screen Alert
        cv2.putText(frame, "ALERT: TAILGATING DETECTED!", (30, 50), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 0, 255), 3)
        
        current_time = time.time()
        
        # Check Cooldown before sending Telegram message
        if (current_time - last_alert_time) > COOLDOWN_SECONDS:
            alert_msg = f"🚨 TAILGATING ALERT! 🚨\nGate: Main Entrance (Kutch Copper)\nIntruders in Zone: {persons_in_zone}\nAction Required!"
            
            # Send the alert
            send_telegram_alert(frame, alert_msg)
            
            # Reset timer
            last_alert_time = current_time 

    # Save to output video
    out.write(frame)

# Clean up
cap.release()
out.release()
print("Processing complete! Application closed successfully.")