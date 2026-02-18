from google.genai import types
from functions.get_files_info import *
from functions.get_file_content import *
from functions.run_python_file import *
from functions.write_file import *
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info, 
        schema_run_python_file, 
        schema_write_file, 
        schema_get_file_content]
)