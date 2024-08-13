import streamlit as st
import yaml
import os
import google.generativeai as genai
from utils.llm_utils import get_llm_client, process_text
from utils.streamlit_utils import init_session_state
import utils.prompt_utils as prompt_utils
from utils.logger import setup_logger
from dotenv import load_dotenv

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
    api_choice = st.sidebar.selectbox("Choose API:", ["Groq", "Gemini", "OpenAI", "Claude", "Meta-Llama"])
 
    if api_choice == "Groq":
        model = st.sidebar.selectbox("Choose model:", [
            "llama-3.1-70b-versatile",
            "llama-3.1-8b-instant",
            "llama3-70b-8192",
            "llama3-8b-8192",
            "mixtral-8x7b-32768",
            "gemma-7b-it",
            "gemma2-9b-it"
        ])
    elif api_choice == "Gemini":
        model = st.sidebar.selectbox("Choose model:", [
            "gemini-1.5-flash",
            "gemini-1.5-pro"
        ])
    elif api_choice == "OpenAI":
        model = st.sidebar.selectbox("Choose model:", [
            "gpt-4o",
            "gpt-4o-mini",
            "gpt-4-turbo",
        ])
    elif api_choice == "Claude":
        model = st.sidebar.selectbox("Choose model:", [
            "claude-3-opus-20240229",
            "claude-3-sonnet-20240229",
            "claude-3-haiku-20240307"
   
        ])
    elif api_choice == "Meta-Llama":
        model = st.sidebar.radio("Choose Meta-Llama Model:", (
            "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
            "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
            "meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo"
        ))
        
    
    temperature = st.sidebar.slider("Temperature:", min_value=0.0, max_value=1.0, value=0.7, step=0.1)
    max_tokens = st.sidebar.slider("Max Tokens:", min_value=100, max_value=8192, value=1024)
    top_p = st.sidebar.slider("Top P:", min_value=0.0, max_value=1.0, value=0.95, step=0.01)
    
    logger.info(f"Selected API: {api_choice}, Model: {model}, Temperature: {temperature}, Max Tokens: {max_tokens}, Top P: {top_p}")
    return api_choice, model, temperature, max_tokens, top_p

