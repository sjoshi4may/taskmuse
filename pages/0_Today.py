import streamlit as st
import datetime as dt
import sqlite3

conn = sqlite3.connect('./data/goals.db', check_same_thread=False)
cur = conn.cursor()

# create table
cur.execute('''Create table if not exists daily_goals (goal_id INTEGER PRIMARY KEY, goal_text text, completed BOOLEAN)''')

# Function to add a goal
def add_goal(goal_text):
    cur.execute('INSERT INTO daily_goals (goal_text, completed) VALUES (?, ?)', (goal_text, False))
    conn.commit()

# Function to delete a goal
def delete_goal(goal_id):
    cur.execute('DELETE FROM daily_goals WHERE goal_id = ?', (goal_id,))
    conn.commit()

# Function to update goal completion status
def update_goal_status(goal_id, new_status):
    cur.execute('UPDATE daily_goals SET completed = ? WHERE goal_id = ?', (new_status, goal_id))
    conn.commit()

## UI
if 'goals' not in st.session_state:
    st.session_state.goals = []

if 'progress' not in st.session_state:
    st.session_state.progress = []

tab1, tab2 = st.tabs(["Goals", 'Achievements'])
with tab1:
    st.title("Goals")
    goal = st.text_input("Enter your goal...")
    # Button to add goal
    if st.button('Add Goal'):
        add_goal(goal)
        st.success('Goal added!')

    st.subheader('Your Goals')
    goals = cur.execute('SELECT * FROM daily_goals').fetchall()
    for goal_id, goal_text, completed in goals:
        col1, col2 = st.columns([0.8, 0.2])
        with col1:
            new_status = st.checkbox(goal_text, value=completed, key=goal_id)
            if new_status != completed:
                update_goal_status(goal_id, new_status)
        with col2:
            # Delete button for each goal
            if st.button('Delete', key=f'button_{goal_id}'):
                delete_goal(goal_id)
                st.rerun()

            # Close the database connection
    conn.close()

with tab2:
    st.title('Achievements')
    with st.form(key="daily progress"):
        progress = st.text_input("Enter what you've achieved today")
        is_submit = st.form_submit_button("submit")

    if is_submit:
        st.session_state.progress.append(progress)

    with st.expander(label = "", expanded=True):
        for i, progress in enumerate(st.session_state.progress):
            st.markdown(f'-  {progress}')
        for key, value in st.session_state.items():
            if 'checkbox_' in key and value is True:
                    k = key.split('_')[-1]
                    st.markdown(f'- {st.session_state.goals[int(k)]}')
