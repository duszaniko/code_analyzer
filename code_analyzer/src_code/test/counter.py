import streamlit as st

def increase_counter():
    st.session_state.counter+=1

def decrease_counter():
    st.session_state.counter=-1
    if st.session_state.counter<0:
        st.session_state.counter=0

st.set_page_config(page_title="Counter", layout='wide')
st.title("Counter")

if "counter" not in st.session_state:
    st.session_state["counter"] = 1

st.button("Increase", on_click=increase_counter)
st.button("Decrease", on_click=decrease_counter)

st.write(st.session_state.counter)  