import os
from flask import Flask, render_template, request
from api import api_bp
import animeworld as aw

app = Flask(__name__)

app.register_blueprint(api_bp)

@app.route("/", methods=["GET", "POST"])
def indexer():
    results = []
    query = ""
    if request.method == "POST":
        query = request.form.get("q", "")
        if query:
            results = aw.find(query)
    return render_template("index.html", results=results, query=query)

if __name__ == "__main__":
    app.run(debug=True)
