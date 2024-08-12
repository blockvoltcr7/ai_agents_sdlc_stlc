import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
from components.chat_interface import chat_interface

# Custom CSS for styling
st.markdown("""
<style>
    .main-title {
        font-size: 3rem !important;
        font-weight: 700;
        background: linear-gradient(45deg, #1e90ff, #ff1493);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        padding: 10px 20px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 12px;
        border: none;
        transition-duration: 0.4s;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
</style>
""", unsafe_allow_html=True)

def introduction():
    st.markdown('<p class="main-title">The Future of AI Agents within the SDLC</p>', unsafe_allow_html=True)
    
    st.write("""
    Welcome to our exploration of AI Agents and their transformative potential in our daily lives. 
    Discover how these intelligent assistants are shaping the future of human-computer interaction 
    and revolutionizing various industries.
    """)
    st.subheader("Learn More About AI Agents")
    st.video("https://www.youtube.com/watch?v=F8NKVhkZZWI")
    
def current_software_development_challenges():
    st.header("Current Challenges in Software Development")
    st.write("""
    The software development industry faces several critical challenges that impact the speed and quality of product delivery:

    1. **Time to Market**: Traditional development processes often lead to lengthy development cycles, 
       delaying product launches and potentially missing market opportunities.

    2. **Documentation Gaps**: Inadequate or outdated documentation can lead to misunderstandings, 
       inefficiencies, and difficulties in maintaining or scaling software.

    3. **Code Quality and Consistency**: Ensuring high-quality, consistent code across large teams 
       and complex projects remains a significant challenge.

    4. **Communication Barriers**: Miscommunication between team members, stakeholders, and departments 
       can lead to project delays and misaligned expectations.

    5. **Adaptability to Change**: Rapidly evolving requirements and technologies require development 
       teams to be highly adaptable, which can be challenging with traditional methodologies.

    6. **Resource Allocation**: Balancing resources across different aspects of development (coding, 
       testing, documentation) can be difficult and often leads to bottlenecks.

    7. **Technical Debt**: Shortcuts taken to meet deadlines can accumulate, leading to increased 
       maintenance costs and decreased agility in the long run.

    These challenges often result in delayed releases, increased costs, and products that may not 
    fully meet customer expectations or market demands.
    """)
    
def ai_agents_solutions():
    st.header("How AI Agents Address Software Development Challenges")
    st.write("""
    AI agents offer innovative solutions to many of the challenges faced in software development:

    1. **Accelerated Development**: 
       - AI agents can automate routine coding tasks, significantly speeding up the development process.
       - They can generate boilerplate code, suggest optimizations, and even complete complex coding tasks.

    2. **Enhanced Documentation**: 
       - AI agents can automatically generate and update documentation as code changes.
       - They can create comprehensive API documentation, user guides, and even architectural diagrams.

    3. **Improved Code Quality**:
       - AI-powered code review can identify bugs, security vulnerabilities, and style inconsistencies in real-time.
       - Agents can suggest best practices and optimizations, ensuring higher code quality across the team.

    4. **Facilitated Communication**:
       - AI agents can translate technical jargon into plain language for stakeholders.
       - They can generate progress reports, summarize meetings, and create visual representations of project status.

    5. **Adaptive Planning**:
       - AI can analyze project data to predict potential bottlenecks and suggest resource allocation adjustments.
       - Agents can help in quickly prototyping and evaluating different approaches to meet changing requirements.

    6. **Efficient Resource Utilization**:
       - By handling routine tasks, AI agents free up developers to focus on complex problem-solving and innovation.
       - They can assist in task prioritization and workload balancing across the team.

    7. **Technical Debt Management**:
       - AI agents can continually monitor and refactor code to reduce technical debt.
       - They can provide insights into the long-term implications of design decisions.

    8. **Continuous Learning and Improvement**:
       - AI agents can analyze successful projects and apply learned patterns to new developments.
       - They adapt to team practices and coding styles, becoming more effective over time.

    By addressing these challenges, AI agents help development teams deliver high-quality products faster, 
    adapt more quickly to market demands, and maintain a competitive edge in the fast-paced software industry.
    """)    

def what_are_ai_agents():
    st.header("What are AI Agents?")
    st.write("""
    AI Agents are autonomous or semi-autonomous software entities that can perceive their environment, 
    make decisions, and take actions to achieve specific goals. They use artificial intelligence 
    technologies such as machine learning, natural language processing, and computer vision to interact 
    with users and systems in increasingly sophisticated ways.
    """)
    # Display the image
    st.image("../resources/images/agents-diagram.png", caption="AI Agents Diagram", use_column_width=True)

def why_ai_agents_matter():
    st.header("Why AI Agents are the Future")
    st.write("""
    1. **Flexibility and Adaptability**: AI Agents can handle a wider range of queries and adapt to new challenges.
    2. **Complex Problem Solving**: They can tackle open-ended tasks where programmed solutions may not be feasible.
    3. **Improved Accuracy**: Through iterative planning and access to external data, AI Agents can enhance decision-making.
    4. **Personalization**: AI Agents learn from interactions to provide tailored experiences.
    5. **Efficiency**: They automate complex tasks, saving time and reducing human error.
    6. **Accessibility**: AI Agents make advanced technologies accessible to non-experts.
    7. **Scalability**: They can handle multiple tasks simultaneously across various domains.
    """)