def generate_and_display(doc_name, prompt_key, prompts, api_choice, model, temperature, max_tokens, top_p, context="individual", **kwargs):
    if prompt_key not in prompts:
        logger.error(f"Prompt '{prompt_key}' not found in loaded prompts.")
        st.error(f"Prompt '{prompt_key}' not found in loaded prompts.")
        return
    
    if doc_name not in st.session_state.planning_docs:
        initial_prompt = prompts[prompt_key].format(**kwargs)
        logger.info(f"Generating content for {doc_name} using {api_choice} model: {model}")
        response = process_text(initial_prompt, "", api_choice, model, temperature, top_p, max_tokens)
        st.session_state.planning_docs[doc_name] = response
        logger.info(f"Content generated for {doc_name}")

    st.subheader(f"Generated {doc_name.replace('_', ' ').title()}:")
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

    prompts_path = os.path.join("../resources", "prompts", "pages", "planning_prompts.yaml")
    logger.info(f"Loading prompts from: {prompts_path}")
    prompts = load_prompts(prompts_path)
    
    if not prompts:
        logger.error("Failed to load prompts. Please check the YAML file.")
        st.error("Failed to load prompts. Please check the YAML file.")
        return

    init_session_state("planning_docs", {})
    init_session_state("all_sections_generated", False)

    # Add model selection to sidebar
    api_choice, model, temperature, max_tokens, top_p = sidebar_model_selection()

    # Define all input variables first
    feature_idea = st.text_area("Describe your feature idea:", 
                                value="AI-driven personalized investment portfolio rebalancing for our wealth management platform", 
                                height=150)
    competitors = st.text_input("List main competitors (comma-separated):", 
                                value="Charles Schwab, Fidelity Investments, Vanguard, Merrill Lynch")
    target_audience = st.text_input("Define target audience:", 
                                    value="High-net-worth individuals aged 35-65, small business owners, and retirees seeking personalized wealth management")
    expected_benefits = st.text_area("List expected benefits:", 
                                     value="Improved portfolio performance, increased client satisfaction, reduced manual workload for financial advisors, competitive edge in personalized wealth management, potential to attract younger tech-savvy clients")
    project_objectives = st.text_area("Define project objectives:", 
                                      value="Develop an AI algorithm for personalized portfolio rebalancing, integrate with existing wealth management platform, ensure compliance with financial regulations, create intuitive interfaces for both clients and financial advisors")
    timeframe = st.selectbox("Select timeframe:", ["3 months", "6 months", "1 year"], index=1)
    stakeholders = st.text_area("List key stakeholders and their roles:", 
                                value="CIO (project sponsor), Head of Wealth Management (project lead), Lead Financial Advisor, Data Scientist, UI/UX Designer, Backend Developer, Compliance Officer, Marketing Director, Client Relations Manager")
    potential_risks = st.text_area("List potential risks:", 
                                   value="Regulatory compliance issues, data security and privacy concerns, resistance from traditional financial advisors, client trust in AI-driven recommendations, integration challenges with legacy systems, market volatility impacting AI performance")
    team_size = st.number_input("Estimated team size:", min_value=1, max_value=100, value=10)

    # Now add the "Generate All Sections" button and its logic
    st.header("Generate All Sections")
    if st.button("Generate All Sections Sequentially"):
        with st.spinner("Generating all sections..."):
            sections = [
                ("feature_proposal", "feature_proposal", {"feature_idea": feature_idea}),
                ("market_analysis", "market_analysis", {"feature_idea": feature_idea, "competitors": competitors}),
                ("business_case", "business_case", {"feature_idea": feature_idea, "target_audience": target_audience, "expected_benefits": expected_benefits}),
                ("project_charter", "project_charter", {"feature_idea": feature_idea, "project_objectives": project_objectives}),
                ("product_roadmap", "product_roadmap", {"feature_idea": feature_idea, "timeframe": timeframe}),
                ("stakeholder_analysis", "stakeholder_analysis", {"stakeholders": stakeholders}),
                ("risk_register", "risk_register", {"potential_risks": potential_risks}),
                ("resource_estimation", "resource_estimation", {"feature_idea": feature_idea, "team_size": team_size})
            ]
            
            for doc_name, prompt_key, kwargs in sections:
                generate_and_display(doc_name, prompt_key, prompts, api_choice, model, temperature, max_tokens, top_p, context="all", **kwargs)
                st.success(f"{doc_name.replace('_', ' ').title()} generated!")
        
        st.session_state.all_sections_generated = True
        st.success("All sections have been generated!")

    # Only show individual section buttons if all sections haven't been generated
    if not st.session_state.all_sections_generated:
        st.header("1. Feature Ideation")
        if st.button("Generate Feature Proposal") or "feature_proposal" in st.session_state.planning_docs:
            generate_and_display("feature_proposal", "feature_proposal", prompts, api_choice, model, temperature, max_tokens, top_p, feature_idea=feature_idea)

        st.header("2. Market Research")
        if st.button("Conduct Market Analysis") or "market_analysis" in st.session_state.planning_docs:
            generate_and_display("market_analysis", "market_analysis", prompts, api_choice, model, temperature, max_tokens, top_p, feature_idea=feature_idea, competitors=competitors)

        st.header("3. Business Case Development")
        if st.button("Generate Business Case") or "business_case" in st.session_state.planning_docs:
            generate_and_display("business_case", "business_case", prompts, api_choice, model, temperature, max_tokens, top_p, feature_idea=feature_idea, target_audience=target_audience, expected_benefits=expected_benefits)

        st.header("4. Project Charter")
        if st.button("Create Project Charter") or "project_charter" in st.session_state.planning_docs:
            generate_and_display("project_charter", "project_charter", prompts, api_choice, model, temperature, max_tokens, top_p, 
                                 feature_idea=feature_idea, 
                                 project_objectives=project_objectives)  

        st.header("5. High-level Product Roadmap")
        if st.button("Generate Product Roadmap") or "product_roadmap" in st.session_state.planning_docs:
            generate_and_display("product_roadmap", "product_roadmap", prompts, api_choice, model, temperature, max_tokens, top_p, 
                                 feature_idea=feature_idea, 
                                 timeframe=timeframe)
            
        st.header("6. Stakeholder Analysis")
        if st.button("Perform Stakeholder Analysis") or "stakeholder_analysis" in st.session_state.planning_docs:
            generate_and_display("stakeholder_analysis", "stakeholder_analysis", prompts, api_choice, model, temperature, max_tokens, top_p, 
                                 stakeholders=stakeholders)

        st.header("7. Initial Risk Assessment")
        if st.button("Generate Risk Register") or "risk_register" in st.session_state.planning_docs:
            generate_and_display("risk_register", "risk_register", prompts, api_choice, model, temperature, max_tokens, top_p, 
                                 potential_risks=potential_risks)

        st.header("8. Resource Estimation")
        if st.button("Estimate Resources") or "resource_estimation" in st.session_state.planning_docs:
            generate_and_display("resource_estimation", "resource_estimation", prompts, api_choice, model, temperature, max_tokens, top_p, feature_idea=feature_idea, team_size=team_size)

    st.header("Review and Finalize")
    if st.button("Review All Documents"):
        for doc_name, content in st.session_state.planning_docs.items():
            st.subheader(doc_name.replace("_", " ").title())
            st.write(content)
            st.markdown("---")

    if st.button("Finalize Planning Phase"):
        logger.info("Planning phase completed. All documents have been saved.")
        st.success("Planning phase completed! All documents have been saved.")

    # Add a button to reset the process
    if st.button("Reset Planning Phase"):
        st.session_state.planning_docs = {}
        st.session_state.all_sections_generated = False
        st.rerun()

def main():
    logger.info("Starting the Planning Phase application")
    planning_phase()

if __name__ == "__main__":
    main()
