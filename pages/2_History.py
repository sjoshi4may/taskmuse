import streamlit as st
import datetime as dt
from utils import connect_to_db

conn, cur = connect_to_db('./data/goals.db')
selected_date = st.date_input('Select a date to check goals and progress', value="today")

goals = cur.execute(f"SELECT * FROM daily_goals WHERE date_added = '{selected_date}'").fetchall()
completed_goals = cur.execute(f"SELECT * FROM daily_progress WHERE date_added = '{selected_date}'").fetchall()

col_goals, col_progress = st.columns([0.5, 0.5])


with col_goals:
    st.subheader('To do')
    for _, _, goal_text, _ in goals:
        st.markdown(f'- {goal_text}')

with col_progress:
    st.subheader('Completed')
    for _, _, progress_text in completed_goals:
        st.markdown(f"<p style='color:green;'> - {progress_text}</p>", unsafe_allow_html=True)