import sys
import cv2
import numpy as np
import mediapipe as mp
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QSlider, QVBoxLayout, QLabel, QFileDialog, QHBoxLayout
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import Qt, QUrl, QTimer

class VideoPlayer(QWidget):
    def __init__(self):
        super().__init__()

        # Initialize Media Player
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        # Video Widget
        self.videoWidget = QVideoWidget()

        # Buttons
        self.playButton = QPushButton("Play")
        self.stopButton = QPushButton("Stop")
        self.openButton = QPushButton("Open File")
        self.volumeSlider = QSlider(Qt.Horizontal)
        self.volumeSlider.setRange(0, 100)
        self.volumeSlider.setValue(50)
        self.seekBar = QSlider(Qt.Horizontal)
        self.seekBar.setRange(0, 0)

        # Layout Setup
        controlLayout = QHBoxLayout()
        controlLayout.addWidget(self.playButton)
        controlLayout.addWidget(self.stopButton)
        controlLayout.addWidget(self.openButton)
        controlLayout.addWidget(QLabel("Volume"))
        controlLayout.addWidget(self.volumeSlider)

        layout = QVBoxLayout()
        layout.addWidget(self.videoWidget)
        layout.addWidget(self.seekBar)
        layout.addLayout(controlLayout)
        self.setLayout(layout)

        # Event Listeners
        self.playButton.clicked.connect(self.play_video)
        self.stopButton.clicked.connect(self.stop_video)
        self.openButton.clicked.connect(self.open_file)
        self.volumeSlider.valueChanged.connect(self.set_volume)
        self.seekBar.sliderMoved.connect(self.set_position)

        self.mediaPlayer.setVideoOutput(self.videoWidget)
        self.mediaPlayer.positionChanged.connect(self.position_changed)
        self.mediaPlayer.durationChanged.connect(self.duration_changed)

        # Eye & Hand Detection
        self.timer = QTimer()
        self.timer.timeout.connect(self.process_frame)
        self.timer.start(100)

        self.eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
        self.cap = cv2.VideoCapture(0)
        self.eye_detected = False

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.mp_draw = mp.solutions.drawing_utils

    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open Video")
        if filename:
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(filename)))
            self.playButton.setEnabled(True)

    def play_video(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def stop_video(self):
        self.mediaPlayer.stop()

    def set_volume(self, value):
        self.mediaPlayer.setVolume(value)

    def set_position(self, position):
        self.mediaPlayer.setPosition(position)

    def position_changed(self, position):
        self.seekBar.setValue(position)

    def duration_changed(self, duration):
        self.seekBar.setRange(0, duration)

    def process_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return

        height, width, _ = frame.shape

        # Eye Detection for Play/Pause
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        eyes = self.eye_cascade.detectMultiScale(gray, 1.2, 5)

        if len(eyes) > 0:
            if not self.eye_detected:
                self.mediaPlayer.play()
            self.eye_detected = True
        else:
            if self.eye_detected:
                self.mediaPlayer.pause()
            self.eye_detected = False

        # Draw control regions
        cv2.rectangle(frame, (50, 50), (250, 250), (0, 255, 0), 2)  # Volume Control Box
        cv2.putText(frame, "Volume", (90, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        cv2.rectangle(frame, (width-250, 50), (width-50, 250), (0, 0, 255), 2)  # Seek Control Box
        cv2.putText(frame, "Forward", (width-200, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(frame_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

                # Get hand position
                wrist = hand_landmarks.landmark[self.mp_hands.HandLandmark.WRIST]
                index_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]

                hand_x, hand_y = int(index_tip.x * width), int(index_tip.y * height)

                # Volume Control (Left Box)
                if 50 < hand_x < 250 and 50 < hand_y < 250:
                    volume = int((1 - (hand_y - 50) / 200) * 100)
                    self.mediaPlayer.setVolume(max(0, min(100, volume)))
                    self.volumeSlider.setValue(volume)

                # Seek Control (Right Box)
                elif width-250 < hand_x < width-50 and 50 < hand_y < 250:
                    position = int((hand_x - (width-250)) / 200 * self.mediaPlayer.duration())
                    self.mediaPlayer.setPosition(position)

        cv2.imshow("Gesture Control", frame)
        cv2.waitKey(1)

    def closeEvent(self, event):
        self.cap.release()
        cv2.destroyAllWindows()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = VideoPlayer()
    player.setWindowTitle("AI Gesture-Controlled Video Player")
    player.resize(800, 600)
    player.show()
    sys.exit(app.exec_())
