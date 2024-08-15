import streamlit as st
import yaml
import os
from utils.llm_utils import get_llm_client, process_text
from utils.streamlit_utils import init_session_state
import utils.prompt_utils as prompt_utils
from utils.logger import setup_logger
from dotenv import load_dotenv
from utils.cloud_arch_diagram_ import generate_cloud_architecture_diagram

# Load environment variables and set up logger
load_dotenv()
logger = setup_logger()

@st.cache_data
def load_prompts(file_path):
    try:
        prompts = prompt_utils.load_prompts(file_path)
        logger.info(f"Successfully loaded prompts from {file_path}")
        return prompts
    except Exception as e:
        logger.error(f"Failed to load prompts from {file_path}: {str(e)}")
        st.error(f"Failed to load prompts from {file_path}: {str(e)}")
        return None

def sidebar_model_selection():
    st.sidebar.header("Model Selection")
    api_choice = st.sidebar.selectbox("Choose API:", ["Groq", "Gemini", "OpenAI", "Claude", "Meta-Llama"], key="api_choice")
 
    model_options = {
        "Groq": ["llama-3.1-70b-versatile", "llama-3.1-8b-instant", "llama3-70b-8192", "llama3-8b-8192", "mixtral-8x7b-32768", "gemma-7b-it", "gemma2-9b-it"],
        "Gemini": ["gemini-1.5-flash", "gemini-1.5-pro"],
        "OpenAI": ["gpt-4o", "gpt-4o-mini", "gpt-4-turbo"],
        "Claude": ["claude-3-opus-20240229", "claude-3-sonnet-20240229", "claude-3-haiku-20240307"],
        "Meta-Llama": ["meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo", "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo", "meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo"]
    }

    model = st.sidebar.selectbox("Choose model:", model_options[api_choice], key="model")
    
    temperature = st.sidebar.slider("Temperature:", min_value=0.0, max_value=1.0, value=0.7, step=0.1, key="temperature")
    max_tokens = st.sidebar.slider("Max Tokens:", min_value=100, max_value=8192, value=1024, key="max_tokens")
    top_p = st.sidebar.slider("Top P:", min_value=0.0, max_value=1.0, value=0.95, step=0.01, key="top_p")
    
    return api_choice, model, temperature, max_tokens, top_p

def generate_and_display(design_component, prompts, api_choice, model, temperature, max_tokens, top_p, context, **kwargs):
    if design_component not in prompts:
        logger.error(f"Prompt '{design_component}' not found in loaded prompts.")
        st.error(f"Prompt '{design_component}' not found in loaded prompts.")
        return
    
    try:
        # Add feature_name and context to kwargs
        kwargs['feature_name'] = st.session_state.feature_name
        kwargs['context'] = context
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

