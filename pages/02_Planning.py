import streamlit as st
from utils.groq_utils import get_groq_client, get_groq_response
from utils.streamlit_utils import init_session_state

def planning_phase():
    st.title("Planning Phase: New Feature Playground")

    # Initialize session state for storing generated documents
    init_session_state("planning_docs", {})

    # Feature Ideation
    st.header("1. Feature Ideation")
    feature_idea = st.text_area("Describe your feature idea:", height=150)
    if st.button("Generate Feature Proposal"):
        prompt = f"Based on this feature idea: {feature_idea}, generate a comprehensive feature proposal document."
        response = get_groq_response(get_groq_client(), [{"role": "user", "content": prompt}])
        st.session_state.planning_docs["feature_proposal"] = response
        st.success("Feature Proposal generated!")

    # Market Research
    st.header("2. Market Research")
    competitors = st.text_input("List main competitors (comma-separated):")
    if st.button("Conduct Market Analysis"):
        prompt = f"Conduct a market analysis for a feature similar to: {feature_idea}. Consider these competitors: {competitors}"
        response = get_groq_response(get_groq_client(), [{"role": "user", "content": prompt}])
        st.session_state.planning_docs["market_analysis"] = response
        st.success("Market Analysis completed!")

    # Business Case Development
    st.header("3. Business Case Development")
    target_audience = st.text_input("Define target audience:")
    expected_benefits = st.text_area("List expected benefits:")
    if st.button("Generate Business Case"):
        prompt = f"Create a business case for this feature: {feature_idea}. Target audience: {target_audience}. Expected benefits: {expected_benefits}"
        response = get_groq_response(get_groq_client(), [{"role": "user", "content": prompt}])
        st.session_state.planning_docs["business_case"] = response
        st.success("Business Case generated!")

    # Project Charter
    st.header("4. Project Charter")
    project_objectives = st.text_area("Define project objectives:")
    if st.button("Create Project Charter"):
        prompt = f"Create a project charter for developing this feature: {feature_idea}. Objectives: {project_objectives}"
        response = get_groq_response(get_groq_client(), [{"role": "user", "content": prompt}])
        st.session_state.planning_docs["project_charter"] = response
        st.success("Project Charter created!")

    # High-level Product Roadmap
    st.header("5. High-level Product Roadmap")
    timeframe = st.selectbox("Select timeframe:", ["3 months", "6 months", "1 year"])
    if st.button("Generate Product Roadmap"):
        prompt = f"Create a high-level product roadmap for this feature: {feature_idea}. Timeframe: {timeframe}"
        response = get_groq_response(get_groq_client(), [{"role": "user", "content": prompt}])
        st.session_state.planning_docs["product_roadmap"] = response
        st.success("Product Roadmap generated!")

    # Stakeholder Analysis
    st.header("6. Stakeholder Analysis")
    stakeholders = st.text_area("List key stakeholders and their roles:")
    if st.button("Perform Stakeholder Analysis"):
        prompt = f"Perform a stakeholder analysis for this feature project. Stakeholders: {stakeholders}"
        response = get_groq_response(get_groq_client(), [{"role": "user", "content": prompt}])
        st.session_state.planning_docs["stakeholder_analysis"] = response
        st.success("Stakeholder Analysis completed!")

    # Initial Risk Assessment
    st.header("7. Initial Risk Assessment")
    potential_risks = st.text_area("List potential risks:")
    if st.button("Generate Risk Register"):
        prompt = f"Create an initial risk register for this feature project. Potential risks: {potential_risks}"
        response = get_groq_response(get_groq_client(), [{"role": "user", "content": prompt}])
        st.session_state.planning_docs["risk_register"] = response
        st.success("Risk Register generated!")

    # Resource Estimation
    st.header("8. Resource Estimation")
    team_size = st.number_input("Estimated team size:", min_value=1, max_value=100, value=5)
    if st.button("Estimate Resources"):
        prompt = f"Provide a high-level resource estimation for developing this feature: {feature_idea}. Team size: {team_size}"
        response = get_groq_response(get_groq_client(), [{"role": "user", "content": prompt}])
        st.session_state.planning_docs["resource_estimation"] = response
        st.success("Resource Estimation completed!")

    # Review and Finalize
    st.header("Review and Finalize")
    if st.button("Review All Documents"):
        for doc_name, content in st.session_state.planning_docs.items():
            st.subheader(doc_name.replace("_", " ").title())
            st.write(content)
            st.markdown("---")

    if st.button("Finalize Planning Phase"):
        # Here you would implement the logic to save all documents to your chosen storage solution
        st.success("Planning phase completed! All documents have been saved.")

def main():
    planning_phase()

if __name__ == "__main__":
    main()