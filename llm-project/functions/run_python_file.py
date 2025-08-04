import os
import subprocess


def run_python_file(working_directory, file_path, args=[]):
    abs_working_dir = os.path.abspath(working_directory)
    target_file = os.path.abspath(os.path.join(working_directory, file_path))

    if not target_file.startswith(abs_working_dir):
        return f"Error: Cannot execute \"{file_path}\" as it is outside the permitted working directory"
    if not os.path.exists(target_file):
        return f"Error: File \"{file_path}\" not found."
    if not target_file.endswith(".py"):
        return f"Error: \"{file_path}\" is not a Python file."
    try:
        run_args = ["uv", "run", target_file]
        run_args.extend(args)

        completed_process = subprocess.run(run_args,
                timeout=30,
                cwd=abs_working_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True)

        result = []

        if completed_process.stdout:
            result.append("STDOUT:")
            result.append(completed_process.stdout.strip())
        if completed_process.stderr:
            result.append("STDERR:")
            result.append(completed_process.stderr.strip())
        if not (completed_process.stdout or completed_process.stderr):
            result.append("No output produced.")
        if completed_process.returncode != 0:
            result.append(f"Process exited with code {result.returncode}")

        return "\n".join(result)
    except Exception as e:
        return f"Error: executing Python file: {e}"
