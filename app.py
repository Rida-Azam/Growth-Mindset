import streamlit as st
import requests
import datetime
import pandas as pd

st.set_page_config(page_title="Daily Motivation & Habit Tracker", layout="centered")

# Title
st.title("🌟 Daily Motivation & Habit Tracker")
st.markdown("---")  # Add a separator for better UI

# Fetch Daily Quote
quote_url = "https://zenquotes.io/api/random"
response = requests.get(quote_url)
if response.status_code == 200:
    quote = response.json()[0]['q']
    author = response.json()[0]['a']
    st.info(f"💡 **Motivation for Today:** *{quote}* - {author}")
else:
    st.info("🔹 Stay positive and keep going!")

# Habit Tracker
st.subheader("📅 Track Your Daily Habits")

# Allow user to add custom habits
custom_habit = st.text_input("Add a new habit (Press Enter to add)")
if "habits" not in st.session_state:
    st.session_state.habits = ["Read for 30 min", "Exercise", "Code for 1 hour", "Meditate"]

if custom_habit and custom_habit not in st.session_state.habits:
    st.session_state.habits.append(custom_habit)

habit_status = {}
for habit in st.session_state.habits:
    habit_status[habit] = st.checkbox(habit)

# Save data
date = datetime.date.today()  # Define date globally to avoid errors

if st.button("Save Progress"):
    habit_data = pd.DataFrame([habit_status])
    habit_data["Date"] = date
    habit_data.to_csv("habit_tracker.csv", mode='a', header=False, index=False)
    st.success("✅ Progress Saved!")

st.markdown("---")

# Reflection
st.subheader("📝 Daily Reflection")
reflection = st.text_area("Write about your day...")
if st.button("Submit Reflection"):
    with open("reflections.txt", "a", encoding="utf-8") as f:
        f.write(f"{date}: {reflection}\n")
    st.success("🌟 Reflection Saved!")

st.markdown("---")

# Progress Visualization
st.subheader("📊 Weekly Progress")
try:
    df = pd.read_csv("habit_tracker.csv", names=st.session_state.habits + ["Date"])
    progress_count = df[st.session_state.habits].sum()
    st.bar_chart(progress_count)
except FileNotFoundError:
    st.warning("No data yet. Start tracking today!")

st.markdown("💪 **Stay consistent and keep growing!**")

