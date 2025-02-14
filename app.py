from flask import Flask, render_template, request, url_for
import json

from werkzeug.utils import redirect

app = Flask(__name__)

def load_posts():
    with open("blog.json", "r") as file:
        return json.load(file)

def save_posts(posts):
    with open("blog.json", "w") as file:
        json.dump(posts, file, indent=4)

@app.route('/')
def homepage():
    return 'Welcome to the Masterblog!'

@app.route('/index')
def index():
    posts = load_posts()
    return render_template('index.html', posts=posts)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == "POST":
        posts = load_posts()
        new_post = {
            "id": len(posts) + 1,
            "author": request.form["author"],
            "title": request.form["title"],
            "content": request.form["content"]
            }
        posts.append(new_post)
        save_posts(posts)
        return redirect(url_for("index"))

    return render_template("add.html")

@app.route("/delete/<int:post_id>", methods=["POST"])
def delete(post_id):
    posts = load_posts()
    posts = [post for post in posts if post["id"] != post_id]  # Remove post
    save_posts(posts)
    return redirect(url_for("index"))

@app.route("/update/<int:post_id>", methods=["GET", "POST"])
def update(post_id):
    posts = load_posts()
    post = next((p for p in posts if p["id"] == post_id), None)

    if not post:
        return "Post not found", 404

    if request.method == "POST":
        post["title"] = request.form["title"]
        post["author"] = request.form["author"]
        post["content"] = request.form["content"]
        save_posts(posts)
        return redirect(url_for("index"))

    return render_template("update.html", post=post)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)