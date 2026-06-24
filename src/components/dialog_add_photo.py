import hashlib
import io

import streamlit as st  # type: ignore[import]
from PIL import Image, UnidentifiedImageError  # type: ignore[import]

MAX_PHOTOS = 20
MAX_FILE_BYTES = 10 * 1024 * 1024
MAX_IMAGE_SIZE = (1920, 1920)


def _add_photo(uploaded_file) -> bool:
    raw = uploaded_file.getvalue()
    if not raw or len(raw) > MAX_FILE_BYTES:
        st.warning("Each image must be smaller than 10 MB.")
        return False

    digest = hashlib.sha256(raw).hexdigest()
    photo_hashes = st.session_state.setdefault("attendance_image_hashes", set())
    if digest in photo_hashes:
        return False
    if len(st.session_state.attendance_images) >= MAX_PHOTOS:
        st.warning(f"You can analyze at most {MAX_PHOTOS} photos at once.")
        return False

    try:
        with Image.open(io.BytesIO(raw)) as image:
            image = image.convert("RGB")
            image.thumbnail(MAX_IMAGE_SIZE)
            st.session_state.attendance_images.append(image.copy())
    except (UnidentifiedImageError, OSError):
        st.warning(f"{uploaded_file.name or 'The uploaded file'} is not a valid image.")
        return False

    photo_hashes.add(digest)
    return True


@st.dialog("Capture or upload photos")
def add_photos_dialog():
    st.write("Add classroom photos to scan for attendance.")
    st.session_state.setdefault("photo_tab", "camera")
    st.session_state.setdefault("attendance_images", [])
    st.session_state.setdefault("attendance_image_hashes", set())

    camera_column, upload_column = st.columns(2)
    with camera_column:
        if st.button(
            "Camera",
            type="primary" if st.session_state.photo_tab == "camera" else "tertiary",
            width="stretch",
        ):
            st.session_state.photo_tab = "camera"
            st.rerun()

    with upload_column:
        if st.button(
            "Upload photos",
            type="primary" if st.session_state.photo_tab == "upload" else "tertiary",
            width="stretch",
        ):
            st.session_state.photo_tab = "upload"
            st.rerun()

    added = 0
    if st.session_state.photo_tab == "camera":
        camera_photo = st.camera_input("Take Snapshot", key="dialog_cam")
        if camera_photo and _add_photo(camera_photo):
            added = 1
    else:
        uploaded_files = st.file_uploader(
            "Choose image files",
            type=["jpg", "png", "jpeg"],
            accept_multiple_files=True,
            key="dialog_upload",
        )
        for uploaded_file in uploaded_files or []:
            added += int(_add_photo(uploaded_file))

    if added:
        st.toast(f"Added {added} photo{'s' if added != 1 else ''}.")
        st.rerun()

    st.caption(f"{len(st.session_state.attendance_images)} / {MAX_PHOTOS} photos added")
    if st.button("Done", type="primary", width="stretch"):
        st.rerun()
