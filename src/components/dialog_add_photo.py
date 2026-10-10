import streamlit as st
from PIL import Image


@st.dialog("Capture or Upload Photos")
def add_photos_dialog():
    st.markdown(
        '<p style="color:#cbd5e1; font-size:0.9rem; margin-bottom:14px;">'
        'Add one or more classroom snapshots for facial recognition analysis.'
        '</p>',
        unsafe_allow_html=True,
    )

    if "photo_tab" not in st.session_state:
        st.session_state.photo_tab = "camera"

    t1, t2 = st.columns(2)
    with t1:
        type_camera = "primary" if st.session_state.photo_tab == "camera" else "secondary"
        if st.button("Live Camera", type=type_camera, width="stretch", icon="📷"):
            st.session_state.photo_tab = "camera"
            st.rerun()

    with t2:
        type_upload = "primary" if st.session_state.photo_tab == "upload" else "secondary"
        if st.button("Upload Files", type=type_upload, width="stretch", icon="📁"):
            st.session_state.photo_tab = "upload"
            st.rerun()

    st.markdown("<div style='margin: 10px 0;'></div>", unsafe_allow_html=True)

    if st.session_state.photo_tab == "camera":
        cam_photo = st.camera_input("Take Snapshot", key="dialog_cam")
        if cam_photo:
            st.session_state.attendance_images.append(Image.open(cam_photo))
            st.toast("Photo captured and added to batch!", icon="📸")
            st.rerun()

    if st.session_state.photo_tab == "upload":
        uploaded_files = st.file_uploader(
            "Choose image files",
            type=["jpg", "png", "jpeg"],
            accept_multiple_files=True,
            key="dialog_upload",
        )
        if uploaded_files:
            for f in uploaded_files:
                st.session_state.attendance_images.append(Image.open(f))
            st.toast(f"{len(uploaded_files)} photos added to batch!", icon="✅")
            st.rerun()

    st.markdown("<div style='margin: 14px 0;'></div>", unsafe_allow_html=True)
    if st.button("Done", type="primary", width="stretch", icon="✓"):
        st.rerun()