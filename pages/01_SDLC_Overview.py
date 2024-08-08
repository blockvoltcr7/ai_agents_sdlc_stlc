import streamlit as st
import plotly.graph_objects as go
from utils.streamlit_utils import add_floating_chat_button
from components.chat_interface import chat_interface
def introduction():
    st.title("SDLC Overview: AI-Powered Software Development")
    st.write("""
    Welcome to the SDLC Overview page. This page provides an introduction to the Software Development Life Cycle (SDLC) 
    and demonstrates how AI agents can support various team members throughout different phases of the SDLC.
    """)

def sdlc_overview():
    with st.expander("What is SDLC?"):
        st.write("""
        The Software Development Life Cycle (SDLC) is a structured framework that outlines the steps involved in planning, designing,
        building, testing, and deploying a software application.
        Its goal is to ensure the final product effectively meets user needs and adheres to high quality standards.
        """)

def create_sdlc_visualization():
    st.header("SDLC Phases Visualization")
    try:
        phases = ["Planning", "Analysis", "Design", "Implementation", "Testing", "Deployment", "Maintenance"]
        edges = [(phases[i], phases[(i + 1) % len(phases)]) for i in range(len(phases))]

        fig = go.Figure()

        for phase in phases:
            fig.add_trace(go.Scatter(
                x=[phases.index(phase)],
                y=[1],
                text=[phase],
                mode='markers+text',
                textposition='top center',
                marker=dict(size=20, symbol='circle')
            ))

        for start, end in edges:
            fig.add_trace(go.Scatter(
                x=[phases.index(start), phases.index(end)],
                y=[1, 1],
                mode='lines',
                line=dict(width=2)
            ))

        fig.update_layout(
            showlegend=False,
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            margin=dict(l=20, r=20, t=20, b=20),
            plot_bgcolor='white'
        )

        st.plotly_chart(fig)
        st.caption("The SDLC is a cyclical process with distinct phases that ensure continuous improvement and delivery of quality software.")
    except Exception as e:
        st.error(f"An error occurred while creating the SDLC visualization: {str(e)}")
        st.write("Please try refreshing the page. If the problem persists, contact support.")

def explore_sdlc_phases():
    st.header("Explore SDLC Phases")
    phases = ["Planning", "Analysis", "Design", "Implementation", "Testing", "Deployment", "Maintenance"]
    tabs = st.tabs(phases)

    for i, phase in enumerate(phases):
        with tabs[i]:
            st.subheader(f"{phase} Phase")
            st.write(f"Overview of the {phase.lower()} phase...")
            st.write("**Key Activities and Deliverables:**")
            st.write("List key activities and deliverables here...")
            st.info(f"**AI Support in {phase} Phase:** AI can assist by providing insights, automation, and efficiency improvements in various tasks related to this phase.")

def ai_agents_in_roles():
    st.header("AI Agents Supporting SDLC Roles")
    roles = ["Project Manager", "Developer", "Tester", "Business Analyst", "Operations"]
    selected_role = st.selectbox("Select a role to see how AI agents can assist:", roles)

    role_descriptions = {
        "Project Manager": "AI can assist Project Managers by providing project insights, risk management, and automated reporting.",
        "Developer": "AI can help Developers with code suggestions, bug detection, and automated testing.",
        "Tester": "AI can support Testers by generating test cases, automating tests, and identifying defects.",
        "Business Analyst": "AI can assist Business Analysts with data analysis, requirement gathering, and market research.",
        "Operations": "AI can help Operations with deployment automation, monitoring, and maintenance predictions."
    }

    st.write(role_descriptions[selected_role])


def sidebar_resources():
    st.sidebar.title("Resources and Next Steps")
    st.sidebar.write("[SDLC Wikipedia](https://en.wikipedia.org/wiki/Systems_development_life_cycle)")
    st.sidebar.write("[AI and The Next Computing platforms](https://www.youtube.com/watch?v=w-cmMcMZoZ4&t=391s)")
    st.sidebar.button("Explore AI-Powered Development Tools")

def feedback_section():
    st.header("We value your feedback")
    feedback = st.text_area("Please share your feedback or suggestions:")
    if st.button("Submit Feedback"):
        st.write("Thank you for your feedback!")
    if st.button("👍"):
        st.write("Thank you for your positive feedback!")
    if st.button("👎"):
        st.write("We appreciate your honesty and will work to improve.")
        
def interactive_demo():
    st.header("Interactive AI Assistant Demo")
    st.write("This demo uses Groq's LLM to simulate an AI assistant helping with SDLC-related questions.")

    system_message = """
    You are an AI assistant specialized in the Software Development Life Cycle (SDLC). 
    Provide concise, helpful responses about SDLC phases, roles, and how AI can assist in each. 
    Keep responses under 100 words. Focus on practical applications and real-world examples 
    when discussing AI integration in SDLC processes.
    """
    
    chat_interface(system_message)

def footer():
    st.write("---")
    st.write("© Sami Sabir-Idrissi | Last updated: August 2024")

def main():
    introduction()
    sdlc_overview()
    create_sdlc_visualization()
    explore_sdlc_phases()
    ai_agents_in_roles()
    interactive_demo()  # This now includes the chat interface directly
    sidebar_resources()
    feedback_section()
    footer()

if __name__ == "__main__":
    main()