import streamlit as st
import base64


def header_dashboard(teacher_name="Teacher"):

    with open("src/components/assets/logo.png", "rb") as f:
        data = base64.b64encode(f.read()).decode()

    st.markdown(f"""
    <div style="
        position:fixed;
        top:0;
        left:0;
        width:100%;
        height:80px;
        background:rgba(2,6,23,0.95);
        backdrop-filter:blur(12px);
        border-bottom:1px solid rgba(255,255,255,0.08);
        display:flex;
        justify-content:space-between;
        align-items:center;
        padding:0 40px;
        z-index:99999;
        box-shadow:0 4px 20px rgba(0,0,0,0.25);
    ">

        <div style="
            display:flex;
            align-items:center;
            gap:15px;
        ">
            <img src="data:image/png;base64,{data}"
                 style="width:55px;height:55px;
                 filter:drop-shadow(0 0 12px #00ffc6);">

            <div>
                <div style="
                    color:white;
                    font-size:24px;
                    font-weight:700;
                    letter-spacing:1px;
                ">
                    IDENTRA
                </div>

                <div style="
                    color:#94a3b8;
                    font-size:12px;
                ">
                    Recognize • Analyze • Automate
                </div>
            </div>
        </div>

        <div style="
            display:flex;
            align-items:center;
            gap:12px;
            color:white;
        ">

            <div style="
                width:42px;
                height:42px;
                border-radius:50%;
                background:linear-gradient(135deg,#06b6d4,#6366f1);
                display:flex;
                align-items:center;
                justify-content:center;
                font-weight:bold;
                font-size:18px;
            ">
                {teacher_name[0].upper()}
            </div>

            <div>
                <div style="
                    color:#22d3ee;
                    font-size:15px;
                    font-weight:600;
                ">
                    Welcome
                </div>

                <div style="
                    color:white;
                    font-size:16px;
                    font-weight:500;
                ">
                    {teacher_name}
                </div>
            </div>

        </div>

    </div>

    <div style="height:95px;"></div>
    """, unsafe_allow_html=True)