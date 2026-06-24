import logging
import time
from collections.abc import Callable
from typing import Any

import bcrypt

from src.database.config import get_supabase_client, reset_supabase_client

logger = logging.getLogger(__name__)


def normalize_subject_code(subject_code: Any) -> str:
    return str(subject_code or "").strip().upper()


def _execute(operation: Callable[[Any], Any], *, retry: bool = True):
    """Execute a Supabase operation and reconnect once after an idle failure."""
    attempts = 2 if retry else 1
    last_error = None

    for attempt in range(attempts):
        try:
            return operation(get_supabase_client())
        except Exception as exc:
            last_error = exc
            logger.warning(
                "Supabase operation failed (attempt %s/%s): %s",
                attempt + 1,
                attempts,
                type(exc).__name__,
            )
            if attempt + 1 < attempts:
                reset_supabase_client()
                time.sleep(0.25)

    raise RuntimeError(
        "The database is temporarily unavailable. Please try again."
    ) from last_error


def hash_pass(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def check_pass(password: str, hashed: str) -> bool:
    if not password or not hashed:
        return False
    try:
        return bcrypt.checkpw(
            password.encode("utf-8"), str(hashed).encode("utf-8")
        )
    except (TypeError, ValueError):
        logger.warning("Rejected an invalid stored password hash")
        return False


def check_teacher_exists(username):
    username = str(username or "").strip()
    if not username:
        return False
    response = _execute(
        lambda client: client.table("teachers")
        .select("username")
        .eq("username", username)
        .limit(1)
        .execute()
    )
    return bool(response.data)


def create_teacher(username, password, name):
    data = {
        "username": str(username).strip(),
        "password": hash_pass(password),
        "name": str(name).strip(),
    }
    response = _execute(
        lambda client: client.table("teachers").insert(data).execute(),
        retry=False,
    )
    return response.data


def teacher_login(username, password):
    username = str(username or "").strip()
    if not username or not password:
        return None
    response = _execute(
        lambda client: client.table("teachers")
        .select("*")
        .eq("username", username)
        .limit(1)
        .execute()
    )
    if response.data and check_pass(password, response.data[0].get("password")):
        return response.data[0]
    return None


def get_all_students():
    return _execute(
        lambda client: client.table("students").select("*").execute()
    ).data or []


def create_student(new_name, face_embedding=None, voice_embedding=None):
    data = {
        "name": str(new_name).strip(),
        "face_embedding": face_embedding,
        "voice_embedding": voice_embedding,
    }
    response = _execute(
        lambda client: client.table("students").insert(data).execute(),
        retry=False,
    )
    return response.data


def create_subject(subject_code, name, section, teacher_id):
    data = {
        "subject_code": normalize_subject_code(subject_code),
        "name": str(name).strip(),
        "section": str(section).strip(),
        "teacher_id": teacher_id,
    }
    response = _execute(
        lambda client: client.table("subjects").insert(data).execute(),
        retry=False,
    )
    return response.data


def get_teacher_subjects(teacher_id):
    response = _execute(
        lambda client: client.table("subjects")
        .select("*, subject_students(count), attendance_logs(timestamp)")
        .eq("teacher_id", teacher_id)
        .execute()
    )
    subjects = response.data or []

    for subject in subjects:
        counts = subject.get("subject_students") or []
        subject["total_students"] = counts[0].get("count", 0) if counts else 0
        attendance = subject.get("attendance_logs") or []
        subject["total_classes"] = len(
            {log.get("timestamp") for log in attendance if log.get("timestamp")}
        )
        subject.pop("subject_students", None)
        subject.pop("attendance_logs", None)

    return subjects


def enroll_student_to_subject(student_id, subject_id):
    data = {"student_id": student_id, "subject_id": subject_id}
    response = _execute(
        lambda client: client.table("subject_students").insert(data).execute(),
        retry=False,
    )
    return response.data


def unenroll_student_to_subject(student_id, subject_id):
    response = _execute(
        lambda client: client.table("subject_students")
        .delete()
        .eq("student_id", student_id)
        .eq("subject_id", subject_id)
        .execute(),
        retry=False,
    )
    return response.data


def get_student_subjects(student_id):
    response = _execute(
        lambda client: client.table("subject_students")
        .select("*, subjects(*)")
        .eq("student_id", student_id)
        .execute()
    )
    return response.data or []


def get_student_attendance(student_id):
    response = _execute(
        lambda client: client.table("attendance_logs")
        .select("*, subjects(*)")
        .eq("student_id", student_id)
        .execute()
    )
    return response.data or []


def create_attendance(logs):
    if not logs:
        return []
    response = _execute(
        lambda client: client.table("attendance_logs").insert(logs).execute(),
        retry=False,
    )
    return response.data


def get_attendance_for_teacher(teacher_id):
    response = _execute(
        lambda client: client.table("attendance_logs")
        .select("*, subjects!inner(*)")
        .eq("subjects.teacher_id", teacher_id)
        .execute()
    )
    return response.data or []


def get_subject_by_code(subject_code):
    code = normalize_subject_code(subject_code)
    if not code:
        return None
    response = _execute(
        lambda client: client.table("subjects")
        .select("subject_id, name, subject_code")
        .ilike("subject_code", code)
        .limit(1)
        .execute()
    )
    return response.data[0] if response.data else None


def is_student_enrolled(student_id, subject_id):
    response = _execute(
        lambda client: client.table("subject_students")
        .select("student_id")
        .eq("subject_id", subject_id)
        .eq("student_id", student_id)
        .limit(1)
        .execute()
    )
    return bool(response.data)


def get_enrolled_students(subject_id):
    response = _execute(
        lambda client: client.table("subject_students")
        .select("*, students(*)")
        .eq("subject_id", subject_id)
        .execute()
    )
    return response.data or []
