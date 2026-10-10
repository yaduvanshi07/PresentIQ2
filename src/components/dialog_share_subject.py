import io
import segno
import streamlit as st


@st.dialog("Share Course Invitation")
def share_subject_dialog(subject_name, subject_code):
    app_domain = "presentiq-main.streamlit.app"
    join_url = f"https://{app_domain}/?join-code={subject_code}"

    st.markdown(
        f'<div style="background:rgba(30, 16, 25, 0.85); border:1px solid rgba(244, 63, 94, 0.35); border-radius:12px; padding:12px 16px; margin-bottom:16px;">'
        f'<div style="font-size:0.75rem; color:#f59e0b; font-weight:700; text-transform:uppercase; letter-spacing:0.05em;">Course Invitation</div>'
        f'<h3 style="margin:2px 0 0 0; color:#ffffff; font-size:1.15rem;">{subject_name}</h3>'
        f'</div>',
        unsafe_allow_html=True,
    )

    qr = segno.make(join_url)
    out = io.BytesIO()
    qr.save(out, kind="png", scale=8, border=2)

    col1, col2 = st.columns([1.1, 0.9], vertical_alignment="center", gap="medium")

    with col1:
        st.markdown('<div style="font-size:0.85rem; font-weight:600; color:#cbd5e1; margin-bottom:4px;">Join Link:</div>', unsafe_allow_html=True)
        st.code(join_url, language="text")

        st.markdown('<div style="font-size:0.85rem; font-weight:600; color:#cbd5e1; margin-bottom:4px; margin-top:8px;">Subject Code:</div>', unsafe_allow_html=True)
        st.code(subject_code, language="text")
        st.caption("Students can scan the QR code or enter this code directly in their portal.")

    with col2:
        st.image(out.getvalue(), caption="Scan to auto-enroll", width="stretch")