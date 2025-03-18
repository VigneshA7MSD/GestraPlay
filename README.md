AI Gesture-Controlled Video Player

📌 Overview

This project is an AI-powered video player that allows users to control playback, volume, and seeking using hand gestures and eye tracking. It integrates OpenCV, MediaPipe, and PyQt5 to provide a seamless hands-free experience.

🎯 Features

✅ Gesture-Based Controls:

Hand movement for volume and seek control.

Eye tracking for automatic play/pause.

✅ Media Player:

Play/Pause/Stop controls.

Volume and seek bar.

File selection for video playback.

✅ Real-Time Computer Vision:

Uses OpenCV for webcam capture.

Haar Cascade for eye detection.

MediaPipe Hands API for gesture recognition.

✅ Seamless UI:

Built using PyQt5 for smooth integration.

Uses QMediaPlayer and QVideoWidget.

📂 Project Structure

AI_Gesture_Video_Player/
│-- model                 # Main application script
│-- implementation        # colap files, screenshot
│-- README.md               # Project documentation
│-- assets/                 # Icons, images, or additional resources like video
│-- Documents/                 # Report and PPT

🏗️ Modules Breakdown

1️⃣ User Interface (UI) - PyQt5

Video Display: Uses QVideoWidget for rendering.

Controls: Play, Stop, Open File, Volume, Seek Bar.

Event Handling: UI elements interact with QMediaPlayer.

2️⃣ Media Processing - PyQt5 QMediaPlayer & OpenCV

QMediaPlayer: Handles video playback.

QVideoWidget: Displays video.

Webcam Feed: Captures frames for gesture recognition.

3️⃣ Computer Vision - OpenCV & MediaPipe

Eye Detection (Haar Cascade Classifier)

Eyes detected: Play video.

Eyes closed: Pause video.

Hand Tracking (MediaPipe Hands API)

Volume Control: Hand up/down in the left region.

Seek Control: Hand left/right in the right region.

4️⃣ Gesture-Based Control Mapping

Volume Control (Left Box) → Move hand up/down to adjust volume.

Seek Control (Right Box) → Move hand left/right to seek.

5️⃣ Backend Processing

Synchronizes UI, Media Playback, and Computer Vision.

Handles gesture-to-action mapping.

Manages OpenCV & PyQt5 resources efficiently.

6️⃣ System Integration

QTimer runs process_frame() every 100ms for real-time gesture recognition.

Signal-Slot mechanism ensures UI updates in sync with gestures.

🔧 Installation

Prerequisites

Ensure you have Python installed. Recommended version: Python 3.8+.

Install Dependencies

pip install -r requirements.txt

Run the Application

python main.py

🛠️ Technologies Used

Python

OpenCV (Computer Vision Processing)

MediaPipe (Hand Tracking API)

PyQt5 (GUI and Media Player)

📌 Future Enhancements

🔊 Voice Control Integration

🎭 Custom Gesture Mapping

🆔 Multiple User Profiles

☁️ Cloud Storage Integration

🤝 Contributing

Contributions are welcome! Feel free to fork the repo and submit a PR.

📝 License

This project is licensed under the MIT License.

📧 Contact

For any queries, reach out to: advr9087@gmail.com

🚀 Enjoy hands-free video control! 🎥

