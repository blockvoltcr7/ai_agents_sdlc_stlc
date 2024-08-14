# AI Agents Showcase for SDLC

## Overview
This codebase showcases how AI can bring value to the Software Development Life Cycle (SDLC) using AI agents. The project demonstrates the integration of advanced AI models to enhance various stages of the SDLC, ultimately improving efficiency and decision-making within organizations.

## Getting Started

### Prerequisites
- Python (version X.X.X)
- pip (Python package installer)

### Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/blockvoltcr7/ai_agents_sdlc_stlc.git
   cd yourproject
   ```

2. **Create a Virtual Environment**:
   ```bash
   python3 -m venv venv
   ```

3. **Activate the Virtual Environment**:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install Required Packages**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Add Environment Variables**:
   Create a `.env` file in the root directory of the project and add your API keys and secrets in the following format:
   ```
    OPENAI_API_KEY= <REQUIRED>
    ANTHROPIC_API_KEY= <REQUIRED>
    TOGETHER_API_KEY= <REQUIRED>
    ERASER_IO_API_KEY= <REQUIRED>
    GROK_API_KEY= <REQUIRED>
    GEMINI_API_KEY= <REQUIRED>
   ```

### Usage
To run the application, execute:
   ```
    streamlit run welcome.py
   ```