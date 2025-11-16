# CodeToDiagram

CodeToDiagram is a web application that automatically analyzes source code and generates interactive flowchart diagrams along with comprehensive AI-powered summaries. The tool leverages Google's Gemini AI to understand code structure and logic, producing visual representations through Mermaid.js diagrams that help developers quickly understand complex codebases.

## Features

- **Multi-Language Support**: Analyzes Python (.py), Jupyter Notebooks (.ipynb), and C++ (.cpp) files
- **AI-Powered Diagramming**: Generates Mermaid flowchart diagrams showing control flow, functions, classes, and relationships
- **Intelligent Summaries**: Provides detailed analysis including code purpose, key components, logic flow, complexity assessment, and improvement suggestions
- **Code Statistics**: Displays metrics such as function count, class count, and import dependencies
- **Interactive Interface**: Upload files through browser, view original code, and download generated diagrams
- **Custom Styling**: Professional UI with glass-effect design and themed backgrounds

## How It Works

1. **Code Parsing**: Uses Python's Abstract Syntax Tree (AST) for Python files and regex patterns for C++ to extract code structure
2. **AI Analysis**: Sends parsed structure to Google Gemini AI for intelligent diagram generation and summary creation
3. **Visualization**: Renders interactive Mermaid flowcharts in the browser
4. **Export**: Allows downloading of diagram code for external use

## Technology Stack

- **Python** - Core application language
- **Streamlit** - Web interface framework
- **Google Gemini AI** - Code analysis and generation
- **Mermaid.js** - Interactive diagram rendering
- **Python AST** - Code structure parsing

## Installation

```bash
# Clone repository
git clone https://github.com/your-username/CodeToDiagram.git
cd CodeToDiagram

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file with your API key
echo "GEMINI_API_KEY=your_api_key_here" > .env
```

**Get your Gemini API key**: Visit [Google AI Studio](https://makersuite.google.com/app/apikey) to generate a free API key.

## Usage

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`.

1. Enter your Gemini API key in the sidebar
2. Upload a code file (.py, .ipynb, or .cpp)
3. Click "Generate Diagram & Summary"
4. View the flowchart and AI analysis
5. Download the Mermaid diagram if needed

## Project Structure

```
├── app.py                # Main Streamlit application and UI
├── code_parser.py        # Code parsing module (AST and regex)
├── diagram_generator.py  # Gemini API integration and diagram generation
├── requirements.txt      # Python dependencies
└── .env                  # API key configuration (must be created)
```

## Module Overview

- **app.py**: Handles user interface, file uploads, and coordinates between parser and generator
- **code_parser.py**: Extracts functions, classes, imports, and control flow from source code
- **diagram_generator.py**: Interfaces with Gemini AI to generate diagrams and summaries

## Requirements

- streamlit
- google-generativeai
- python-dotenv
- mermaid

## Webpage View
<img width="1919" height="862" alt="image" src="https://github.com/user-attachments/assets/f222da7e-fe0c-4dfa-bac0-114f6dc2e185" />

<img width="1919" height="1079" alt="image" src="https://github.com/user-attachments/assets/50b31772-cbe0-4e59-827c-96d6c2064b32" />

