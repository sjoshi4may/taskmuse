import streamlit as st
from utils import *

month, year = dt.datetime.now().strftime('%B'), dt.datetime.now().strftime('%Y')
st.title(f"{month}-{year}")

## setup the table
conn, cur = connect_to_db('./data/goals.db')
create_monthly_table('monthly_goals', cur)

goals = cur.execute(f"SELECT * FROM monthly_goals").fetchall()
completed_goals = cur.execute(f"SELECT * FROM monthly_goals WHERE completed = True").fetchall()

if 'month_goals' not in st.session_state:
    st.session_state.month_goals = []


goal = st.text_input('Enter your goals for this month ...')
if st.button('submit'):
    add_monthly_goal(goal, month, cur, conn)
    st.success('Goal added!')
    st.rerun()

col1, col2 = st.columns([0.5,0.5])
with col1:
    with st.expander('To Do'):
        for id, date, month, goal_text, _ in goals:
            st.markdown(f'- {goal_text}')

with col2:
    for _,_,_,goal_text,_ in completed_goals:
        st.markdown(f"<p style='color:green;'> - {goal_text}</p>", unsafe_allow_html=True)




