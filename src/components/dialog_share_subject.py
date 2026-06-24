import streamlit as st
import segno
import io
from urllib.parse import quote

from src.database.db import normalize_subject_code


def _get_app_base_url():
    try:
        host = st.context.headers.get("host")
        proto = st.context.headers.get("x-forwarded-proto", "https")
        if host:
            return f"{proto}://{host}".rstrip("/")
    except Exception:
        pass

    configured_url = st.secrets.get("APP_URL")
    if configured_url:
        return str(configured_url).rstrip("/")

    return "https://identra-main.streamlit.app"


@st.dialog("Share Class Link")
def share_subject_dialog(subject_name, subject_code):
    subject_code = normalize_subject_code(subject_code)
    join_url = f"{_get_app_base_url()}/?join-code={quote(subject_code)}"

    # Apna actual Streamlit app URL yahan rakho
    app_domain = "https://identra-ai.streamlit.app"

    # Join URL
    join_url = f"{app_domain}/?join-code={subject_code}"

    st.header("Scan to Join")

    qr = segno.make(join_url)

    out = io.BytesIO()
    qr.save(out, kind="png", scale=10, border=1)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Copy Link")
        st.code(join_url, language="text")
        st.code(subject_code, language="text")
        st.info("Copy this link to share on WhatsApp or Email")

    with col2:
        st.markdown("### Scan to Join")
        st.image(
            out.getvalue(),
            caption=f"QR Code for {subject_name}",
            use_container_width=True
        )