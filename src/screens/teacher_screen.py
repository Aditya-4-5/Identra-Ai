import streamlit as st  # type: ignore[import]
from src.ui.base_layout import style_background_dashboard, style_base_layout
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from src.components.subject_card import subject_card
from src.database.db import check_teacher_exists, create_teacher, teacher_login, get_teacher_subjects, get_attendance_for_teacher
from src.components.dialog_create_subject import create_subject_dialog
from src.components.dialog_share_subject import share_subject_dialog
from src.components.dialog_add_photo import add_photos_dialog
from src.pipelines.face_pipeline import predict_attendance
from src.components.dialog_attendance_results import attendance_result_dialog
import numpy as np  # type: ignore[import]
import pandas as pd  # type: ignore[import]
from datetime import datetime
from src.database.config import supabase

def inject_pro_ui():
    st.markdown("""
    <style>
            
    html, body, [data-testid="stAppViewContainer"] {
        background: linear-gradient(180deg, #020617 0%, #0f172a 100%);
        font-family: 'Inter', sans-serif;
    }

    .block-container {
        padding: 30px 50px !important;
    }
                
    h1, h2, h3 {
        color: #ffffff !important;
        font-weight: 600;
        letter-spacing: 0.4px;
    }

    div[data-testid="stContainer"] {
        background: rgba(15, 23, 42, 0.65) !important;
        border-radius: 18px !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        backdrop-filter: blur(14px);
        padding: 20px !important;
        transition: all 0.3s ease;
        position: relative;
    }
    div[data-testid="stContainer"]::before {
        content: "";
        position: absolute;
        inset: 0;
        border-radius: 18px;
        padding: 1px;
        background: linear-gradient(135deg,#00ffc6,#6366f1,#ff2d6f);
        -webkit-mask: linear-gradient(#000 0 0) content-box, linear-gradient(#000 0 0);
        -webkit-mask-composite: xor;
        opacity: 0.2;
    }
    div[data-testid="stContainer"]:hover {
        transform: translateY(-6px);
        box-shadow: 0 20px 60px rgba(0,0,0,0.5);
    }
    button {
        border-radius: 8px !important;
        font-weight: 600 !important;
        transition: 0.2s ease;
    }

    button[kind="primary"] {
        background: linear-gradient(135deg,#00ffc6,#6366f1) !important;
        color: #000 !important;
    }

    button[kind="primary"]:hover {
        transform: translateY(-2px);
    }

    button[kind="secondary"] {
        background: rgba(255,255,255,0.08) !important;
        color: white !important;
    }

    button[kind="tertiary"] {
        background: transparent !important;
        color: #94a3b8 !important;
    }

    input, textarea {
        border-radius: 10px !important;
    }
    [data-testid="stCameraInput"] {
        border-radius: 20px;
        border: 1px solid rgba(255,255,255,0.12);
        overflow: hidden;
    }

    [data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
    }

    hr {
        border-color: rgba(255,255,255,0.08);
    }

    [data-testid="stToast"] {
        border-radius: 12px;
    }
    ::-webkit-scrollbar {
        width: 6px;
    }

    ::-webkit-scrollbar-thumb {
        background: #00ffc6;
        border-radius: 10px;
    }

    </style>
    """, unsafe_allow_html=True)


from src.components.dialog_voice_attendance import voice_attendance_dialog

def teacher_screen():

    style_background_dashboard()
    style_base_layout()
    inject_pro_ui()

    if "teacher_data" in st.session_state:
        teacher_dashboard()
    elif 'teacher_login_type' not in st.session_state or st.session_state.teacher_login_type == "login":
        teacher_screen_login()
    elif st.session_state.teacher_login_type == "register":
        teacher_screen_register()


