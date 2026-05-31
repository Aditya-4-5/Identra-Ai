import streamlit as st
import time
from src.components.header import header_home
from src.components.footer import footer_home
from src.ui.base_layout import style_base_layout, style_background_home

def home_screen():

    if "loaded" not in st.session_state:
        st.session_state.loaded = False

    if not st.session_state.loaded:
        st.markdown("""
        <div class="full-loader">
            <div class="loader-line"></div>
            <div class="loader-text"> 🚀 Launching intelligent attendance platform... <br> <br>⏳ Please wait...</div>
        </div>
        """, unsafe_allow_html=True)

        _inject_home_theme()  
        time.sleep(2)
        st.session_state.loaded = True
        st.rerun()

    header_home()
    style_background_home()
    style_base_layout()
    _inject_home_theme()

    st.markdown("""
        <div class="att-logo-pill">
            <span class="att-dot"></span>
            AI System Active
        </div>

        <div class="att-main-title">
            Smart <span class="att-accent">Attendance</span>
        </div>

        <p class="att-subtitle">
            Powered by facial recognition & machine learning
        </p>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown("""
        <div class="att-card">
            <div class="att-card-icon">🎓</div>
            <div class="att-card-role">STUDENT</div>
            <div class="att-card-title">I'm a Student</div>
            <p class="att-card-desc">
                View attendance, mark presence & track performance.
            </p>
        </div>
        """, unsafe_allow_html=True)

        if st.button('→ Student Portal', key='student_btn'):
            st.session_state['login_type'] = 'student'
            st.rerun()

    with col2:
        st.markdown("""
        <div class="att-card">
            <div class="att-card-icon">🧑‍🏫</div>
            <div class="att-card-role">TEACHER</div>
            <div class="att-card-title">I'm a Teacher</div>
            <p class="att-card-desc">
                Manage classes & review AI attendance reports.
            </p>
        </div>
        """, unsafe_allow_html=True)

        if st.button('→ Teacher Portal', key='teacher_btn'):
            st.session_state['login_type'] = 'teacher'
            st.rerun()

    footer_home()


def _inject_home_theme():

    st.markdown("""
    <style>

    /* ===== FULL PAGE ===== */
    html, body, [data-testid="stApp"], [data-testid="stAppViewContainer"] {
        background: linear-gradient(180deg, #0f172a 0%, #020617 100%) !important;
        margin: 0;
        height: 100%;
    }

    .main, .block-container {
        background: transparent !important;
    }

    .block-container {
        max-width: 100% !important;
        padding: 50px 60px !important;
        position: relative;
        z-index: 2;
    }


    .full-loader {
        position: fixed;
        inset: 0;
        background: #020617;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        z-index: 9999;
    }

    .loader-line {
        width: 200px;
        height: 3px;
        background: linear-gradient(90deg, transparent, #00ffc6, transparent);
        animation: loadMove 1.5s infinite;
    }

    .loader-text {
        color: #00ffc6;
        margin-top: 10px;
        font-size: 14px;
    }

    @keyframes loadMove {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }

    .custom-logo {
        font-size: 18px;
        font-weight: 600;
        color: #00ffc6;
        margin-bottom: 10px;
    }

    /* ===== HEADER ===== */
    .att-main-title {
        font-size: 42px;
        font-weight: 700;
        color: #ffffff;
    }

    .att-accent {
        color: #00ffc6;
    }

    .att-subtitle {
        color: rgba(255,255,255,0.85);
        margin-bottom: 30px;
    }

    .att-logo-pill {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 6px 14px;
        border-radius: 50px;
        background: rgba(0,255,150,0.15);
        color: #00ff9c;
        font-size: 12px;
        margin-bottom: 10px;
    }

    .att-dot {
        width: 8px;
        height: 8px;
        background: #00ff9c;
        border-radius: 50%;
    }

    .att-card {
        background: rgba(15, 23, 42, 0.7);
        border-radius: 20px;
        padding: 22px;
        border: 1px solid rgba(255,255,255,0.08);
        backdrop-filter: blur(12px);
        transition: 0.3s;
    }

    .att-card:hover {
        transform: translateY(-6px);
        box-shadow: 0 20px 50px rgba(0,0,0,0.5);
    }

    .att-card-role { color: #94a3b8; font-size: 11px; }
    .att-card-title { color: #fff; font-weight: 700; }
    .att-card-desc { color: #cbd5e1; }


    div[data-testid="stButton"] button {
        border-radius: 8px;
        background: linear-gradient(135deg, #ff4d8d, #ff2d6f);
        color: white;
    }

    footer { display: none !important; }

    </style>
    """, unsafe_allow_html=True)