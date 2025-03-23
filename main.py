from kivy.app import App
from kivy.uix.image import Image
from kivy.graphics.texture import Texture
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
import cv2
import mediapipe as mp
import pyautogui
import time

class GestureApp(App):
    def build(self):
        # Initialize MediaPipe
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands()
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(refine_landmarks=True)

        # Get screen resolution for proper scaling
        self.screen_width, self.screen_height = pyautogui.size()

        # Camera setup
        self.capture = cv2.VideoCapture(0)
        self.image = Image()

        # Gesture tracking variables
        self.prev_x, self.prev_y = None, None
        self.last_click_time = 0
        self.last_hand_detected = None

        # UI Layout
        layout = BoxLayout()
        layout.add_widget(self.image)

        # Start updating frames
        Clock.schedule_interval(self.update, 1.0 / 60.0)  # 30 FPS
        return layout

    def update(self, dt):
        ret, frame = self.capture.read()
        if not ret:
            return

        frame = cv2.flip(frame, 1)  # Mirror effect
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process hands and face
        results_hands = self.hands.process(rgb_frame)
        results_face = self.face_mesh.process(rgb_frame)

        # Eye Blink Detection (Click Simulation)
        if results_face.multi_face_landmarks:
            landmarks = results_face.multi_face_landmarks[0].landmark
            left_eye = [landmarks[145], landmarks[159]]

            if (left_eye[0].y - left_eye[1].y) < 0.006:
                pyautogui.click()
                print("Eye Blink Detected: Click")

        # Hand Gesture Control
        if results_hands.multi_hand_landmarks:
            for idx, landmarks in enumerate(results_hands.multi_hand_landmarks):
                handedness = results_hands.multi_handedness[idx].classification[0].label  # "Left" or "Right"

                # Get index finger tip position
                index_tip = landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
                index_mid = landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_PIP]

                # Left Hand Controls Mouse Cursor
                if handedness == "Left":
                    cursor_x = int(index_tip.x * self.screen_width)
                    cursor_y = int(index_tip.y * self.screen_height)

                    # Move mouse cursor smoothly
                    if self.prev_x is not None and self.prev_y is not None:
                        dx, dy = cursor_x - self.prev_x, cursor_y - self.prev_y
                        if abs(dx) > 5 or abs(dy) > 5:  # Reduce jitter
                            pyautogui.moveTo(cursor_x, cursor_y, duration=0.1)
                            print(f"Moving Mouse to: {cursor_x}, {cursor_y}")

                    self.prev_x, self.prev_y = cursor_x, cursor_y

                    # Gesture for Right Click (Left Hand)
                    if index_tip.y >= index_mid.y:
                        pyautogui.rightClick()
                        print("Right Click Triggered")

                # Right Hand Controls Left Click and Double Click
                elif handedness == "Right":
                    # Click gesture (index finger below middle finger)
                    if index_tip.y >= index_mid.y:
                        current_time = time.time()
                        if current_time - self.last_click_time < 0.5:
                            pyautogui.doubleClick()
                            print("Double Click Triggered")
                        else:
                            pyautogui.click()
                            print("Left Click Triggered")

                        self.last_click_time = current_time

        # Convert frame to Kivy texture
        buf = cv2.flip(rgb_frame, 0).tobytes()
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt="rgb")
        texture.blit_buffer(buf, colorfmt="rgb", bufferfmt="ubyte")
        self.image.texture = texture

    def on_stop(self):
        self.capture.release()

if __name__ == "__main__":
    GestureApp().run()
