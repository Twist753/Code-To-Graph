import ast
import json
import re

class CodeParser:
    """Parse different code file types and extract structure"""
    
    def parse_file(self, content, file_type):
        """Main entry point for parsing files"""
        if file_type == 'py':
            return self.parse_python(content)
        elif file_type == 'ipynb':
            return self.parse_jupyter(content)
        elif file_type == 'cpp':
            return self.parse_cpp(content)
        else:
            raise ValueError(f"Unsupported file type: {file_type}")
    
    def parse_python(self, code):
        """Parse Python code using AST"""
        try:
            tree = ast.parse(code)
            structure = {
                'functions': [],
                'classes': [],
                'imports': [],
                'control_flow': []
            }
            
            for node in ast.walk(tree):
                # Extract functions
                if isinstance(node, ast.FunctionDef):
                    structure['functions'].append({
                        'name': node.name,
                        'args': [arg.arg for arg in node.args.args],
                        'line': node.lineno
                    })
                
                # Extract classes
                elif isinstance(node, ast.ClassDef):
                    methods = [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
                    structure['classes'].append({
                        'name': node.name,
                        'methods': methods,
                        'line': node.lineno
                    })
                
                # Extract imports
                elif isinstance(node, ast.Import):
                    for alias in node.names:
                        structure['imports'].append(alias.name)
                
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        structure['imports'].append(node.module)
                
                # Extract control flow
                elif isinstance(node, (ast.If, ast.For, ast.While)):
                    structure['control_flow'].append({
                        'type': type(node).__name__,
                        'line': node.lineno
                    })
            
            return structure
        
        except SyntaxError as e:
            return {
                'error': f'Syntax error in Python code: {str(e)}',
                'functions': [],
                'classes': [],
                'imports': [],
                'control_flow': []
            }
    
    def parse_jupyter(self, content):
        """Parse Jupyter notebook and extract Python code"""
        try:
            notebook = json.loads(content)
            all_code = []
            
            # Extract code from all code cells
            for cell in notebook.get('cells', []):
                if cell.get('cell_type') == 'code':
                    code_lines = cell.get('source', [])
                    if isinstance(code_lines, list):
                        all_code.append(''.join(code_lines))
                    else:
                        all_code.append(code_lines)
            
            # Parse combined code
            combined_code = '\n\n'.join(all_code)
            return self.parse_python(combined_code)
        
        except json.JSONDecodeError:
            return {
                'error': 'Invalid Jupyter notebook format',
                'functions': [],
                'classes': [],
                'imports': [],
                'control_flow': []
            }
    
    def parse_cpp(self, code):
        """Parse C++ code using regex (simple approach)"""
        structure = {
            'functions': [],
            'classes': [],
            'includes': [],
            'control_flow': []
        }
        
        # Extract includes
        include_pattern = r'#include\s*[<"]([^>"]+)[>"]'
        structure['includes'] = re.findall(include_pattern, code)
        
        # Extract function definitions (simplified)
        func_pattern = r'(?:void|int|float|double|char|bool|string|auto)\s+(\w+)\s*\([^)]*\)\s*{'
        functions = re.findall(func_pattern, code)
        structure['functions'] = [{'name': f, 'line': 0} for f in functions]
        
        # Extract class definitions
        class_pattern = r'class\s+(\w+)\s*(?::\s*public\s+\w+)?\s*{'
        classes = re.findall(class_pattern, code)
        structure['classes'] = [{'name': c, 'methods': []} for c in classes]
        
        # Extract control flow keywords
        lines = code.split('\n')
        for i, line in enumerate(lines, 1):
            if re.search(r'\bif\s*\(', line):
                structure['control_flow'].append({'type': 'If', 'line': i})
            elif re.search(r'\bfor\s*\(', line):
                structure['control_flow'].append({'type': 'For', 'line': i})
            elif re.search(r'\bwhile\s*\(', line):
                structure['control_flow'].append({'type': 'While', 'line': i})
        
        return structure
    
    def get_code_complexity(self, structure):
        """Calculate basic complexity metrics"""
        return {
            'num_functions': len(structure.get('functions', [])),
            'num_classes': len(structure.get('classes', [])),
            'num_imports': len(structure.get('imports', [])) + len(structure.get('includes', [])),
            'num_control_structures': len(structure.get('control_flow', []))
        }