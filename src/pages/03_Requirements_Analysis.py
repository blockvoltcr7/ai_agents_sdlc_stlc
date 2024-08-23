import streamlit as st
import yaml
import os
from utils.llm_utils import process_text
from utils.streamlit_utils import init_session_state
from utils.logger import setup_logger

# Set up the logger
logger = setup_logger()

def load_prompts(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            prompts = yaml.safe_load(file)
        logger.info(f"Successfully loaded prompts from {file_path}")
        return prompts
    except Exception as e:
        logger.error(f"Failed to load prompts from {file_path}: {str(e)}")
        return None

def sidebar_model_selection():
    st.sidebar.header("Model Selection")
    api_choice = st.sidebar.selectbox("Choose API:", ["OpenAI", "Gemini", "Claude", "Groq", "Meta-Llama"], key="api_choice")
 
    model_options = {
        "Groq": ["llama-3.1-70b-versatile", "llama-3.1-8b-instant", "llama3-70b-8192", "llama3-8b-8192", "mixtral-8x7b-32768", "gemma-7b-it", "gemma2-9b-it"],
        "Gemini": ["gemini-1.5-flash", "gemini-1.5-pro"],
        "OpenAI": ["gpt-4o", "gpt-4o-mini", "gpt-4-turbo"],
        "Claude": ["claude-3-opus-20240229", "claude-3-sonnet-20240229", "claude-3-haiku-20240307"],
        "Meta-Llama": ["meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo", "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo", "meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo"]
    }

    model = st.sidebar.selectbox("Choose model:", model_options[api_choice], key="model")
    
    temperature = st.sidebar.slider(
        "Temperature:",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.1,
        key="temperature",
        help="Controls randomness in the output. Higher values (e.g., 0.8) make the output more random, while lower values (e.g., 0.2) make it more focused and deterministic."
    )
    max_tokens = st.sidebar.slider(
        "Max Tokens:",
        min_value=100,
        max_value=8192,
        value=2500,
        key="max_tokens",
        help="The maximum number of tokens to generate in the response. One token is roughly 4 characters for normal English text."
    )
    top_p = st.sidebar.slider(
        "Top P:",
        min_value=0.0,
        max_value=1.0,
        value=0.95,
        step=0.01,
        key="top_p",
        help="An alternative to sampling with temperature, called nucleus sampling. The model considers the results of the tokens with top_p probability mass. 0.1 means only the tokens comprising the top 10% probability mass are considered."
    )
    
    logger.info(f"Selected API: {api_choice}, Model: {model}, Temperature: {temperature}, Max Tokens: {max_tokens}, Top P: {top_p}")
    return api_choice, model, temperature, max_tokens, top_p

def write_to_markdown(doc_name, content):
    output_dir = "../demo/Requirements_phase_output"
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, f"{doc_name}.md")
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)
    logger.info(f"Written {doc_name} to {file_path}")

def generate_and_display(req_type, prompts, api_choice, model, temperature, max_tokens, top_p, **kwargs):
    if req_type not in prompts:
        logger.error(f"Prompt '{req_type}' not found in loaded prompts.")
        st.error(f"Prompt '{req_type}' not found in loaded prompts. Skipping this requirement type.")
        return
    
    st.subheader(f"Prompt for {req_type}:")
    st.code(prompts[req_type]["prompt"], language="yaml")
    
    # Add information about which planning documents were used
    if req_type in ["functional_requirements", "non_functional_requirements"]:
        st.info("This requirement is based on the Feature Proposal, Market Analysis, business_case, and Risk Register from the planning phase.")
    
    initial_prompt = prompts[req_type]["prompt"].format(
        context=kwargs.get('planning_context', ''),
        feature_name=kwargs.get('feature_name', '')
    )
    
    logger.info(f"Generating content for {req_type} using {api_choice} model: {model}")
    response = process_text(initial_prompt, "", api_choice, model, temperature, top_p, max_tokens)
    st.session_state.requirements[req_type] = response
    logger.info(f"Content generated for {req_type}")

    st.subheader(f"Generated {req_type}:")
    st.write(st.session_state.requirements[req_type])

    # Write the content to a markdown file
    write_to_markdown(req_type, st.session_state.requirements[req_type])

    user_suggestions = st.text_area(f"Suggestions for {req_type} (optional):", height=100, key=f"{req_type}_suggestions")

    if st.button(f"Regenerate {req_type} with Suggestions", key=f"regenerate_{req_type}"):
        if user_suggestions:
            refined_prompt = f"""
            Original content: {st.session_state.requirements[req_type]}
            
            User suggestions: {user_suggestions}
            
            Please generate an updated version of the {req_type} 
            incorporating the user's suggestions while maintaining the overall 
            structure and purpose of the requirements.
            """
        else:
            refined_prompt = prompts[req_type]["prompt"].format(**kwargs)

        logger.info(f"Regenerating content for {req_type} with user suggestions")
        response = process_text(refined_prompt, "", api_choice, model, temperature, top_p, max_tokens)
        logger.info(f"Processed response for {req_type}: {response[:100]}...")
        st.session_state.requirements[req_type] = response
        st.success(f"{req_type} regenerated with suggestions!")
        st.rerun()

def main():
    st.title("Requirements Analysis Phase")
    st.write("In this phase, we'll analyze the planning documents and generate detailed requirements for the new feature.")

    prompts_path = os.path.join("../resources", "prompts", "pages", "requirements_prompts.yaml")
    prompts = load_prompts(prompts_path)

    if not prompts:
        st.error("Failed to load prompts. Please check the YAML file.")
        return

    init_session_state("requirements", {})

    api_choice, model, temperature, max_tokens, top_p = sidebar_model_selection()

    st.header("1. Planning Phase Summary")
    planning_docs = st.session_state.get("planning_docs", {})

    # Create specific contexts for different requirement types
    functional_nonfunctional_context = " ".join([
        planning_docs.get("feature_proposal", ""),
        planning_docs.get("market_analysis", ""),
        planning_docs.get("risk_register", ""),
        planning_docs.get("business_case", "")
    ])

    for doc_name, content in planning_docs.items():
        with st.expander(f"{doc_name.replace('_', ' ').title()}"):
            st.write(content)

    st.header("2. Requirements Generation")
    requirement_types = ["functional_requirements", "non_functional_requirements", "technical_requirements", 
                         "user_interface_requirements", "security_requirements", "performance_requirements"]
    for req_type in requirement_types:
        with st.expander(req_type):
            if st.button(f"Generate {req_type}", key=f"generate_{req_type}"):
                if req_type in ["functional_requirements", "non_functional_requirements"]:
                    context = functional_nonfunctional_context
                else:
                    context = " ".join(planning_docs.values())  # fallback to using all docs
                
                generate_and_display(
                    req_type,
                    prompts,
                    api_choice,
                    model,
                    temperature,
                    max_tokens,
                    top_p,
                    feature_name="AI-driven personalized investment portfolio rebalancing",
                    planning_context=context
                )

if __name__ == "__main__":
    main()