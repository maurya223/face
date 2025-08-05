import face_recognition
import cv2
import numpy as np
import csv
from datetime import datetime
import os
from PIL import Image

# --------- Check Image Format and Existence --------- #
print("🔍 Verifying face images:")
for name in ["monu.png", "rohan.png"]:
    try:
        img = Image.open(name).convert("RGB")
        arr = np.array(img)
        print(f"✅ {name} loaded successfully — shape={arr.shape}, dtype={arr.dtype}")
    except FileNotFoundError:
        print(f"❌ File not found: {name}")
    except Exception as e:
        print(f"❌ Error loading {name}: {e}")

# --------- Helper Function: Convert and Load Face Encoding --------- #
def load_face_encoding(image_path):
    try:
        img = Image.open(image_path)

        if img.mode not in ('RGB', 'L'):
            img = img.convert("RGB")

        rgb_image_np = np.array(img)

        if rgb_image_np.dtype != np.uint8:
            rgb_image_np = rgb_image_np.astype(np.uint8)

        encodings = face_recognition.face_encodings(rgb_image_np)
        if not encodings:
            print(f"❌ No face found in {image_path}")
            return None
        print(f"✅ Loaded face from {image_path}")
        return encodings[0]
    except Exception as e:
        print(f"❌ Error processing {image_path}: {e}")
        return None

# --------- Ensure Script Runs from Its Own Directory --------- #
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# --------- Load and Encode Known Faces --------- #
known_face_encodings = []
known_face_names = []



people = {
    "monu": "monu_fixed.jpg",
    "rohan": "rohan_fixed.jpg"
}

for name, img_file in people.items():
    encoding = load_face_encoding(img_file)
    if encoding is not None:
        known_face_encodings.append(encoding)
        known_face_names.append(name)

if not known_face_encodings:
    print("❌ No known faces loaded. Exiting.")
    exit()

students_marked = known_face_names.copy()

# --------- Create Attendance CSV --------- #
now = datetime.now()
current_date = now.strftime("%Y-%m-%d")
f = open(f"{current_date}.csv", "w", newline="")
csv_writer = csv.writer(f)
csv_writer.writerow(["Name", "Time"])

# --------- Start Webcam for Real-time Recognition --------- #
video_capture = cv2.VideoCapture(0)

while True:
    ret, frame = video_capture.read()
    if not ret:
        print("❌ Couldn't read from webcam.")
        continue

    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    for face_encoding, face_location in zip(face_encodings, face_locations):
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)

        name = "Unknown"
        if matches[best_match_index]:
            name = known_face_names[best_match_index]

            if name in students_marked:
                students_marked.remove(name)
                time_now = datetime.now().strftime("%H:%M:%S")
                csv_writer.writerow([name, time_now])
                print(f"🟢 Marked present: {name} at {time_now}")

        top, right, bottom, left = [v * 4 for v in face_location]
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, f"{name}", (left, top - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)

    cv2.imshow("Attendance System - Press 'q' to Quit", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# --------- Cleanup --------- #
video_capture.release()
cv2.destroyAllWindows()
f.close()
print("📁 Attendance saved and program closed.")
