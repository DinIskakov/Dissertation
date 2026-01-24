"""Streamlit dashboard for crafting a subject with topics, country, and language."""
from __future__ import annotations

import json
from typing import List

import streamlit as st


def format_topics(raw: str) -> List[str]:
    """Turn a free-form textarea into a clean list of topics."""
    return [line.strip() for line in raw.splitlines() if line.strip()]


def render_badges(items: List[str], label: str):
    if not items:
        st.info(f"No {label} provided yet.")
        return
    cols = st.columns(3)
    for idx, item in enumerate(items):
        with cols[idx % len(cols)]:
            st.markdown(
                f'<div class="badge">{item}</div>',
                unsafe_allow_html=True,
            )


# def inject_style():
#     st.markdown(
#         """
#         <style>
#         @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700&family=Manrope:wght@400;600&display=swap');
#         :root {
#             --bg: linear-gradient(135deg, #0c162d 0%, #0f2e4d 40%, #0b1727 100%);
#             --panel: #0f1f3a;
#             --accent: #50c2ff;
#             --muted: #8ea0c2;
#         }
#         body, .main {
#             font-family: 'Manrope', 'Space Grotesk', 'Helvetica Neue', sans-serif;
#             color: #e8eefc;
#             background: var(--bg);
#         }
#         .block-container {
#             padding: 2.5rem 3rem 3rem 3rem;
#             border-radius: 1.2rem;
#             background: radial-gradient(100% 120% at 20% 20%, rgba(80,194,255,0.1), transparent),
#                         radial-gradient(80% 100% at 80% 0%, rgba(111,76,255,0.16), transparent),
#                         rgba(7,14,30,0.6);
#             box-shadow: 0 20px 50px rgba(5,10,20,0.6);
#         }
#         .stButton>button {
#             width: 100%;
#             border: none;
#             background: linear-gradient(90deg, #50c2ff, #6f4cff);
#             color: #0b1224;
#             font-weight: 700;
#             letter-spacing: 0.01em;
#             padding: 0.85rem 1.2rem;
#             border-radius: 0.75rem;
#             box-shadow: 0 10px 25px rgba(80,194,255,0.35);
#         }
#         .badge {
#             display: inline-block;
#             padding: 0.45rem 0.75rem;
#             margin: 0.25rem 0;
#             border-radius: 999px;
#             border: 1px solid rgba(80,194,255,0.35);
#             background: rgba(80,194,255,0.08);
#             color: #e8eefc;
#             font-weight: 600;
#             font-size: 0.9rem;
#             letter-spacing: 0.01em;
#         }
#         .stTextInput>div>div>input, .stTextArea>div>textarea, .stSelectbox>div>div>select {
#             background: var(--panel);
#             border: 1px solid rgba(255,255,255,0.08);
#             color: #e8eefc;
#         }
#         </style>
#         """,
#         unsafe_allow_html=True,
#     )


def app():
    st.set_page_config(
        page_title="Subject & Topics Dashboard",
        page_icon="S",
        layout="wide",
    )
    #inject_style()

    st.title("Subject & Topic Builder")
    st.caption("Type your subject, list as many topics as you like, and pick country/language.")

    countries = [
        "United States",
        "United Kingdom",
        "Brasil",
        "Indonesia",
        "Japan",
        "Malaysia",
        "The Netherlands",
        "Mexico",
        "Spain",
        "Russia",
        "Turkey",
        "Canada",
        "Italy",
        "France",
        "Germany",
        "Other / Custom",
    ]

    languages = [
        "English",
        "Spanish",
        "Portuguese",
        "French",
        "German",
        "Italian",
        "Russian",
        "Turkish",
        "Japanese",
        "Bahasa Indonesia",
        "Malay",
        "Other / Custom",
    ]

    with st.form("subject_form"):
        subject = st.text_input("Subject", placeholder="e.g., Climate change impacts on coastal cities")
        topics_raw = st.text_area(
            "Topics (one per line)",
            placeholder="e.g., Flood resilience\nGreen infrastructure\nInsurance markets",
            height=160,
        )
        col1, col2 = st.columns(2)
        with col1:
            country = st.selectbox("Country focus", countries, index=0)
            custom_country = st.text_input("Custom country (optional)")
        with col2:
            language = st.selectbox("Language", languages, index=0)
            custom_language = st.text_input("Custom language (optional)")

        submitted = st.form_submit_button("Generate selection")

    topics = format_topics(topics_raw)
    chosen_country = custom_country.strip() or country
    chosen_language = custom_language.strip() or language

    if submitted:
        if not subject.strip():
            st.warning("Please provide a subject.")
            return

        st.subheader("Your selection")
        st.write(f"**Subject:** {subject.strip()}")
        st.write(f"**Country:** {chosen_country}")
        st.write(f"**Language:** {chosen_language}")

        st.markdown("**Topics:**")
        render_badges(topics, label="topics")

        st.markdown("---")
        st.code(
            json.dumps(
                {
                    "subject": subject.strip(),
                    "topics": topics,
                    "country": chosen_country,
                    "language": chosen_language,
                },
                indent=2,
            ),
            language="json",
        )
    else:
        st.info("Fill the form and hit Generate to see a structured summary.")


if __name__ == "__main__":
    app()
