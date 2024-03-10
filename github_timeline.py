from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

def get_github_timeline(username):
    url = f"https://api.github.com/users/{username}/repos"
    response = requests.get(url)
    repos = response.json()
    timeline = []

    for repo in repos:
        repo_info = {
            "name": repo["name"],
            "created_at": repo["created_at"],
            "description": repo["description"]
        }
        timeline.append(repo_info)

    return timeline

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        username = request.form["username"]
        if username:
            timeline = get_github_timeline(username)
            return render_template("timeline.html", username=username, timeline=timeline)
        else:
            return render_template("index.html", error="Please enter a valid GitHub username.")
    return render_template("index.html", error=None)

if __name__ == "__main__":
    app.run(debug=True)
