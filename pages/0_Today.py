import streamlit as st
import datetime as dt

if 'goals' not in st.session_state:
    st.session_state.goals = []

if 'progress' not in st.session_state:
    st.session_state.progress = []

tab1, tab2 = st.tabs(["Goals", 'Achievements'])
with tab1:
    st.title("Goals")
    with st.form(key="daily goals"):
        goal = st.text_input("Enter your goal...")
        is_submit = st.form_submit_button("submit")

    if is_submit:
        st.session_state.goals.append(goal)

    with st.expander(label="Today", expanded=True):
        for i, goal in enumerate(st.session_state.goals):
            st.checkbox(label=f'{goal}', key=f'checkbox_{i}')
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
