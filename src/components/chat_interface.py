import streamlit as st
from utils.llm_utils import get_llm_client, process_text
from utils.streamlit_utils import init_session_state

def chat_interface(system_message, initial_prompt=""):
    # Add model selection to sidebar
    api_choice = st.sidebar.selectbox("Choose API:", ["OpenAI", "Gemini", "Claude", "Groq", "Meta-Llama"])
    
    if api_choice == "Groq":
        model = st.sidebar.selectbox("Choose model:", ["llama3-70b-8192", "mixtral-8x7b-32768"])
    elif api_choice == "Gemini":
        model = st.sidebar.selectbox("Choose model:", ["gemini-1.5-flash", "gemini-1.5-pro"])
    elif api_choice == "OpenAI":
        model = st.sidebar.selectbox("Choose model:", ["gpt-3.5-turbo", "gpt-4"])
    elif api_choice == "Claude":
        model = st.sidebar.selectbox("Choose model:", ["claude-3-5-sonnet-20240620", "claude-3-opus-20240229"])
    elif api_choice == "Meta-Llama":
        model = st.sidebar.selectbox("Choose model:", [
            "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
            "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
            "meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo"
        ])
    
    temperature = st.sidebar.slider("Temperature:", min_value=0.0, max_value=1.0, value=0.7, step=0.1)
    max_tokens = st.sidebar.number_input("Max Tokens:", min_value=1, max_value=8192, value=2000)
    top_p = st.sidebar.slider("Top P:", min_value=0.0, max_value=1.0, value=0.95, step=0.01)

    init_session_state("messages", [{"role": "system", "content": system_message}])

    for message in st.session_state.messages[1:]:  # Skip the system message
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if initial_prompt:
        st.text_area("Suggested prompt (click to edit):", value=initial_prompt, height=100, key="suggested_prompt")
        st.write("You can copy the above prompt or type your own message below.")

    prompt = st.chat_input("Type your message here...")

    if prompt:
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        content = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])
        response = process_text(content, prompt, api_choice, model, temperature, top_p, max_tokens)
        
        with st.chat_message("assistant"):
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})