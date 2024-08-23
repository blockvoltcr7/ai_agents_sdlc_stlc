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
    output_dir = "../demo/Design_phase_output"
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, f"{doc_name}.md")
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)
    logger.info(f"Written {doc_name} to {file_path}")

def generate_and_display(design_component, prompts, api_choice, model, temperature, max_tokens, top_p, context, **kwargs):
    if design_component not in prompts:
        logger.error(f"Prompt '{design_component}' not found in loaded prompts.")
        st.error(f"Prompt '{design_component}' not found in loaded prompts.")
        return
    
    try:
        initial_prompt = prompts[design_component]["prompt"].format(**kwargs)
    except KeyError as e:
        logger.error(f"Missing key in prompt formatting for {design_component}: {e}")
        st.error(f"An error occurred while formatting the prompt for {design_component}: missing key {e}")
        return
    except Exception as e:
        logger.error(f"Unexpected error in prompt formatting for {design_component}: {e}")
        st.error(f"An unexpected error occurred while formatting the prompt for {design_component}: {e}")
        return
    
    logger.info(f"Generating content for {design_component} using {api_choice} model: {model}")
    
    try:
        with st.spinner(f"Generating {design_component.replace('_', ' ').title()}..."):
            response = process_text(initial_prompt, context, api_choice, model, temperature, top_p, max_tokens)
        if not response:
            raise ValueError("Empty response received from the model")
        st.session_state.design_docs[design_component] = response
        logger.info(f"Content generated for {design_component}")
        st.success(f"{design_component.replace('_', ' ').title()} generated successfully!")
    except Exception as e:
        logger.error(f"Error generating content for {design_component}: {e}")
        st.error(f"An error occurred while generating content for {design_component}: {e}")
        return

    st.subheader(f"Generated {design_component.replace('_', ' ').title()}:")
    st.write(st.session_state.design_docs[design_component])

    # Write the content to a markdown file
    write_to_markdown(design_component, st.session_state.design_docs[design_component])

    user_suggestions = st.text_area(f"Suggestions for {design_component.replace('_', ' ').title()} (optional):", height=100)

    if st.button(f"Regenerate {design_component.replace('_', ' ').title()} with Suggestions"):
        regenerate_with_suggestions(design_component, user_suggestions, prompts, api_choice, model, temperature, max_tokens, top_p, context, **kwargs)

def regenerate_with_suggestions(design_component, user_suggestions, prompts, api_choice, model, temperature, max_tokens, top_p, context, **kwargs):
    try:
        if user_suggestions:
            refined_prompt = f"""
            Original content: {st.session_state.design_docs[design_component]}
            
            User suggestions: {user_suggestions}
            
            Please generate an updated version of the {design_component.replace('_', ' ')} 
            incorporating the user's suggestions while maintaining the overall 
            structure and purpose of the document.
            """
        else:
            refined_prompt = prompts[design_component]["prompt"].format(**kwargs)

        logger.info(f"Regenerating content for {design_component} with user suggestions")
        with st.spinner(f"Regenerating {design_component.replace('_', ' ').title()}..."):
            response = process_text(refined_prompt, context, api_choice, model, temperature, top_p, max_tokens)
        if not response:
            raise ValueError("Empty response received from the model during regeneration")
        st.session_state.design_docs[design_component] = response
        st.success(f"{design_component.replace('_', ' ').title()} regenerated with suggestions!")
        st.rerun()
    except Exception as e:
        logger.error(f"Error regenerating content for {design_component}: {e}")
        st.error(f"An error occurred while regenerating content for {design_component}: {e}")

