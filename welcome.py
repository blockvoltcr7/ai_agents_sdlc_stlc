import streamlit as st

st.set_page_config(
    page_title="AI Agents in SDLC",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    st.title("AI Agents in Software Development Life Cycle")
    st.write(
        "Welcome to our interactive exploration of AI integration in the SDLC. "
        "This app demonstrates how AI agents can be integrated into various phases "
        "of the Software Development Life Cycle."
    )

    st.sidebar.success("Select a page above.")

    # Main page content
    st.write("""
    The Software Development Life Cycle (SDLC) is a process used by the software industry to design, develop and test high quality software. The SDLC aims to produce a high-quality software that meets or exceeds customer expectations, reaches completion within times and cost estimates.
    
    This app explores how AI agents can be integrated into each phase of the SDLC to enhance efficiency, accuracy, and overall software quality.
    """)

    # You can add more content to the main page here

if __name__ == "__main__":
    main()