import io
import segno
import streamlit as st


@st.dialog("Share Course Invitation")
def share_subject_dialog(subject_name, subject_code):
    app_domain = "presentiq-main.streamlit.app"
    join_url = f"https://{app_domain}/?join-code={subject_code}"

    st.markdown(
        """
        <style>
            div[data-testid="stDialog"] div[data-testid="stCode"],
            div[data-testid="stDialog"] div[data-testid="stCodeBlock"] {
                background: #180912 !important;
                border: 1px solid rgba(244, 63, 94, 0.45) !important;
                border-radius: 10px !important;
                box-shadow: inset 0 2px 8px rgba(0, 0, 0, 0.5) !important;
            }
            div[data-testid="stDialog"] div[data-testid="stCode"] pre,
            div[data-testid="stDialog"] div[data-testid="stCodeBlock"] pre {
                background: transparent !important;
                padding: 10px 14px !important;
            }
            div[data-testid="stDialog"] div[data-testid="stCode"] code,
            div[data-testid="stDialog"] div[data-testid="stCodeBlock"] code {
                background: transparent !important;
                border: none !important;
                color: #f8fafc !important;
                font-family: 'JetBrains Mono', monospace !important;
                font-size: 0.92rem !important;
                font-weight: 600 !important;
                padding: 0 !important;
                letter-spacing: 0.02em !important;
            }
            div[data-testid="stDialog"] div[data-testid="stCode"] button,
            div[data-testid="stDialog"] div[data-testid="stCodeBlock"] button {
                color: #fda4af !important;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f'<div style="background:rgba(30, 16, 25, 0.85); border:1px solid rgba(244, 63, 94, 0.35); border-radius:12px; padding:14px 18px; margin-bottom:16px; display:flex; justify-content:space-between; align-items:center;">'
        f'<div>'
        f'<div style="font-size:0.75rem; color:#f59e0b; font-weight:700; text-transform:uppercase; letter-spacing:0.05em;">Course Invitation</div>'
        f'<h3 style="margin:2px 0 0 0; color:#ffffff; font-size:1.2rem; font-weight:700;">{subject_name}</h3>'
        f'</div>'
        f'<div style="background:rgba(225, 29, 72, 0.25); border:1px solid rgba(244, 63, 94, 0.5); padding:6px 14px; border-radius:8px; font-family:\'JetBrains Mono\', monospace; font-size:1rem; font-weight:700; color:#fde68a; letter-spacing:0.05em;">{subject_code}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    qr = segno.make(join_url)
    out = io.BytesIO()
    qr.save(out, kind="png", scale=8, border=2)

    col1, col2 = st.columns([1.1, 0.9], vertical_alignment="center", gap="medium")

    with col1:
        st.markdown('<div style="font-size:0.85rem; font-weight:600; color:#cbd5e1; margin-bottom:6px;">Join Link:</div>', unsafe_allow_html=True)
        st.code(join_url, language="text")

        st.markdown('<div style="font-size:0.85rem; font-weight:600; color:#cbd5e1; margin-bottom:6px; margin-top:10px;">Subject Code:</div>', unsafe_allow_html=True)
        st.code(subject_code, language="text")
        st.caption("Students can scan the QR code or enter this code directly in their portal.")

    with col2:
        st.image(out.getvalue(), caption="Scan to auto-enroll", width="stretch")