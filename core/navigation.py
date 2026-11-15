
import streamlit as st

def render_navigation():

    # ASTRA_PAGE_TRANSITION_V1
    st.markdown("""
    <style>
    @keyframes astraPageEnter {
        from {
            opacity: 0;
            transform: translateX(22px);
            filter: blur(2px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
            filter: blur(0);
        }
    }

    section.main .block-container {
        animation: astraPageEnter 0.42s cubic-bezier(.2,.7,.2,1) both;
    }

    [data-testid="stPageLink"] a {
        transition: background .22s ease,
                    border-color .22s ease,
                    transform .22s ease;
    }

    [data-testid="stPageLink"] a:hover {
        transform: translateY(-2px);
    }

    @media (prefers-reduced-motion: reduce) {
        section.main .block-container {
            animation: none !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <style>
    section[data-testid="stSidebar"],
    [data-testid="collapsedControl"] {
        display: none !important;
    }

    .block-container {
        padding-top: 2.4rem !important;
        padding-left: 3rem !important;
        padding-right: 3rem !important;
        max-width: 1500px !important;
    }

    div[data-testid="stPageLink"] a {
        background: linear-gradient(135deg, #102947, #173B60) !important;
        border: 1px solid #294765 !important;
        border-radius: 12px !important;
        padding: 10px 8px !important;
        min-height: 44px !important;
        justify-content: center !important;
        color: #EAF4FF !important;
        font-weight: 650 !important;
        text-decoration: none !important;
        transition: all .2s ease !important;
    }

    div[data-testid="stPageLink"] a:hover {
        background: linear-gradient(135deg, #1671B8, #106AC5) !important;
        border-color: #55E8FF !important;
        box-shadow: 0 0 16px rgba(34, 223, 255, .18) !important;
        color: white !important;
    }

    div[data-testid="stPageLink"] p {
        font-size: 0.88rem !important;
        text-align: center !important;
        white-space: nowrap !important;
    }

    div[data-testid="stHorizontalBlock"] {
        gap: 10px !important;
    }

    hr {
        border-color: #294765 !important;
        margin-top: 1.2rem !important;
        margin-bottom: 2.2rem !important;
    }

    @media (max-width: 800px) {
        .block-container {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
            padding-top: 1.5rem !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)

    links = [
        ("pages/1_Overview.py", "Overview"),
        ("pages/2_Crew_Health.py", "Crew Health"),
        ("pages/3_Sleep_Recovery.py", "Sleep Recovery"),
        ("pages/4_Mission_Setup.py", "Mission Setup"),
        ("pages/5_Scenario_Lab.py", "Scenario Lab"),
        ("pages/6_Decision_Report.py", "Decision Report"),
    ("pages/7_Daily_Health_Monitoring.py", "Daily Monitoring"),
    ]

    columns = st.columns(8)
    for column, (page, label) in zip(columns, links):
        with column:
            st.page_link(page, label=label)

    st.divider()
