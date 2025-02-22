import streamlit as st
import requests
import datetime
import pandas as pd
import os

# Set Page Configuration
st.set_page_config(page_title="Daily Motivation & Habit Tracker", layout="centered")

# Title & Separator
st.title("🌟 Daily Motivation & Habit Tracker")
st.markdown("---")

# Fetch Daily Quote
quote_url = "https://zenquotes.io/api/random"
response = requests.get(quote_url)

if response.status_code == 200:
    quote_data = response.json()
    if quote_data:
        quote = quote_data[0]['q']
        author = quote_data[0]['a']
        st.info(f"💡 **Motivation for Today:** *{quote}* - {author}")
else:
    st.info("🔹 Stay positive and keep going!")

# Habit Tracker
st.subheader("📅 Track Your Daily Habits")

# Initialize habits in session state
if "habits" not in st.session_state:
    st.session_state.habits = ["Read for 30 min", "Exercise", "Code for 1 hour", "Meditate"]

# Allow user to add custom habits dynamically
custom_habit = st.text_input("➕ Add a new habit (Press Enter)")
if custom_habit:
    if custom_habit not in st.session_state.habits:
        st.session_state.habits.append(custom_habit)
        st.success(f"✅ Added habit: {custom_habit}")

# Checkbox for habit tracking
habit_status = {habit: st.checkbox(habit) for habit in st.session_state.habits}

# Save Progress Button
date = datetime.date.today()

if st.button("💾 Save Progress"):
    habit_data = pd.DataFrame([habit_status])
    habit_data["Date"] = date
    file_path = "habit_tracker.csv"
    
    # Append or create CSV
    habit_data.to_csv(file_path, mode='a', header=not os.path.exists(file_path), index=False)
    
    st.success("✅ Progress Saved!")

st.markdown("---")

# Reflection Section
st.subheader("📝 Daily Reflection")
reflection = st.text_area("💭 Write about your day...")
if st.button("Submit Reflection"):
    with open("reflections.txt", "a", encoding="utf-8") as f:
        f.write(f"{date}: {reflection}\n")
    st.success("🌟 Reflection Saved!")

st.markdown("---")

# Progress Visualization
st.subheader("📊 Weekly Progress")

try:
    # Read CSV safely
    df = pd.read_csv("habit_tracker.csv", names=st.session_state.habits + ["Date"], on_bad_lines="skip")
    
    # Count completed habits
    progress_count = df[st.session_state.habits].sum()
    
    if progress_count.empty:
        st.warning("⚠️ No data available. Start tracking today!")
    else:
        st.bar_chart(progress_count)

except FileNotFoundError:
    st.warning("⚠️ No data yet. Start tracking today!")

st.markdown("💪 **Stay consistent and keep growing!**")
