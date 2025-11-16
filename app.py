import streamlit as st
import base64
from code_parser import CodeParser
from diagram_generator import DiagramGenerator
import streamlit.components.v1 as components

# --- Page Configuration ---
st.set_page_config(
    page_title="CodeToDiagram",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Forced Light-Theme CSS with New Styling ---
st.markdown("""
    <style>
    * {
        color-scheme: light !important;
    }
    
    body, [data-testid="stAppViewContainer"], [data-testid="stHeader"], [data-testid="stToolbar"] {
        /* Layer 1: SVG pattern (top) - Opacity increased and colors added */
        background-image: 
            url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='300' height='300' viewBox='0 0 300 300'%3E%3Ctext x='20' y='40' style='font-family: monospace; font-size: 20px; fill: rgba(0,0,0,0.3); transform: rotate(-25deg);'%3E&lt;/&gt;%3C/text%3E%3Ctext x='150' y='170' style='font-family: monospace; font-size: 20px; fill: rgba(255,105,180,0.3); transform: rotate(-25deg);'%3E{ }%3C/text%3E%3Ctext x='80' y='100' style='font-family: monospace; font-size: 20px; fill: rgba(173,216,230,0.5); transform: rotate(-25deg);'%3E( )%3C/text%3E%3Ctext x='200' y='60' style='font-family: monospace; font-size: 20px; fill: rgba(255,255,224,0.3); transform: rotate(-25deg);'%3E[ ]%3C/text%3E%3Ctext x='100' y='250' style='font-family: monospace; font-size: 20px; fill: rgba(0,0,0,0.3); transform: rotate(-25deg);'%3E//%3C/text%3E%3C/svg%3E"),
        /* Layer 2: Color gradient (bottom) */
            radial-gradient(ellipse at center, #FFFFFF 40%, #FFF1F1 70%, #FFFBEB 100%);
        
        background-repeat: repeat, no-repeat !important;
        background-attachment: fixed, fixed !important;
        background-position: center center, center center !important;
        background-size: auto, cover !important; /* SVG repeats, gradient covers */
        color: #000000 !important;
    }

    /* Add padding to bottom for fixed footer */
    [data-testid="stAppViewContainer"] {
        padding-bottom: 3rem !important;
    }
    
    /* Ensure all text is black */
    div, p, span, h1, h2, h3, h4, h5, h6, li, label, a {
        color: #000000 !important;
    }

    /* Remove sidebar UI */
    [data-testid="stSidebar"] {
        display: none;
    }

    /* Style form elements for light theme */
    .stTextArea textarea, .stTextInput input, [data-testid="stFileUploader"] {
        background-color: #FAFAFA !important;
        color: #000000 !important;
        border: 1px solid #DDDDDD !important;
    }
    
    /* Button Styling */
    .stButton button {
        background-color: #007BFF;
        color: white !important;
        border-radius: 4px;
        border: none;
    }
    .stButton button:hover {
        background-color: #0056b3;
    }

    /* Code Block Styling */
    .stCodeBlock {
        background-color: #F0F2F6 !important;
        border-radius: 4px;
    }

    /* Notification Box Styling (Formal) */
    [data-testid="stInfo"] {
        background-color: #E6F7FF !important;
        color: #000000 !important;
        border: 1px solid #B0E0FF !important;
        border-radius: 4px;
    }
    [data-testid="stSuccess"] {
        background-color: #E6F7EA !important;
        color: #000000 !important;
        border: 1px solid #B0E6C0 !important;
        border-radius: 4px;
    }
    [data-testid="stError"] {
        background-color: #FDECEA !important;
        color: #000000 !important;
        border: 1px solid #F5C6CB !important;
        border-radius: 4px;
    }
    
    /* Footer Styling (Fixed) */
    .footer {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        text-align: center;
        padding: 0.5rem 0;
        font-size: 0.9rem;
        color: #666666 !important;
        background-color: #FFFFFF; /* Give footer a solid background */
        border-top: 1px solid #E0E0E0;
        z-index: 99;
    }
    
    /* Title with Name Styling */
    .title-container {
        display: flex;
        justify-content: space-between;
        align-items: baseline; /* Aligns text neatly */
        width: 100%;
    }
    .title-main {
        font-size: 2.25rem; /* Standard title size */
        font-weight: 600;
        color: #000000 !important;
    }
    .title-name {
        font-size: 1.1rem;
        font-style: italic;
        color: #555555 !important;
    }
    
    /* 2. Upgraded Column Border & Glass Effect */
    div[data-testid="stHorizontalBlock"] {
        border: 1px solid rgba(255, 255, 255, 0.7); /* Lighter border for glass */
        border-radius: 16px; /* More rounded */
        background-color: rgba(255, 255, 255, 0.6); /* More transparent */
        backdrop-filter: blur(12px); /* More blur */
        -webkit-backdrop-filter: blur(12px);
        margin-bottom: 1.5rem; /* Add spacing between the blocks */
        padding: 0; /* Remove parent padding to allow separator to work */
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05); /* Soft drop shadow */
    }

    /* 1. Column Separator Line */
    /* Target the individual columns INSIDE the stHorizontalBlock */
    div[data-testid="stHorizontalBlock"] > div {
        padding: 1.5rem; /* Add padding to inner columns */
    }
    /* Add the border to the first column */
    div[data-testid="stHorizontalBlock"] > div:first-child {
        border-right: 1px solid rgba(200, 200, 200, 0.6);
    }
    
    /* Style the expander *inside* the glass block to be less obtrusive */
    div[data-testid="stHorizontalBlock"] [data-testid="stExpander"] {
        border: 1px solid #E0E0E0;
        background-color: #FAFAFA;
    }
    
    </style>
""", unsafe_allow_html=True)


def get_download_link(diagram_code, filename="diagram.mmd"):
    """Generates a download link for the Mermaid code (no emoji)."""
    b64 = base64.b64encode(diagram_code.encode()).decode()
    return f'<a href="data:text/plain;base64,{b64}" download="{filename}">Download Mermaid Diagram</a>'

def render_mermaid(mermaid_code: str):
    """Renders the Mermaid diagram."""
    mermaid_html = f"""
    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
    <div class="mermaid">
        {mermaid_code}
    </div>
    <script>
        mermaid.initialize({{ startOnLoad: true }});
    </script>
    """
    # Set a fixed height for the mermaid container
    components.html(mermaid_html, height=550, scrolling=True) # Adjusted height
    
def main():
    
    # Title with Name
    st.markdown("""
        <div class="title-container">
            <h1 class="title-main">CodeToDiagram</h1>
            <span class="title-name">Abhinav Tyagi(102203725) and Nitika(102203847)</span>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("### Transform your code into interactive diagrams and summaries")

    st.markdown("---") 
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Supported Files")
        st.markdown("""
        - Python (.py)
        - Jupyter Notebook (.ipynb)
        - C++ (.cpp)
        """)
    with col2:
        st.subheader("Features")
        st.markdown("""
        - Control Flow Diagrams
        - Class Diagrams
        - AI-Powered Summaries
        - Downloadable Diagrams
        """)
    
    st.markdown("---")

    # --- File Uploader ---
    uploaded_file = st.file_uploader(
        "Upload your code file",
        type=['py', 'ipynb', 'cpp'],
        help="Select a Python, Jupyter Notebook, or C++ file"
    )

    if uploaded_file:
        st.success(f"File uploaded: {uploaded_file.name}")

        file_content = uploaded_file.read().decode('utf-8')
        file_extension = uploaded_file.name.split('.')[-1]

        with st.expander("View Original Code", expanded=False):
            st.code(file_content, language='python' if file_extension in ['py', 'ipynb'] else 'cpp')

        if st.button("Generate Diagram & Summary", type="primary"):
            with st.spinner("Analyzing code and generating diagram..."):
                try:
                    parser = CodeParser()
                    diagram_gen = DiagramGenerator()  # No API key needed

                    code_structure = parser.parse_file(file_content, file_extension)

                    diagram_code = diagram_gen.generate_mermaid_diagram(code_structure, file_extension)
                    summary = diagram_gen.generate_summary(file_content, file_extension)

                    # --- Two-Column Output ---
                    # This st.columns block will ALSO be styled by the [data-testid="stHorizontalBlock"] CSS
                    col_diagram, col_summary = st.columns([1, 1])

                    with col_diagram:
                        st.subheader("Code Diagram")
                        render_mermaid(diagram_code)
                    
                        st.markdown(
                            get_download_link(diagram_code, f"{uploaded_file.name}_diagram.mmd"),
                            unsafe_allow_html=True
                        )
                    
                        with st.expander("View Mermaid Code"):
                            st.code(diagram_code, language="mermaid")
                        
                    with col_summary:
                        st.subheader("AI Summary")
                        st.markdown(summary, unsafe_allow_html=True)

                        st.info(f"""
                        **Code Statistics:**
                        - Functions: {len(code_structure.get('functions', []))}
                        - Classes: {len(code_structure.get('classes', []))}
                        - Imports: {len(code_structure.get('imports', []))}
                        """)
                    
                    st.success("Analysis complete!")

                except Exception as e:
                    st.error(f"Error processing file: {str(e)}")

    else:
        st.info("Upload a code file to get started!")

    # --- Footer (Fixed) ---
    st.markdown(
        """
        <div class="footer">
            CodeToDiagram | 2025
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()