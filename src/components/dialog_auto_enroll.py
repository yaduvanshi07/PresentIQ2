import streamlit as st
import time
from src.database.db import enroll_student_to_subject
from src.database.config import supabase


@st.dialog("Quick Enrollment")
def auto_enroll_dialog(subject_code):
    student_id = st.session_state.student_data["student_id"]

    res = supabase.table("subjects").select("subject_id, name").eq("subject_code", subject_code).execute()
    if not res.data:
        st.error("Invalid or expired subject code.")
        if st.button("Close", type="secondary"):
            st.query_params.clear()
            st.rerun()
        return

    subject = res.data[0]

    check = (
        supabase.table("subject_students")
        .select("*")
        .eq("subject_id", subject["subject_id"])
        .eq("student_id", student_id)
        .execute()
    )
    if check.data:
        st.info("You are already enrolled in this course.")
        if st.button("Got it!", type="primary"):
            st.query_params.clear()
            st.rerun()
        return

    st.markdown(
        f'<div style="background:rgba(30, 16, 25, 0.85); border:1px solid rgba(244, 63, 94, 0.35); border-radius:12px; padding:16px; margin-bottom:14px; text-align:center;">'
        f'<div style="font-size:0.8rem; color:#f59e0b; font-weight:700; text-transform:uppercase; letter-spacing:0.05em;">Invitation to Join</div>'
        f'<h3 style="margin:4px 0 8px 0; color:#ffffff;">{subject["name"]}</h3>'
        f'<span style="background:rgba(225, 29, 72, 0.25); color:#fda4af; border:1px solid rgba(244, 63, 94, 0.45); font-family:monospace; font-size:0.8rem; font-weight:600; padding:2px 8px; border-radius:6px;">{subject_code}</span>'
        f'</div>',
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Cancel", type="secondary", width="stretch"):
            st.query_params.clear()
            st.rerun()
    with col2:
        if st.button("Confirm Enrollment", type="primary", width="stretch", icon="✨"):
            enroll_student_to_subject(student_id, subject["subject_id"])
            st.success("Successfully enrolled in the course!")
            st.query_params.clear()
            time.sleep(1.5)
            st.rerun()
