import streamlit as st

from src.ui.base_layout import style_background_dashboard, style_base_layout
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from PIL import Image
import numpy as np
from src.pipelines.face_pipeline import predict_attendance, get_face_embeddings, train_classifier
from src.pipelines.voice_pipeline import get_voice_embedding
from src.database.db import get_all_students, create_student, get_student_subjects, get_student_attendance, unenroll_student_to_subject

from src.components.dialog_enroll import enroll_dialog
from src.components.subject_card import subject_card


def inject_super_ui():
    st.markdown("""
    <style>

    html, body, [data-testid="stAppViewContainer"] {
        background: linear-gradient(180deg, #020617 0%, #0f172a 100%);
    }

    .block-container {
        padding: 40px 60px !important;
    }

    h1, h2, h3 {
        color: #ffffff !important;
    }

    div[data-testid="stContainer"] {
        background: rgba(15, 23, 42, 0.6) !important;
        border-radius: 20px !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        backdrop-filter: blur(14px);
        padding: 20px !important;
        transition: 0.3s ease;
        position: relative;
    }

    div[data-testid="stContainer"]::before {
        content: "";
        position: absolute;
        inset: 0;
        border-radius: 20px;
        padding: 1px;
        background: linear-gradient(135deg,#00ffc6,#6366f1,#ff2d6f);
        -webkit-mask: linear-gradient(#000 0 0) content-box, linear-gradient(#000 0 0);
        -webkit-mask-composite: xor;
        opacity: 0.25;
    }

    div[data-testid="stContainer"]:hover {
        transform: translateY(-6px);
        box-shadow: 0 20px 60px rgba(0,0,0,0.6);
    }

    button {
        border-radius: 8px !important;
        font-weight: 600 !important;
    }

    button[kind="primary"] {
        background: linear-gradient(135deg,#00ffc6,#6366f1) !important;
        color: black !important;
    }

    button[kind="secondary"] {
        background: rgba(255,255,255,0.08) !important;
        color: white !important;
    }

    [data-testid="stCameraInput"] {
        border-radius: 20px;
        border: 1px solid rgba(255,255,255,0.15);
        overflow: hidden;
    }

    hr {
        border-color: rgba(255,255,255,0.1);
    }

    footer { display:none; }

    </style>
    """, unsafe_allow_html=True)

def student_dashboard():
    student_data = st.session_state.student_data
    student_id = student_data['student_id']

    c1, c2 = st.columns(2)
    with c1:
        header_dashboard()
    with c2:
        st.subheader(f"👋 Welcome, {student_data['name']}")
        if st.button("Logout", type='secondary'):
            st.session_state['is_logged_in'] = False
            del st.session_state.student_data
            st.rerun()

    st.write("")

    c1, c2 = st.columns(2)
    with c1:
        st.header('📚 Your Enrolled Subjects')
    with c2:
        if st.button('➕ Enroll in Subject', type='primary', use_container_width=True):
            enroll_dialog()

    st.divider()

    with st.spinner('Loading your subjects...'):
        subjects = get_student_subjects(student_id)
        logs = get_student_attendance(student_id)

    stats_map = {}

    for log in logs:
        sid = log['subject_id']

        if sid not in stats_map:
            stats_map[sid] = {"total": 0, "attended": 0}

        stats_map[sid]['total'] += 1

        if log.get('is_present'):
            stats_map[sid]['attended'] += 1

    cols = st.columns(2)

    for i, sub_node in enumerate(subjects):
        sub = sub_node['subjects']
        sid = sub['subject_id']

        stats = stats_map.get(sid, {"total": 0, "attended": 0})

        def unenroll_button():
            if st.button("Unenroll", key=f"un_{sid}", type='secondary'):
                unenroll_student_to_subject(student_id, sid)
                st.toast(f'Unenrolled from {sub["name"]}')
                st.rerun()

        with cols[i % 2]:
            subject_card(
                name=sub['name'],
                code=sub['subject_code'],
                section=sub['section'],
                stats=[
                    ('📅', 'Total', stats['total']),
                    ('✅', 'Attended', stats['attended']),
                ],
                footer_callback=unenroll_button
            )

    footer_dashboard()

def student_screen():

    style_background_dashboard()
    style_base_layout()
    inject_super_ui()

    if "student_data" in st.session_state:
        student_dashboard()
        return

    header_dashboard()
    st.header('🔐 Login using FaceID')

    st.write("")
    st.write("")

    show_registration = False
    photo_source = st.camera_input("📷 Position your face")

    if photo_source:
        img = np.array(Image.open(photo_source).convert("RGB"))

        with st.spinner('🤖 AI is scanning...'):
            detected, all_ids, num_faces = predict_attendance(img)

            if num_faces == 0:
                st.error('❌ Dear user, please scan again!')
            elif num_faces > 1:
                st.warning('⚠ Multiple faces found')
            else:
                if detected:
                    student_id = list(detected.keys())[0]
                    all_students = get_all_students()
                    student = next((s for s in all_students if s['student_id'] == student_id), None)

                    if student:
                        st.session_state.is_logged_in = True
                        st.session_state.user_role = 'student'
                        st.session_state.student_data = student
                        st.toast(f'Welcome {student["name"]}')
                        st.rerun()
                else:
                    st.info('Face not recognized! Register below.')
                    show_registration = True

    if show_registration:
        with st.container(border=True):
            st.header('📝 Register New Profile')

            new_name = st.text_input("Enter your name")

            st.subheader('🎤 Optional Voice Enrollment')

            audio_data = st.audio_input('Record your voice')

            if st.button('Create Account', type='primary'):
                if new_name:
                    with st.spinner('Creating profile...'):
                        img = np.array(Image.open(photo_source).convert("RGB"))
                        encodings = get_face_embeddings(img)

                        if encodings:
                            face_emb = encodings[0].tolist()

                            voice_emb = None
                            if audio_data:
                                voice_emb = get_voice_embedding(audio_data.getvalue())

                            response_data = create_student(
                                new_name,
                                face_embedding=face_emb,
                                voice_embedding=voice_emb
                            )

                            if response_data:
                                train_classifier()
                                st.session_state.is_logged_in = True
                                st.session_state.user_role = 'student'
                                st.session_state.student_data = response_data[0]
                                st.toast(f'Profile Created! Hi {new_name}!')
                                st.rerun()
                        else:
                            st.error('Face capture failed')
                else:
                    st.warning('Please enter your name!')

    st.write("")
    st.write("")

    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if st.button("⬅ Back to Home", type='secondary', use_container_width=True):
            st.session_state['login_type'] = None
            st.rerun()

    footer_dashboard()
