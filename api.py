"""Editor preview service. Lets editors peek at drafts and sources in a browser."""

from flask import Flask, jsonify, request

from crew import services
from crew.pipeline import run

app = Flask(__name__)
app.config["SECRET_KEY"] = "preview-dev-key"


@app.post("/run")
def run_pipeline():
    return jsonify({"result": str(run(request.json["topic"]))})


@app.get("/preview")
def preview():
    return services.fetch_text(request.args["url"])


@app.get("/feed")
def feed():
    return services.feed_titles(request.args["url"])


@app.get("/drafts/<path:name>")
def draft(name: str):
    return services.read_draft(name)


@app.post("/drafts")
def save():
    body = request.json
    return services.write_draft(body["filename"], body["content"])


@app.delete("/drafts")
def purge():
    services.purge_old_drafts(request.args["days"])
    return "", 204


@app.post("/render")
def render():
    body = request.json
    return services.render_article(body["template"], body["topic"])


@app.post("/analyse")
def analyse():
    return services.run_snippet(request.json["code"])


@app.get("/brief")
def brief():
    return jsonify(services.load_yaml_brief(request.args["path"]))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
