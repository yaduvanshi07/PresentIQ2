import streamlit as st


def style_background_home():
    """Lighter, rich ruby-crimson gradient with luminous ambient warmth."""
    st.markdown(
'<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" crossorigin="anonymous" referrerpolicy="no-referrer" />'
'<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap" />',
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <style>

            .stApp {
                background: radial-gradient(circle at 50% 12%, #8e2343 0%, #6d1a33 32%, #4d1023 68%, #2e0814 100%) !important;
                background-attachment: fixed !important;
                color: #f8fafc !important;
            }

            .stApp div[data-testid="stColumn"] {
                background: rgba(68, 18, 34, 0.76) !important;
                backdrop-filter: blur(20px) !important;
                -webkit-backdrop-filter: blur(20px) !important;
                border: 1px solid rgba(244, 63, 94, 0.38) !important;
                padding: 2.2rem 2rem !important;
                border-radius: 1.25rem !important;
                box-shadow: 0 16px 36px -10px rgba(0, 0, 0, 0.45), 0 0 24px rgba(225, 29, 72, 0.15) !important;
                transition: all 0.25s ease !important;
            }

            .stApp div[data-testid="stColumn"]:hover {
                transform: translateY(-3px) !important;
                border-color: rgba(251, 191, 36, 0.7) !important;
                box-shadow: 0 20px 45px -10px rgba(225, 29, 72, 0.4), 0 0 30px rgba(251, 191, 36, 0.25) !important;
            }

            .portal-tag {
                display: inline-flex;
                align-items: center;
                gap: 6px;
                padding: 4px 14px;
                border-radius: 9999px;
                font-size: 0.75rem;
                font-weight: 700;
                letter-spacing: 0.08em;
                text-transform: uppercase;
                margin-bottom: 12px;
            }
            .portal-tag-student {
                background: rgba(225, 29, 72, 0.25);
                color: #fda4af;
                border: 1px solid rgba(244, 63, 94, 0.5);
            }
            .portal-tag-teacher {
                background: rgba(245, 158, 11, 0.25);
                color: #fde68a;
                border: 1px solid rgba(245, 158, 11, 0.5);
            }

            .portal-desc {
                color: #e2e8f0;
                font-size: 0.95rem;
                line-height: 1.6;
                margin: 10px 0 20px 0;
            }

            .feature-pill {
                display: flex;
                align-items: center;
                gap: 10px;
                font-size: 0.88rem;
                color: #f1f5f9;
                margin-bottom: 10px;
                font-weight: 500;
            }
            .feature-pill i {
                color: #f59e0b;
                width: 18px;
                text-align: center;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def style_background_dashboard():
    """Lighter dashboard gradient: warm ruby-slate with ambient glow."""
    st.markdown(
'<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" crossorigin="anonymous" referrerpolicy="no-referrer" />'
'<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap" />',
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <style>

            .stApp {
                background: radial-gradient(circle at 50% 0%, #821f3c 0%, #62162e 35%, #440d1e 72%, #260611 100%) !important;
                background-attachment: fixed !important;
                color: #f8fafc !important;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def style_base_layout():
    """Universal Styling: FontAwesome + Google Fonts via <link>, High-Contrast Cards, Sharp Typography."""
    st.markdown(
'<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" crossorigin="anonymous" referrerpolicy="no-referrer" />'
'<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap" />',
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <style>

            /* Hide Default Streamlit Chrome */
            #MainMenu, footer, header {
                visibility: hidden;
                display: none;
            }

            /* Container Spacing */
            .block-container {
                max-width: 1140px !important;
                padding-top: 1.5rem !important;
                padding-bottom: 2.5rem !important;
                padding-left: 1.5rem !important;
                padding-right: 1.5rem !important;
            }

            /* Clean Typography */
            html, body, [class*="css"], .stMarkdown, p, span:not([data-testid="stIconMaterial"]):not(.material-symbols-rounded), label, div {
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
                -webkit-font-smoothing: antialiased;
                -moz-osx-font-smoothing: grayscale;
            }

            h1, h2, h3, h4, h5, h6 {
                font-family: 'Plus Jakarta Sans', -apple-system, sans-serif !important;
                font-weight: 700 !important;
                letter-spacing: -0.02em !important;
                color: #ffffff !important;
            }

            h1 {
                font-size: 2rem !important;
                line-height: 1.25 !important;
                margin-bottom: 0.4rem !important;
            }

            h2 {
                font-size: 1.45rem !important;
                line-height: 1.3 !important;
                margin-top: 0.4rem !important;
                margin-bottom: 0.4rem !important;
            }

            h3 {
                font-size: 1.15rem !important;
                line-height: 1.35 !important;
                font-weight: 600 !important;
            }

            p, label {
                color: #e2e8f0 !important;
                font-size: 0.92rem !important;
                line-height: 1.5 !important;
            }

            code {
                font-family: 'JetBrains Mono', monospace !important;
                background: rgba(225, 29, 72, 0.25) !important;
                color: #fca5a5 !important;
                padding: 0.25em 0.5em !important;
                border-radius: 6px !important;
                font-size: 0.88em !important;
                border: 1px solid rgba(244, 63, 94, 0.4) !important;
            }

            /* Ensure Material Symbols icons render with their own font */
            span[data-testid="stIconMaterial"],
            .material-symbols-rounded {
                font-family: 'Material Symbols Rounded' !important;
                font-style: normal;
                font-weight: 400;
                line-height: 1;
                letter-spacing: normal;
                text-transform: none;
                white-space: nowrap;
                word-wrap: normal;
                direction: ltr;
                -webkit-font-smoothing: antialiased;
                -moz-osx-font-smoothing: grayscale;
                font-feature-settings: 'liga';
            }

            /* Ensure FontAwesome icons inherit proper font */
            .fa-solid, .fa-regular, .fa-brands, .fas, .far, .fab {
                font-family: "Font Awesome 6 Free", "Font Awesome 6 Brands" !important;
                font-style: normal;
                display: inline-block;
                line-height: 1;
            }

            /* Standardized Button Styling */
            button, .stButton > button {
                font-family: 'Plus Jakarta Sans', sans-serif !important;
                font-weight: 600 !important;
                font-size: 0.925rem !important;
                border-radius: 10px !important;
                padding: 0.55rem 1.2rem !important;
                transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
                border: 1px solid transparent !important;
                cursor: pointer !important;
            }

            /* Primary Button (Crimson-Ruby) */
            button[kind="primary"], .stButton > button[data-testid="baseButton-primary"] {
                background: linear-gradient(135deg, #e11d48 0%, #be123c 60%, #9f1239 100%) !important;
                color: #ffffff !important;
                border: 1px solid #f43f5e !important;
                box-shadow: 0 4px 16px 0 rgba(225, 29, 72, 0.45) !important;
            }
            button[kind="primary"]:hover, .stButton > button[data-testid="baseButton-primary"]:hover {
                background: linear-gradient(135deg, #f43f5e 0%, #e11d48 100%) !important;
                box-shadow: 0 6px 22px 0 rgba(225, 29, 72, 0.65) !important;
                transform: translateY(-1px) !important;
                border-color: #fda4af !important;
            }

            /* Secondary Button */
            button[kind="secondary"], .stButton > button[data-testid="baseButton-secondary"] {
                background: rgba(255, 255, 255, 0.12) !important;
                color: #ffffff !important;
                border: 1px solid rgba(255, 255, 255, 0.25) !important;
                backdrop-filter: blur(10px) !important;
            }
            button[kind="secondary"]:hover, .stButton > button[data-testid="baseButton-secondary"]:hover {
                background: rgba(255, 255, 255, 0.22) !important;
                border-color: #f59e0b !important;
                color: #fde68a !important;
                transform: translateY(-1px) !important;
            }

            /* Tertiary / Ghost Button (Card Actions) */
            button[kind="tertiary"], .stButton > button[data-testid="baseButton-tertiary"] {
                background: rgba(255, 255, 255, 0.08) !important;
                color: #e2e8f0 !important;
                border: 1px solid rgba(255, 255, 255, 0.18) !important;
                border-radius: 10px !important;
            }
            button[kind="tertiary"]:hover, .stButton > button[data-testid="baseButton-tertiary"]:hover {
                background: rgba(225, 29, 72, 0.25) !important;
                color: #ffffff !important;
                border-color: rgba(244, 63, 94, 0.5) !important;
                transform: translateY(-1px) !important;
            }

            /* Inputs and Selects */
            div[data-baseweb="input"] {
                border-radius: 10px !important;
                background-color: rgba(50, 13, 24, 0.8) !important;
                border: 1px solid rgba(255, 255, 255, 0.22) !important;
                color: #ffffff !important;
            }
            div[data-baseweb="input"]:focus-within {
                border-color: #f43f5e !important;
                box-shadow: 0 0 0 3px rgba(225, 29, 72, 0.3) !important;
            }
            div[data-baseweb="input"] input {
                font-family: 'Inter', sans-serif !important;
                font-size: 0.95rem !important;
                color: #ffffff !important;
            }

            div[data-baseweb="select"] {
                border-radius: 10px !important;
                background-color: rgba(50, 13, 24, 0.8) !important;
            }

            /* Containers & Cards */
            div[data-testid="stForm"], div[data-testid="stVerticalBlockBorderWrapper"] {
                background: rgba(62, 16, 30, 0.78) !important;
                backdrop-filter: blur(16px) !important;
                border-radius: 16px !important;
                border: 1px solid rgba(244, 63, 94, 0.35) !important;
                box-shadow: 0 8px 30px 0 rgba(0, 0, 0, 0.38) !important;
                padding: 1.4rem !important;
            }

            /* Dividers */
            hr {
                margin: 1.2rem 0 !important;
                border: 0 !important;
                border-top: 1px solid rgba(255, 255, 255, 0.15) !important;
            }

            /* ── Custom Toast Styling ── */
            @keyframes toast-slide-in {
                0%   { transform: translateX(100%) scale(0.92); opacity: 0; }
                60%  { transform: translateX(-4%) scale(1.01); opacity: 1; }
                100% { transform: translateX(0) scale(1); opacity: 1; }
            }
            @keyframes toast-glow-pulse {
                0%, 100% { box-shadow: 0 8px 32px rgba(225, 29, 72, 0.25), 0 0 0 0 rgba(245, 158, 11, 0.0); }
                50%      { box-shadow: 0 8px 32px rgba(225, 29, 72, 0.35), 0 0 18px 2px rgba(245, 158, 11, 0.12); }
            }

            div[data-testid="stToast"] {
                background: linear-gradient(135deg, rgba(75, 30, 50, 0.95) 0%, rgba(45, 20, 35, 0.98) 100%) !important;
                backdrop-filter: blur(24px) !important;
                -webkit-backdrop-filter: blur(24px) !important;
                border: 1px solid rgba(244, 63, 94, 0.45) !important;
                border-left: 4px solid #f59e0b !important;
                border-radius: 14px !important;
                color: #f8fafc !important;
                font-family: 'Plus Jakarta Sans', sans-serif !important;
                font-weight: 600 !important;
                font-size: 0.95rem !important;
                padding: 14px 20px !important;
                animation: toast-slide-in 0.5s cubic-bezier(0.34, 1.56, 0.64, 1) forwards,
                           toast-glow-pulse 2.5s ease-in-out 0.5s infinite !important;
                box-shadow: 0 12px 40px rgba(0, 0, 0, 0.5), 0 0 20px rgba(225, 29, 72, 0.2) !important;
                letter-spacing: 0.01em !important;
            }

            div[data-testid="stToast"] button[aria-label="Close"] {
                color: #94a3b8 !important;
                transition: all 0.2s ease !important;
            }
            div[data-testid="stToast"] button[aria-label="Close"]:hover {
                color: #fda4af !important;
                transform: scale(1.15) !important;
            }

            /* ── Prominent Metric Cards (Enhanced) ── */
            .metric-card {
                background: linear-gradient(150deg, rgba(72, 20, 36, 0.88) 0%, rgba(46, 12, 22, 0.92) 100%) !important;
                border-radius: 16px !important;
                padding: 1.3rem 1.45rem !important;
                border: 1px solid rgba(244, 63, 94, 0.32) !important;
                border-top: 3px solid #f59e0b !important;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.35), inset 0 1px 0 rgba(255, 255, 255, 0.08) !important;
                display: flex !important;
                flex-direction: column !important;
                gap: 6px !important;
                position: relative !important;
                overflow: hidden !important;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            }
            .metric-card::before {
                content: '';
                position: absolute;
                top: 0; right: 0;
                width: 80px; height: 80px;
                background: radial-gradient(circle, rgba(245, 158, 11, 0.08) 0%, transparent 70%);
                border-radius: 50%;
                transform: translate(20px, -20px);
            }
            .metric-card:hover {
                transform: translateY(-3px);
                border-color: rgba(245, 158, 11, 0.5);
                box-shadow: 0 14px 40px rgba(0, 0, 0, 0.45), 0 0 20px rgba(245, 158, 11, 0.15) !important;
            }
            .metric-card .metric-label {
                font-size: 0.73rem;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 0.08em;
                color: #f59e0b;
                display: flex;
                align-items: center;
                gap: 6px;
            }
            .metric-card .metric-value {
                font-family: 'Plus Jakarta Sans', sans-serif;
                font-size: 1.85rem;
                font-weight: 800;
                color: #ffffff;
                line-height: 1.2;
            }

            /* ── Welcome Hero Card ── */
            .welcome-hero {
                background: linear-gradient(135deg, rgba(65, 30, 48, 0.92) 0%, rgba(40, 20, 32, 0.92) 100%);
                border: 1px solid rgba(244, 63, 94, 0.3);
                border-left: 5px solid #f59e0b;
                border-radius: 18px;
                padding: 22px 26px;
                display: flex;
                align-items: center;
                gap: 18px;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3), 0 0 30px rgba(225, 29, 72, 0.08);
                position: relative;
                overflow: hidden;
            }
            .welcome-hero::after {
                content: '';
                position: absolute;
                top: -40px; right: -40px;
                width: 120px; height: 120px;
                background: radial-gradient(circle, rgba(245, 158, 11, 0.06) 0%, transparent 70%);
                border-radius: 50%;
            }
            .welcome-avatar {
                background: linear-gradient(135deg, #e11d48 0%, #be123c 100%);
                color: #ffffff;
                width: 54px; height: 54px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 1.45rem;
                font-weight: 800;
                font-family: 'Plus Jakarta Sans', sans-serif;
                box-shadow: 0 6px 18px rgba(225, 29, 72, 0.35);
                border: 2px solid #fda4af;
                flex-shrink: 0;
            }

            /* ── Subject Cards (Enhanced) ── */
            .subject-card-wrap {
                background: linear-gradient(150deg, rgba(72, 20, 36, 0.88) 0%, rgba(44, 11, 21, 0.92) 100%) !important;
                backdrop-filter: blur(20px) !important;
                -webkit-backdrop-filter: blur(20px) !important;
                border-radius: 18px !important;
                border: 1px solid rgba(244, 63, 94, 0.32) !important;
                border-top: 4px solid #f59e0b !important;
                padding: 22px 24px !important;
                box-shadow: 0 10px 30px -5px rgba(0, 0, 0, 0.4), 0 0 20px rgba(225, 29, 72, 0.08) !important;
                margin-bottom: 18px !important;
                position: relative !important;
                overflow: hidden !important;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            }
            .subject-card-wrap::before {
                content: '';
                position: absolute;
                top: 0; left: 0;
                width: 100%; height: 4px;
                background: linear-gradient(90deg, #f59e0b, #e11d48, #f59e0b);
                background-size: 200% 100%;
                animation: shimmer-bar 4s ease-in-out infinite;
            }
            @keyframes shimmer-bar {
                0%, 100% { background-position: 0% 0; }
                50%      { background-position: 100% 0; }
            }
            .subject-card-wrap:hover {
                transform: translateY(-4px);
                border-color: rgba(245, 158, 11, 0.55);
                box-shadow: 0 16px 40px -5px rgba(0, 0, 0, 0.45), 0 0 28px rgba(245, 158, 11, 0.12);
            }

            /* Camera Input: Balanced Compact Frame (Single-Page View) */
            div[data-testid="stCameraInput"] {
                max-width: 460px !important;
                margin: 0 auto !important;
                border: 2px dashed rgba(245, 158, 11, 0.6) !important;
                border-radius: 16px !important;
                padding: 0.85rem !important;
                background: rgba(28, 15, 24, 0.85) !important;
                box-shadow: 0 6px 25px rgba(0, 0, 0, 0.4) !important;
            }

            div[data-testid="stCameraInput"] video,
            div[data-testid="stCameraInput"] img {
                max-height: 250px !important;
                width: 100% !important;
                object-fit: cover !important;
                border-radius: 10px !important;
            }

            div[data-testid="stCameraInput"] button {
                background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%) !important;
                color: #0f172a !important;
                font-family: 'Plus Jakarta Sans', sans-serif !important;
                font-weight: 800 !important;
                font-size: 1rem !important;
                letter-spacing: 0.02em !important;
                padding: 0.65rem 1.6rem !important;
                border-radius: 10px !important;
                border: 2px solid #fbbf24 !important;
                box-shadow: 0 4px 18px rgba(245, 158, 11, 0.45) !important;
                transition: all 0.2s ease !important;
                margin-top: 8px !important;
            }
            div[data-testid="stCameraInput"] button:hover {
                background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%) !important;
                transform: translateY(-2px) scale(1.02) !important;
                box-shadow: 0 6px 24px rgba(245, 158, 11, 0.65) !important;
            }

            div[data-testid="stAudioInput"] {
                border: 1px solid rgba(244, 63, 94, 0.4) !important;
                border-radius: 12px !important;
                padding: 0.75rem !important;
                background: rgba(90, 30, 52, 0.55) !important;
            }

            div[data-testid="stFileUploader"] section {
                border: 2px dashed rgba(244, 63, 94, 0.5) !important;
                border-radius: 12px !important;
                background: rgba(90, 30, 52, 0.55) !important;
            }

            div[data-testid="stDataFrame"] {
                border-radius: 12px !important;
                border: 1px solid rgba(255, 255, 255, 0.18) !important;
                overflow: hidden !important;
            }

            div[data-testid="stDialog"] > div {
                background: linear-gradient(145deg, #4d1426 0%, #2e0814 100%) !important;
                border: 1px solid rgba(244, 63, 94, 0.45) !important;
                border-radius: 20px !important;
                color: #ffffff !important;
                box-shadow: 0 25px 65px rgba(0, 0, 0, 0.55), 0 0 30px rgba(244, 63, 94, 0.2) !important;
            }

            div[data-testid="stAlert"] {
                border-radius: 12px !important;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )