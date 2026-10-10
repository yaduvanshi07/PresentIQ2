import streamlit as st
from src.components.header import header_home
from src.components.footer import footer_home
from src.ui.base_layout import style_base_layout, style_background_home


def home_screen():
    style_background_home()
    style_base_layout()
    header_home()

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown(
            '<span class="portal-tag portal-tag-student"><i class="fa-solid fa-graduation-cap"></i> Student Access</span>'
            '<h2 style="color:#ffffff; margin:0 0 4px 0; font-size:1.45rem; font-weight:700;">I am a Student</h2>'
            '<p class="portal-desc">'
            'Access your enrolled subjects and attendance stats with zero passwords using instant FaceID.'
            '</p>',
            unsafe_allow_html=True,
        )

        subcol1, subcol2 = st.columns([1, 1], vertical_alignment="center")
        with subcol1:
            st.image("https://i.ibb.co/844D9Lrt/mascot-student.png", width=125)
        with subcol2:
            st.markdown(
                '<div class="feature-pill"><i class="fa-solid fa-bolt"></i> FaceID Login</div>'
                '<div class="feature-pill"><i class="fa-solid fa-microphone-lines"></i> Voice Profile</div>'
                '<div class="feature-pill"><i class="fa-solid fa-chart-line"></i> Attendance Stats</div>',
                unsafe_allow_html=True,
            )

        st.markdown("<div style='margin-top: 12px;'></div>", unsafe_allow_html=True)
        if st.button(
            "Enter Student Portal  →",
            type="primary",
            use_container_width=True,
            key="home_student_btn",
        ):
            st.session_state["login_type"] = "student"
            st.session_state["show_student_faceid_dialog"] = True
            st.rerun()

    with col2:
        st.markdown(
            '<span class="portal-tag portal-tag-teacher"><i class="fa-solid fa-chalkboard-user"></i> Educator Access</span>'
            '<h2 style="color:#ffffff; margin:0 0 4px 0; font-size:1.45rem; font-weight:700;">I am a Teacher</h2>'
            '<p class="portal-desc">'
            'Conduct AI face scanning or voice recognition for attendance, create subjects, and review records.'
            '</p>',
            unsafe_allow_html=True,
        )

        subcol1, subcol2 = st.columns([1, 1], vertical_alignment="center")
        with subcol1:
            st.image("https://i.ibb.co/CsmQQV6X/mascot-prof.png", width=130)
        with subcol2:
            st.markdown(
                '<div class="feature-pill"><i class="fa-solid fa-camera-retro"></i> Classroom Scanner</div>'
                '<div class="feature-pill"><i class="fa-solid fa-volume-high"></i> Voice Attendance</div>'
                '<div class="feature-pill"><i class="fa-solid fa-file-waveform"></i> Session Reports</div>',
                unsafe_allow_html=True,
            )

        st.markdown("<div style='margin-top: 12px;'></div>", unsafe_allow_html=True)
        if st.button(
            "Enter Teacher Portal  →",
            type="primary",
            use_container_width=True,
            key="home_teacher_btn",
        ):
            st.session_state["login_type"] = "teacher"
            st.rerun()

    footer_home()