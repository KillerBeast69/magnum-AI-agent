import subprocess
from pathlib import Path
from google.genai import types

def run_python_file(working_directory, file_path, args=None):
    try: 

        base = Path(working_directory).resolve()
        target = Path(base / file_path).resolve()

        if not target.is_relative_to(base):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not target.exists() or not target.is_file():
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if target.suffix != ".py":
            return f'Error: "{file_path}" is not a Python file'
        
        absolute_file_path = str(target)
        command = ["python", absolute_file_path]
        if args:
            command.extend(args)
        
        completed_process = subprocess.run(
            command,
            cwd = working_directory,
            capture_output = True,
            text = True,
            timeout = 30
        )
        output_string = ""
        if completed_process.returncode != 0:
            output_string += f"Process exited with code {completed_process.returncode}\n"
        if not completed_process.stdout and not completed_process.stderr:
            output_string += "No output produced"
        else:
            if completed_process.stdout:
                output_string += f"STDOUT: {completed_process.stdout}"
            if completed_process.stderr:
                output_string += f"STDERR: {completed_process.stderr}"

        return output_string.strip()
    except Exception as e:
        return f"Error: executing Python file: {e}"

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file with optional command-line arguments",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the Python file to execute",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                ),
                description="Optional list of command-line arguments to pass to the script",
            ),
        },
        required=["file_path"],
    ),
)