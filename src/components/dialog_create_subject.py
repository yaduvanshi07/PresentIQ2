import streamlit as st
from src.database.db import create_subject


@st.dialog("Create New Subject")
def create_subject_dialog(teacher_id):
    st.markdown(
        '<p style="color:#cbd5e1; font-size:0.88rem; margin-bottom:14px;">'
        'Set up a new subject section for your students.'
        '</p>',
        unsafe_allow_html=True,
    )

    sub_id = st.text_input("Subject Code", placeholder="e.g. CS101")
    sub_name = st.text_input("Subject Name", placeholder="e.g. Introduction to Computer Science")
    sub_section = st.text_input("Section / Batch", placeholder="e.g. Section A")

    st.markdown("<div style='margin: 12px 0;'></div>", unsafe_allow_html=True)

    if st.button("Create Subject Now", type="primary", width="stretch", icon="➕"):
        if sub_id and sub_name and sub_section:
            try:
                create_subject(sub_id.strip().upper(), sub_name.strip(), sub_section.strip(), teacher_id)
                st.toast("Subject created successfully!", icon="🎉")
                import time
                time.sleep(1)
                st.rerun()
            except Exception as e:
                st.error(f"Failed to create subject: {str(e)}")
        else:
            st.warning("Please fill in all the required fields.")