import streamlit as st


def footer_home():
    st.markdown("""
    <style>
    .custom-footer {
        background-color: #0f172a;
        color: white;
        padding: 40px 30px 15px 30px;
        border-top: 1px solid rgba(255,255,255,0.1);
        margin-top: 60px;
    }

    .footer-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 30px;
    }

    .footer-title {
        font-size: 22px;
        font-weight: bold;
        color: #22d3ee;
        margin-bottom: 15px;
    }

    .footer-heading {
        font-size: 18px;
        font-weight: 600;
        margin-bottom: 15px;
    }

    .footer-text {
        color: #cbd5e1;
        line-height: 1.8;
    }

    .copyright {
        text-align: center;
        margin-top: 30px;
        color: #94a3b8;
        font-size: 14px;
    }
    </style>

    <div class="custom-footer">
        <div class="footer-grid">

            <div>
                <div class="footer-title">IDENTRA</div>
                <div class="footer-text">
                    Smart AI Attendance Management System powered by
                    Face Recognition & Automation.
                </div>
            </div>

            <div>
                <div class="footer-heading">Helpful Links</div>
                <div class="footer-text">
                    Dashboard<br>
                    Take Attendance<br>
                    Manage Subjects<br>
                    Attendance Records
                </div>
            </div>

            <div>
                <div class="footer-heading">Get In Touch</div>
                <div class="footer-text">
                    📧 support@identra.ai<br>
                    📧 admin@identra.ai<br>
                    🕒 Support: 10 AM - 6 PM
                </div>
            </div>

            <div>
                <div class="footer-heading">Connect With Us</div>
                <div class="footer-text">
                    📘 Facebook<br>
                    📸 Instagram<br>
                    ▶️ YouTube<br>
                    💼 LinkedIn
                </div>
            </div>

        </div>

        <div class="copyright">
            © 2025 IDENTRA | Recognize • Analyze • Automate <br>
            Developed by ADI 🚀
        </div>
    </div>
    """, unsafe_allow_html=True)


def footer_dashboard():
    footer_home()