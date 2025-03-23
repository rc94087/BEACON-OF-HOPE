# Gesture Control Application

This is a Python-based application that enables **gesture-based control** using **hand and face detection**. The project leverages **OpenCV**, **MediaPipe**, and **PyAutoGUI** for **real-time interaction with the system** through gestures like eye blinks and hand movements.

## Features
- **Mouse Control**: Move the cursor using **hand gestures**.
- **Click with Eye Blink**: Simulates a mouse click when an **eye blink is detected**.
- **Right Click (Left Hand)**: If the **index finger tip is below the middle joint**, it triggers a **right click**.
- **Left Click & Double Click (Right Hand)**: Triggers **click/double-click** based on gesture detection.

## Tech Stack
- **Python**
- **Kivy** (For GUI)
- **OpenCV** (For real-time camera processing)
- **MediaPipe** (For hand and face tracking)
- **PyAutoGUI** (For system interaction)

## Installation  

1. **Clone the Repository**  
   ```bash
   git clone https://github.com/rc94087/BEACON-OF-HOPE.git
   cd BEACON-OF-HOPE

2. **Install Dependencies**
     ```bash
   pip install -r requirements.txt


3. **Run the Application**
   ```bash
   python main.py

 

