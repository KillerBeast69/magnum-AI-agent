import os
from pathlib import Path
from google.genai import types

def write_file(working_directory, file_path, content):
    try:

        base = Path(working_directory).resolve()
        target = Path(base / file_path).resolve()

        if not target.is_relative_to(base):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        if os.path.isdir(target):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        os.makedirs(target.parent, exist_ok=True)

        with open(target, 'w') as f:
            f.write(content)
        
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {e}"

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes text content to a specified file, creating or overwriting it",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to write to, relative to the working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The text content to write to the file",
            ),
        },
        required=["file_path", "content"],
    ),
)