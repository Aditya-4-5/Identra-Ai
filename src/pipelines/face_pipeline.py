import numpy as np
import streamlit as st

from src.database.db import get_all_students


def _load_face_dependencies():
    try:
        import dlib
        import face_recognition_models
    except ImportError as exc:
        st.error(
            "Face recognition dependencies are not installed on this server. "
            "Install dlib and face-recognition-models to use face attendance."
        )
        raise RuntimeError("Missing face recognition dependencies") from exc

    return dlib, face_recognition_models


@st.cache_resource
def load_dlib_models():
    dlib, face_recognition_models = _load_face_dependencies()
    detector = dlib.get_frontal_face_detector() 


    sp = dlib.shape_predictor(
        face_recognition_models.pose_predictor_model_location()
    )

    facerec = dlib.face_recognition_model_v1(
        face_recognition_models.face_recognition_model_location()
    )

    return detector, sp, facerec

def get_face_embeddings(image_np):
    try:
        detector, sp, facerec = load_dlib_models()
    except RuntimeError:
        return []

    faces = detector(image_np, 1)

    encodings= []

    for face in faces:
        shape = sp(image_np, face)
        face_descriptor = facerec.compute_face_descriptor(image_np, shape, 1) #128 embedding

        encodings.append(np.array(face_descriptor))
    return encodings

@st.cache_resource(ttl=300, show_spinner=False)
def get_trained_model():
    X = []
    y = []


    student_db = get_all_students()

    if not student_db:
        return None
    
    for student in student_db:
        embedding = student.get('face_embedding')
        if embedding:
            X.append(np.array(embedding))
            y.append(student.get('student_id'))

    if len(X) ==0:
        return 0
    
    return {'X': np.asarray(X, dtype=np.float64), "y": y}


def train_classifier():
    get_trained_model.clear()
    model_data = get_trained_model()
    return bool(model_data)

def predict_attendance(class_image_np):
    encodings = get_face_embeddings(class_image_np)

    detected_student = {}


    model_data = get_trained_model()

    if not model_data:
        return detected_student, [], len(encodings)
    
    X_train = model_data['X']
    y_train = model_data['y']

    all_students = sorted(list(set(y_train)))

    for encoding in encodings:
        distances = np.linalg.norm(X_train - encoding, axis=1)
        best_index = int(np.argmin(distances))
        predicted_id = int(y_train[best_index])
        best_match_score = float(distances[best_index])

        resemblance_threshold = 0.6

        if best_match_score <= resemblance_threshold:
            detected_student[predicted_id] = True
    return detected_student, all_students, len(encodings)
