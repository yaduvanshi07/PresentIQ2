import streamlit as st
import base64
from pathlib import Path


def _get_logo_data():
    logo_path = Path(__file__).resolve().parent.parent.parent / "assets" / "logo.png"
    if logo_path.exists():
        encoded = base64.b64encode(logo_path.read_bytes()).decode()
        return f"data:image/png;base64,{encoded}"
    return "https://i.ibb.co/YTYGn5qV/logo.png"


def header_home():
    logo_src = _get_logo_data()
    st.markdown(
        f'<div style="display:flex; flex-direction:column; align-items:center; justify-content:center; margin-bottom:28px; margin-top:10px; text-align:center;">'
        f'<div style="position:relative; margin-bottom:14px;">'
        f'<img src="{logo_src}" style="height:85px; border-radius:18px; box-shadow: 0 10px 30px rgba(225,29,72,0.3); border: 2px solid rgba(244,63,94,0.4); object-fit:cover;" />'
        f'</div>'
        f'<div style="display:inline-flex; align-items:center; gap:8px; background:rgba(245,158,11,0.2); border:1px solid rgba(245,158,11,0.5); border-radius:9999px; padding:4px 14px; margin-bottom:10px;">'
        f'<span style="font-size:0.75rem; font-weight:700; color:#fbbf24; letter-spacing:0.08em; text-transform:uppercase;">AI Biometric Attendance</span>'
        f'</div>'
        f'<h1 style="color:#ffffff; margin:0; font-size:2.6rem; letter-spacing:-0.03em; font-weight:800;">PresentIQ</h1>'
        f'<p style="color:#cbd5e1; font-size:1.05rem; margin-top:8px; max-width:520px; line-height:1.55;">'
        f'Modern biometric attendance tracking system with Face & Voice recognition for seamless classroom management.'
        f'</p>'
        f'</div>',
        unsafe_allow_html=True,
    )


def header_dashboard():
    logo_src = _get_logo_data()
    st.markdown(
        f'<div style="display:flex; align-items:center; gap:14px; margin-bottom:8px;">'
        f'<img src="{logo_src}" style="height:46px; border-radius:12px; box-shadow: 0 4px 16px rgba(225,29,72,0.25); border:1px solid rgba(244,63,94,0.3); object-fit:cover;" />'
        f'<div>'
        f'<div style="display:flex; align-items:center; gap:8px;">'
        f'<h2 style="color:#ffffff; margin:0; font-size:1.4rem; font-weight:800; letter-spacing:-0.02em;">PresentIQ</h2>'
        f'<span style="background:rgba(245,158,11,0.22); color:#fde68a; border:1px solid rgba(245,158,11,0.5); font-size:0.7rem; font-weight:700; padding:2px 8px; border-radius:9999px; text-transform:uppercase; letter-spacing:0.05em;">AI Portal</span>'
        f'</div>'
        f'<p style="color:#94a3b8; font-size:0.8rem; margin:0; font-weight:500;">Classroom Intelligence System</p>'
        f'</div>'
        f'</div>',
        unsafe_allow_html=True,
    )