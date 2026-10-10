import streamlit as st
import time
from src.database.db import enroll_student_to_subject
from src.database.config import supabase


@st.dialog("Enroll in Subject")
def enroll_dialog():
    st.markdown(
        '<p style="color:#cbd5e1; font-size:0.88rem; margin-bottom:14px;">'
        'Enter the subject code provided by your educator to enroll in the course.'
        '</p>',
        unsafe_allow_html=True,
    )

    join_code = st.text_input("Subject Code", placeholder="e.g. CS101")

    st.markdown("<div style='margin: 12px 0;'></div>", unsafe_allow_html=True)

    if st.button("Enroll Now", type="primary", width="stretch", icon="✨"):
        if join_code:
            code_clean = join_code.strip().upper()
            res = (
                supabase.table("subjects")
                .select("subject_id, name, subject_code")
                .eq("subject_code", code_clean)
                .execute()
            )
            if res.data:
                subject = res.data[0]
                student_id = st.session_state.student_data["student_id"]

                check = (
                    supabase.table("subject_students")
                    .select("*")
                    .eq("subject_id", subject["subject_id"])
                    .eq("student_id", student_id)
                    .execute()
                )
                if check.data:
                    st.warning("You are already enrolled in this course.")
                else:
                    enroll_student_to_subject(student_id, subject["subject_id"])
                    st.success(f"Successfully enrolled in {subject['name']}!")
                    time.sleep(1)
                    st.rerun()
            else:
                st.error("Subject code not found. Please verify the code with your teacher.")
        else:
            st.warning("Please enter a valid subject code.")