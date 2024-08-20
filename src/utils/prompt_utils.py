import os
import sys
import streamlit as st
import yaml
from typing import Dict, Any

    
def load_prompts(file_path):
    try:
        with open(file_path, 'r') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        st.error(f"Prompts file not found: {file_path}")
        return {}
    except yaml.YAMLError as e:
        st.error(f"Error parsing YAML file: {e}")
        return {}