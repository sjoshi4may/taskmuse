import streamlit as st
import datetime as dt
import sqlite3

month, year = dt.datetime.now().strftime('%B'), dt.datetime.now().strftime('%Y')
st.title(f"{month}-{year}")

if 'checkboxes' not in st.session_state:
    st.session_state.checkboxes = []

warning_placeholder = st.empty()

text = st.text_input('Enter your goal ... ')

if st.button('Add goal'):
    if text:
        st.session_state.checkboxes.append([text, False])

for i, checkbox in enumerate(st.session_state.checkboxes):
    label, value = checkbox
    try:
        st.session_state.checkboxes[i][1] = st.checkbox(label, value=value)
    except st.errors.DuplicateWidgetID:
        warning_placeholder.warning("Please enter a different goal")
