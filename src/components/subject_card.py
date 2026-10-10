import streamlit as st


def subject_card(name, code, section, stats=None, footer_callback=None, progress_pct=None):
    """
    Rich, executive course card displaying course name, section,
    attendance progress gauge, statistics chips, and action callbacks.
    """
    # Detect progress percentage from stats if not explicitly passed
    if progress_pct is None and stats:
        for icon, label, val in stats:
            if "rate" in label.lower():
                try:
                    progress_pct = int(str(val).replace("%", "").strip())
                except Exception:
                    pass

    progress_bar_html = ""
    status_chip = ""
    if progress_pct is not None:
        is_good = progress_pct >= 75
        status_color = "#10b981" if is_good else "#f43f5e"
        status_bg = "rgba(16, 185, 129, 0.18)" if is_good else "rgba(244, 63, 94, 0.18)"
        status_border = "rgba(16, 185, 129, 0.45)" if is_good else "rgba(244, 63, 94, 0.45)"
        status_text = "Good Standing" if is_good else "At Risk (<75%)"

        status_chip = (
            f'<span style="background:{status_bg}; color:{status_color}; border:1px solid {status_border}; '
            f'font-size:0.7rem; font-weight:700; padding:3px 10px; border-radius:999px; letter-spacing:0.04em;">'
            f'● {status_text}'
            f'</span>'
        )

        progress_bar_html = (
            f'<div style="margin: 14px 0 12px 0;">'
            f'<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:5px;">'
            f'<span style="font-size:0.75rem; font-weight:700; text-transform:uppercase; letter-spacing:0.05em; color:#cbd5e1;">Attendance Rate</span>'
            f'<span style="font-size:0.88rem; font-weight:800; color:{status_color}; font-family:\'Plus Jakarta Sans\', sans-serif;">{progress_pct}%</span>'
            f'</div>'
            f'<div style="width:100%; height:7px; background:rgba(255,255,255,0.1); border-radius:999px; overflow:hidden;">'
            f'<div style="width:{min(100, max(0, progress_pct))}%; height:100%; background:linear-gradient(90deg, #f59e0b, {status_color}); border-radius:999px;"></div>'
            f'</div>'
            f'</div>'
        )

    stats_pills = ""
    if stats:
        pills_list = []
        for icon, label, value in stats:
            pills_list.append(
                f'<div style="background:rgba(255,255,255,0.06); border:1px solid rgba(255,255,255,0.14); '
                f'padding:7px 12px; border-radius:10px; display:inline-flex; align-items:center; gap:8px;">'
                f'<span style="font-size:0.95rem; color:#f59e0b;">{icon}</span>'
                f'<div style="display:flex; flex-direction:column;">'
                f'<span style="font-size:0.68rem; font-weight:700; text-transform:uppercase; letter-spacing:0.05em; color:#94a3b8;">{label}</span>'
                f'<span style="font-size:0.98rem; font-weight:800; color:#ffffff; font-family:\'Plus Jakarta Sans\', sans-serif;">{value}</span>'
                f'</div>'
                f'</div>'
            )
        stats_pills = f'<div style="display:flex; gap:8px; flex-wrap:wrap; margin-top:8px; margin-bottom:6px;">{"".join(pills_list)}</div>'

    html = (
        f'<div class="subject-card-wrap">'
        f'<div style="display:flex; justify-content:space-between; align-items:flex-start; gap:12px; margin-bottom:4px;">'
        f'<div>'
        f'<h3 style="margin:0 0 6px 0; color:#ffffff; font-size:1.25rem; font-weight:800; font-family:\'Plus Jakarta Sans\', sans-serif; letter-spacing:-0.01em; line-height:1.3;">{name}</h3>'
        f'<div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap;">'
        f'<div style="display:inline-flex; align-items:center; gap:5px; background:rgba(255,255,255,0.08); color:#e2e8f0; font-size:0.75rem; font-weight:600; padding:2px 9px; border-radius:9999px; border:1px solid rgba(255,255,255,0.15);">'
        f'<span style="color:#f59e0b;">🏷️</span> Section {section}'
        f'</div>'
        f'{status_chip}'
        f'</div>'
        f'</div>'
        f'<span style="background:rgba(245, 158, 11, 0.2); color:#fde68a; border:1px solid rgba(245, 158, 11, 0.5); font-family:\'JetBrains Mono\', monospace; font-size:0.82rem; font-weight:700; padding:4px 10px; border-radius:8px; white-space:nowrap; letter-spacing:0.04em;">{code}</span>'
        f'</div>'
        f'{progress_bar_html}'
        f'{stats_pills}'
        f'</div>'
    )

    st.markdown(html, unsafe_allow_html=True)

    if footer_callback:
        footer_callback()