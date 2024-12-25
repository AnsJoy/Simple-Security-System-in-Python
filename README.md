# Simple Security System Application
This project is a simple security system designed to:

- Capture images using the computer’s camera when specific events occur.
- Log events in a JSON file with details like timestamps, event types and image filenames.
- Handle errors and log them for troubleshooting.

## Assumptions
- The application is used on a single computer with a connected camera.
- The camera is accessible and functional via OpenCV.
- Events are triggered manually via keyboard input:
  - Spacebar (SPACE) is pressed to capture an image.
  - Escape (ESC) is pressed to shut down the system.

## AI Assistant Usage
ChatGPT was used to assist in the development of this project in the following ways:

- Drafting and refining code:
  Generated initial implementations for key functions like `log_event` and `capture_image`.
  
- Documentation:
  Helped create and format this README.md file.