from flask import render_template, request

from app import app


@app.errorhandler(404)
def not_found(e):
    return render_template("public/404.html")


@app.errorhandler(500)
def not_found(e):
    app.logger.error(f"Server error: {e}, route: {request.url}")
    return render_template("public/500.html")


@app.errorhandler(403)
def forbidden(e):
    app.logger.error(f"Forbidden access: {e}, route: {request.url}")
    return render_template("public/403.html")
