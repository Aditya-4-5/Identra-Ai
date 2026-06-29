import time

import streamlit as st

from src.components.footer import footer_home
from src.components.header import header_home
from src.ui.base_layout import style_background_home, style_base_layout


def _inject_home_theme():
    st.markdown(
        """
        <style>
        html, body, [data-testid="stApp"], [data-testid="stAppViewContainer"] {
            background: linear-gradient(180deg, #0f172a 0%, #020617 100%) !important;
            margin: 0;
            min-height: 100%;
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

        .loader {
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: fit-content;
            font-weight: bold;
            font-family: monospace;
            font-size: 30px;
            background: radial-gradient(circle closest-side, #000 94%, #0000)
                right / calc(200% - 1em) 100%;
            animation: l24 1s infinite alternate linear;
            z-index: 9999;
        }

        .loader::before {
            content: "Loading...";
            line-height: 1em;
            color: transparent;
            background: inherit;
            background-image: radial-gradient(circle closest-side, #fff 94%, #000);
            -webkit-background-clip: text;
            background-clip: text;
        }

        @keyframes l24 {
            100% {
                background-position: left;
                transform: translate(-50%, -50%);
            }
        }

        .att-main-title {
            font-size: 42px;
            font-weight: 700;
            color: #ffffff;
        }

        .att-accent {
            color: #00ffc6;
        }

        .att-subtitle {
            color: rgba(255, 255, 255, 0.85);
            margin-bottom: 30px;
        }

        .att-logo-pill {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 6px 14px;
            border-radius: 50px;
            background: rgba(0, 255, 150, 0.15);
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
            border: 1px solid rgba(255, 255, 255, 0.08);
            backdrop-filter: blur(12px);
            transition: 0.3s;
            min-height: 170px;
        }

        .att-card:hover {
            transform: translateY(-6px);
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.5);
        }

        .att-card-icon {
            font-size: 34px;
            margin-bottom: 12px;
        }

        .att-card-role {
            color: #94a3b8;
            font-size: 11px;
            letter-spacing: 1px;
        }

        .att-card-title {
            color: #fff;
            font-weight: 700;
            font-size: 22px;
            margin: 6px 0;
        }

        .att-card-desc {
            color: #cbd5e1;
            margin-bottom: 0;
        }

        div[data-testid="stButton"] button {
            border-radius: 8px;
            background: linear-gradient(135deg, #ff4d8d, #ff2d6f);
            color: white;
        }

        footer {
            display: none !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _show_loader_once():
    if st.session_state.get("home_loaded"):
        return

    _inject_home_theme()
    st.markdown('<div class="loader"></div>', unsafe_allow_html=True)
    time.sleep(2)
    st.session_state.home_loaded = True
    st.rerun()


def home_screen():
    _show_loader_once()

    style_background_home()
    style_base_layout()
    _inject_home_theme()
    header_home()

    st.markdown(
        """
        <div class="att-logo-pill">
            <span class="att-dot"></span>
            AI System Active
        </div>

        <div class="att-main-title">
            Smart <span class="att-accent">Attendance</span>
        </div>

        <p class="att-subtitle">
            Powered by facial recognition and machine learning
        </p>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown(
            """
            <div class="att-card">
                <div class="att-card-icon">Student</div>
                <div class="att-card-role">STUDENT</div>
                <div class="att-card-title">I'm a Student</div>
                <p class="att-card-desc">
                    View attendance, mark presence and track performance.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button("Student Portal", key="student_btn", use_container_width=True):
            st.session_state.login_type = "student"
            st.rerun()

    with col2:
        st.markdown(
            """
            <div class="att-card">
                <div class="att-card-icon">Teacher</div>
                <div class="att-card-role">TEACHER</div>
                <div class="att-card-title">I'm a Teacher</div>
                <p class="att-card-desc">
                    Manage classes and review AI attendance reports.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button("Teacher Portal", key="teacher_btn", use_container_width=True):
            st.session_state.login_type = "teacher"
            st.rerun()

    footer_home()
