import face_recognition
import cv2
import numpy as np
import pandas as pd
import os
from datetime import datetime
from flask import Flask, render_template, Response, redirect, url_for

app = Flask(__name__)

# ── Load known faces ──
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KNOWN_FACES_DIR = os.path.join(BASE_DIR, 'known_faces')
ATTENDANCE_FILE = os.path.join(BASE_DIR, 'attendance.csv')

known_encodings = []
known_names = []

print("Loading known faces...")
for filename in os.listdir(KNOWN_FACES_DIR):
    if filename.endswith(('.jpg', '.jpeg', '.png')):
        name = os.path.splitext(filename)[0]
        image_path = os.path.join(KNOWN_FACES_DIR, filename)
        image = face_recognition.load_image_file(image_path)
        encodings = face_recognition.face_encodings(image)
        if encodings:
            known_encodings.append(encodings[0])
            known_names.append(name)
            print(f"Loaded: {name}")

print(f"Total faces loaded: {len(known_names)}")

# ── Attendance helper ──
def mark_attendance(name):
    now = datetime.now()
    date = now.strftime('%Y-%m-%d')
    time = now.strftime('%H:%M:%S')

    if os.path.exists(ATTENDANCE_FILE):
        df = pd.read_csv(ATTENDANCE_FILE)
    else:
        df = pd.DataFrame(columns=['Name', 'Date', 'Time'])

    # Only mark once per day
    already_marked = ((df['Name'] == name) & (df['Date'] == date)).any()
    if not already_marked:
        new_row = pd.DataFrame({'Name': [name], 'Date': [date], 'Time': [time]})
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv(ATTENDANCE_FILE, index=False)
        print(f"Attendance marked: {name} at {time}")

# ── Camera feed ──
camera = cv2.VideoCapture(0)

def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break

        # Resize for faster processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        # Detect faces
        face_locations = face_recognition.face_locations(rgb_small)
        face_encodings = face_recognition.face_encodings(rgb_small, face_locations)

        for face_encoding, face_location in zip(face_encodings, face_locations):
            matches = face_recognition.compare_faces(known_encodings, face_encoding)
            name = "Unknown"

            face_distances = face_recognition.face_distance(known_encodings, face_encoding)
            if len(face_distances) > 0:
                best_match = np.argmin(face_distances)
                if matches[best_match]:
                    name = known_names[best_match]
                    mark_attendance(name)

            # Scale back up face locations
            top, right, bottom, left = [v * 4 for v in face_location]

            # Draw box and name
            color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
            cv2.putText(frame, name, (left + 6, bottom - 6),
                        cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)

        # Encode frame
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# ── Routes ──
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/attendance')
def attendance():
    if os.path.exists(ATTENDANCE_FILE):
        df = pd.read_csv(ATTENDANCE_FILE)
        records = df.to_dict('records')
    else:
        records = []
    return render_template('attendance.html', records=records)

if __name__ == '__main__':
    app.run(debug=True)