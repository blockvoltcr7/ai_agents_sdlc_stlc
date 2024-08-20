import os
import sys
import streamlit as st
import yaml
from typing import Dict, Any

# Add the src directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

# Remove Groq imports
# from src.utils.streamlit_utils import init_session_state  # Uncomment if needed

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROMPTS_PATH = os.path.normpath(os.path.join(project_root, "resources", "prompts", "pages", "planning_prompts.yaml"))

# Utility function to load prompts from YAML file
def load_prompts(file_path: str) -> Dict[str, Any]:
    try:
        with open(file_path, 'r') as file:
            prompts = yaml.safe_load(file)
        st.sidebar.success(f"Prompts loaded successfully from {file_path}")
        st.sidebar.write("Loaded prompts:", prompts)
        return prompts
    except FileNotFoundError:
        st.error(f"Prompts file not found at {file_path}. Please check the file path.")
        return {}
    except yaml.YAMLError as e:
        st.error(f"Error parsing YAML file: {e}")
        return {}

def display_prompt(prompt_key: str, **kwargs):
    if prompt_key not in prompts:
        st.error(f"Prompt key '{prompt_key}' not found in loaded prompts. Available keys: {list(prompts.keys())}")
        return

    formatted_prompt = prompts[prompt_key].format(**kwargs)
    st.write("Formatted Prompt:")
    st.write(formatted_prompt)

def main():
    st.title("Planning Phase: Feature Development")

    # Load prompts
    global prompts
    prompts = load_prompts(PROMPTS_PATH)

    if not prompts:
        st.warning("No prompts loaded. Please check the YAML file and its path.")
        return

    st.write("Loaded prompts:", prompts)  # Debug information

    # Feature Ideation Section
    st.header("1. Feature Ideation")
    feature_idea = st.text_area(
        "Describe your feature idea:", 
        value="AI-driven personalized investment portfolio rebalancing for our wealth management platform"
    )
    if st.button("Display Feature Proposal Prompt"):
        display_prompt("feature_proposal", feature_idea=feature_idea)

    # You can add more sections here to test other prompts

if __name__ == "__main__":
    main()