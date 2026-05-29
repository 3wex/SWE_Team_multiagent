import os
import subprocess
from langchain_core.tools import tool

WORKSPACE_DIR = './workspace'
os.makedirs(WORKSPACE_DIR, exist_ok=True)

@tool 
def write_to_file(filename: str, content: str) -> str:
    """
    Writes text or code to a file in the local workspace.
    Always use this to save specifications, code, and test files.
    """
    
    filepath = os.path.join(WORKSPACE_DIR, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    return f'Success: File successfully written to {filepath}'
    
@tool
def execute_python_script(filename: str) -> str:
    """
    Executes a Python script from the workspace and returns the standard output and errors.
    Use this to run the code and tests to verify they work.
    """
    filepath = os.path.join(WORKSPACE_DIR, filename)
    if not os.path.exists(filepath):
        return f"Error: File {filename} does not exist."
    
    try:
        result = subprocess.run(
            ["python", filepath], 
            capture_output=True, 
            text=True, 
            timeout=10 # Prevent infinite loops if the code hangs
        )
        
        if result.returncode == 0:
            return f"Execution Successful. Output:\n{result.stdout}"
        else:
            return f"Execution Failed. Error:\n{result.stderr}"
    
    except Exception as e:
        return f"System Error executing file: {str(e)}"