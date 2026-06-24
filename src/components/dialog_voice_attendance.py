from datetime import datetime, timezone

import pandas as pd
import streamlit as st

from src.components.dialog_attendance_results import show_attendance_result
from src.database.db import get_enrolled_students
from src.pipelines.voice_pipeline import process_bulk_audio


@st.dialog("Voice Attendance")
def voice_attendance_dialog(selected_subject_id):
    st.write(
        'Record students saying "I am present", then let the AI recognize them.'
    )

    audio_data = st.audio_input("Record classroom audio")

    if st.button("Analyze Audio", width="stretch", type="primary"):
        if audio_data is None:
            st.warning("Record audio before starting the analysis.")
            return

        with st.spinner("Processing audio data..."):
            enrolled_students = get_enrolled_students(selected_subject_id)
            if not enrolled_students:
                st.warning("No students are enrolled in this course.")
                return

            candidates = {
                node["students"]["student_id"]: node["students"]["voice_embedding"]
                for node in enrolled_students
                if node.get("students")
                and node["students"].get("voice_embedding")
            }
            if not candidates:
                st.error("No enrolled students have registered voice profiles.")
                return

            audio_bytes = audio_data.getvalue()
            if not audio_bytes:
                st.warning("The recording is empty. Please record it again.")
                return

            detected_scores = process_bulk_audio(audio_bytes, candidates)
            timestamp = datetime.now(timezone.utc).isoformat()
            results = []
            attendance_logs = []

            for node in enrolled_students:
                student = node.get("students")
                if not student:
                    continue
                score = float(detected_scores.get(student["student_id"], 0.0))
                is_present = score > 0
                results.append(
                    {
                        "Name": student["name"],
                        "ID": student["student_id"],
                        "Source": round(score, 3) if is_present else "-",
                        "Status": "✅ Present" if is_present else "❌ Absent",
                    }
                )
                attendance_logs.append(
                    {
                        "student_id": student["student_id"],
                        "subject_id": selected_subject_id,
                        "timestamp": timestamp,
                        "is_present": is_present,
                    }
                )

            st.session_state.voice_attendance_results = (
                pd.DataFrame(results),
                attendance_logs,
            )

    if st.session_state.get("voice_attendance_results"):
        st.divider()
        result_frame, logs = st.session_state.voice_attendance_results
        show_attendance_result(result_frame, logs)
