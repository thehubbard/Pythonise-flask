from datetime import datetime
import os

from flask import (
    flash,
    render_template,
    request,
    redirect,
    jsonify,
    make_response,
    send_from_directory,
    abort,
    session,
    url_for,
)
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

        if not len(password) >= 10:
            flash(
                "Password must be at least 10 characters in length", "warning"
            )
            return redirect(request.url)

        flash("Account created!", "success")
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


"""
string: # DEFAULT
int:
float:
path:
uuid:
"""

app.config[
    "CLIENT_IMAGES"
] = f"{os.path.dirname(os.path.realpath(__file__))}/static/client/img"
app.config[
    "CLIENT_CSV"
] = f"{os.path.dirname(os.path.realpath(__file__))}/static/client/csv"
app.config[
    "CLIENT_REPORTS"
] = f"{os.path.dirname(os.path.realpath(__file__))}/static/client/reports"


@app.route("/get-image/<string:image_name>")
def get_image(image_name):
    try:
        return send_from_directory(
            app.config["CLIENT_IMAGES"],
            path=image_name,
            as_attachment=True,
        )
    except FileNotFoundError:
        abort(404)


@app.route("/get-csv/<string:csv_name>")
def get_csv(csv_name):
    try:
        return send_from_directory(
            app.config["CLIENT_CSV"],
            path=csv_name,
            as_attachment=False,
        )
    except FileNotFoundError:
        abort(404)


@app.route("/get-report/<path:report_name>")
def get_report(report_name):
    print(app.config["CLIENT_REPORTS"])
    print(report_name)
    try:
        return send_from_directory(
            app.config["CLIENT_REPORTS"],
            path=report_name,
            as_attachment=False,
        )
    except FileNotFoundError:
        abort(404)


@app.route("/cookies")
def cookies():
    res = make_response("Cookies", 200)

    cookies = request.cookies

    flavor = cookies.get("flavor")
    choc_type = cookies.get("chocolate type")
    chewy = cookies.get("chewy")

    res.set_cookie(
        "flavor",
        value="choc chip",
        max_age=10,
        expires=None,
        path=request.path,
        domain=None,
        secure=False,
        httponly=False,
        samesite=None,
    )

    res.set_cookie("chocolate type", "dark")
    res.set_cookie("chewy", "yes")

    return res


# import secrets
# secrets.token_urlsafe(16)
app.config["SECRET_KEY"] = "wR_UAqhsWrgX5jXGwZLJmw"

users_db = {
    "michael": {
        "username": "michael",
        "email": "michael@example.com",
        "password": "example",
        "bio": "no one",
    },
    "andy": {
        "username": "andy",
        "email": "andy@example.com",
        "password": "april9",
        "bio": "Mouse rat member",
    },
}


@app.route("/sign-in", methods=["POST", "GET"])
def sign_in():
    if request.method == "POST":
        req = request.form

        username = req["username"]
        password = req["password"]

        if username not in users_db:
            print("Username not found")
            return redirect(request.url)
        else:
            user = users_db[username]

        if password != user["password"]:
            print("Incorrect password")
            return redirect(request.url)
        else:
            # DO NOT DO IN PRODUCT USE A UUID INSTEAD
            session["USERNAME"] = user["username"]
            print("session username set")
            return redirect(url_for("profile_si"))

    return render_template("public/sign_in.html")


@app.route("/profile-sign-in")
def profile_si():
    if session.get("USERNAME") is not None:
        username = session.get("USERNAME")
        user = users_db[username]
        return render_template("public/profile-sign-in.html", user=user)
    else:
        print("No username found in session")
        return redirect(url_for("sign_in"))


@app.route("/sign-out")
def sign_out():
    session.pop("USERNAME", None)
    return redirect(url_for("sign_in"))
