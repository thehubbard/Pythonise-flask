from datetime import datetime
import os

from flask import render_template, request, redirect, jsonify, make_response
from werkzeug.utils import secure_filename
from app import app


@app.template_filter("clean_date")
def clean_date(dt):
    return dt.strftime("%d %b %Y")


@app.route("/")
def index():
    # FLASK_ENV has been removed in v2.3
    print(app.config["DB_NAME"])
    return render_template("public/index.html")


@app.route("/jinja")
def jinja():
    my_name = "Michael"
    age = 29
    langs = ["Python", "C++", "Bash", "Fortran", "SQL"]

    friends = {"Bob": 28, "Callum": 27, "Daz": 42}

    colours = ("Red", "Green", "Blue")

    cool = True

    class GitRemote:
        def __init__(self, name, description, url) -> None:
            self.name = name
            self.description = description
            self.url = url

        def pull(self):
            return f"Pulling repo {self.name}"

        def clone(self):
            return f"Cloning repo {self.url}"

    my_remote = GitRemote(
        name="Flask Jinja",
        description="Template design tutorial",
        url="https://github.com/thehubbard/jinja.git",
    )

    def repeat(x, qty):
        return x * qty

    date = datetime.utcnow()

    my_html = "<h1>THIS IS SOME HTML</h1>"

    suspicious = "<script>alert('YOU GOT HACKED!')</script>"

    return render_template(
        "public/jinja.html",
        my_name=my_name,
        age=age,
        langs=langs,
        friends=friends,
        colours=colours,
        cool=cool,
        GitRemote=GitRemote,
        my_remote=my_remote,
        repeat=repeat,
        date=date,
        my_html=my_html,
        suspicious=suspicious,
    )


@app.route("/about")
def about():
    return render_template("public/about.html")


@app.route("/sign-up", methods=["POST", "GET"])
def sign_up():
    if request.method == "POST":
        req = request.form

        username = req["username"]
        email = req.get("email")
        password = request.form["password"]

        print(username, email, password)

        return redirect(request.url)

    return render_template("public/sign_up.html")


users = {
    "mitsuhiko": {
        "name": "Armin Ronacher",
        "bio": "Creatof of the Flask framework",
        "twitter_handle": "@mitsuhiko",
    },
    "gvanrossum": {
        "name": "Guido Van Rossum",
        "bio": "Creator of the Python programming language",
        "twitter_handle": "@gvanrossum",
    },
    "elonmusk": {
        "name": "Elon Musk",
        "bio": "technology entrepreneur, investor, and engineer",
        "twitter_handle": "@elonmusk",
    },
}


@app.route("/profile/<username>")
def profile(username):
    user = None

    if username in users:
        user = users[username]

    return render_template("public/profile.html", username=username, user=user)


@app.route("/profile/<foo>/<bar>/<baz>")
def multi(foo, bar, baz):
    return f"foo is {foo}, bar is {bar}, baz is {baz}"


@app.route("/json", methods=["POST"])
def json():
    if request.is_json:
        req = request.get_json()

        response = {"message": "JSON received!", "name": req.get("name")}

        res = make_response(jsonify(response), 200)

        return res

    else:
        res = make_response(jsonify({"message": "No JSON received!"}), 400)

        return res


@app.route("/guestbook")
def guestbook():
    return render_template("public/guestbook.html")


@app.route("/guestbook/create-entry", methods=["POST"])
def create_entry():
    req = request.get_json()

    print(req)

    res = make_response(jsonify({"message": "JSON received"}), 200)

    return res


@app.route("/query")
def query():
    if request.args:
        args = request.args

        serialized = ", ".join(f"{k}: {v}" for k, v in args.items())
        return f"(Query) {serialized}", 200
    else:
        return "No query received", 200


# ?foo=foo&bar=bar&baz=baz&title=query+strings+with+flask

app.config[
    "IMAGE_UPLOADS"
] = f"{os.path.dirname(os.path.realpath(__file__))}/static/img/uploads"

app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["PNG", "JPG", "JPEG", "GIF"]
app.config["MAX_IMG_FILESIZE"] = 0.5 * 1024 * 1024


def allowed_image(filename):
    if "." not in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False


def allowed_image_filesize(filesize):
    return True if int(filesize) <= app.config["MAX_IMG_FILESIZE"] else False


@app.route("/upload-image", methods=["GET", "POST"])
def upload_image():
    if (request.method == "POST") and (request.files):
        image = request.files["image"]

        if not allowed_image_filesize(request.cookies.get("filesize")):
            print("File exceeded maximum size")

        if image.filename == "":
            print("Image must have a filename")

        if not allowed_image(image.filename):
            print("That file extension is not allowed")
            return redirect(request.url)
        else:
            filename = secure_filename(image.filename)

            image.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))

        print("Image saved")
        print(image.content_length)

        return redirect(request.url)

    return render_template("public/upload_image.html")