def main():
    st.title("Design Phase")
    st.write("Welcome to the Design Phase. We'll create detailed design specifications based on the planning and requirements phases.")

    # Set the feature_name
    st.session_state.feature_name = st.session_state.get("feature_name", "Microservice API for Portfolio Benchmark Analysis using BlackRock Aladdin")

    st.info("""
    Instructions:
    1. Review the context from previous phases in the sidebar.
    2. Use the sidebar to select your preferred AI model and parameters.
    3. Expand each design component section and click 'Generate' to create content for that specific component.
    4. Review and modify the generated content as needed.
    5. Use the 'Review All Design Components' button to see all generated content.
    6. When satisfied, click 'Finalize Design Phase' to complete this stage.
    7. You can download the completed design document at any time.
    """)

    global prompts, api_choice, model, temperature, max_tokens, top_p
    prompts_path = os.path.join("../resources", "prompts", "pages", "design_prompts.yaml")
    prompts = load_prompts(prompts_path)
    
    if not prompts:
        st.error("Failed to load prompts. Please check the console and log for detailed error messages.")
        return

    # Display all prompts
    st.header("Loaded Prompts")
    with st.expander("View All Prompts"):
        for key, value in prompts.items():
            st.subheader(key)
            st.write(value)

    # Load context from previous phases
    planning_docs = st.session_state.get("planning_docs", {})
    requirements = st.session_state.get("requirements", {})
    
    # Create specific contexts for different design components
    contexts = {
        "system_architecture": " ".join([
            planning_docs.get("feature_proposal", ""),
            planning_docs.get("project_charter", ""),
            planning_docs.get("product_roadmap", ""),
            requirements.get("functional_requirements", ""),
            requirements.get("non_functional_requirements", ""),
            requirements.get("technical_requirements", "")
        ]),
        "database_design": " ".join([
            planning_docs.get("feature_proposal", ""),
            requirements.get("functional_requirements", ""),
            requirements.get("data_requirements", ""),
            requirements.get("security_requirements", "")
        ]),
        "user_interface_design": " ".join([
            planning_docs.get("feature_proposal", ""),
            planning_docs.get("market_analysis", ""),
            requirements.get("user_interface_requirements", ""),
            requirements.get("functional_requirements", ""),
            requirements.get("non_functional_requirements", "")
        ]),
        "api_design": " ".join([
            planning_docs.get("feature_proposal", ""),
            planning_docs.get("product_roadmap", ""),
            requirements.get("functional_requirements", ""),
            requirements.get("technical_requirements", ""),
            requirements.get("performance_requirements", "")
        ]),
        "sequence_diagrams": " ".join([
            planning_docs.get("feature_proposal", ""),
            requirements.get("functional_requirements", ""),
            requirements.get("technical_requirements", "")
        ]),
        "security_design": " ".join([
            planning_docs.get("risk_register", ""),
            requirements.get("security_requirements", ""),
            requirements.get("non_functional_requirements", "")
        ]),
        "performance_considerations": " ".join([
            planning_docs.get("market_analysis", ""),
            planning_docs.get("product_roadmap", ""),
            requirements.get("performance_requirements", ""),
            requirements.get("non_functional_requirements", "")
        ]),
        "testing_strategy": " ".join([
            planning_docs.get("risk_register", ""),
            planning_docs.get("project_charter", ""),
            requirements.get("functional_requirements", ""),
            requirements.get("non_functional_requirements", ""),
            requirements.get("technical_requirements", ""),
            requirements.get("user_interface_requirements", ""),
            requirements.get("security_requirements", ""),
            requirements.get("performance_requirements", "")
        ]),
        "design_review": " ".join([
            planning_docs.get("feature_proposal", ""),
            planning_docs.get("market_analysis", ""),
            planning_docs.get("project_charter", ""),
            planning_docs.get("product_roadmap", ""),
            planning_docs.get("risk_register", ""),
            requirements.get("functional_requirements", ""),
            requirements.get("non_functional_requirements", ""),
            requirements.get("technical_requirements", ""),
            requirements.get("user_interface_requirements", ""),
            requirements.get("security_requirements", ""),
            requirements.get("performance_requirements", "")
        ])
    }

    # Display context in sidebar
    st.sidebar.header("Context from Previous Phases")
    with st.sidebar.expander("View Context"):
        for key, value in contexts.items():
            st.subheader(key.replace("_", " ").title())
            st.write(value)

    design_components = [
        "system_architecture", "database_design", "user_interface_design",
        "api_design", "sequence_diagrams", "security_design", "performance_considerations",
        "testing_strategy", "design_review"
    ]

    init_session_state("design_docs", {component: "" for component in design_components})

    api_choice, model, temperature, max_tokens, top_p = sidebar_model_selection()

    # Individual section generation
    for component in design_components:
        with st.expander(component.replace("_", " ").title()):
            if not st.session_state.design_docs[component]:
                st.write(f"Click the button below to generate content for {component.replace('_', ' ').title()}")
                if st.button(
                    f"Generate {component.replace('_', ' ').title()}",
                    key=f"generate_{component}",
                    help=f"Click to generate content for the {component.replace('_', ' ').title()} section using AI."
                ):
                    with st.spinner(f"Generating {component.replace('_', ' ').title()}..."):
                        generate_and_display(component, prompts, api_choice, model, temperature, max_tokens, top_p, contexts[component])
            else:
                st.write(st.session_state.design_docs[component])
                if st.button(
                    f"Regenerate {component.replace('_', ' ').title()}",
                    key=f"regenerate_{component}",
                    help=f"Click to regenerate content for the {component.replace('_', ' ').title()} section. This will overwrite the existing content."
                ):
                    with st.spinner(f"Regenerating {component.replace('_', ' ').title()}..."):
                        generate_and_display(component, prompts, api_choice, model, temperature, max_tokens, top_p, contexts[component])

    st.header("Review and Finalize")
    
    # Review All Design Components
    if st.button(
        "Review All Design Components",
        help="Click to view all generated design components in one place."
    ):
        generated_components = [comp for comp in design_components if st.session_state.design_docs[comp]]
        if not generated_components:
            st.warning("No design components have been generated yet.")
        else:
            for component in generated_components:
                st.subheader(component.replace("_", " ").title())
                st.write(st.session_state.design_docs[component])
                st.markdown("---")

    # Finalize Design Phase
    if st.button(
        "Finalize Design Phase",
        help="Click when you're satisfied with all generated components to mark the design phase as complete."
    ):
        generated_components = [comp for comp in design_components if st.session_state.design_docs[comp]]
        if not generated_components:
            st.warning("Please generate at least one design component before finalizing.")
        elif len(generated_components) < len(design_components):
            st.warning("Not all components have been generated. Are you sure you want to finalize?")
            if st.button("Yes, finalize with incomplete components"):
                logger.info("Design phase completed with incomplete components.")
                st.success("Design phase completed! All generated documents have been saved.")
        else:
            logger.info("Design phase completed. All documents have been saved.")
            st.success("Design phase completed! All documents have been saved.")

    # Download Design Document
    generated_components = [comp for comp in design_components if st.session_state.design_docs[comp]]
    if generated_components:
        design_doc = "# Design Document\n\n"
        design_doc += "\n\n".join([f"## {comp.replace('_', ' ').title()}\n\n{st.session_state.design_docs[comp]}" for comp in generated_components])
        
        st.download_button(
            label="Download Design Document",
            data=design_doc,
            file_name="design_document.md",
            mime="text/markdown",
            key="download_design_doc",
            help="Click to download all generated design components as a single markdown document."
        )
    else:
        st.warning("Generate at least one design component before downloading the document.")

    # Reset Design Phase
    if st.button(
        "Reset Design Phase",
        help="Click to clear all generated content and start the design phase from scratch. Use with caution!"
    ):
        if st.confirm("Are you sure you want to reset the Design Phase? All generated content will be lost."):
            for key in list(st.session_state.keys()):
                if key.startswith("design"):
                    del st.session_state[key]
            st.success("Design Phase has been reset.")
            st.rerun()

if __name__ == "__main__":
    main()