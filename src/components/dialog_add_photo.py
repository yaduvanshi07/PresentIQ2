import streamlit as st
from PIL import Image


@st.dialog("Capture or Upload Photos")
def add_photos_dialog():
    st.markdown(
        '<p style="color:#cbd5e1; font-size:0.9rem; margin-bottom:12px;">'
        'Add one or more classroom snapshots for facial recognition analysis.'
        '</p>',
        unsafe_allow_html=True,
    )

    if "attendance_images" not in st.session_state:
        st.session_state.attendance_images = []

    tab_upload, tab_camera = st.tabs(["📁 Upload Files", "📷 Live Camera"])

    with tab_upload:
        uploaded_files = st.file_uploader(
            "Choose classroom image files",
            type=["jpg", "png", "jpeg"],
            accept_multiple_files=True,
            key="dialog_upload_files",
        )
        if uploaded_files:
            if st.button(
                f"Add {len(uploaded_files)} Photo(s) to Batch",
                type="primary",
                width="stretch",
                icon=":material/add_photo_alternate:",
                key="dialog_add_upload_btn",
            ):
                for f in uploaded_files:
                    st.session_state.attendance_images.append(Image.open(f))
                st.toast(f"{len(uploaded_files)} photo(s) added to batch!", icon="✅")
                st.rerun()

    with tab_camera:
        cam_photo = st.camera_input("Take Snapshot", key="dialog_cam_input")
        if cam_photo:
            if st.button(
                "Add Snapshot to Batch",
                type="primary",
                width="stretch",
                icon=":material/add_a_photo:",
                key="dialog_add_cam_btn",
            ):
                st.session_state.attendance_images.append(Image.open(cam_photo))
                st.toast("Snapshot added to batch!", icon="📸")
                st.rerun()

    count = len(st.session_state.attendance_images)
    st.markdown(
        f'<div style="background:rgba(245,158,11,0.15); border:1px solid rgba(245,158,11,0.4); border-radius:8px; padding:8px 12px; margin: 14px 0 10px 0; color:#fde68a; font-size:0.85rem; display:flex; align-items:center; gap:8px;">'
        f'<i class="fa-solid fa-images" style="color:#f59e0b;"></i>'
        f'<span>Current Batch: <strong>{count}</strong> photo{"s" if count != 1 else ""} ready for analysis</span>'
        f'</div>',
        unsafe_allow_html=True,
    )

    if st.button("Done", type="primary" if count > 0 else "secondary", width="stretch", icon=":material/check:", key="dialog_done_btn"):
        st.rerun()