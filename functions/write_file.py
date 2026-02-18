import os
from pathlib import Path

def write_file(working_directory, file_path, content):
    try:

        base = Path(working_directory).resolve()
        target = Path(base / file_path).resolve()

        if not target.is_relative_to(base):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        if os.path.isdir(target):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        os.makedirs(file_path, exist_ok=True)

        with open(target, 'w') as f:
            f.write(content)
        
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {e}"