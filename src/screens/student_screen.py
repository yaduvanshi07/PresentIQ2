import streamlit as st
import time
import numpy as np
from PIL import Image

from src.ui.base_layout import style_background_dashboard, style_base_layout
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from src.components.dialog_enroll import enroll_dialog
from src.components.subject_card import subject_card

from src.components.dialog_faceid_verify import student_faceid_dialog
from src.pipelines.face_pipeline import predict_attendance, get_face_embeddings, train_classifier
from src.pipelines.voice_pipeline import get_voice_embedding
from src.database.db import (
    get_all_students,
    create_student,
    get_student_subjects,
    get_student_attendance,
    unenroll_student_to_subject,
)


def student_dashboard():
    student_data = st.session_state.student_data
    student_id = student_data["student_id"]
    student_name = student_data["name"]
    initial = student_name[0].upper() if student_name else "S"

    # Top Branding Header
    header_dashboard()

    st.markdown("<div style='margin: 0.6rem 0;'></div>", unsafe_allow_html=True)

    # Welcome Profile Hero Card (unified with logout)
    with st.container(border=True, key="welcome_hero_container"):
        hero_col, logout_col = st.columns([4, 1], vertical_alignment="center")
        with hero_col:
            st.markdown(
                f'<div style="display:flex; align-items:center; gap:18px;">'
                f'<div class="welcome-avatar">{initial}</div>'
                f'<div>'
                f'<h2 style="margin:0; font-size:1.45rem; color:#ffffff; font-weight:800; font-family:\'Plus Jakarta Sans\', sans-serif;">Hi {student_name}, welcome back! 👋</h2>'
                f'<div style="display:flex; align-items:center; gap:8px; margin-top:6px;">'
                f'<span style="background:rgba(245, 158, 11, 0.2); color:#fde68a; border:1px solid rgba(245, 158, 11, 0.45); font-size:0.72rem; font-weight:700; padding:3px 10px; border-radius:9999px; text-transform:uppercase; letter-spacing:0.05em;">🎓 Student</span>'
                f'<span style="color:#94a3b8; font-size:0.82rem;">• Biometric Profile Verified</span>'
                f'</div>'
                f'</div>'
                f'</div>',
                unsafe_allow_html=True,
            )
        with logout_col:
            if st.button("Logout", type="secondary", key="student_logout_btn", icon=":material/logout:", width="stretch"):
                st.session_state["is_logged_in"] = False
                if "student_data" in st.session_state:
                    del st.session_state.student_data
                st.rerun()

    st.markdown("<div style='margin: 1rem 0;'></div>", unsafe_allow_html=True)

    # Action Bar & Enrolled Subjects Heading
    c1, c2 = st.columns([2, 1], vertical_alignment="center")
    with c1:
        st.markdown(
            '<h2 style="margin:0; font-size:1.45rem; font-weight:700;"><span style="color:#f59e0b; margin-right:8px;">📖</span>Enrolled Subjects</h2>'
            '<p style="margin:0; color:#cbd5e1; font-size:0.88rem;">Track your real-time course attendance and statistics.</p>',
            unsafe_allow_html=True,
        )
    with c2:
        if st.button("Enroll in Subject", type="primary", icon=":material/add:", width="stretch"):
            enroll_dialog()

    # Load Data
    with st.spinner("Loading your enrolled subjects..."):
        subjects = get_student_subjects(student_id)
        logs = get_student_attendance(student_id)

    stats_map = {}
    total_classes = 0
    total_attended = 0

    for log in logs:
        sid = log["subject_id"]
        if sid not in stats_map:
            stats_map[sid] = {"total": 0, "attended": 0}

        stats_map[sid]["total"] += 1
        total_classes += 1

        if log.get("is_present"):
            stats_map[sid]["attended"] += 1
            total_attended += 1

    overall_pct = int((total_attended / total_classes * 100)) if total_classes > 0 else 0
    total_absent = max(0, total_classes - total_attended)
    is_eligible = overall_pct >= 75
    rate_color = "#10b981" if is_eligible else "#f43f5e"
    rate_bg = "rgba(16, 185, 129, 0.18)" if is_eligible else "rgba(244, 63, 94, 0.18)"
    rate_border = "rgba(16, 185, 129, 0.45)" if is_eligible else "rgba(244, 63, 94, 0.45)"
    rate_status = "Exam Eligible" if is_eligible else "Attendance Alert (<75%)"

    # Executive Attendance Intelligence Bar
    st.markdown("<div style='margin: 0.8rem 0 1.2rem 0;'></div>", unsafe_allow_html=True)
    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span class="metric-label"><i class="fa-solid fa-chart-pie" style="margin-right:6px;"></i>Attendance Standing</span>
                    <span style="background:{rate_bg}; color:{rate_color}; border:1px solid {rate_border}; font-size:0.68rem; font-weight:700; padding:2px 8px; border-radius:999px; letter-spacing:0.04em;">● {rate_status}</span>
                </div>
                <div style="display:flex; align-items:baseline; gap:8px; margin-top:6px;">
                    <span class="metric-value" style="color:{rate_color}; font-size:2.2rem;">{overall_pct}%</span>
                    <span style="color:#cbd5e1; font-size:0.82rem; font-weight:600;">cumulative</span>
                </div>
                <div style="width:100%; height:7px; background:rgba(255,255,255,0.1); border-radius:999px; overflow:hidden; margin-top:8px;">
                    <div style="width:{min(100, overall_pct)}%; height:100%; background:linear-gradient(90deg, #f59e0b, {rate_color}); border-radius:999px;"></div>
                </div>
                <div style="color:#94a3b8; font-size:0.75rem; margin-top:6px;">Minimum 75% required for term examinations</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with m2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span class="metric-label"><i class="fa-solid fa-calendar-check" style="margin-right:6px;"></i>Classroom Sessions</span>
                    <span style="background:rgba(245, 158, 11, 0.18); color:#fde68a; border:1px solid rgba(245, 158, 11, 0.45); font-size:0.68rem; font-weight:700; padding:2px 8px; border-radius:999px;">{total_classes} TOTAL</span>
                </div>
                <div style="display:flex; align-items:baseline; gap:8px; margin-top:6px;">
                    <span class="metric-value" style="font-size:2.2rem;">{total_classes}</span>
                    <span style="color:#cbd5e1; font-size:0.82rem; font-weight:600;">sessions logged</span>
                </div>
                <div style="display:flex; gap:8px; margin-top:8px;">
                    <span style="background:rgba(16, 185, 129, 0.16); color:#a7f3d0; border:1px solid rgba(16, 185, 129, 0.35); font-size:0.75rem; font-weight:700; padding:3px 10px; border-radius:8px;">✓ {total_attended} Present</span>
                    <span style="background:rgba(244, 63, 94, 0.16); color:#fda4af; border:1px solid rgba(244, 63, 94, 0.35); font-size:0.75rem; font-weight:700; padding:3px 10px; border-radius:8px;">✗ {total_absent} Absent</span>
                </div>
                <div style="color:#94a3b8; font-size:0.75rem; margin-top:6px;">Automated facial biometric session log</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with m3:
        st.markdown(
            f"""
            <div class="metric-card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span class="metric-label"><i class="fa-solid fa-graduation-cap" style="margin-right:6px;"></i>Course Load</span>
                    <span style="background:rgba(59, 130, 246, 0.18); color:#93c5fd; border:1px solid rgba(59, 130, 246, 0.45); font-size:0.68rem; font-weight:700; padding:2px 8px; border-radius:999px;">ACTIVE TERM</span>
                </div>
                <div style="display:flex; align-items:baseline; gap:8px; margin-top:6px;">
                    <span class="metric-value" style="font-size:2.2rem;">{len(subjects)}</span>
                    <span style="color:#cbd5e1; font-size:0.82rem; font-weight:600;">registered courses</span>
                </div>
                <div style="display:flex; align-items:center; gap:6px; margin-top:8px; color:#e2e8f0; font-size:0.76rem; font-weight:600;">
                    <span style="color:#10b981;">⚡</span> 100% Real-Time Educator Cloud Sync
                </div>
                <div style="color:#94a3b8; font-size:0.75rem; margin-top:6px;">Updated automatically after every lecture</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<div style='margin: 1.2rem 0;'></div>", unsafe_allow_html=True)

    if not subjects:
        st.markdown(
            '<div style="text-align:center; padding: 2.5rem 1.5rem; background:rgba(58, 16, 28, 0.7); border-radius:16px; border: 1px dashed rgba(244, 63, 94, 0.35); margin: 0.8rem 0;">'
            '<div style="font-size:2.2rem; margin-bottom:8px; color:#f59e0b;">📚</div>'
            '<h3 style="margin:0 0 6px 0; color:#ffffff;">No subjects enrolled yet</h3>'
            '<p style="color:#cbd5e1; font-size:0.9rem; margin-bottom:14px;">Click the button above or use a join link to enroll in your courses.</p>'
            '</div>',
            unsafe_allow_html=True,
        )
    else:
        cols = st.columns(2)
        for i, sub_node in enumerate(subjects):
            sub = sub_node["subjects"]
            sid = sub["subject_id"]
            stats = stats_map.get(sid, {"total": 0, "attended": 0})
            sub_pct = int((stats["attended"] / stats["total"] * 100)) if stats["total"] > 0 else 0
            missed = max(0, stats["total"] - stats["attended"])

            def make_unenroll_button(subject_id, subject_name):
                def _callback():
                    if st.button(
                        f"Unenroll from {subject_name}",
                        type="tertiary",
                        width="stretch",
                        icon=":material/delete:",
                        key=f"unenroll_{subject_id}",
                    ):
                        unenroll_student_to_subject(student_id, subject_id)
                        st.toast(f"Unenrolled from {subject_name} successfully!")
                        st.rerun()
                return _callback

            with cols[i % 2]:
                subject_card(
                    name=sub["name"],
                    code=sub["subject_code"],
                    section=sub["section"],
                    stats=[
                        ("📅", "Sessions Held", stats["total"]),
                        ("✅", "Attended", stats["attended"]),
                        ("❌", "Missed", missed),
                    ],
                    progress_pct=sub_pct,
                    footer_callback=make_unenroll_button(sid, sub["name"]),
                )

    footer_dashboard()


def student_screen():
    style_background_dashboard()
    style_base_layout()

    if "student_data" in st.session_state:
        student_dashboard()
        return

    # Top Back Bar
    nav_c1, nav_c2 = st.columns([2, 1], vertical_alignment="center")
    with nav_c1:
        header_dashboard()
    with nav_c2:
        st.markdown("<div style='text-align:right;'>", unsafe_allow_html=True)
        if st.button("Back to Home", type="secondary", key="student_back_home", icon=":material/arrow_back:"):
            st.session_state["login_type"] = None
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='margin: 0.8rem 0;'></div>", unsafe_allow_html=True)

    if "show_student_faceid_dialog" not in st.session_state:
        st.session_state["show_student_faceid_dialog"] = True

    # Centered Compact Auth Card Container
    col_l, col_center, col_r = st.columns([1, 1.8, 1])
    with col_center:
        with st.container(border=True):
            st.markdown(
                '<div style="text-align:center; margin-bottom:16px;">'
                '<span style="background:rgba(225, 29, 72, 0.25); color:#fda4af; border:1px solid rgba(244, 63, 94, 0.45); font-size:0.75rem; font-weight:700; padding:3px 12px; border-radius:9999px; text-transform:uppercase; letter-spacing:0.06em;">⚡ Biometric FaceID</span>'
                '<h2 style="margin:8px 0 4px 0; font-size:1.45rem; color:#ffffff;">Student Attendance Portal</h2>'
                '<p style="color:#cbd5e1; font-size:0.86rem; margin:0 auto; line-height:1.5;">'
                'Authenticate instantly with your facial biometric features to access your enrolled courses and attendance statistics.'
                '</p>'
                '</div>',
                unsafe_allow_html=True,
            )

            st.markdown(
                """
                <div style="background:rgba(105, 36, 62, 0.55); border:1px dashed rgba(254, 205, 211, 0.45); border-radius:14px; padding:20px; text-align:center; margin-bottom:16px;">
                    <div style="font-size:2.5rem; margin-bottom:6px;">📸</div>
                    <div style="color:#ffffff; font-weight:700; font-size:1rem;">FaceID Verification Ready</div>
                    <div style="color:#fbcfe8; font-size:0.82rem; margin-top:2px;">Live camera FaceID snapshot</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            if st.button("Verify FaceID", type="primary", icon=":material/face:", width="stretch", key="student_verify_faceid_btn"):
                st.session_state["show_student_faceid_dialog"] = True

            if st.session_state.get("show_student_faceid_dialog", False):
                student_faceid_dialog()

    footer_dashboard()