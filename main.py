import os
import argparse
import time
import sys
from prompts import system_prompt
from dotenv import load_dotenv
from google import genai
from google.genai import types, errors
from functions.call_function import available_functions, call_function




def main():
    print("Hello from ai-agent!")
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    if api_key == None:
        raise RuntimeError("api key not available")

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    # toggle to enable and disable meta data
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    # Now we can access `args.user_prompt`

    client = genai.Client(api_key=api_key)

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    # prompter to the google flash
    conversation_history = []

    for _ in range(20):
        response = client.models.generate_content(
                model='gemini-2.5-flash', 
                contents=messages,
                config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                tools=[available_functions],
                temperature=0)
            )
        
        candidates = response.candidates

        if candidates:
            for candidate in candidates:
                messages.append(candidate.content)

        # output
        list_of_function_results = []
        if args.verbose:
            # prompt meta data
            prompt_tokens = response.usage_metadata.prompt_token_count
            response_tokens = response.usage_metadata.candidates_token_count
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {prompt_tokens}")
            print(f"Response tokens: {response_tokens}")
        if response.function_calls:
            for function_call in response.function_calls:
                function_call_result = call_function(function_call, verbose=args.verbose)
                if not function_call_result.parts:
                    raise Exception("function call returned no parts")
                if not function_call_result.parts[0].function_response:
                    raise Exception("Part is not a function response")
                if not function_call_result.parts[0].function_response.response:
                    raise Exception("Function response has no content")
                list_of_function_results.append(function_call_result.parts[0])

                if args.verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
        else:
            print(response.text)
            return
        
        messages.append(types.Content(role="user", parts=list_of_function_results))
    
    print("You ran out of prompts")
    sys.exit(1)


if __name__ == "__main__":
    main()

