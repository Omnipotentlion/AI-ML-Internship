from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash
from flask import session

from database import get_db_connection

from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/")
def home():

    if "user_id" in session:
        return redirect("/chat")

    return redirect("/login")


@auth_bp.route("/register", methods=["GET","POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db_connection()

        existing = conn.execute(
            "SELECT * FROM users WHERE email=?",
            (email,)
        ).fetchone()

        if existing:
            flash("Email already exists")
            return redirect("/register")

        hashed = generate_password_hash(password)

        conn.execute(
            "INSERT INTO users(name,email,password) VALUES(?,?,?)",
            (name,email,hashed)
        )

        conn.commit()
        conn.close()

        flash("Registration Successful")
        return redirect("/login")

    return render_template("register.html")


@auth_bp.route("/login", methods=["GET","POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        conn = get_db_connection()

        user = conn.execute(
            "SELECT * FROM users WHERE email=?",
            (email,)
        ).fetchone()

        conn.close()

        if user and check_password_hash(user["password"],password):

            session["user_id"] = user["id"]
            session["user_name"] = user["name"]

            return redirect("/chat")

        flash("Invalid Credentials")

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():

    session.clear()

    return redirect("/login")