import streamlit as st
import pandas as pd
import requests

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(
    page_title="PaperRank AI",
    layout="wide",
    page_icon="📘"
)

# -------------------------------
# COLORS
# -------------------------------
BG = "#050816"
TEXT = "#F9FAFB"
TEXT_GRAY = "#9CA3AF"
ACCENT = "#5BC0EB"

# -------------------------------
# CUSTOM CSS
# -------------------------------
st.markdown(f"""
<style>

    html, body, [data-testid="stAppViewContainer"] {{
        background-color: {BG};
        color: {TEXT};
    }}

    h1, h2, h3, h4, h5, h6 {{
        color: {TEXT};
        font-weight: 700;
    }}

    /* Hide Streamlit default top bar */
    header[data-testid="stHeader"] {{
        display: none !important;
    }}
    [data-testid="stToolbar"] {{
        display: none !important;
    }}

    .block-container {{
        padding-top: 1.5rem !important;
    }}

    /* Search button */
    .stButton > button {{
        background: linear-gradient(90deg, #A259FF, #C47CFF);
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 10px 18px !important;
        font-size: 0.95rem !important;
        font-weight: 600 !important;
        box-shadow: 0px 4px 12px rgba(162, 89, 255, 0.4) !important;
    }}
    .stButton > button:hover {{
        opacity: 0.95 !important;
    }}

</style>
""", unsafe_allow_html=True)

# -------------------------------
# HEADER
# -------------------------------
col_logo, col_title, col_profile = st.columns([1, 3, 1])

with col_logo:
    st.image("paperrank.png", width=60)

with col_title:
    st.markdown(
        f"<h1 style='text-align:center; color:{ACCENT}; margin-top:10px;'>PaperRank AI</h1>",
        unsafe_allow_html=True
    )

with col_profile:
    st.markdown(
        "<div style='margin-top:10px; float:right; width:40px; height:40px; "
        "background:linear-gradient(135deg,#5BC0EB,#1C82FF); border-radius:50%; "
        "display:flex; align-items:center; justify-content:center; color:white;'>A</div>",
        unsafe_allow_html=True
    )


st.markdown("<h2>Discover papers that matter</h2>", unsafe_allow_html=True)
st.write("Ranked research papers with explainable AI scoring. Get your reading list in seconds.")


form = st.container()
with form:
    col_query, col_rank, col_btn = st.columns([5, 3, 2])


    with col_query:
        query = st.text_input(
            "Research Topic",
            placeholder="Eg: mRNA vaccine efficacy, quantum computing...",
        )

    with col_rank:
        st.markdown(
            "<div style='font-size:0.85rem; color:#9CA3AF; margin-bottom:4px;'>Ranking Style</div>",
            unsafe_allow_html=True
        )

        ranking_mode = st.selectbox(
            "Ranking Style",
            ["Best Overall", "Most Relevant", "Most Innovative", "Highest Quality"],
            label_visibility="collapsed",
        )

        desc = {
            "Best Overall": "A balanced mix of relevance, research quality, and innovation.",
            "Most Relevant": "Papers most related to your topic.",
            "Most Innovative": "Novel ideas, unique approaches, new concepts.",
            "Highest Quality": "Strong evidence, citations, methodology.",
        }

        st.markdown(
            f"<div style='font-size:0.78rem; color:#9CA3AF; margin-top:-10px;'>{desc[ranking_mode]}</div>",
            unsafe_allow_html=True
        )

    with col_btn:
        st.write("")  # spacing
        search_btn = st.button("Search", use_container_width=True)



st.caption("💡 Tip: Be specific for better results")


results = []

if search_btn:
    if not query.strip():
        st.warning("Please enter a topic.")
    else:

        # Create loader
        loader_placeholder = st.empty()
        loader_placeholder.markdown("""
        <div style="text-align:center; margin-top:20px;">
            <img src="https://i.gifer.com/YCZH.gif" width="120px">
            <p style="color:#9CA3AF;">Analyzing papers with AI... This may take a moment.</p>
        </div>
        """, unsafe_allow_html=True)

        payload = {
            "topics": query,
            "ranking_mode": ranking_mode,
            "max_results": 30
        }

        try:
            response = requests.post(
                "https://nontheosophic-prenatural-avah.ngrok-free.dev/webhook/paperrank",
                
                json=payload,
                timeout=300
            )

            # Remove loader
            loader_placeholder.empty()

            if response.status_code != 200:
                st.error(f"Server returned error: {response.status_code}")
            else:
                try:
                    results = response.json()

                    # Fix: ensure results is ALWAYS a list of dicts
                    if isinstance(results, dict):
                        if "json" in results:
                            results = [results["json"]]
                        else:
                            results = [results]
                    st.session_state["results"] = results

                except:
                    st.error("❌ Invalid JSON returned by n8n.")

        except requests.exceptions.ConnectionError:
            loader_placeholder.empty()
            st.error("❌ Could not connect to n8n. Make sure it is running.")

        except Exception as e:
            loader_placeholder.empty()
            st.error(f"Unexpected Error. Please try after some time")


# -------- INIT SESSION STATE ----------
if "results" not in st.session_state:
    st.session_state["results"] = []


# ------------- RESULTS SECTION ----------
st.markdown("## Results")

if st.session_state["results"]:
    results = st.session_state["results"]

    df = pd.DataFrame(results)

    st.download_button(
        label="⬇️ Download Results (CSV)",
        data=df.to_csv(index=False),
        file_name="paperrank_results.csv",
        mime="text/csv"
    )

    for idx, r in enumerate(results, 1):

        title = r.get("title", "No Title")
        paper_url = r.get("url", "#")

        st.markdown(
            f"""
            <div style="padding:15px; margin:10px 0;
                        background-color:#0B1021; border-radius:8px;
                        border:1px solid #1F2937;">
                        <h3 style="margin:0; font-size:1.1rem;">
                            <a href="{paper_url}" target="_blank" style="color:white; text-decoration:none;">
                                {idx}. {title}
                            </a>
                        </h3>
                <p style="opacity:0.7;">Published: {r.get('year','-')}</p>
                <p>{r.get('abstract','No abstract available')}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

else:
    st.info("Enter a research topic and click Search.")


# -------------------------------
# FOOTER
# -------------------------------
st.markdown(
    "<p style='text-align:center; opacity:0.5; margin-top:40px;'>© 2025 PaperRank AI • Research Discovery</p>",
    unsafe_allow_html=True
)
