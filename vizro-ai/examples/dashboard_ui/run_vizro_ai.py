import argparse
import logging

import black
import pandas as pd
from actions import get_vizro_ai_dashboard
from dash.exceptions import PreventUpdate
import plotly.express as px


def run_vizro_ai_dashboard(user_prompt, model, api_key, api_base, n_clicks):
    """Gets the AI response and adds it to the chatbot window."""
    filename = "gapminder.csv"
    def create_response(ai_response, user_prompt, filename):
        print("ai response: *******************************", ai_response, "*******************************")
        return (
            ai_response,
            {"ai_response": ai_response, "prompt": user_prompt, "filename": filename},
        )

    if not n_clicks:
        raise PreventUpdate

    # if not data:
    #     ai_response = "Please upload data to proceed!"
    #     return create_response(ai_response, user_prompt, None)

    if not api_key:
        ai_response = "API key not found. Make sure you enter your API key!"
        return create_response(ai_response, user_prompt, filename)

    try:
        # df = pd.DataFrame(data["data"])
        df = px.data.gapminder()
        ai_outputs = get_vizro_ai_dashboard(
            user_prompt=user_prompt, dfs=df, model=model, api_key=api_key, api_base=api_base
        )
        ai_code = ai_outputs.code
        formatted_code = black.format_str(ai_code, mode=black.Mode(line_length=100))

        ai_response = "\n".join(["```python", formatted_code, "```"])

        return create_response(ai_response, user_prompt, filename)

    except Exception as exc:
        logging.exception(exc)
        ai_response = f"Sorry, I can't do that. Following Error occurred: {exc}"
        return create_response(ai_response, user_prompt, filename)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process some arguments.")
    parser.add_argument("--arg1", required=True, help="User prompt")
    # parser.add_argument("--arg2", required=True, help="Data")
    parser.add_argument("--arg2", required=True, help="Model")
    parser.add_argument("--arg3", required=True, help="API key")
    parser.add_argument("--arg4", required=True, help="API base")
    parser.add_argument("--arg5", required=True, help="n_clicks")

    args = parser.parse_args()

    run_vizro_ai_dashboard(args.arg1, args.arg2, args.arg3, args.arg4, args.arg5)
