import os


def get_files_info(working_directory, directory="."):
    abs_working_dir = os.path.abspath(working_directory)
    target_dir = os.path.abspath(os.path.join(working_directory, directory))

    if not target_dir.startswith(abs_working_dir):
        return f"Error: Cannot list \"{directory}\" as it is outside the permitted working directory"
    if not os.path.isdir(target_dir):
        return f"Error: \"{directory}\" is not a directory"
    contents = []
    for f in os.listdir(target_dir):
        current_file_path = os.path.join(target_dir, f)
        size = os.path.getsize(current_file_path)
        is_dir = os.path.isdir(current_file_path)
        contents.append(f"- {f}: file_size={size} bytes, is_dir={is_dir}")
    return "\n".join(contents)
