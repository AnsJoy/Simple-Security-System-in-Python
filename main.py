import cv2
import os
import json
import logging
from datetime import datetime

# Predefined event types
EVENT_TYPES = [
    "System Startup",
    "Image Captured",
    "System Shutdown",
    "Unknown Key Pressed"
]

# Predefined error types
ERROR_TYPES = [
    "Camera Access Error",
    "Frame Capture Error",
    "Failed to capture and save an image",
    "Unexpected system error"
]

# Set up logging
logging.basicConfig(filename="system.log", level=logging.INFO, 
                    format="%(asctime)s - %(levelname)s - %(message)s")

# File for storing events
event_log_file = "event_log.json"

# Initialize JSON file if it doesn't exist
if not os.path.exists(event_log_file):
    with open(event_log_file, "w") as f:
        json.dump([], f)

# Logs an event to the JSON file and system log
def log_event(event_type, img_name=None):
    try:
        if event_type not in EVENT_TYPES:
            raise ValueError(f"Unknown event type: {event_type}")
        
        event = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "event_type": event_type,
            "image_filename": img_name
        }

        # Append to JSON file
        with open(event_log_file, "r") as f:
            events = json.load(f)
        events.append(event)
        with open(event_log_file, "w") as f:
            json.dump(events, f, indent=4)

        # Log to system log
        logging.info(f"Event logged: {event}")
    except Exception as e:
        logging.error(f"Failed to log event to JSON: {e}")

# Logs an error to the system log
def log_error(error_type, exception=None):
    if error_type not in ERROR_TYPES:
        error_type = "Unexpected system error"

    error_message = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "error_type": error_type,
        "details": str(exception) if exception else "No additional details."
    }
    
    logging.error(f"Error logged: {error_message}")

# Captures and saves an image with a timestamped filename
def capture_image(frame, img_counter):
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        img_name = f"captured_image_{timestamp}_{img_counter}.png"
        cv2.imwrite(img_name, frame)
        logging.info(f"Image saved: {img_name}")
        return img_name
    except Exception as e:
        log_error(ERROR_TYPES[2], e)
        return None

def main():
    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        log_error(ERROR_TYPES[0])
        return

    log_event(EVENT_TYPES[0])  # System Startup
    logging.info("Camera initialized. Press SPACE to capture images or ESC to exit.")

    img_counter = 0

    try:
        while True:
            ret, frame = cam.read()
            if not ret:
                log_error(ERROR_TYPES[1])
                break

            # Add instructional text in red color
            text = "Press SPACE to capture, ESC to exit."
            cv2.putText(frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

            cv2.imshow("Security System", frame)

            k = cv2.waitKey(1)
            if k % 256 == 27:  # ESC pressed
                log_event(EVENT_TYPES[2])  # System Shutdown
                break
            elif k % 256 == 32:  # SPACE pressed
                img_name = capture_image(frame, img_counter)
                if img_name:
                    log_event(EVENT_TYPES[1], img_name)  # Image Captured
                    img_counter += 1
            elif k != -1 and k % 256 not in (27, 32):  # Unrecognized key pressed
                try:
                    key_name = chr(k % 256) if 32 <= k % 256 <= 126 else "Unknown Key"
                except ValueError:
                    key_name = "Unknown Key"
                log_event(EVENT_TYPES[3], f"Key {key_name} pressed")

    except Exception as e:
        log_error(ERROR_TYPES[3], e)
    finally:
        cam.release()
        cv2.destroyAllWindows()
        logging.info("Camera released and all windows closed.")

if __name__ == "__main__":
    main()