def future_of_ai_agents():
    st.header("The Future of AI Agents in Software Development")
    st.write("""
    As AI agents continue to evolve, we can expect them to become an integral part of the software development lifecycle:

    1. **End-to-End Development Assistance**: AI agents will be capable of assisting in every phase of development, 
       from initial concept to deployment and maintenance.

    2. **Advanced Predictive Analytics**: They will provide deeper insights into project trajectories, potential risks, 
       and opportunities for optimization.

    3. **Natural Language Programming**: The ability to translate human language directly into functional code will 
       make programming more accessible and efficient.

    4. **Autonomous Bug Fixing**: AI agents will not only detect but also automatically fix certain categories of bugs, 
       significantly reducing debugging time.

    5. **Personalized Developer Assistance**: Each developer will have a personalized AI assistant that understands 
       their coding style, strengths, and areas for improvement.

    6. **Cross-Functional Collaboration**: AI agents will facilitate smoother collaboration between different 
       departments, bridging the gap between technical and non-technical team members.

    7. **Ethical and Compliance Monitoring**: They will help ensure that software development adheres to ethical 
       standards and regulatory requirements.

    The ultimate goal is to empower development teams to create innovative, high-quality software products that 
    precisely meet customer needs, while significantly reducing time-to-market and development costs.
    """)
    
    
def future_of_ai_agents():
    st.header("The Future Landscape of AI Agents")
    st.write("""
    Industry leaders envision a transformative future for AI agents:

    1. **Personalized AI Assistants**: Every individual and business will have their own AI assistant, 
       tailored to their specific needs and preferences.

    2. **AI Studio for Creators**: Tools like Meta's AI Studio will empower creators to build their own 
       AI-powered assistants, democratizing AI development.

    3. **Open-Source AI Models**: The proliferation of open-source AI models, like Meta's Llama, will 
       accelerate innovation by allowing developers to build on existing work.

    4. **Integration with Mixed Reality**: AI agents will power advanced features in mixed reality headsets, 
       such as AI-driven avatars and sophisticated display systems.

    5. **Enhanced Social Media Experiences**: AI will further refine recommendation systems and content 
       curation on platforms like Instagram and Facebook.

    6. **Collaborative Problem-Solving**: AI agents will work together, combining their specialized 
       knowledge to tackle complex, multifaceted challenges.

    7. **Adaptive Learning Systems**: In education, AI agents will deliver personalized learning experiences, 
       adapting in real-time to individual learning styles and progress.

    8. **AI-Driven Healthcare**: From diagnosis to treatment planning, AI agents will become integral to 
       healthcare delivery, improving patient outcomes.

    9. **Ethical AI Development**: As AI agents become more prevalent, there will be an increased focus on 
       developing them with strong ethical considerations and user privacy in mind.

    10. **Seamless Integration**: AI agents will become an invisible yet indispensable part of our daily lives, 
        seamlessly integrating with our routines and enhancing our capabilities across various domains.
    """)
    st.subheader("Future of AI Agents")
    st.video("https://www.youtube.com/watch?v=xhQfRSueFZI")

def ai_agent_chat():
    st.header("Experience an AI Agent")
    st.write("Interact with our demo AI agent to see the potential of this technology.")
    
    st.subheader("AI Agent Tools")
    st.write("Click on a tool to see an example of how to use it:")

    tools = {
        "yFinance": "Can you search for the latest financial data on Apple Inc. using yFinance?",
        "Stock Price and News": "What's the current stock price and latest news for Tesla?",
        "DALL-E": "Could you create an image of a futuristic city using DALL-E?",
        "YouTube Summarizer": "Can you summarize the content of the YouTube video at https://www.youtube.com/watch?v=dQw4w9WgXcQ?",
        "Web Scraper": "Could you scrape the main headlines from the BBC News homepage using Selenium?",
        "Website Search": "Can you search the Wikipedia website for information about artificial intelligence using the WebsiteSearchTool?"
    }

    # Use session state to store the current prompt
    if "current_prompt" not in st.session_state:
        st.session_state.current_prompt = ""

    # Create a button for each tool
    cols = st.columns(3)
    for i, (tool, prompt) in enumerate(tools.items()):
        if cols[i % 3].button(tool):
            st.session_state.current_prompt = prompt

    system_message = """
    You are an AI agent specialized in explaining AI technology and its applications. 
    You have access to the following tools:
    1. yFinance: for searching internet and financial data
    2. Stock Price and News Retrieval
    3. DALL-E: for image creation
    4. YouTube Video Summarizer
    5. Selenium: for web scraping
    6. WebsiteSearchTool: for searching specific websites

    Provide concise, informative responses and showcase your ability to reason, plan, 
    and use these tools to solve user queries. When a user asks about using a specific tool,
    explain how you would use it to address their query, but don't actually execute the tool.
    """
    
    # Pass the current prompt to the chat interface
    chat_interface(system_message, st.session_state.current_prompt)


def main():
    introduction()
    add_vertical_space(2)
    what_are_ai_agents()
    add_vertical_space(2)
    current_software_development_challenges()
    add_vertical_space(2)
    ai_agents_solutions()
    add_vertical_space(2)
    future_of_ai_agents()
    add_vertical_space(2)
    ai_agent_chat()

if __name__ == "__main__":
    main()