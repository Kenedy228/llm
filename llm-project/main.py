import sys
from google import genai
from google.genai import types
from config import API_KEY
from config import MODEL
from config import WORKING_DIR
from config import MAX_ITERS
from prompt import available_functions
from prompt import system_prompt
from functions.utils import func_names

api_key = API_KEY
client = genai.Client(api_key=api_key)
model = MODEL


def handle_user_prompt(args):
    if len(args) == 1:
        print("exec failure: provide a valid prompt \"uv run main.py <prompt> <args>\"")
        sys.exit(1)

    user_prompt, verbose = None, False

    if len(args) == 2:
        if args[1] == "--verbose":
            print("exec failure: provide a valid prompt \"uv run main.py <prompt> <args>\"")
            sys.exit(1)
        user_prompt = args[1]

    if len(args) == 3:
        if args[1] == "--verbose":
            print("exec failure: provide a valid prompt \"uv run main.py <prompt> <args>\"")
            sys.exit(1)
        if args[2] != "--verbose":
            print("exec failure: unknown flag")
            sys.exit(1)
        user_prompt = args[1]
        verbose = args[2]

    return user_prompt, verbose


def call_function(function_call_part, verbose=False):

    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f"Calling function: {function_call_part.name}")
    if function_call_part.name not in func_names:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unknown function: {function_call_part.name}"},
                )
            ],
        )
    all_args = {**function_call_part.args, "working_directory": WORKING_DIR}
    function_result = func_names[function_call_part.name](**all_args)
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call_part.name,
                response={"result": function_result},
            )
        ],
    )


def generate_content(user_prompt, messages, verbose=False):
    response = client.models.generate_content(model=model, contents=messages, config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt))

    if verbose:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)

    if response.candidates:
        for candidate in response.candidates:
            function_call_content = candidate.content
            messages.append(function_call_content)

    if not response.function_calls:
        return response.text

    function_responses = []
    for function_call_part in response.function_calls:
        function_call_result = call_function(function_call_part, verbose)
        if (
            not function_call_result.parts
            or not function_call_result.parts[0].function_response
        ):
            raise Exception("empty function call result")
        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
        function_responses.append(function_call_result.parts[0])

    if not function_responses:
        raise Exception("no function responses generated, exiting.")

    messages.append(types.Content(role="tool", parts=function_responses))


def main():
    user_prompt, verbose = handle_user_prompt(sys.argv)

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]

    iters = 0
    while True:
        iters += 1
        if iters > MAX_ITERS:
            print(f"Maximum iterations ({MAX_ITERS}) reached")
            sys.exit(1)
        try:
            final_response = generate_content(user_prompt, messages, verbose)
            if final_response:
                print(f"Final response:\n{final_response}")
                break
        except Exception as e:
            print(f"Error: {e}")
            return


if __name__ == "__main__":
    main()
