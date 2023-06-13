import os

import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)  # Passes current module to Flask
openai.api_key = os.getenv("OPENAI_API_KEY")  # Secret key in .env file


@app.route(
    "/", methods=("GET", "POST")
)  # Index function should be able to do GET and POST.
def index():  # index function
    if request.method == "POST":  # If POST request
        field = request.form["field"]
        description = request.form["description"]
        target_audience = request.form["target_audience"]
        professionality = request.form["creativity"]
        response = openai.Completion.create(  # Calls OpenAI API to generate response
            model="text-davinci-003",  # Model
            prompt=generate_prompt(
                request.form["field"],
                request.form["description"],
                request.form["target_audience"],
                request.form["creativity"],
            ),  # Calls generate_prompt function
            temperature=0.5,
        )
        return redirect(
            url_for(
                "index",
                result=response.choices[0].text,
                field=request.form["field"],
                description=request.form["description"],
                target_audience=request.form["target_audience"],
                professionality=request.form["creativity"],
            )
        )  # Creates a text-generated response

    result = request.args.get("result")  # Assigns the response to 'result'
    return render_template("index.html", result=result)


def generate_prompt(
    field, description, target_audience, creativity
):  # Defines the generate_prompt function
    return f""""Please suggest three original one-word fun names for a company that aligns with the following factors. 
    The company operates in the {field} industry and its description is "{description}." The target audience for this company is 
    {target_audience}, and the desired level of professionalism/creativity for the name is {creativity}, on a scale from 1-5 
    (where 5 is very creative and 1 is not very creative). The name should be simple, easy-to-remember, and promote brand recognition and 
    word-of-mouth marketing. Avoid overly complex or convoluted names that are difficult to recall or spell correctly. Also, please avoid trendy or buzzword-driven names 
    that may quickly become outdated. The name should remain relevant and adaptable as the company evolves and potentially expands its products/services. Lastly, try not to
    suggest too many portmanteau names or names ending in '-ify.'
    
Names:
"""
