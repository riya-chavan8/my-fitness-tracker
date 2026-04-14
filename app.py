import streamlit as st
import pandas as pd
import json
import os
from datetime import date

# --- 1. SIMPLE LOGIN SYSTEM ---
def login():
    st.sidebar.title("Login")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    
    # Simple hardcoded credentials for learning
    if username == "admin" and password == "1234":
        return True
    elif username != "" or password != "":
        st.sidebar.error("Invalid credentials")
    return False

# --- 2. DATA PERSISTENCE ---
DATA_FILE = "fitness_history.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# --- 3. MAIN APP LOGIC ---
if login():
    st.title("🏆 My Professional Fitness Tracker")
    
    data = load_data()
    today = str(date.today())
    
    # Sidebar for data entry
    st.sidebar.success("Logged in as Admin")
    st.sidebar.header("Daily Entry")
    
    # Initialize today if missing
    if today not in data:
        data[today] = {"water": 0, "sleep": 0, "workout": 0}

    # Inputs
    w = st.sidebar.number_input("Water (glasses)", 0, 20, data[today]["water"])
    s = st.sidebar.slider("Sleep (hours)", 0.0, 12.0, float(data[today]["sleep"]))
    wk = st.sidebar.checkbox("Workout Completed", value=bool(data[today]["workout"]))

    if st.sidebar.button("Save Daily Record"):
        data[today] = {"water": w, "sleep": s, "workout": int(wk)}
        save_data(data)
        st.toast("Record Saved!")

    # --- DASHBOARD ---
    tab1, tab2 = st.tabs(["Today's Overview", "History & Trends"])

    with tab1:
        col1, col2, col3 = st.columns(3)
        col1.metric("Water", f"{data[today]['water']} gl", "Target: 8")
        col2.metric("Sleep", f"{data[today]['sleep']} hr", "Target: 8")
        col3.metric("Workout", "✅" if data[today]['workout'] else "❌")

    with tab2:
        if data:
            df = pd.DataFrame.from_dict(data, orient='index').reset_index()
            df.columns = ['Date', 'Water', 'Sleep', 'Workout']
            
            st.subheader("Progress Over Time")
            st.line_chart(df.set_index('Date')[['Water', 'Sleep']])
            
            st.subheader("Raw History Data")
            st.dataframe(df) # Shows all past records in a table
        else:
            st.write("No history found yet!")
else:
    st.warning("Please enter your username and password in the sidebar to continue.")
    st.info("Hint: admin / 1234")
