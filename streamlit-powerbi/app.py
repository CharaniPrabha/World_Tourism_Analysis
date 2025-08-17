# -------------------- app.py --------------------
import streamlit as st
import sqlite3
import re
import bcrypt
import base64
from datetime import datetime

# Set background image
def set_bg_from_local(image_file):
    with open(image_file, "rb") as file:
        encoded = base64.b64encode(file.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        .topnav {{
            display: flex;
            justify-content: center;
            gap: 3rem;
            background-color: rgba(255, 255, 255, 0.1);
            padding: 1rem;
            border-radius: 10px;
            margin-bottom: 1.5rem;
        }}
        .topnav a {{
            color: black;
            font-weight: bold;
            text-decoration: none;
            padding: 0.5rem 1rem;
            border-radius: 5px;
        }}
        .topnav a:hover {{
            background-color: #ddd;
            color: black;
        }}
        </style>
        <div class="topnav">
            <a href="/Home" target="_self">Home</a>
            <a href="/Dashboard" target="_self">Dashboard</a>
            <a href="/Conclusion" target="_self">Conclusion</a>
        </div>
        """,
        unsafe_allow_html=True
    )

# Set page config
st.set_page_config(page_title="World Tourism Login", layout="centered", initial_sidebar_state="collapsed")
set_bg_from_local("bg.png")  # Change to your background image filename

# Connect to DB
conn = sqlite3.connect("users.db")

c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY, 
    password TEXT
)''')
conn.commit()

c.execute('''CREATE TABLE IF NOT EXISTS activity_log (username TEXT, page TEXT, timestamp TEXT)''')
conn.commit()

# Password Hashing

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed)

# User Auth
st.title("World Tourism Login Portal")
auth_option = st.radio("Select Option", ["Login", "Signup"], horizontal=True)

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if auth_option == "Signup":
    if st.button("Sign Up"):
        if username and password:
            c.execute("SELECT * FROM users WHERE username = ?", (username,))
            if c.fetchone():
                st.error("Username already exists.")
            else:
                hashed_pwd = hash_password(password)
                c.execute("INSERT INTO users VALUES (?, ?)" , (username, hashed_pwd))
                conn.commit()
                st.success("Signup successful! You can now log in.")
        else:
            st.warning("Please enter both username and password.")

elif auth_option == "Login":
    if st.button("Login"):
        if username and password:
            c.execute("SELECT password FROM users WHERE username = ?", (username,))
            result = c.fetchone()
            if result and check_password(password, result[0]):
                st.session_state.authenticated = True
                st.session_state.username = username
                st.success("Login successful!")
                st.switch_page("pages/Home.py")
            else:
                st.error("Invalid credentials.")
        else:
            st.warning("Please enter both username and password.")

# -------------------- Common Navbar Function --------------------
def show_top_nav():
    st.markdown(
        """
        <style>
        .topnav {
            display: flex;
            justify-content: center;
            gap: 3rem;
            background-color: rgba(255, 255, 255, 0.1);
            padding: 1rem;
            border-radius: 10px;
            margin-bottom: 1.5rem;
        }
        .topnav a {
            color: black;
            font-weight: bold;
            text-decoration: none;
            padding: 0.5rem 1rem;
            border-radius: 5px;
        }
        .topnav a:hover {
            background-color: #ddd;
            color: black;
        }
        </style>
        <div class="topnav">
            <a href="/Home" target="_self">Home</a>
            <a href="/Dashboard" target="_self">Dashboard</a>
            <a href="/Conclusion" target="_self">Conclusion</a>
        </div>
        """,
        unsafe_allow_html=True
    )
