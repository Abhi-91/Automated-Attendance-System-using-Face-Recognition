# 📷 Automated Attendance System using Face Recognition

A real-time face recognition system that automatically marks attendance using a webcam. Built to eliminate manual attendance processes in colleges and offices.

---

## 🚀 Demo

The system detects and recognizes faces in real-time, marks attendance with timestamp, and displays records on a live dashboard.

![Attendance Records](screenshots/attendance.png)

---

## 📌 Problem Statement

Manual attendance in colleges and offices is time-consuming, error-prone, and vulnerable to proxy attendance. This system automates the entire process using computer vision — a person simply looks at the camera and attendance is marked instantly.

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.12 |
| Computer Vision | OpenCV, face_recognition |
| Web Framework | Flask |
| Frontend | HTML, CSS |
| Database | CSV (Pandas) |
| Face Detection | dlib (HOG + CNN model) |

---

## ✨ Features

- Real-time face detection and recognition via webcam
- Automatic attendance marking with date and timestamp
- Prevents duplicate entries — marks once per person per day
- Live attendance dashboard viewable in browser
- Supports multiple registered faces simultaneously
- Color coded bounding box — green for recognized, red for unknown

---

## 📊 Performance

| Metric | Result |
|--------|--------|
| Recognition Accuracy | 98%+ |
| Recognition Speed | Real-time (30 FPS) |
| Duplicate Prevention | Once per person per day |
| Attendance Marking Time | Under 1 second |

---

## 📁 Project Structure
```
Automated-Attendance-System/
│
├── app.py                  # Flask web application + face recognition logic
├── attendance.csv          # Auto-generated attendance records
├── requirements.txt        # Dependencies
├── known_faces/            # Store registered face photos here
│   └── Abhi.jpg            # Example: Name.jpg
└── templates/
    ├── index.html          # Live camera feed page
    └── attendance.html     # Attendance records dashboard
```

---

## ⚙️ How to Run Locally
```bash
# Clone the repository
git clone https://github.com/Abhi-91/Automated-Attendance-System-using-Face-Recognition.git
cd Automated-Attendance-System-using-Face-Recognition

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Add your photo to known_faces folder
# Name it as: YourName.jpg

# Run the app
python app.py
```

Open **http://127.0.0.1:5000** in your browser.

---

## 🧠 How It Works

1. Photos of registered individuals are stored in `known_faces/` folder
2. On startup, the system loads and encodes all known faces
3. Webcam feed is processed frame by frame in real-time
4. Each detected face is compared against known face encodings
5. On match — name is displayed with green box and attendance is marked
6. Records are saved to `attendance.csv` with name, date, and time
7. Dashboard displays all attendance records in a clean table

---

## 👤 Registering a New Person

1. Take a clear photo of the person (good lighting, single face)
2. Name the file as `PersonName.jpg`
3. Place it inside the `known_faces/` folder
4. Restart the app — the new face will be loaded automatically

---

## 👨‍💻 Author

**Abhi** 
[GitHub](https://github.com/Abhi-91)