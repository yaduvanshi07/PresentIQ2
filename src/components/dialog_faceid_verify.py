import streamlit as st
import numpy as np
from PIL import Image
import time

from src.pipelines.face_pipeline import predict_attendance, get_face_embeddings, train_classifier
from src.pipelines.voice_pipeline import get_voice_embedding
from src.database.db import get_all_students, create_student


@st.dialog("Capture photos")
def student_faceid_dialog():
    """Popup modal dialog for Student FaceID biometric verification via camera snapshot."""
    st.markdown(
        '<p style="color:#cbd5e1; font-size:0.9rem; margin-bottom:14px;">'
        'Position your face in the camera frame to scan for FaceID attendance.'
        '</p>',
        unsafe_allow_html=True,
    )

    photo_source = st.camera_input("Take Snapshot", key="student_dialog_cam")

    # Biometric face processing
    if photo_source is not None:
        img_pil = Image.open(photo_source).convert("RGB")
        img_np = np.array(img_pil)

        with st.spinner("Analyzing biometric features with facial recognition AI..."):
            detected, all_ids, num_faces = predict_attendance(img_np)

        if num_faces == 0:
            st.warning("⚠️ No face detected! Please ensure your face is well-lit and centered.")
        elif num_faces > 1:
            st.warning("⚠️ Multiple faces detected! Please ensure only one person is in the frame.")
        else:
            if detected:
                student_id = list(detected.keys())[0]
                all_students = get_all_students()
                student = next((s for s in all_students if s["student_id"] == student_id), None)

                if student:
                    st.markdown(
                        f"""
                        <div style="background:rgba(16, 185, 129, 0.22); border:1px solid #10b981; border-radius:12px; padding:16px; text-align:center; margin:12px 0;">
                            <div style="font-size:1.8rem;">✅</div>
                            <h3 style="color:#ffffff; margin:4px 0;">Biometric Match Confirmed!</h3>
                            <p style="color:#a7f3d0; margin:0; font-size:0.95rem;">Welcome back, <b>{student['name']}</b></p>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                    st.session_state.is_logged_in = True
                    st.session_state.user_role = "student"
                    st.session_state.student_data = student
                    st.session_state.show_student_faceid_dialog = False
                    st.toast(f"Welcome back, {student['name']}!", icon="👋")
                    time.sleep(1)
                    st.rerun()
            else:
                st.markdown(
                    """
                    <div style="background:rgba(245, 158, 11, 0.18); border:1px solid rgba(245, 158, 11, 0.45); border-radius:12px; padding:12px; margin:12px 0;">
                        <h4 style="color:#fde68a; margin:0 0 4px 0;">👤 Face Not Recognized</h4>
                        <p style="color:#cbd5e1; margin:0; font-size:0.84rem;">Register your profile with this snapshot to access your attendance.</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                new_name = st.text_input("Full Name", placeholder="e.g. Akash Sharma", key="dialog_reg_student_name")

                st.markdown(
                    """
                    <div style="margin-top:10px; margin-bottom:4px;">
                        <div style="font-weight:600; font-size:0.86rem; color:#ffffff;">🎙️ Optional: Voice Biometrics</div>
                        <div style="font-size:0.78rem; color:#cbd5e1;">Record verification phrase (e.g. 'I am present').</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                audio_data = None
                try:
                    audio_data = st.audio_input("Record verification phrase", key="dialog_reg_voice_sample")
                except Exception:
                    pass

                st.markdown("<div style='margin-top:10px;'></div>", unsafe_allow_html=True)
                if st.button("Complete Registration & Enter", type="primary", width="stretch", icon=":material/check:", key="dialog_reg_complete_btn"):
                    if new_name and new_name.strip():
                        with st.spinner("Enrolling facial & voice biometric profile..."):
                            encodings = get_face_embeddings(img_np)
                            if encodings:
                                face_emb = encodings[0].tolist()
                                voice_emb = None
                                if audio_data:
                                    voice_emb = get_voice_embedding(audio_data.read())

                                response_data = create_student(new_name.strip(), face_embedding=face_emb, voice_embedding=voice_emb)
                                if response_data:
                                    train_classifier()
                                    st.session_state.is_logged_in = True
                                    st.session_state.user_role = "student"
                                    st.session_state.student_data = response_data[0]
                                    st.session_state.show_student_faceid_dialog = False
                                    st.toast(f"Profile created! Welcome, {new_name}!", icon="🎉")
                                    time.sleep(1)
                                    st.rerun()
                            else:
                                st.error("Could not extract facial features from photo. Please try capturing another photo.")
                    else:
                        st.warning("Please enter your full name.")
