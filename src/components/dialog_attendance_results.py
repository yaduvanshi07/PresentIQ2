import streamlit as st
from src.database.db import create_attendance


def show_attendance_result(df, logs):
    total_count = len(df)
    present_count = len(df[df["Status"].str.contains("Present", na=False)]) if "Status" in df.columns else 0
    absent_count = total_count - present_count

    st.markdown(
        f'<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px; background:rgba(255,255,255,0.08); border:1px solid rgba(255,255,255,0.16); padding:10px 14px; border-radius:10px;">'
        f'<span style="font-size:0.85rem; color:#cbd5e1;">Session Summary:</span>'
        f'<div style="display:flex; gap:12px;">'
        f'<span style="font-size:0.85rem; font-weight:700; color:#10b981;">✅ {present_count} Present</span>'
        f'<span style="font-size:0.85rem; font-weight:700; color:#f43f5e;">❌ {absent_count} Absent</span>'
        f'</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    st.dataframe(df, hide_index=True, width="stretch")

    st.markdown("<div style='margin: 14px 0;'></div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Discard Session", width="stretch", type="secondary", icon="❌"):
            st.session_state.voice_attendance_results = None
            st.session_state.attendance_images = []
            st.rerun()

    with col2:
        if st.button("Confirm & Save Logs", width="stretch", type="primary", icon="💾"):
            try:
                create_attendance(logs)
                st.toast("Attendance records saved successfully!", icon="✅")
                st.session_state.attendance_images = []
                st.session_state.voice_attendance_results = None
                st.rerun()
            except Exception:
                st.error("Failed to sync attendance logs to the database.")


@st.dialog("Review Attendance Results")
def attendance_result_dialog(df, logs):
    show_attendance_result(df, logs)
