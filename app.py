# app.py
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="AI Agents in SDLC", layout="wide")

def main():
    st.title("AI Agents in Software Development Life Cycle")
    st.sidebar.title("Navigation")
    
    pages = {
        "Home": home_page,
        "SDLC Overview": sdlc_overview,
        "Planning": planning_page,
        "Requirements Analysis": requirements_page,
        "Design": design_page,
        "Implementation": implementation_page,
        "Testing": testing_page,
        "Deployment": deployment_page,
        "Maintenance": maintenance_page,
        "CrewAI Demo": crewai_demo,
        "Vector Store": vector_store_demo,
        "Text-to-Speech": tts_demo
    }
    
    selection = st.sidebar.radio("Go to", list(pages.keys()))
    
    page = pages[selection]
    page()

def home_page():
    st.header("Welcome to AI Agents in SDLC")
    st.write("This app demonstrates how AI agents can be integrated into various phases of the Software Development Life Cycle.")

    # Create SDLC phase visualization
    phases = ["Planning", "Analysis", "Design", "Implementation", "Testing", "Deployment", "Maintenance"]
    durations = [1, 2, 2, 3, 2, 1, 3]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(phases, durations, color='skyblue')
    ax.set_xlabel('Duration (Months)')
    ax.set_title('Software Development Life Cycle (SDLC) Phases')
    
    # Customize the plot for better readability in Streamlit
    ax.invert_yaxis()  # Invert y-axis to show phases from top to bottom
    ax.set_axisbelow(True)  # Put the grid behind the bars
    ax.grid(axis='x', linestyle='--', alpha=0.7)
    
    # Add value labels to the end of each bar
    for i, v in enumerate(durations):
        ax.text(v, i, f' {v}', va='center')
    
    # Display the plot in Streamlit
    st.pyplot(fig)

    st.write("""
    The Software Development Life Cycle (SDLC) is a process used by the software industry to design, develop and test high quality software. The SDLC aims to produce a high-quality software that meets or exceeds customer expectations, reaches completion within times and cost estimates.
    
    This app explores how AI agents can be integrated into each phase of the SDLC to enhance efficiency, accuracy, and overall software quality.
    """)

    st.subheader("Navigate through the sidebar to explore AI integration in each SDLC phase.")

def sdlc_overview():
    st.header("SDLC Overview")
    st.write("Here we'll provide an interactive diagram of SDLC phases and AI integration points.")

# Placeholder functions for other pages
def planning_page():
    st.header("AI in Planning")

def requirements_page():
    st.header("AI in Requirements Analysis")

def design_page():
    st.header("AI in Design")

def implementation_page():
    st.header("AI in Implementation")

def testing_page():
    st.header("AI in Testing")

def deployment_page():
    st.header("AI in Deployment")

def maintenance_page():
    st.header("AI in Maintenance")

def crewai_demo():
    st.header("CrewAI Demonstration")

def vector_store_demo():
    st.header("Vector Store Integration")

def tts_demo():
    st.header("Text-to-Speech Feature")

if __name__ == "__main__":
    main()