def system_architecture():
    st.header("System Architecture Design")
    st.write("This section outlines the overall structure of the system.")
    
    if st.button("Generate System Architecture"):
        with st.spinner("Generating System Architecture..."):
            # Generate text content
            generate_and_display("system_architecture", prompts, api_choice, model, temperature, max_tokens, top_p, context)
            
            # Generate cloud architecture diagram
            '''
            before generating the diagram we need to process the text first.
            we need to extract the text and break it down into components.
            then we need to call claude anthropic opus (complex task) to break down system architecture in a language
            that is in the language of the diagram in order for eraser io to understand it.
            
            we need to load llama index vector store with the eraser io knowledge base.
            then we need to feed the system architecture text to the llama index vector store.
            along with the text we need to ask the llm to create a system cloud architecture
            using the eraser io language. 
            
            get three responses, 1 for each cloud provider (aws, azure, gcp).
            
            if this doesnt work then we will use a combination of crewai agents and load them with the expected structure and data to use.
            the token size will be large there for try to use gemini flash because they can handle a large token size.
            
            '''
            try:
                diagram_path = generate_cloud_architecture_diagram(
                    st.session_state.feature_name,
                    additional_context=st.session_state.design_docs.get("system_architecture", "")
                )
                st.success("Cloud Architecture Diagram generated successfully!")
                st.image(diagram_path, caption="Cloud Architecture Diagram", use_column_width=True)
                st.session_state.design_docs["system_architecture_diagram"] = diagram_path
            except Exception as e:
                st.error(f"Failed to generate Cloud Architecture Diagram: {str(e)}")

    if "system_architecture" in st.session_state.design_docs:
        st.subheader("Generated System Architecture Description:")
        st.write(st.session_state.design_docs["system_architecture"])

    if "system_architecture_diagram" in st.session_state.design_docs:
        st.subheader("Generated Cloud Architecture Diagram:")
        st.image(st.session_state.design_docs["system_architecture_diagram"], caption="Cloud Architecture Diagram", use_column_width=True)

    user_suggestions = st.text_area("Suggestions for System Architecture (optional):", height=100)

    if st.button("Regenerate System Architecture with Suggestions"):
        with st.spinner("Regenerating System Architecture..."):
            regenerate_with_suggestions("system_architecture", user_suggestions, prompts, api_choice, model, temperature, max_tokens, top_p, context)
            
            # Regenerate cloud architecture diagram
            try:
                diagram_path = generate_cloud_architecture_diagram(
                    st.session_state.feature_name,
                    additional_context=st.session_state.design_docs.get("system_architecture", "")
                )
                st.success("Cloud Architecture Diagram regenerated successfully!")
                st.session_state.design_docs["system_architecture_diagram"] = diagram_path
                st.image(diagram_path, caption="Regenerated Cloud Architecture Diagram", use_column_width=True)
            except Exception as e:
                st.error(f"Failed to regenerate Cloud Architecture Diagram: {str(e)}")

def database_design():
    st.header("Database Design")
    st.write("This section details the database structure and relationships.")
    if st.button("Generate Database Design"):
        generate_and_display("database_design", prompts, api_choice, model, temperature, max_tokens, top_p, context)

def user_interface_design():
    st.header("User Interface Design")
    st.write("This section describes the user interface layout and interactions.")
    if st.button("Generate User Interface Design"):
        generate_and_display("user_interface_design", prompts, api_choice, model, temperature, max_tokens, top_p, context)

def api_design():
    st.header("API Design")
    st.write("This section outlines the API structure and endpoints.")
    if st.button("Generate API Design"):
        generate_and_display("api_design", prompts, api_choice, model, temperature, max_tokens, top_p, context)

def sequence_diagrams():
    st.header("Sequence Diagrams")
    st.write("This section provides sequence diagrams for key processes.")
    if st.button("Generate Sequence Diagrams"):
        generate_and_display("sequence_diagrams", prompts, api_choice, model, temperature, max_tokens, top_p, context)

def security_design():
    st.header("Security Design")
    st.write("This section outlines the security measures and considerations.")
    if st.button("Generate Security Design"):
        generate_and_display("security_design", prompts, api_choice, model, temperature, max_tokens, top_p, context)

def performance_considerations():
    st.header("Performance Considerations")
    st.write("This section discusses performance optimization strategies.")
    if st.button("Generate Performance Considerations"):
        generate_and_display("performance_considerations", prompts, api_choice, model, temperature, max_tokens, top_p, context)

def testing_strategy():
    st.header("Testing Strategy")
    st.write("This section outlines the approach for testing the feature.")
    if st.button("Generate Testing Strategy"):
        generate_and_display("testing_strategy", prompts, api_choice, model, temperature, max_tokens, top_p, context)

def design_review():
    st.header("Design Review and Approval")
    st.write("This section provides a summary and approval process for the design.")
    if st.button("Generate Design Review"):
        generate_and_display("design_review", prompts, api_choice, model, temperature, max_tokens, top_p, context)

def is_component_generated(component_name):
    return component_name in st.session_state.design_docs and st.session_state.design_docs[component_name]

