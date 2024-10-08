import streamlit as st
import yaml
import os
import google.generativeai as genai
from utils.llm_utils import get_llm_client, process_text
from utils.streamlit_utils import init_session_state
import utils.prompt_utils as prompt_utils
from utils.logger import setup_logger
from dotenv import load_dotenv
import pyperclip

# Load environment variables
load_dotenv()

# Set up the logger
logger = setup_logger()

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    logger.error("GEMINI_API_KEY environment variable is not set")

def load_prompts(file_path):
    try:
        prompts = prompt_utils.load_prompts(file_path)
        logger.info(f"Successfully loaded prompts from {file_path}")
        return prompts
    except Exception as e:
        logger.error(f"Failed to load prompts from {file_path}: {str(e)}")
        return None

def sidebar_model_selection():
    st.sidebar.header("Model Selection")
    api_choice = st.sidebar.selectbox("Choose API:", ["Claude", "Gemini", "OpenAI", "Groq", "Meta-Llama"], key="api_choice")
 
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
        value=1024,
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

def generate_and_display(doc_name, prompt_key, prompts, api_choice, model, temperature, max_tokens, top_p, context="individual", **kwargs):
    if prompt_key not in prompts:
        logger.error(f"Prompt '{prompt_key}' not found in loaded prompts.")
        st.error(f"Prompt '{prompt_key}' not found in loaded prompts.")
        return
    
    if doc_name not in st.session_state.planning_docs or st.session_state.regenerate_all:
        initial_prompt = prompts[prompt_key].format(**kwargs)
        logger.info(f"Generating content for {doc_name} using {api_choice} model: {model}")
        response = process_text(initial_prompt, "", api_choice, model, temperature, top_p, max_tokens)
        st.session_state.planning_docs[doc_name] = response
        logger.info(f"Content generated for {doc_name}")

    st.subheader(f"Generated {doc_name.replace('_', ' ').title()}:")
    
    # Display the generated content as text
    st.write(st.session_state.planning_docs[doc_name])

    # Create a unique key for each text area
    unique_key = f"{doc_name}_suggestions_{prompt_key}_{context}"

    user_suggestions = st.text_area(
        f"Suggestions for {doc_name.replace('_', ' ').title()} (optional):",
        height=100,
        key=unique_key
    )

    if st.button(f"Regenerate {doc_name.replace('_', ' ').title()} with Suggestions", key=f"regenerate_{unique_key}"):
        if user_suggestions:
            refined_prompt = f"""
            Original content: {st.session_state.planning_docs[doc_name]}
            
            User suggestions: {user_suggestions}
            
            Please generate an updated version of the {doc_name.replace('_', ' ')} 
            incorporating the user's suggestions while maintaining the overall 
            structure and purpose of the document.
            """
        else:
            refined_prompt = prompts[prompt_key].format(**kwargs)

        logger.info(f"Regenerating content for {doc_name} with user suggestions")
        response = process_text(refined_prompt, "", api_choice, model, temperature, top_p, max_tokens)
        logger.info(f"Processed response for {doc_name}: {response[:100]}...")  # Log first 100 characters
        st.session_state.planning_docs[doc_name] = response
        st.success(f"{doc_name.replace('_', ' ').title()} regenerated with suggestions!")
        st.rerun()

