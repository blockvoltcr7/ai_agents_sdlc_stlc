import streamlit as st
from streamlit_float import float_init

def init_session_state(key, default_value):
	if key not in st.session_state:
		st.session_state[key] = default_value

def add_floating_chat_button():
	float_init()
	with st.sidebar:
		float_button = st.button("Chat with AI Assistant")
	return float_button