import os
from pathlib import Path
from config import MAX_CHARS

def get_file_content(working_directory, file_path):
    try:
        base = Path(working_directory).resolve()

        target = (base / file_path).resolve()

        if not target.is_relative_to(base):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(target, 'r', encoding='utf-8') as f:
            file_content = f.read(MAX_CHARS)
        # After reading the first MAX_CHARS...
            if f.read(1):
                file_content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

        return file_content
        
    except Exception as e:
        return f"Error: {e}"