def update_progress(design_components):
    total_components = len(design_components)
    completed_components = sum(1 for component in design_components if is_component_generated(component.__name__))
    progress = completed_components / total_components
    st.sidebar.progress(progress)
    st.sidebar.text(f"Progress: {completed_components}/{total_components} components completed")

    # Detailed component status
    st.sidebar.header("Design Progress")
    for component in design_components:
        component_name = component.__name__
        if is_component_generated(component_name):
            st.sidebar.success(f"✅ {component_name.replace('_', ' ').title()}")
        else:
            st.sidebar.error(f"❌ {component_name.replace('_', ' ').title()}")

def main():
    st.title("Design Phase")
    st.write("Welcome to the Design Phase. We'll create detailed design specifications based on the planning and requirements phases.")

    # Set the feature_name
    st.session_state.feature_name = st.session_state.get("feature_name", "AI-driven personalized investment portfolio rebalancing")

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
    
    # Combine context
    context = "Planning Phase Summary:\n"
    for doc_name, content in planning_docs.items():
        context += f"{doc_name.replace('_', ' ').title()}:\n{content}\n\n"
    
    context += "Requirements Phase Summary:\n"
    for req_type, content in requirements.items():
        context += f"{req_type.replace('_', ' ').title()}:\n{content}\n\n"

    # Display context in sidebar
    st.sidebar.header("Context from Previous Phases")
    with st.sidebar.expander("View Context"):
        st.write(context)

    design_components = [
        system_architecture, database_design, user_interface_design,
        api_design, sequence_diagrams, security_design, performance_considerations,
        testing_strategy, design_review
    ]

    init_session_state("design_docs", {component.__name__: "" for component in design_components})

    api_choice, model, temperature, max_tokens, top_p = sidebar_model_selection()

    # Individual section generation
    for component in design_components:
        with st.expander(component.__name__.replace("_", " ").title()):
            if not is_component_generated(component.__name__):
                st.write(f"Click the button below to generate content for {component.__name__.replace('_', ' ').title()}")
                if st.button(
                    f"Generate {component.__name__.replace('_', ' ').title()}",
                    key=f"generate_{component.__name__}",
                    help=f"Click to generate content for the {component.__name__.replace('_', ' ').title()} section using AI."
                ):
                    with st.spinner(f"Generating {component.__name__.replace('_', ' ').title()}..."):
                        generate_and_display(component.__name__, prompts, api_choice, model, temperature, max_tokens, top_p, context)
                    update_progress(design_components)
            else:
                st.write(st.session_state.design_docs[component.__name__])
                if st.button(
                    f"Regenerate {component.__name__.replace('_', ' ').title()}",
                    key=f"regenerate_{component.__name__}",
                    help=f"Click to regenerate content for the {component.__name__.replace('_', ' ').title()} section. This will overwrite the existing content."
                ):
                    with st.spinner(f"Regenerating {component.__name__.replace('_', ' ').title()}..."):
                        generate_and_display(component.__name__, prompts, api_choice, model, temperature, max_tokens, top_p, context)
                    update_progress(design_components)

    st.header("Review and Finalize")
    
    # Review All Design Components
    if st.button(
        "Review All Design Components",
        help="Click to view all generated design components in one place."
    ):
        generated_components = [comp for comp in design_components if is_component_generated(comp.__name__)]
        if not generated_components:
            st.warning("No design components have been generated yet.")
        else:
            for component in generated_components:
                st.subheader(component.__name__.replace("_", " ").title())
                st.write(st.session_state.design_docs[component.__name__])
                st.markdown("---")

    # Finalize Design Phase
    if st.button(
        "Finalize Design Phase",
        help="Click when you're satisfied with all generated components to mark the design phase as complete."
    ):
        generated_components = [comp for comp in design_components if is_component_generated(comp.__name__)]
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
    generated_components = [comp for comp in design_components if is_component_generated(comp.__name__)]
    if generated_components:
        design_doc = "# Design Document\n\n"
        design_doc += "\n\n".join([f"## {comp.__name__.replace('_', ' ').title()}\n\n{st.session_state.design_docs[comp.__name__]}" for comp in generated_components])
        
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

    update_progress(design_components)  # Final update to ensure sidebar is current

if __name__ == "__main__":
    main()