def teacher_dashboard():
    teacher_data = st.session_state.teacher_data

    header_dashboard()

    st.markdown(f"""
<div style="
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    z-index: 99999;
    background: #0f172a;
">
    <marquee style="
        color: white;
        padding: 10px;
        font-size: 18px;
        font-weight: bold;
    ">
        👨‍🏫 Welcome Back, {teacher_data['name']}
    </marquee>
</div>
""", unsafe_allow_html=True)

    if "current_teacher_tab" not in st.session_state:
        st.session_state.current_teacher_tab = 'take_attendance'

    tab1, tab2, tab3 = st.columns(3)

    with tab1:
        type1 = "primary" if st.session_state.current_teacher_tab == 'take_attendance' else "tertiary"
        if st.button('Take Attendance', type=type1, use_container_width=True):
            st.session_state.current_teacher_tab = 'take_attendance'
            st.rerun()

    with tab2:
        type2 = "primary" if st.session_state.current_teacher_tab == 'manage_subjects' else "tertiary"
        if st.button('Manage Subjects', type=type2, use_container_width=True):
            st.session_state.current_teacher_tab = 'manage_subjects'
            st.rerun()

    with tab3:
        type3 = "primary" if st.session_state.current_teacher_tab == 'attendance_records' else "tertiary"
        if st.button('Attendance Records', type=type3, use_container_width=True):
            st.session_state.current_teacher_tab = 'attendance_records'
            st.rerun() 

    st.divider()

    if st.session_state.current_teacher_tab == "take_attendance":
        teacher_tab_take_attendance()

    if st.session_state.current_teacher_tab == "manage_subjects":
        teacher_tab_manage_subjects()

    if st.session_state.current_teacher_tab == "attendance_records":
        teacher_tab_attendance_records()

    st.markdown("""
    <style>
    .logout-btn {
        position: fixed;
        bottom: 30px;
        right: 30px;
        z-index: 9999;
    }
    .logout-btn button {
        background: linear-gradient(135deg,#ff4d4d,#ff6b6b);
        color: white;
        border-radius: 50px;
        padding: 12px 20px;
        font-weight: 600;
        border: none;
        box-shadow: 0 10px 25px rgba(0,0,0,0.4);
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="logout-btn">', unsafe_allow_html=True)

    if st.button("🚪 Logout"):
        if "teacher_data" in st.session_state:
            del st.session_state.teacher_data
        if "teacher_login_type" in st.session_state:
            del st.session_state.teacher_login_type
        st.rerun()  

    st.markdown('</div>', unsafe_allow_html=True)

    footer_dashboard()


def teacher_tab_take_attendance():
    teacher_id = st.session_state.teacher_data['teacher_id']
    st.header('Take AI Attendance')

    if 'attendance_images' not in st.session_state:
        st.session_state.attendance_images = []

    subjects = get_teacher_subjects(teacher_id)

    if not subjects:
        st.warning('You havent created any subjects yet! Please create one to begin!')
        return

    subject_options = {f"{s['name']} - {s['subject_code']}": s['subject_id'] for s in subjects}

    col1, col2 = st.columns([3, 1], vertical_alignment='bottom')

    with col1:
        selected_subject_label = st.selectbox('Select Subject', options=list(subject_options.keys()))

    with col2:
        if st.button('Add Photos', type='primary', icon=':material/photo_prints:', use_container_width=True):
            add_photos_dialog()

    selected_subject_id = subject_options[selected_subject_label]

    st.divider()

    if st.session_state.attendance_images:
        st.header('Added Photos')
        gallery_cols = st.columns(4)

        for idx, img in enumerate(st.session_state.attendance_images):
            with gallery_cols[idx % 4]:
                st.image(img, use_container_width=True, caption=f'Photo {idx+1}')

    has_photos = bool(st.session_state.attendance_images)
    c1, c2, c3 = st.columns(3)

    with c1:
        if st.button('Clear all photos', type='tertiary', icon=':material/delete:', use_container_width=True, disabled=not has_photos):
            st.session_state.attendance_images = []
            st.rerun()  # FIX: rerun so gallery clears immediately

    with c2:
        if st.button('Run Face Analysis', type='secondary', icon=':material/analytics:', use_container_width=True, disabled=not has_photos):
            with st.spinner('Deep scanning classroom photos...'):
                all_detected_ids = {}

                for idx, img in enumerate(st.session_state.attendance_images):
                    img_np = np.array(img.convert('RGB'))
                    detected, _, _ = predict_attendance(img_np)

                    if detected:
                        for sid in detected.keys():
                            student_id = int(sid)
                            all_detected_ids.setdefault(student_id, []).append(f"Photo {idx+1}")

                enrolled_res = supabase.table('subject_students').select("*, students(*)").eq('subject_id', selected_subject_id).execute()
                enrolled_students = enrolled_res.data

                if not enrolled_students:
                    st.warning('No students enrolled in this course')
                else:
                    results, attendance_to_log = [], []
                    current_timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

                    for node in enrolled_students:
                        student = node['students']
                        sources = all_detected_ids.get(int(student['student_id']), [])
                        is_present = len(sources) > 0

                        results.append({
                            "Name": student['name'],
                            "ID": student['student_id'],
                            "Source": ", ".join(sources) if is_present else "-",
                            "Status": "✅ Present" if is_present else "❌ Absent"
                        })

                        attendance_to_log.append({
                            'student_id': student['student_id'],
                            'subject_id': selected_subject_id,
                            'timestamp': current_timestamp,
                            'is_present': bool(is_present)
                        })

                    attendance_result_dialog(pd.DataFrame(results), attendance_to_log)

    with c3:
        if st.button('Use Voice Attendance', type='primary', icon=':material/mic:', use_container_width=True):
            voice_attendance_dialog(selected_subject_id)


def teacher_tab_manage_subjects():
    teacher_id = st.session_state.teacher_data['teacher_id']
    col1, col2 = st.columns(2)
    with col1:
        st.header('Manage Subjects')

    with col2:
        if st.button('Create New Subject', use_container_width=True):
            create_subject_dialog(teacher_id)

    subjects = get_teacher_subjects(teacher_id)

    if subjects:
        # FIX: moved subject_card and share_btn inside the for loop (was broken outside before)
        for sub in subjects:
            stats = [
                ("🫂", "Students", sub['total_students']),
                ("🕰️", "Classes", sub['total_classes']),
            ]

            def share_btn(sub=sub):  # FIX: default arg captures current sub in closure
                if st.button(f"Share Code: {sub['name']}", key=f"share_{sub['subject_code']}", icon=":material/share:"):
                    share_subject_dialog(sub['name'], sub['subject_code'])
                st.write("")  # FIX: replaced invalid st.space()

            subject_card(
                name=sub['name'],
                code=sub['subject_code'],
                section=sub['section'],
                stats=stats,
                footer_callback=share_btn
            )
    else:
        st.info("NO SUBJECTS FOUND. CREATE ONE ABOVE")


def teacher_tab_attendance_records():
    st.header('Attendance Records')

    teacher_id = st.session_state.teacher_data['teacher_id']

    records = get_attendance_for_teacher(teacher_id)

    if not records:
        return

    data = []

    for r in records:
        ts = r.get('timestamp')

        data.append({
            "ts_group": ts.split(".")[0] if ts else None,
            "Time": datetime.fromisoformat(ts).strftime("%Y-%m-%d %I:%M %p") if ts else "N/A",
            "Subject": r['subjects']['name'],
            "Subject Code": r['subjects']['subject_code'],
            "is_present": bool(r.get('is_present', False))
        })

    df = pd.DataFrame(data)

    summary = (
        df.groupby(['ts_group', 'Time', 'Subject', 'Subject Code'])
        .agg(
            Present_Count=('is_present', 'sum'),
            Total_Count=('is_present', 'count')
        ).reset_index()
    )

    summary['Attendance Stats'] = (
        "✅ " + summary['Present_Count'].astype(str) + " /"
        + summary['Total_Count'].astype(str) + ' Students'
    )

    display_df = (
        summary.sort_values(by='ts_group', ascending=False)
        [['Time', 'Subject', 'Subject Code', 'Attendance Stats']]
    )

    st.dataframe(display_df, use_container_width=True, hide_index=True)

    csv = display_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="⬇️ Download Attendance as CSV",
        data=csv,
        file_name="attendance_records.csv",
        mime="text/csv",
        type="primary",
        width='stretch'
    )


def inject_glass_button():
    st.markdown("""
    <style>
    div.stButton > button {
        background: rgba(255,255,255,0.08);
        border: 1px solid rgba(255,255,255,0.15);
        backdrop-filter: blur(12px);
        color: white;
        border-radius: 30px;
        font-weight: 600;
        padding: 12px;
        transition: all 0.3s ease;
    }

    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 30px rgba(0,0,0,0.4);
        background: rgba(255,255,255,0.12);
    }
    </style>
    """, unsafe_allow_html=True)


def teacher_screen_login():

    inject_glass_button()
    header_dashboard()

    st.header('Login using password', anchor=False)
    st.write("")
    st.write("")

    teacher_username = st.text_input("Enter username", placeholder='Enter your username')
    teacher_pass = st.text_input("Enter password", type='password', placeholder="Enter password")

    st.divider()

    btnc1, btnc2 = st.columns(2)

    with btnc1:
        if st.button('Login', icon=':material/passkey:', use_container_width=True):
            teacher = teacher_login(teacher_username, teacher_pass)

            if teacher:
                st.session_state.teacher_data = teacher
                st.session_state.teacher_login_type = None
                st.toast("Welcome back!", icon="👋")
                st.rerun()  # FIX: rerun so dashboard loads immediately after login
            else:
                st.error("Invalid username and password combo")

    with btnc2:
        if st.button('Register Instead', type="primary", icon=':material/passkey:', use_container_width=True):
            st.session_state.teacher_login_type = 'register'
            st.rerun()  # FIX: rerun to switch to register screen

    st.write("")
    st.write("")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("⬅ Back to Home", use_container_width=True):
            st.session_state['login_type'] = None
            st.rerun()

    footer_dashboard()


def register_teacher(teacher_username, teacher_name, teacher_pass, teacher_pass_confirm):
    if not teacher_username or not teacher_name or not teacher_pass:
        return False, "All Fields are required!"
    if check_teacher_exists(teacher_username):
        return False, "Username already taken"
    if teacher_pass != teacher_pass_confirm:
        return False, "Password doesn't match"

    try:
        create_teacher(teacher_username, teacher_pass, teacher_name)
        return True, "Successfully Created! Login Now"
    except Exception:
        return False, "Unexpected Error!"


def teacher_screen_register():

    inject_glass_button()
    header_dashboard()

    st.header('Register your teacher profile')
    st.write("")
    st.write("")

    teacher_username = st.text_input("Enter username", placeholder='Enter your username')
    teacher_name = st.text_input("Enter name", placeholder='Enter your name')
    teacher_pass = st.text_input("Enter password", type='password', placeholder="Enter password")
    teacher_pass_confirm = st.text_input("Confirm your password", type='password', placeholder="Enter password")

    st.divider()
    btnc1, btnc2 = st.columns(2)

    with btnc1:
        if st.button('Register now', icon=':material/passkey:', use_container_width=True):
            success, message = register_teacher(
                teacher_username, teacher_name, teacher_pass, teacher_pass_confirm
            )
            if success:
                st.success(message)
                import time
                time.sleep(2)
                st.session_state.teacher_login_type = "login"
                st.rerun()  # FIX: rerun to go back to login screen
            else:
                st.error(message)

    with btnc2:
        if st.button('Login Instead', type="primary", icon=':material/passkey:', use_container_width=True):
            st.session_state.teacher_login_type = 'login'
            st.rerun()  # FIX: rerun to switch screen

    st.write("")
    st.write("")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("⬅ Back to Login", use_container_width=True):
            st.session_state.teacher_login_type = 'login'
            st.rerun()

    footer_dashboard()