import google.generativeai as genai
from dotenv import load_dotenv
import os
load_dotenv()

class DiagramGenerator:
    """Generate Mermaid diagrams and summaries using Gemini API"""
    
    def __init__(self):
        """Initialize Gemini API"""
        api_key = os.getenv('GEMINI_API_KEY')
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-pro')
    
    def generate_mermaid_diagram(self, code_structure, file_type):
        """Generate Mermaid diagram code based on code structure"""
        
        # Build context for Gemini
        context = self._build_structure_context(code_structure, file_type)
        
        prompt = f"""
You are a code visualization expert. Given the following code structure, generate a Mermaid diagram.

{context}

Requirements:
1. Create a flowchart (use 'flowchart TD' syntax)
2. Show the main flow of execution
3. Include all functions and classes
4. Show control flow (if/else, loops) where applicable
5. Keep it clean and readable
6. Use appropriate shapes: rectangles for functions, diamonds for conditionals, circles for start/end
7. Return ONLY the Mermaid code, no explanations, no preamble or markdown backticks

NOTE - Always provide a correct and valid mermaid. Double check for any syntax errors in it.

Example format:
flowchart TD
    A[Start] --> B[Function1]
    B --> C{{If condition?}}
    C -->|Yes| D[Action1]
    C -->|No| E[Action2]
    D --> F[End]
    E --> F
"""
        
        try:
            response = self.model.generate_content(prompt)
            mermaid_code = response.text.strip()
            
            # Clean up the response (remove markdown if present)
            mermaid_code = mermaid_code.replace('```mermaid', '').replace('```', '').strip()
            
            # Fallback if Gemini fails
            if not mermaid_code or len(mermaid_code) < 20:
                return self._generate_fallback_diagram(code_structure, file_type)
            
            return mermaid_code
        
        except Exception as e:
            print(f"Error generating diagram with Gemini: {e}")
            return self._generate_fallback_diagram(code_structure, file_type)
    
    def generate_summary(self, code_content, file_type):
        """Generate AI-powered code summary"""
        
        lang_map = {'py': 'Python', 'ipynb': 'Python (Jupyter)', 'cpp': 'C++'}
        language = lang_map.get(file_type, 'Unknown')
        
        # Truncate code if too long (Gemini has token limits)
        max_length = 8000
        if len(code_content) > max_length:
            code_content = code_content[:max_length] + "\n... (truncated)"
        
        prompt = f"""
Analyze this {language} code and provide a comprehensive summary.

Code:
```
{code_content}
```

Provide:
1. **Purpose**: What does this code do? (2-3 sentences)
2. **Key Components**: Main functions, classes, or modules
3. **Logic Flow**: How does the code work?
4. **Complexity**: Is it simple, moderate, or complex?
5. **Potential Issues**: Any code smells or improvements?

Note: There should not be any emoji in the output. keep it formal. also try to keep it small and concise, just enough to explain things. Use only markdown formatting
"""
        
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        
        except Exception as e:
            return f"⚠️ Could not generate summary: {str(e)}\n\nPlease check your API key or try again."
    
    def _build_structure_context(self, structure, file_type):
        """Build a text description of code structure"""
        context_parts = []
        
        # Functions
        if structure.get('functions'):
            func_names = [f['name'] for f in structure['functions']]
            context_parts.append(f"Functions: {', '.join(func_names)}")
        
        # Classes
        if structure.get('classes'):
            for cls in structure['classes']:
                methods = ', '.join(cls.get('methods', []))
                context_parts.append(f"Class {cls['name']} with methods: {methods}")
        
        # Imports/Includes
        imports = structure.get('imports', []) + structure.get('includes', [])
        if imports:
            context_parts.append(f"Dependencies: {', '.join(imports[:5])}")  # Limit to 5
        
        # Control flow
        if structure.get('control_flow'):
            flow_types = [cf['type'] for cf in structure['control_flow']]
            context_parts.append(f"Control structures: {', '.join(set(flow_types))}")
        
        return "\n".join(context_parts) if context_parts else "Empty or simple code structure"
    
    def _generate_fallback_diagram(self, structure, file_type):
        """Generate a basic Mermaid diagram without Gemini (fallback)"""
        
        mermaid_lines = ["flowchart TD"]
        mermaid_lines.append("    Start([Start]) --> Main")
        
        # Add functions
        functions = structure.get('functions', [])
        if functions:
            for i, func in enumerate(functions[:10]):  # Limit to 10
                func_id = f"F{i}"
                mermaid_lines.append(f"    Main --> {func_id}[{func['name']}]")
        
        # Add classes
        classes = structure.get('classes', [])
        if classes:
            for i, cls in enumerate(classes[:5]):  # Limit to 5
                cls_id = f"C{i}"
                mermaid_lines.append(f"    Main --> {cls_id}[Class: {cls['name']}]")
                
                # Add methods
                for j, method in enumerate(cls.get('methods', [])[:3]):  # Limit to 3
                    method_id = f"M{i}{j}"
                    mermaid_lines.append(f"    {cls_id} --> {method_id}[{method}]")
        
        # Add control flow
        if structure.get('control_flow'):
            mermaid_lines.append("    Main --> Control{{Control Flow}}")
            control_types = list(set([cf['type'] for cf in structure['control_flow']]))
            for i, ct in enumerate(control_types[:3]):
                mermaid_lines.append(f"    Control --> CF{i}[{ct}]")
        
        mermaid_lines.append("    Main --> End([End])")
        
        return "\n".join(mermaid_lines)