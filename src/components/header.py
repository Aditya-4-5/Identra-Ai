import streamlit as st
import base64

def header_home():

    with open("src/components/assets/logo.png", "rb") as f:
        data = base64.b64encode(f.read()).decode()

    st.markdown(f"""
    <div style='text-align:center; margin-top:30px;'>
        <img src='data:image/png;base64,{data}' width='240'>
        <h2 style='color:#2EF2C3; margin-top:10px;'>⚡ Smart AI Attendance</h2>
    </div>

    <style>
    img {{
        filter: drop-shadow(0 0 25px #00ffc6);
    }}
    </style>
    """, unsafe_allow_html=True)

def header_dashboard():

    with open("src/components/assets/logo.png", "rb") as f:
        data = base64.b64encode(f.read()).decode()

    st.markdown(f"""
    <div style='text-align:center; margin-top:20px; margin-bottom:10px;'>
        <img src='data:image/png;base64,{data}' width='220'>
    </div>

    <style>
    img {{
        filter: drop-shadow(0 0 20px #00ffc6);
    }}
    </style>
    """, unsafe_allow_html=True)