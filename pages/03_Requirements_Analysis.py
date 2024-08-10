import streamlit as st
from utils.groq_utils import get_groq_client, get_groq_response
from utils.streamlit_utils import init_session_state

def load_planning_documents():
    # In a real scenario, this would fetch documents from cloud storage
    # For now, we'll simulate this with session state
    return st.session_state.get("planning_docs", {})

def generate_requirements(context, requirement_type):
    prompt = f"Based on the following context from the planning phase: {context}, generate a list of 5-7 {requirement_type} requirements for the feature. Format each requirement as a bullet point."
    return get_groq_response(get_groq_client(), [{"role": "user", "content": prompt}])

def main():
    st.title("Requirements Analysis Phase")
    st.write("In this phase, we'll analyze the planning documents and generate detailed requirements for the new feature.")

    # Step 1: Planning Phase Summary Review
    st.header("1. Planning Phase Summary")
    planning_docs = load_planning_documents()
    for doc_name, content in planning_docs.items():
        with st.expander(f"{doc_name.replace('_', ' ').title()}"):
            st.write(content)

    # Step 2: Requirements Generation
    st.header("2. Requirements Generation")
    requirement_types = ["Functional", "Non-Functional", "Technical", "User Interface", "Security", "Performance"]
    
    # Initialize session state for requirements if not already done
    init_session_state("requirements", {type: "" for type in requirement_types})
    init_session_state("current_type", "")

    selected_type = st.selectbox("Select requirement type to generate:", requirement_types)

    if st.button("Generate Requirements") and selected_type:
        st.session_state.current_type = selected_type
        context = " ".join(planning_docs.values())  # Combine all planning docs for context
        with st.spinner(f"Generating {selected_type} requirements..."):
            generated_reqs = generate_requirements(context, selected_type)
            st.session_state.requirements[selected_type] = generated_reqs
        st.success(f"{selected_type} requirements generated!")

    # Step 3: Iterative Requirement Refinement
    st.header("3. Requirement Refinement")
    if st.session_state.current_type:
        current_type = st.session_state.current_type
        st.subheader(f"Refine {current_type} Requirements")
        refined_reqs = st.text_area(
            f"Edit {current_type} Requirements",
            value=st.session_state.requirements[current_type],
            height=300
        )
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Update Requirements"):
                st.session_state.requirements[current_type] = refined_reqs
                st.success(f"{current_type} requirements updated!")
        
        with col2:
            if st.button("Regenerate"):
                context = " ".join(planning_docs.values())
                with st.spinner(f"Regenerating {current_type} requirements..."):
                    regenerated_reqs = generate_requirements(context, current_type)
                    st.session_state.requirements[current_type] = regenerated_reqs
                st.success(f"{current_type} requirements regenerated!")
                st.experimental_rerun()

    # Display progress
    st.sidebar.header("Progress")
    for req_type in requirement_types:
        if st.session_state.requirements[req_type]:
            st.sidebar.success(f"✅ {req_type}")
        else:
            st.sidebar.error(f"❌ {req_type}")

if __name__ == "__main__":
    main()