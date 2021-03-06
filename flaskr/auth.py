import functools

from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from werkzeug.security import (
    check_password_hash,
    generate_password_hash,
)

from flaskr.db import get_db

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/register", methods=("GET", "POST"))
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        error = None

        if not username:
            error = "Username is required."
        elif not password:
            error = "Password is required."

        if error is None:
            if not db.exists(username):
                user_id = str(db.incrby("next_user_id", 1))
                db.set(username, user_id)
                db.hmset(
                    "user:" + user_id,
                    {
                        "username": username,
                        "password": generate_password_hash(password),
                    },
                )
                return redirect(url_for("auth.login"))
            else:
                error = f"User {username} is already registered."

        flash(error)

    return render_template("auth/register.html")


@bp.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        error = None
        user = db.exists(username)
        user_id = str(db.get(username))

        if not user:
            error = "Incorrect username."
        elif not check_password_hash(
            db.hget("user:" + user_id, "password"), password
        ):
            error = "Incorrect password."

        if error is None:
            session.clear()
            session["user_id"] = user_id

            return redirect(url_for("index"))

        flash(error)

    return render_template("auth/login.html")


@bp.before_app_request
def load_logged_in_user():
    user_id = str(session.get("user_id"))

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().hget("user:" + user_id, "username")


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view
