import streamlit as st
import numpy as np
import pandas as pd
from datetime import datetime

from src.ui.base_layout import style_background_dashboard, style_base_layout
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from src.components.subject_card import subject_card
from src.database.db import (
    check_teacher_exists,
    create_teacher,
    teacher_login,
    get_teacher_subjects,
    get_attendance_for_teacher,
)
from src.components.dialog_create_subject import create_subject_dialog
from src.components.dialog_share_subject import share_subject_dialog
from src.components.dialog_add_photo import add_photos_dialog
from src.components.dialog_attendance_results import attendance_result_dialog
from src.components.dialog_voice_attendance import voice_attendance_dialog
from src.pipelines.face_pipeline import predict_attendance
from src.database.config import supabase


def teacher_screen():
    style_background_dashboard()
    style_base_layout()

    if "teacher_data" in st.session_state:
        teacher_dashboard()
    elif "teacher_login_type" not in st.session_state or st.session_state.teacher_login_type == "login":
        teacher_screen_login()
    elif st.session_state.teacher_login_type == "register":
        teacher_screen_register()


def teacher_dashboard():
    teacher_data = st.session_state.teacher_data
    teacher_name = teacher_data["name"]
    initial = teacher_name[0].upper() if teacher_name else "T"

    # Top Branding Header
    header_dashboard()

    st.markdown("<div style='margin: 0.6rem 0;'></div>", unsafe_allow_html=True)

    # Welcome Profile Hero Card (unified in one single box)
    with st.container(border=True, key="teacher_welcome_container"):
        hero_col, logout_col = st.columns([4, 1], vertical_alignment="center")
        with hero_col:
            st.markdown(
                f'<div style="display:flex; align-items:center; gap:18px;">'
                f'<div style="background:linear-gradient(135deg, #f59e0b 0%, #d97706 100%); color:#0f172a; width:52px; height:52px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:1.4rem; font-weight:800; font-family:\'Plus Jakarta Sans\', sans-serif; box-shadow:0 4px 15px rgba(245,158,11,0.4); border:2px solid #fde68a; flex-shrink:0;">{initial}</div>'
                f'<div>'
                f'<h2 style="margin:0; font-size:1.45rem; color:#ffffff; font-weight:800; font-family:\'Plus Jakarta Sans\', sans-serif; line-height:1.25;">Hi {teacher_name}, welcome back! 👋</h2>'
                f'<div style="display:flex; align-items:center; gap:8px; margin-top:6px;">'
                f'<span style="background:rgba(245, 158, 11, 0.2); color:#fde68a; border:1px solid rgba(245, 158, 11, 0.45); font-size:0.72rem; font-weight:700; padding:3px 10px; border-radius:9999px; text-transform:uppercase; letter-spacing:0.05em;"><i class="fa-solid fa-chalkboard-user" style="margin-right:4px;"></i>Educator</span>'
                f'<span style="color:#cbd5e1; font-size:0.82rem;">• Classrooms & Courses Active</span>'
                f'</div>'
                f'</div>'
                f'</div>',
                unsafe_allow_html=True,
            )
        with logout_col:
            if st.button("Logout", type="secondary", key="teacher_logout_btn", icon=":material/logout:", width="stretch"):
                st.session_state["is_logged_in"] = False
                if "teacher_data" in st.session_state:
                    del st.session_state.teacher_data
                st.rerun()

    st.markdown("<div style='margin: 1rem 0;'></div>", unsafe_allow_html=True)

    if "current_teacher_tab" not in st.session_state:
        st.session_state.current_teacher_tab = "take_attendance"

    # Tab Navigation Controls
    tab1, tab2, tab3 = st.columns(3)

    with tab1:
        type1 = "primary" if st.session_state.current_teacher_tab == "take_attendance" else "secondary"
        if st.button("Take Attendance", type=type1, width="stretch", icon=":material/ar_on_you:"):
            st.session_state.current_teacher_tab = "take_attendance"
            st.rerun()

    with tab2:
        type2 = "primary" if st.session_state.current_teacher_tab == "manage_subjects" else "secondary"
        if st.button("Manage Subjects", type=type2, width="stretch", icon=":material/menu_book:"):
            st.session_state.current_teacher_tab = "manage_subjects"
            st.rerun()

    with tab3:
        type3 = "primary" if st.session_state.current_teacher_tab == "attendance_records" else "secondary"
        if st.button("Attendance Records", type=type3, width="stretch", icon=":material/analytics:"):
            st.session_state.current_teacher_tab = "attendance_records"
            st.rerun()

    st.markdown("<div style='margin: 0.8rem 0;'></div>", unsafe_allow_html=True)

    if st.session_state.current_teacher_tab == "take_attendance":
        teacher_tab_take_attendance()
    elif st.session_state.current_teacher_tab == "manage_subjects":
        teacher_tab_manage_subjects()
    elif st.session_state.current_teacher_tab == "attendance_records":
        teacher_tab_attendance_records()

    footer_dashboard()


