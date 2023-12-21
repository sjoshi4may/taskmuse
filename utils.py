import sqlite3
import datetime as dt

def connect_to_db(db):
    """connects to a new/existing databse and returns the connection and cursor"""
    conn = sqlite3.connect(db,  check_same_thread=False)
    cur = conn.cursor()
    return conn, cur

def create_goals_table(table_name, cur):
    cur.execute(
        f'''Create table if not exists {table_name} 
        (goal_id INTEGER PRIMARY KEY,
         date_added DATE,
         goal_text text, 
         completed BOOLEAN)''')

def create_progress_table(table_name, cur):
    cur.execute(
        f'''Create table if not exists {table_name} 
        (date_added DATE,
        progress_id INTEGER PRIMARY KEY, 
        progress_text text)''')

def create_monthly_table(table_name, cur):
    cur.execute(
        f'''Create table if not exists {table_name} 
        (id INTEGER PRIMARY KEY,
         date_added DATE,
         month_added text,
         goal_text text, 
         completed BOOLEAN)''')

# Function to add a goal
def add_goal(goal_text, cur, conn):
    cur.execute('INSERT INTO daily_goals (date_added, goal_text, completed) VALUES (?, ?, ?)',
                (dt.datetime.today().strftime('%Y-%m-%d'), goal_text, False))
    conn.commit()

# Function to delete a goal
def delete_goal(goal_id, cur, conn):
    cur.execute('DELETE FROM daily_goals WHERE goal_id = ?', (goal_id,))
    conn.commit()

# Function to update goal completion status
def update_goal_status(goal_id, new_status, cur, conn):
    cur.execute('UPDATE daily_goals SET completed = ? WHERE goal_id = ?', (new_status, goal_id))
    conn.commit()


def add_progress(progress_text, cur, conn):
    cur.execute('INSERT INTO daily_progress (date_added, progress_text) VALUES (?, ?)',
                (dt.datetime.today().strftime('%Y-%m-%d'), progress_text))
    conn.commit()

def delete_progress(progress_id, cur, conn):
    cur.execute('DELETE FROM daily_progress WHERE progress_id = ?', (progress_id,))
    conn.commit()

# Function to update goal completion status
def update_progress(progress_id, progress_text, cur, conn):
    cur.execute('UPDATE daily_progress SET progress_text = ?, date_added = ? WHERE progress_id = ?',
                (progress_text, dt.datetime.today().strftime('%Y-%m-%d'), progress_id))
    conn.commit()

def add_monthly_goal(goal_text, month, cur, conn):
    cur.execute('INSERT INTO monthly_goals (date_added, month_added, goal_text, completed) VALUES (?, ?, ?, ?)',
                (dt.datetime.today().strftime('%Y-%m-%d'), month, goal_text, False))
    conn.commit()

import streamlit as st


def custom_task_status(label, complete_checkbox, in_progress_checkbox):
    """
    Custom Streamlit component to display task status with two checkboxes.

    Args:
        label (str): The label or task description.
        complete_checkbox (bool): The state of the "Complete" checkbox.
        in_progress_checkbox (bool): The state of the "In Progress" checkbox.

    Returns:
        (bool, bool): A tuple containing the updated states of both checkboxes.
    """
    st.write(label)
    complete = st.checkbox("Complete", value=complete_checkbox)
    in_progress = st.checkbox("In Progress", value=in_progress_checkbox)

    return complete, in_progress
