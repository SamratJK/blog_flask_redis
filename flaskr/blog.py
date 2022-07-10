from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    url_for,
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db
from datetime import datetime

bp = Blueprint("blog", __name__)


@bp.route("/")
def index():
    db = get_db()
    posts = []
    post_get = db.lrange("posts", 0, -1)
    for post_id in post_get:
        post = db.hgetall("post" + post_id)
        print(post)
        posts.append(post)
    return render_template("blog/index.html", posts=posts)


@bp.route("/create", methods=("GET", "POST"))
@login_required
def create():
    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        error = None

        if not title:
            error = "Title is required."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            post_id = str(db.incr("next_post_id"))
            db.hmset(
                "post" + post_id,
                {
                    "id": post_id,
                    "username": g.user,
                    "title": title,
                    "body": body,
                    "created": str(datetime.now().strftime("%Y-%m-%d")),
                },
            )

            db.lpush("posts", post_id)
            return redirect(url_for("blog.index"))

    return render_template("blog/create.html")


def get_post(id, check_author=True):
    post = get_db().hgetall("post" + id)

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post["username"] != g.user:
        abort(403)

    return post


@bp.route("/<int:id>/update", methods=("GET", "POST"))
@login_required
def update(id):
    post = get_post(str(id))

    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        error = None

        if not title:
            error = "Title is required."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.hmset(
                "post" + str(id),
                {
                    "id": id,
                    "username": g.user,
                    "title": title,
                    "body": body,
                    "created": str(datetime.now().strftime("%Y-%m-%d")),
                },
            )
            return redirect(url_for("blog.index"))

    return render_template("blog/update.html", post=post)


@bp.route("/<int:id>/delete", methods=("POST",))
@login_required
def delete(id):
    get_post(str(id))
    db = get_db()
    db.delete("post" + str(id))
    return redirect(url_for("blog.index"))
