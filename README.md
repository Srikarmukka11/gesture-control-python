# gesture-control-python
Gesture Control System using Python 🖐️💻
Control your laptop mouse cursor and system functions using your hand gestures captured via webcam!
This project uses OpenCV, MediaPipe, PyAutoGUI, and Kalman Filter for ultra-smooth motion tracking.

🚀 Features

Feature	Description
🖱️ Mouse Control	Move mouse dynamically with your index finger
🔈 Volume Control	Control system volume using hand gestures
📷 Screenshot	Capture the screen with a "V" gesture
📜 Scroll Pages	Scroll webpages using swipe gestures
🔐 Lock Screen	Lock your device using a closed fist gesture
🔌 Sleep Mode	Put laptop to sleep using flat palm
🧠 App Launch	Launch specific apps via hand gestures
🧹 Kalman Filter	Smooth and predictive mouse movement filtering
📸 Demo
(Optional: Add a short demo GIF here)


🛠️ Built With
Python 3.x

OpenCV — Computer Vision Library

MediaPipe — Hand Tracking and Gesture Detection

PyAutoGUI — GUI Automation (Mouse, Keyboard)

FilterPy — Kalman Filtering

NumPy — Data Manipulation

📥 Installation
Clone the repository:

bash
Copy
Edit
git clone https://github.com/YOUR-USERNAME/gesture-control-python.git
cd gesture-control-python
Install dependencies:

bash
Copy
Edit
pip install -r requirements.txt
⚙️ How to Run
bash
Copy
Edit
python optimized_main_with_kalman.py
Keep your webcam ON.

Move your hand inside the frame.

Your index finger controls the mouse cursor! 🖱️✨

Perform different gestures to trigger actions!

📋 Folder Structure
bash
Copy
Edit
gesture-control-python/
│
├── optimized_main_with_kalman.py    # Main Gesture Control Program
├── README.md                        # Project Documentation
├── requirements.txt                 # Python Libraries List
└── demo.gif                          # (Optional) Demo Recording
🎯 Future Upgrades
Add multi-hand support (e.g., dual hand gestures).

Use deep learning to improve gesture recognition.

Custom app launchers based on gestures.

Integrate voice feedback ("Volume Increased", "Screenshot Taken").

🧑‍💻 Author
Srikar Mukka
