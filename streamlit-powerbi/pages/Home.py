import streamlit as st
import sqlite3
from datetime import datetime

st.set_page_config(page_title="Home", layout="centered")

# ─────────────────────────────
# 🎨 Apply Bright Business Background
# ─────────────────────────────
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
# 🚫 Block if Not Authenticated
# ─────────────────────────────
if "authenticated" not in st.session_state or not st.session_state.authenticated:
    st.warning("Please login to access this page.")
    st.stop()

# ─────────────────────────────
# 📝 Log User Activity
# ─────────────────────────────
def log_activity(username, page):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("INSERT INTO activity VALUES (?, ?, ?)", (username, page, str(datetime.now())))
    conn.commit()
    conn.close()

log_activity(st.session_state.username, "Home")

# ─────────────────────────────
# 🏠 Page Content
# ─────────────────────────────
st.title("Welcome to World Tourism")
st.write(f"Logged in as: `{st.session_state.username}`")

st.header("Explore the World")
st.markdown("""
- Travelers across India and around the globe are increasingly seeking meaningful experiences as they explore diverse states and regions. Domestic tourism has seen a significant rise, with people opting for short getaways and culturally immersive journeys. States like Rajasthan, Kerala, and Himachal Pradesh are particularly popular due to their distinct heritage, scenic landscapes, and hospitality. From desert safaris in Jaisalmer to backwater cruises in Alleppey, travelers are tailoring their trips to explore local flavors, traditions, and offbeat destinations.
""")

# ─────────────────────────────
# 🔁 Navigation Buttons
# ─────────────────────────────
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("📊 Go to Dashboard"):
        st.switch_page("pages/Dashboard.py")
with col2:
    if st.button("📌 Go to Conclusion"):
        st.switch_page("pages/Conclusion.py")
