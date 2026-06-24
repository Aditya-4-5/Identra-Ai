import streamlit as st
from src.database.db import (
    enroll_student_to_subject,
    get_subject_by_code,
    is_student_enrolled,
    normalize_subject_code,
)


@st.dialog("Enroll in Subject")
def enroll_dialog():
    st.write('Enter the subject code provided by your teacher to enroll')
    join_code = st.text_input('Subject Code', placeholder='Eg. CS101')

    if st.button('Enroll now', type='primary', width='stretch'):
        join_code = normalize_subject_code(join_code)

        if join_code:
            subject = get_subject_by_code(join_code)
            if subject:
                student_id = st.session_state.student_data['student_id']

                if is_student_enrolled(student_id, subject['subject_id']):
                    st.warning('You are already enrolled in this program')
                else:
                    enroll_student_to_subject(student_id, subject['subject_id'])
                    st.toast('Successfully enrolled!')
                    st.rerun()
            else:
                st.error('Subject Code not found!')
        else:
            st.warning('Please enter a subject code')
