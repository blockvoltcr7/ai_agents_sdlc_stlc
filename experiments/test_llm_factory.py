import sys
import os
import streamlit as st
# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)
from llms.llm_factory import LLMFactory

def main():
    st.title("Anthropic LLM Demo")

    llm_type = st.selectbox("Select LLM Type", LLMFactory.get_available_llms())
    
    if llm_type == "anthropic":
        model = st.selectbox("Select Anthropic Model", LLMFactory.get_available_models(llm_type))
    else:
        model = None

    llm = LLMFactory.create_llm(llm_type, model)

    prompt = st.text_area("Enter your prompt:")
    if st.button("Generate"):
        with st.spinner("Generating response..."):
            response = llm.send_prompt(prompt)
            st.write(response)

if __name__ == "__main__":
    main()