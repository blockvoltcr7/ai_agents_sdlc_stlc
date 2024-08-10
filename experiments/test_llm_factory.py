import streamlit as st
from llms.llm_factory import LLMFactory

def main():
    st.title("Anthropic LLM Demo")

    llm_type = st.selectbox("Select LLM Type", LLMFactory.get_available_llms())
    
    if llm_type == "anthropic":
        model = st.selectbox("Select Anthropic Model", ["claude-3-opus-20240229", "claude-3-sonnet-20240229"])
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
