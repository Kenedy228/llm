from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.get_files_info import get_files_info
from functions.run_python_file import run_python_file
from functions.schemas import schema_get_files_info
from functions.schemas import schema_get_file_content
from functions.schemas import schema_write_file
from functions.schemas import schema_run_python_file


func_names = {
    "get_file_content": get_file_content,
    "write_file": write_file,
    "get_files_info": get_files_info,
    "run_python_file": run_python_file
}

schemas_names = {
    "schema_get_file_content": schema_get_file_content,
    "schema_write_file": schema_write_file,
    "schema_get_files_info": schema_get_files_info,
    "schema_run_python_file": schema_run_python_file
}


def get_function_declarations():
    schemas = []
    for name in schemas_names:
        schemas.append(schemas_names[name])
    return schemas
