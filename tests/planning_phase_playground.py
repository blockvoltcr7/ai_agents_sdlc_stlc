import streamlit as st
from utils.groq_utils import get_groq_client, get_groq_response
from utils.streamlit_utils import init_session_state

def planning_phase():
    """
    This function defines the planning phase of a new feature development project in a wealth management platform.
    It guides the user through various steps including feature ideation, market research, business case development, 
    project charter creation, product roadmap generation, stakeholder analysis, risk assessment, and resource estimation.
    Each step generates a corresponding document based on user inputs and stores it in the session state.
    """

    # Set the title of the Streamlit app
    st.title("Planning Phase: New Feature Playground")

    # Initialize session state for storing generated documents
    init_session_state("planning_docs", {})

    def generate_and_display(doc_name, initial_prompt):
        """
        Generates a document based on the provided prompt, stores it in the session state, 
        and displays the result in the Streamlit app. Allows users to provide feedback and regenerate 
        the document based on their suggestions.

        Parameters:
        - doc_name (str): The name of the document to be generated.
        - initial_prompt (str): The prompt used to generate the document.
        """
        if doc_name not in st.session_state.planning_docs:
            response = get_groq_response(get_groq_client(), [{"role": "user", "content": initial_prompt}])
            st.session_state.planning_docs[doc_name] = response

        st.subheader(f"Generated {doc_name.replace('_', ' ').title()}:")
        st.write(st.session_state.planning_docs[doc_name])

        # User input for suggestions to refine the document
        user_suggestions = st.text_area(
            f"Suggestions for {doc_name.replace('_', ' ').title()} (optional):",
            height=100,
            key=f"{doc_name}_suggestions"
        )

        # Regenerate document based on user suggestions
        if st.button(f"Regenerate {doc_name.replace('_', ' ').title()} with Suggestions"):
            if user_suggestions:
                refined_prompt = f"""
                Original content: {st.session_state.planning_docs[doc_name]}
                
                User suggestions: {user_suggestions}
                
                Please generate an updated version of the {doc_name.replace('_', ' ')} 
                incorporating the user's suggestions while maintaining the overall 
                structure and purpose of the document.
                """
            else:
                refined_prompt = initial_prompt

            response = get_groq_response(get_groq_client(), [{"role": "user", "content": refined_prompt}])
            st.session_state.planning_docs[doc_name] = response
            st.success(f"{doc_name.replace('_', ' ').title()} regenerated with suggestions!")
            st.rerun()  # This line has been updated

    # Feature Ideation Section
    st.header("1. Feature Ideation")
    feature_idea = st.text_area("Describe your feature idea:", 
                                value="AI-driven personalized investment portfolio rebalancing for our wealth management platform", 
                                height=150)
    if st.button("Generate Feature Proposal") or "feature_proposal" in st.session_state.planning_docs:
        prompt = f"Based on this feature idea: {feature_idea}, generate a comprehensive feature proposal document for a wealth management firm like Edward Jones."
        generate_and_display("feature_proposal", prompt)

    # Market Research Section
    st.header("2. Market Research")
    competitors = st.text_input("List main competitors (comma-separated):", 
                                value="Charles Schwab, Fidelity Investments, Vanguard, Merrill Lynch")
    if st.button("Conduct Market Analysis") or "market_analysis" in st.session_state.planning_docs:
        prompt = f"Conduct a market analysis for a feature similar to: {feature_idea} in the wealth management industry. Consider these competitors: {competitors}"
        generate_and_display("market_analysis", prompt)

    # Business Case Development Section
    st.header("3. Business Case Development")
    target_audience = st.text_input("Define target audience:", 
                                    value="High-net-worth individuals aged 35-65, small business owners, and retirees seeking personalized wealth management")
    expected_benefits = st.text_area("List expected benefits:", 
                                     value="Improved portfolio performance, increased client satisfaction, reduced manual workload for financial advisors, competitive edge in personalized wealth management, potential to attract younger tech-savvy clients")
    if st.button("Generate Business Case") or "business_case" in st.session_state.planning_docs:
        prompt = f"Create a business case for this feature: {feature_idea} for a wealth management firm. Target audience: {target_audience}. Expected benefits: {expected_benefits}"
        generate_and_display("business_case", prompt)

    # Project Charter Section
    st.header("4. Project Charter")
    project_objectives = st.text_area("Define project objectives:", 
                                      value="Develop an AI algorithm for personalized portfolio rebalancing, integrate with existing wealth management platform, ensure compliance with financial regulations, create intuitive interfaces for both clients and financial advisors")
    if st.button("Create Project Charter") or "project_charter" in st.session_state.planning_docs:
        prompt = f"Create a project charter for developing this feature: {feature_idea} in a wealth management firm. Objectives: {project_objectives}"
        generate_and_display("project_charter", prompt)

    # High-level Product Roadmap Section
    st.header("5. High-level Product Roadmap")
    timeframe = st.selectbox("Select timeframe:", ["3 months", "6 months", "1 year"], index=1)
    if st.button("Generate Product Roadmap") or "product_roadmap" in st.session_state.planning_docs:
        prompt = f"Create a high-level product roadmap for this feature: {feature_idea} in a wealth management platform. Timeframe: {timeframe}"
        generate_and_display("product_roadmap", prompt)

    # Stakeholder Analysis Section
    st.header("6. Stakeholder Analysis")
    stakeholders = st.text_area("List key stakeholders and their roles:", 
                                value="CIO (project sponsor), Head of Wealth Management (project lead), Lead Financial Advisor, Data Scientist, UI/UX Designer, Backend Developer, Compliance Officer, Marketing Director, Client Relations Manager")
    if st.button("Perform Stakeholder Analysis") or "stakeholder_analysis" in st.session_state.planning_docs:
        prompt = f"Perform a stakeholder analysis for this feature project in a wealth management firm. Stakeholders: {stakeholders}"
        generate_and_display("stakeholder_analysis", prompt)

    # Initial Risk Assessment Section
    st.header("7. Initial Risk Assessment")
    potential_risks = st.text_area("List potential risks:", 
                                   value="Regulatory compliance issues, data security and privacy concerns, resistance from traditional financial advisors, client trust in AI-driven recommendations, integration challenges with legacy systems, market volatility impacting AI performance")
    if st.button("Generate Risk Register") or "risk_register" in st.session_state.planning_docs:
        prompt = f"Create an initial risk register for this feature project in a wealth management context. Potential risks: {potential_risks}"
        generate_and_display("risk_register", prompt)

    # Resource Estimation Section
    st.header("8. Resource Estimation")
    team_size = st.number_input("Estimated team size:", min_value=1, max_value=100, value=10)
    if st.button("Estimate Resources") or "resource_estimation" in st.session_state.planning_docs:
        prompt = f"Provide a high-level resource estimation for developing this feature: {feature_idea} in a wealth management firm. Team size: {team_size}"
        generate_and_display("resource_estimation", prompt)

    # Review and Finalize Section
    st.header("Review and Finalize")
    if st.button("Review All Documents"):
        # Display all generated documents for review
        for doc_name, content in st.session_state.planning_docs.items():
            st.subheader(doc_name.replace("_", " ").title())
            st.write(content)
            st.markdown("---")

    if st.button("Finalize Planning Phase"):
        # Display a success message when the planning phase is completed
        st.success("Planning phase completed! All documents have been saved.")

def main():
    """
    Main function to run the Streamlit app. 
    This function initializes the planning phase.
    """
    planning_phase()

if __name__ == "__main__":
    main()