import streamlit as st
import pandas as pd
import json
import os
from datetime import date

# --- SETUP ---
DATA_FILE = "fitness_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# --- APP ---
st.title("🚀 My Fitness Tracker")

data = load_data()
today = str(date.today())

if today not in data:
    data[today] = {"water": 0, "sleep": 0, "workout": 0}

# Sidebar inputs
st.sidebar.header("Log Activity")
w = st.sidebar.number_input("Water (Glasses)", 0, 20, data[today]["water"])
s = st.sidebar.slider("Sleep (Hours)", 0.0, 12.0, float(data[today]["sleep"]))
work = st.sidebar.checkbox("Workout Done", value=bool(data[today]["workout"]))

if st.sidebar.button("Save"):
    data[today] = {"water": w, "sleep": s, "workout": int(work)}
    save_data(data)
    st.rerun()

# Display
c1, c2 = st.columns(2)
c1.metric("Water", f"{data[today]['water']} gl")
c2.metric("Sleep", f"{data[today]['sleep']} hrs")

if data:
    df = pd.DataFrame.from_dict(data, orient='index')
    st.line_chart(df[['water', 'sleep']])
