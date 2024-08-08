import streamlit as st
from utils.groq_utils import get_groq_client, get_groq_response
from utils.streamlit_utils import init_session_state

def chat_interface(system_message):
    client = get_groq_client()
    init_session_state("messages", [{"role": "system", "content": system_message}])

    for message in st.session_state.messages[1:]:  # Skip the system message
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Type your message here..."):
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        response = get_groq_response(client, st.session_state.messages)
        
        with st.chat_message("assistant"):
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})