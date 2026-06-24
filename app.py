from pathlib import Path

import streamlit as st  # type: ignore[import]

from src.components.dialog_auto_enroll import auto_enroll_dialog
from src.database.db import normalize_subject_code
from src.screens.home_screen import home_screen
from src.screens.student_screen import student_screen
from src.screens.teacher_screen import teacher_screen


def _get_join_code() -> str:
    for query_key in ("join-code", "join_code", "code", "subject_code"):
        query_value = st.query_params.get(query_key)
        if query_value:
            return normalize_subject_code(query_value)
    return ""


def main():
    st.set_page_config(
        page_title="Identra - Making Attendance faster using AI",
        page_icon=str(Path(__file__).parent / "src/components/assets/logo.png"),
    )

    if "login_type" not in st.session_state:
        st.session_state.login_type = None

    join_code = _get_join_code()
    if join_code and st.session_state.login_type != "student":
        st.session_state.login_type = "student"
        st.rerun()

    match st.session_state.login_type:
        case "teacher":
            teacher_screen()
        case "student":
            student_screen()
        case _:
            home_screen()

    if (
        join_code
        and st.session_state.get("is_logged_in")
        and st.session_state.get("user_role") == "student"
    ):
        auto_enroll_dialog(join_code)


if __name__ == "__main__":
    main()
