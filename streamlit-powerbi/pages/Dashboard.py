import streamlit as st
import sqlite3
from datetime import datetime


st.markdown(
    """
    <style>
    /* Background gradient */
    .stApp {
        background: linear-gradient(to bottom right, #e6f0ff, #ffffff);
    }

    /* Make top nav buttons look cleaner */
    .stButton > button {
        background-color: #1a73e8;
        color: white;
        border-radius: 8px;
        padding: 6px 16px;
        border: none;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton > button:hover {
        background-color: #1558b0;
        transform: scale(1.02);
    }

    /* Page title styling */
    h1, h2, h3 {
        color: #0b3d91;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ─────────────────────────────
# 🔐 Top Navigation Bar
# ─────────────────────────────
top_col1, top_col2, top_col3, top_col4 = st.columns([2, 2, 2, 1])

with top_col4:
    if "authenticated" not in st.session_state or not st.session_state.authenticated:
        if st.button("Login/Signup"):
            st.switch_page("app.py")
    else:
        if st.button("Logout"):
            st.session_state.authenticated = False
            st.session_state.username = ""
            st.success("Logged out successfully.")
            st.switch_page("app.py")

# ─────────────────────────────
# 🔒 Access Control
# ─────────────────────────────
if "authenticated" not in st.session_state or not st.session_state.authenticated:
    st.warning("Please login first.")
    st.stop()

# ─────────────────────────────
# 📝 Log Activity
# ─────────────────────────────
def log_activity(username, page):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("INSERT INTO activity VALUES (?, ?, ?)", (username, page, str(datetime.now())))
    conn.commit()
    conn.close()

log_activity(st.session_state.username, "Dashboard")

# ─────────────────────────────
# 📊 Page Setup
# ─────────────────────────────
st.set_page_config(page_title="Dashboard", layout="wide")
st.title("📊 Power BI Dashboard")
st.markdown("Tourism Analytics Dashboard:")

# ─────────────────────────────
# 📊 Dashboard + Chatbot Side-by-Side
# ─────────────────────────────
col1, col2 = st.columns([3, 1])  # 3:1 ratio for better space distribution

with col1:
    dashboard_url = "https://app.powerbi.com/view?r=eyJrIjoiNzlhNWE4MGYtNDk2My00OWU2LThkYTktNDI0NzRiMTkzOTFlIiwidCI6IjkxNjBlMzdhLTQyY2ItNDRlNS1iYjY2LTZiMGMxYjMxZTgwNSJ9"
    st.components.v1.iframe(dashboard_url, height=600, scrolling=True)

with col2:
    st.subheader("💬 Dashboard Assistant")

    predefined_qa = {
        "What is the top tourist destination?": "According to the dashboard, the top tourist destination is Goa.",
        "Which month had the highest visitors?": "The month of December recorded the highest number of visitors.",
        "Which country sends the most tourists?": "The highest number of international tourists came from the USA.",
        "What is the average stay duration?": "The average stay duration is 5.2 days.",
        "What is the total tourism revenue?": "The total tourism revenue recorded is ₹250 Crores."
    }

    question = st.selectbox("Choose a question:", [""] + list(predefined_qa.keys()))

    if question:
        st.info(predefined_qa[question])

# ─────────────────────────────
# 📌 Navigation Button
# ─────────────────────────────
st.markdown("---")
if st.button("📌 Go to Conclusion Page"):
    st.switch_page("pages/Conclusion.py")
