import sys
from google import genai
from google.genai import types
from config import API_KEY, MODEL
from prompt import available_functions, system_prompt

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


def generate_report(response, user_prompt, verbose=False):
    for f in response.function_calls:
        print(f"Calling function: {f.name}({f.args})")
    if verbose:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


def main():
    user_prompt, verbose = handle_user_prompt(sys.argv)
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]
    response = client.models.generate_content(model=model, contents=messages, config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt))
    generate_report(response, user_prompt, verbose)


if __name__ == "__main__":
    main()
