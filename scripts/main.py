import cv2
import numpy as np
import sqlite3
import face_recognition

# Function to fetch all people from the database
def fetch_people():
    conn = sqlite3.connect('../database/people.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name, image FROM people')
    people = cursor.fetchall()
    conn.close()
    return [(name, np.frombuffer(image, np.uint8)) for name, image in people]

# Load known images
def load_known_people():
    people = fetch_people()
    known_faces = []
    known_names = []
    for name, image_blob in people:
        img = cv2.imdecode(image_blob, cv2.IMREAD_COLOR)
        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        face_encodings = face_recognition.face_encodings(rgb_img)
        if face_encodings:
            known_faces.append(face_encodings[0])
            known_names.append(name)
    return known_faces, known_names

# Main function for live camera feed
def main():
    known_faces, known_names = load_known_people()
    
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for (face_encoding, face_location) in zip(face_encodings, face_locations):
            matches = face_recognition.compare_faces(known_faces, face_encoding)
            name = "Unknown"

            if True in matches:
                matched_indices = [i for (i, match) in enumerate(matches) if match]
                face_distances = face_recognition.face_distance(known_faces, face_encoding)
                best_match_index = np.argmin(face_distances[matched_indices])
                name = known_names[matched_indices[best_match_index]]

            top, right, bottom, left = face_location
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        cv2.imshow('Camera', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
