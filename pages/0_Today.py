import streamlit as st
import datetime as dt
import sqlite3
from utils import *

today = dt.datetime.today().strftime('%Y-%m-%d')
conn, cur = connect_to_db('./data/goals.db')

# Setup the tables
create_goals_table('daily_goals', cur)
create_progress_table('daily_progress', cur)


## UI
if 'goals' not in st.session_state:
    st.session_state.goals = []

if 'progress' not in st.session_state:
    st.session_state.progress = []

tab1, tab2 = st.tabs(["Goals", 'Achievements'])
with tab1:
    dat = dt.datetime.today().strftime('%Y-%m-%d')
    st.title(dat)
    goal = st.text_input("Enter your goal...")
    # Button to add goal
    if st.button('Add'):
        add_goal(goal, cur, conn)
        st.success('Goal added!')
        st.rerun()

    goals = cur.execute(f"SELECT * FROM daily_goals where completed=False").fetchall()
    with st.expander('To Do'):

        for goal_id, date_added, goal_text, completed in goals:
            col1, col2, col3 = st.columns([0.2, 0.8,  0.2])
            with col1:
                st.text(date_added)

            with col2:
                new_status = st.checkbox(goal_text, value=completed, key=f'checkbox_{goal_id}')
                if new_status != completed:
                    update_goal_status(goal_id, new_status, cur, conn)
                    add_progress(goal_text, cur, conn)
                    st.rerun()
            with col3:
                # Delete button for each goal
                if st.button('Delete', key=f'button_{goal_id}'):
                    delete_goal(goal_id, cur, conn)
                    st.rerun()

with tab2:
    progress = st.text_input("Enter any completed tasks ...")
    if st.button("Add achievement"):
        add_progress(progress, cur, conn)
        st.success('Achievement added!')
        st.rerun()

    st.subheader('Finished Tasks')

    progresses = cur.execute(f"SELECT * FROM daily_progress where date_added = '{today}'").fetchall()

    for date, progress_id, progress_text in progresses:
        st.markdown(f"<p style='color:green;'> - {progress_text}</p>", unsafe_allow_html=True)

    completed_goals = cur.execute(f'SELECT * FROM daily_goals WHERE completed=True and date_added = {today}').fetchall()
    for goal_id, date_added, goal_text, completed in completed_goals:
        st.markdown(f"<p style='color:green;'> - {goal_text}</p>", unsafe_allow_html=True)

conn.close()