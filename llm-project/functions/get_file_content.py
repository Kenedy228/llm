import os


MAX_CHARS = 10000

def get_file_content(working_directory, file_path):
    abs_working_dir = os.path.abspath(working_directory)
    target_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not target_path.startswith(abs_working_dir):
        return f"Error: Cannot read \"{file_path}\" as it is outside the permitted working directory"
    if not os.path.isfile(target_path):
        return f"Error: File not found or is not a regular file: \"{file_path}\""
    contents = None
    with open(target_path, "r") as f:
        contents = f.read(MAX_CHARS)
    if len(contents) == MAX_CHARS:
        contents = f"{contents}[...File \"{target_path}\" truncated at {MAX_CHARS} characters]"
    return contents

    