def teacher_tab_take_attendance():
    teacher_id = st.session_state.teacher_data["teacher_id"]

    st.markdown(
        '<div style="margin-bottom: 0.8rem;">'
        '<h2 style="margin:0; font-size:1.4rem;"><i class="fa-solid fa-camera" style="color:#f59e0b; margin-right:8px;"></i>AI Attendance Session</h2>'
        '<p style="margin:0; color:#cbd5e1; font-size:0.85rem;">Select a course and upload classroom photos or record group audio.</p>'
        '</div>',
        unsafe_allow_html=True,
    )

    if "attendance_images" not in st.session_state:
        st.session_state.attendance_images = []

    subjects = get_teacher_subjects(teacher_id)

    if not subjects:
        st.markdown(
            '<div style="text-align:center; padding: 2.2rem 1.5rem; background:rgba(38, 20, 32, 0.7); border-radius:14px; border: 1px dashed rgba(244, 63, 94, 0.35); margin: 0.8rem 0;">'
            '<div style="font-size:2rem; margin-bottom:6px; color:#f59e0b;"><i class="fa-solid fa-book-open"></i></div>'
            '<h3 style="margin:0 0 4px 0; color:#ffffff; font-size:1.1rem;">No subjects created yet</h3>'
            '<p style="color:#cbd5e1; font-size:0.85rem; margin-bottom:12px;">Please create a subject under the \'Manage Subjects\' tab before taking attendance.</p>'
            '</div>',
            unsafe_allow_html=True,
        )
        return

    subject_options = {f"{s['name']} ({s['subject_code']}) - Sec {s['section']}": s["subject_id"] for s in subjects}

    col1, col2 = st.columns([3, 1], vertical_alignment="bottom")
    with col1:
        selected_subject_label = st.selectbox("Select Target Subject", options=list(subject_options.keys()))
    with col2:
        if st.button("Add Photos", type="primary", icon=":material/add_a_photo:", width="stretch"):
            add_photos_dialog()

    selected_subject_id = subject_options[selected_subject_label]

    st.markdown("<div style='margin: 0.8rem 0;'></div>", unsafe_allow_html=True)

    if st.session_state.attendance_images:
        st.markdown(
            f'<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">'
            f'<h3 style="margin:0; font-size:1.1rem;"><i class="fa-solid fa-images" style="color:#f59e0b; margin-right:6px;"></i>Classroom Photos ({len(st.session_state.attendance_images)})</h3>'
            f'</div>',
            unsafe_allow_html=True,
        )
        gallery_cols = st.columns(4)
        for idx, img in enumerate(st.session_state.attendance_images):
            with gallery_cols[idx % 4]:
                st.image(img, width="stretch", caption=f"Snapshot #{idx+1}")

    has_photos = bool(st.session_state.attendance_images)

    st.markdown("<div style='margin: 0.8rem 0;'></div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)

    with c1:
        if st.button(
            "Clear Photos",
            width="stretch",
            type="tertiary",
            icon=":material/delete:",
            disabled=not has_photos,
        ):
            st.session_state.attendance_images = []
            st.rerun()

    with c2:
        if st.button(
            "Run Face Analysis",
            width="stretch",
            type="primary",
            icon=":material/face:",
            disabled=not has_photos,
        ):
            with st.spinner("Deep scanning classroom photos using facial recognition AI..."):
                all_detected_ids = {}

                for idx, img in enumerate(st.session_state.attendance_images):
                    img_np = np.array(img.convert("RGB"))
                    detected, _, _ = predict_attendance(img_np)

                    if detected:
                        for sid in detected.keys():
                            student_id = int(sid)
                            all_detected_ids.setdefault(student_id, []).append(f"Photo {idx+1}")

                enrolled_res = (
                    supabase.table("subject_students")
                    .select("*, students(*)")
                    .eq("subject_id", selected_subject_id)
                    .execute()
                )
                enrolled_students = enrolled_res.data

                if not enrolled_students:
                    st.warning("No students enrolled in this course yet.")
                else:
                    results, attendance_to_log = [], []
                    current_timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

                    for node in enrolled_students:
                        student = node["students"]
                        sources = all_detected_ids.get(int(student["student_id"]), [])
                        is_present = len(sources) > 0

                        results.append(
                            {
                                "Name": student["name"],
                                "ID": student["student_id"],
                                "Source": ", ".join(sources) if is_present else "-",
                                "Status": "✅ Present" if is_present else "❌ Absent",
                            }
                        )

                        attendance_to_log.append(
                            {
                                "student_id": student["student_id"],
                                "subject_id": selected_subject_id,
                                "timestamp": current_timestamp,
                                "is_present": bool(is_present),
                            }
                        )

                    attendance_result_dialog(pd.DataFrame(results), attendance_to_log)

    with c3:
        if st.button(
            "Voice Attendance",
            type="secondary",
            width="stretch",
            icon=":material/mic:",
        ):
            voice_attendance_dialog(selected_subject_id)


def teacher_tab_manage_subjects():
    teacher_id = st.session_state.teacher_data["teacher_id"]

    col1, col2 = st.columns([2, 1], vertical_alignment="center")
    with col1:
        st.markdown(
            '<h2 style="margin:0; font-size:1.4rem;"><i class="fa-solid fa-list-check" style="color:#f59e0b; margin-right:8px;"></i>Subject Management</h2>'
            '<p style="margin:0; color:#cbd5e1; font-size:0.85rem;">Create courses and share instant enrollment QR codes.</p>',
            unsafe_allow_html=True,
        )
    with col2:
        if st.button("Create New Subject", type="primary", icon=":material/add:", width="stretch"):
            create_subject_dialog(teacher_id)

    st.markdown("<div style='margin: 1rem 0;'></div>", unsafe_allow_html=True)

    subjects = get_teacher_subjects(teacher_id)
    if subjects:
        cols = st.columns(2)
        for i, sub in enumerate(subjects):
            stats = [
                ('<i class="fa-solid fa-user-group"></i>', "Students", sub["total_students"]),
                ('<i class="fa-solid fa-clock-rotate-left"></i>', "Classes", sub["total_classes"]),
            ]

            def make_share_button(sub_name, sub_code):
                def _callback():
                    if st.button(
                        f"Share QR / Link: {sub_code}",
                        key=f"share_{sub_code}",
                        icon=":material/qr_code:",
                        type="secondary",
                        width="stretch",
                    ):
                        share_subject_dialog(sub_name, sub_code)
                return _callback

            with cols[i % 2]:
                subject_card(
                    name=sub["name"],
                    code=sub["subject_code"],
                    section=sub["section"],
                    stats=stats,
                    footer_callback=make_share_button(sub["name"], sub["subject_code"]),
                )
    else:
        st.markdown(
            '<div style="text-align:center; padding: 2.2rem 1.5rem; background:rgba(38, 20, 32, 0.7); border-radius:14px; border: 1px dashed rgba(244, 63, 94, 0.35); margin: 0.8rem 0;">'
            '<div style="font-size:2rem; margin-bottom:6px; color:#f59e0b;"><i class="fa-solid fa-folder-open"></i></div>'
            '<h3 style="margin:0 0 4px 0; color:#ffffff; font-size:1.1rem;">No subjects found</h3>'
            '<p style="color:#cbd5e1; font-size:0.85rem; margin-bottom:12px;">Create your first subject above to get started with classroom attendance.</p>'
            '</div>',
            unsafe_allow_html=True,
        )


def teacher_tab_attendance_records():
    st.markdown(
        '<div style="margin-bottom: 0.8rem;">'
        '<h2 style="margin:0; font-size:1.4rem;"><i class="fa-solid fa-table-list" style="color:#f59e0b; margin-right:8px;"></i>Attendance History & Records</h2>'
        '<p style="margin:0; color:#cbd5e1; font-size:0.85rem;">Overview of all completed attendance sessions across your courses.</p>'
        '</div>',
        unsafe_allow_html=True,
    )

    teacher_id = st.session_state.teacher_data["teacher_id"]
    records = get_attendance_for_teacher(teacher_id)

    if not records:
        st.markdown(
            '<div style="text-align:center; padding: 2.2rem 1.5rem; background:rgba(38, 20, 32, 0.7); border-radius:14px; border: 1px dashed rgba(244, 63, 94, 0.35); margin: 0.8rem 0;">'
            '<div style="font-size:2rem; margin-bottom:6px; color:#f59e0b;"><i class="fa-solid fa-chart-column"></i></div>'
            '<h3 style="margin:0 0 4px 0; color:#ffffff; font-size:1.1rem;">No attendance logs yet</h3>'
            '<p style="color:#cbd5e1; font-size:0.85rem;">Once you take attendance for any course, complete logs will appear here.</p>'
            '</div>',
            unsafe_allow_html=True,
        )
        return

    data = []
    for r in records:
        ts = r.get("timestamp")
        data.append(
            {
                "ts_group": ts.split(".")[0] if ts else None,
                "Time": datetime.fromisoformat(ts).strftime("%Y-%m-%d %I:%M %p") if ts else "N/A",
                "Subject": r["subjects"]["name"],
                "Subject Code": r["subjects"]["subject_code"],
                "is_present": bool(r.get("is_present", False)),
            }
        )

    df = pd.DataFrame(data)

    summary = (
        df.groupby(["ts_group", "Time", "Subject", "Subject Code"])
        .agg(
            Present_Count=("is_present", "sum"),
            Total_Count=("is_present", "count"),
        )
        .reset_index()
    )

    summary["Attendance"] = (
        "✅ "
        + summary["Present_Count"].astype(str)
        + " / "
        + summary["Total_Count"].astype(str)
        + " Present"
    )

    display_df = summary.sort_values(by="ts_group", ascending=False)[
        ["Time", "Subject", "Subject Code", "Attendance"]
    ]

    st.dataframe(display_df, width="stretch", hide_index=True)


def login_teacher(username, password):
    if not username or not password:
        return False
    teacher = teacher_login(username, password)
    if teacher:
        st.session_state.user_role = "teacher"
        st.session_state.teacher_data = teacher
        st.session_state.is_logged_in = True
        return True
    return False


def teacher_screen_login():
    nav_c1, nav_c2 = st.columns([2, 1], vertical_alignment="center")
    with nav_c1:
        header_dashboard()
    with nav_c2:
        st.markdown("<div style='text-align:right;'>", unsafe_allow_html=True)
        if st.button("Back to Home", type="secondary", key="teacher_back_home", icon=":material/arrow_back:"):
            st.session_state["login_type"] = None
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='margin: 1rem 0;'></div>", unsafe_allow_html=True)

    col_l, col_center, col_r = st.columns([1, 1.8, 1])
    with col_center:
        with st.container(border=True):
            st.markdown(
                '<div style="text-align:center; margin-bottom:16px;">'
                '<span style="background:rgba(245,158,11,0.25); color:#fde68a; border:1px solid rgba(245,158,11,0.5); font-size:0.72rem; font-weight:700; padding:3px 10px; border-radius:9999px; text-transform:uppercase; letter-spacing:0.06em;"><i class="fa-solid fa-lock" style="margin-right:4px;"></i>Teacher Portal</span>'
                '<h2 style="margin:6px 0 2px 0; font-size:1.45rem; color:#ffffff;">Educator Login</h2>'
                '<p style="color:#cbd5e1; font-size:0.85rem; margin:0;">Enter your credentials to manage your classrooms</p>'
                '</div>',
                unsafe_allow_html=True,
            )

            teacher_username = st.text_input("Username", placeholder="e.g. ananyaroy")
            teacher_pass = st.text_input("Password", type="password", placeholder="Enter your password")

            st.markdown("<div style='margin: 0.8rem 0;'></div>", unsafe_allow_html=True)

            btnc1, btnc2 = st.columns(2)
            with btnc1:
                if st.button("Sign In", type="primary", icon=":material/login:", width="stretch"):
                    if login_teacher(teacher_username, teacher_pass):
                        st.toast("Welcome back!", icon="👋")
                        import time
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("Invalid username or password combination.")

            with btnc2:
                if st.button("Register New", type="secondary", icon=":material/person_add:", width="stretch"):
                    st.session_state.teacher_login_type = "register"
                    st.rerun()

    footer_dashboard()


def register_teacher(teacher_username, teacher_name, teacher_pass, teacher_pass_confirm):
    if not teacher_username or not teacher_name or not teacher_pass:
        return False, "All fields are required."
    if check_teacher_exists(teacher_username):
        return False, "This username is already taken. Please choose another."
    if teacher_pass != teacher_pass_confirm:
        return False, "Passwords do not match."

    try:
        create_teacher(teacher_username, teacher_pass, teacher_name)
        return True, "Account created successfully! You can now log in."
    except Exception:
        return False, "An unexpected error occurred while creating your account."


def teacher_screen_register():
    nav_c1, nav_c2 = st.columns([2, 1], vertical_alignment="center")
    with nav_c1:
        header_dashboard()
    with nav_c2:
        st.markdown("<div style='text-align:right;'>", unsafe_allow_html=True)
        if st.button("Back to Home", type="secondary", key="teacher_reg_back_home", icon=":material/arrow_back:"):
            st.session_state["login_type"] = None
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='margin: 1rem 0;'></div>", unsafe_allow_html=True)

    col_l, col_center, col_r = st.columns([1, 1.8, 1])
    with col_center:
        with st.container(border=True):
            st.markdown(
                '<div style="text-align:center; margin-bottom:16px;">'
                '<span style="background:rgba(225, 29, 72, 0.25); color:#fda4af; border:1px solid rgba(244, 63, 94, 0.5); font-size:0.72rem; font-weight:700; padding:3px 10px; border-radius:9999px; text-transform:uppercase; letter-spacing:0.06em;"><i class="fa-solid fa-user-plus" style="margin-right:4px;"></i>New Educator</span>'
                '<h2 style="margin:6px 0 2px 0; font-size:1.45rem; color:#ffffff;">Create Account</h2>'
                '<p style="color:#cbd5e1; font-size:0.85rem; margin:0;">Register your profile to create and manage courses</p>'
                '</div>',
                unsafe_allow_html=True,
            )

            teacher_username = st.text_input("Choose Username", placeholder="e.g. ananyaroy")
            teacher_name = st.text_input("Full Name", placeholder="e.g. Prof. Ananya Roy")
            teacher_pass = st.text_input("Password", type="password", placeholder="Enter password")
            teacher_pass_confirm = st.text_input("Confirm Password", type="password", placeholder="Repeat password")

            st.markdown("<div style='margin: 0.8rem 0;'></div>", unsafe_allow_html=True)

            btnc1, btnc2 = st.columns(2)
            with btnc1:
                if st.button("Create Account", type="primary", icon=":material/check:", width="stretch"):
                    success, message = register_teacher(
                        teacher_username, teacher_name, teacher_pass, teacher_pass_confirm
                    )
                    if success:
                        st.success(message)
                        import time
                        time.sleep(1.5)
                        st.session_state.teacher_login_type = "login"
                        st.rerun()
                    else:
                        st.error(message)

            with btnc2:
                if st.button("Back to Login", type="secondary", icon=":material/arrow_back:", width="stretch"):
                    st.session_state.teacher_login_type = "login"
                    st.rerun()

    footer_dashboard()