def planning_phase():
    st.title("Planning Phase: New Feature Playground")

    # Initialize session state variables
    if "feature_idea" not in st.session_state:
        st.session_state.feature_idea = ""
    if "competitors" not in st.session_state:
        st.session_state.competitors = ""
    if "target_audience" not in st.session_state:
        st.session_state.target_audience = ""
    if "expected_benefits" not in st.session_state:
        st.session_state.expected_benefits = ""
    if "project_objectives" not in st.session_state:
        st.session_state.project_objectives = ""
    if "timeframe" not in st.session_state:
        st.session_state.timeframe = "6 months"
    if "stakeholders" not in st.session_state:
        st.session_state.stakeholders = ""
    if "potential_risks" not in st.session_state:
        st.session_state.potential_risks = ""
    if "team_size" not in st.session_state:
        st.session_state.team_size = 10

    prompts_path = os.path.join("../resources", "prompts", "pages", "planning_prompts.yaml")
    logger.info(f"Loading prompts from: {prompts_path}")
    prompts = load_prompts(prompts_path)
    
    if not prompts:
        logger.error("Failed to load prompts. Please check the YAML file.")
        st.error("Failed to load prompts. Please check the YAML file.")
        return

    init_session_state("planning_docs", {})
    init_session_state("all_sections_generated", False)
    init_session_state("regenerate_all", False)

    # Load values from the YAML file
    planning_input_data = os.path.join("../resources", "page_auto_inputs", "planning.yaml")
    with open(planning_input_data, 'r', encoding='utf-8') as file:  # Specify encoding
        planning_input_data = yaml.safe_load(file)

    # Initialize session state for user inputs using values from the YAML file
    st.session_state.feature_idea = st.text_area("Describe your feature idea:", 
                                value=st.session_state.feature_idea or planning_input_data.get('idea', ""), 
                                height=150, key="feature_idea_input")
    st.session_state.competitors = st.text_input("List main competitors (comma-separated):", 
                                value=st.session_state.competitors or planning_input_data.get('competitors', ""),
                                key="competitors_input")
    st.session_state.target_audience = st.text_input("Define target audience:", 
                                    value=st.session_state.target_audience or planning_input_data.get('target_audience', ""),
                                    key="target_audience_input")
    st.session_state.expected_benefits = st.text_area("List expected benefits:", 
                                     value=st.session_state.expected_benefits or planning_input_data.get('expected_benefits', ""),
                                     key="expected_benefits_input")
    st.session_state.project_objectives = st.text_area("Define project objectives:", 
                                      value=st.session_state.project_objectives or planning_input_data.get('project_objectives', ""),
                                      key="project_objectives_input")
    st.session_state.timeframe = st.selectbox("Select timeframe:", ["3 months", "6 months", "1 year"], 
                                              index=["3 months", "6 months", "1 year"].index(st.session_state.timeframe) if st.session_state.timeframe else 1,
                                              key="timeframe_input")
    st.session_state.stakeholders = st.text_area("List key stakeholders and their roles:", 
                                value=st.session_state.stakeholders or planning_input_data.get('stakeholders', ""),
                                key="stakeholders_input")
    st.session_state.potential_risks = st.text_area("List potential risks:", 
                                   value=st.session_state.potential_risks or planning_input_data.get('potential_risks', ""),
                                   key="potential_risks_input")
    st.session_state.team_size = st.number_input("Estimated team size:", min_value=1, max_value=100, 
                                                 value=int(st.session_state.team_size) if st.session_state.team_size else 10,
                                                 key="team_size_input")

    # Add model selection to sidebar
    api_choice, model, temperature, max_tokens, top_p = sidebar_model_selection()

    # Now add the "Generate All Sections" button and its logic
    st.header("Generate All Sections")
    if st.button("Generate All Sections Sequentially"):
        st.session_state.regenerate_all = True
        with st.spinner("Generating all sections..."):
            sections = [
                ("feature_proposal", "feature_proposal", {"feature_idea": st.session_state.feature_idea}),
                ("market_analysis", "market_analysis", {"feature_idea": st.session_state.feature_idea, "competitors": st.session_state.competitors}),
                ("business_case", "business_case", {"feature_idea": st.session_state.feature_idea, "target_audience": st.session_state.target_audience, "expected_benefits": st.session_state.expected_benefits}),
                ("project_charter", "project_charter", {"feature_idea": st.session_state.feature_idea, "project_objectives": st.session_state.project_objectives}),
                ("product_roadmap", "product_roadmap", {"feature_idea": st.session_state.feature_idea, "timeframe": st.session_state.timeframe}),
                ("stakeholder_analysis", "stakeholder_analysis", {"stakeholders": st.session_state.stakeholders}),
                ("risk_register", "risk_register", {"potential_risks": st.session_state.potential_risks}),
                ("resource_estimation", "resource_estimation", {"feature_idea": st.session_state.feature_idea, "team_size": st.session_state.team_size})
            ]
            
            for doc_name, prompt_key, kwargs in sections:
                generate_and_display(doc_name, prompt_key, prompts, api_choice, model, temperature, max_tokens, top_p, context="all", **kwargs)
                st.success(f"{doc_name.replace('_', ' ').title()} generated!")
        
        st.session_state.all_sections_generated = True
        st.session_state.regenerate_all = False
        st.success("All sections have been generated!")
        st.rerun()

    # Only show individual section buttons if all sections haven't been generated
    if not st.session_state.all_sections_generated:
        sections = [
            ("1. Feature Ideation", "feature_proposal", "feature_proposal", {"feature_idea": st.session_state.feature_idea}),
            ("2. Market Research", "market_analysis", "market_analysis", {"feature_idea": st.session_state.feature_idea, "competitors": st.session_state.competitors}),
            ("3. Business Case Development", "business_case", "business_case", {"feature_idea": st.session_state.feature_idea, "target_audience": st.session_state.target_audience, "expected_benefits": st.session_state.expected_benefits}),
            ("4. Project Charter", "project_charter", "project_charter", {"feature_idea": st.session_state.feature_idea, "project_objectives": st.session_state.project_objectives}),
            ("5. High-level Product Roadmap", "product_roadmap", "product_roadmap", {"feature_idea": st.session_state.feature_idea, "timeframe": st.session_state.timeframe}),
            ("6. Stakeholder Analysis", "stakeholder_analysis", "stakeholder_analysis", {"stakeholders": st.session_state.stakeholders}),
            ("7. Initial Risk Assessment", "risk_register", "risk_register", {"potential_risks": st.session_state.potential_risks}),
            ("8. Resource Estimation", "resource_estimation", "resource_estimation", {"feature_idea": st.session_state.feature_idea, "team_size": st.session_state.team_size})
        ]

        for header, doc_name, prompt_key, kwargs in sections:
            st.header(header)
            if st.button(f"Generate {doc_name.replace('_', ' ').title()}") or doc_name in st.session_state.planning_docs:
                generate_and_display(doc_name, prompt_key, prompts, api_choice, model, temperature, max_tokens, top_p, **kwargs)

    st.header("Review and Finalize")
    if st.button("Review All Documents"):
        full_content = ""
        for doc_name, content in st.session_state.planning_docs.items():
            st.subheader(doc_name.replace("_", " ").title())
            st.write(content)
            full_content += f"\n\n{doc_name.replace('_', ' ').title()}:\n{content}"
            st.markdown("---")
        
        # Add a single "Copy to Clipboard" button for all documents
        if st.button("Copy All to Clipboard"):
            pyperclip.copy(full_content)
            st.success("All documents copied to clipboard!")

    if st.button("Finalize Planning Phase"):
        logger.info("Planning phase completed. All documents have been saved.")
        st.success("Planning phase completed! All documents have been saved.")

    # Add a button to reset the process
    if st.button("Reset Planning Phase"):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.rerun()

def main():
    logger.info("Starting the Planning Phase application")
    planning_phase()

if __name__ == "__main__":
    main()