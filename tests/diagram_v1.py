import streamlit as st
import graphviz as gv

# Function to create the SDLC flowchart
def create_sdlc_flowchart():
    # Define the SDLC phases
    phases = ["Planning", "Analysis", "Design", "Implementation", "Testing", "Deployment", "Maintenance"]

    # Create a graph object
    graph = gv.Digraph()

    # Add nodes
    for phase in phases:
        graph.node(phase)

    # Add edges
    for i in range(len(phases) - 1):
        graph.edge(phases[i], phases[i+1])

    return graph

# Create the SDLC flowchart
flowchart = create_sdlc_flowchart()

# Display the total duration and flowchart in Streamlit
st.title("SDLC Flowchart and Project Duration Estimation")

# Render the flowchart in Streamlit
st.graphviz_chart(flowchart.source)
