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


if "authenticated" not in st.session_state or not st.session_state.authenticated:
    st.warning("Please login first.")
    st.stop()

def log_activity(username, page):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("INSERT INTO activity VALUES (?, ?, ?)", (username, page, str(datetime.now())))
    conn.commit()
    conn.close()

log_activity(st.session_state.username, "Conclusion")

st.set_page_config(page_title="Conclusion", layout="centered")
st.title("✅ Conclusion")
import streamlit as st

st.markdown("""
### 🔹 **Overall Tourist Trends (2003–2012)**

* **Total Tourist Arrivals**: The global sum of tourist arrivals reached **862 million** over the period.  
* **Maximum Arrivals by a Single Country**: **France** leads as the top tourist destination with **81 million** tourists, making up **9.38%** of total global arrivals.  
* **Year-on-Year Growth**: A **YoY growth rate of 0.07** indicates steady, though moderate, increases in global tourism during this decade.  
* **Consistent Annual Distribution**: Each year (2003–2012) contributed nearly equally to the total tourist arrivals (~10% each), suggesting stability in global travel demand.

---

### 🔹 **Top Performing Countries**

* **France, Spain, and the United States** dominate tourist arrivals, followed closely by **China, Italy, and the United Kingdom**.  
* **China** shows remarkable performance with over **501 million** tourist arrivals and a **steady growth trajectory** from 2009 onwards.  
* Other strong performers include **Turkey, Germany, and Mexico**, making them consistent mid-tier contributors.  
* **Treemap & Bar Charts** show how France maintains a **clear lead**, but other countries are catching up in terms of growth trends.

---

### 🔹 **Growth Patterns & Forecast**

* **Growth from 2009 onward** is clearly upward, as shown in the line chart for China and the global trend.  
* Forecasts predict that by **2020**, global arrivals would surpass **1.5 billion**, marking a **significant jump** from under **1 billion in 2010**.  
* Countries like **Zimbabwe and Zambia** show fluctuating patterns but overall upward momentum in arrivals, indicating emerging tourism markets.  
* The **forecast chart** also shows confidence intervals, indicating relatively stable and predictable growth trends.

---

### 🔹 **Insights for Decision-Makers**

* Tourism boards should focus on **France, Spain, USA, and China** for best practices in infrastructure and marketing.  
* **Emerging countries** like Zambia and Zimbabwe can become future hotspots with strategic investments.  
* Policy-makers should take note of the **resilience of the tourism sector** (especially post-2009), emphasizing its role in economic recovery.  
* The **steady rise in global tourism** supports investment in eco-tourism, travel tech, and global connectivity.

---
""")


if st.button("⬅️ Back to Home"):
    st.switch_page("pages/Home.py")
