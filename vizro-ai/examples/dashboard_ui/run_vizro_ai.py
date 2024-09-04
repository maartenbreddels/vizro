import logging

import black
import pandas as pd

from dash.exceptions import PreventUpdate
from actions import get_vizro_ai_dashboard
import argparse
import subprocess



def run_vizro_ai_dashboard(user_prompt, data, model, api_data, n_clicks):
    """Gets the AI response and adds it to the chatbot window."""

    def create_response(ai_response, user_prompt, filename):
        return (
            ai_response,
            {"ai_response": ai_response, "prompt": user_prompt, "filename": filename},
        )

    if not n_clicks:
        raise PreventUpdate

    if not data:
        ai_response = "Please upload data to proceed!"
        return create_response(ai_response, user_prompt, None)

    if not api_data:
        ai_response = "API key not found. Make sure you enter your API key!"
        return create_response(ai_response, user_prompt, data["filename"])

    try:
        df = pd.DataFrame(data["data"])
        ai_outputs = get_vizro_ai_dashboard(
            user_prompt=user_prompt, dfs=df, model=model, api_key=api_data["api_key"], api_base=api_data["api_base"]
        )
        ai_code = ai_outputs.code
        formatted_code = black.format_str(ai_code, mode=black.Mode(line_length=100))

        ai_response = "\n".join(["```python", formatted_code, "```"])

        return create_response(ai_response, user_prompt, data["filename"])

    except Exception as exc:
        logging.exception(exc)
        ai_response = f"Sorry, I can't do that. Following Error occurred: {exc}"
        return create_response(ai_response, user_prompt, data["filename"])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process some arguments.")
    parser.add_argument('--arg1',  required=True, help="First argument")
    parser.add_argument('--arg2', required=True, help="Second argument")
    parser.add_argument('--arg3', required=True, help="Third argument")
    parser.add_argument('--arg4',  required=True, help="Fourth argument")
    parser.add_argument('--arg5', required=True, help="Fourth argument")

    args = parser.parse_args()
    print("args: ", args)
    run_vizro_ai_dashboard(args.arg1, args.arg2, args.arg3, args.arg4, args.arg5)
