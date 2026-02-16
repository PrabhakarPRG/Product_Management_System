from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from db import get_db
from utils.email_utils import generate_otp, send_otp_email

auth_bp = Blueprint("auth", __name__, url_prefix="")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        db = get_db()
        cur = db.cursor(dictionary=True)
        cur.execute("SELECT * FROM users WHERE username=%s", (username,))
        user = cur.fetchone()

        if not user:
            flash("User not found", "danger")
            return redirect(url_for("auth.login"))

        if user["password"] != password:
            flash("Incorrect password", "danger")
            return redirect(url_for("auth.login"))

        otp = generate_otp()
        session["otp"] = otp
        session["otp_user"] = user["id"]

        send_otp_email(user["email"], otp)

        flash("OTP sent to your email", "success")
        return redirect(url_for("auth.verify_otp"))

    return render_template("auth/login.html")


@auth_bp.route("/verify-otp", methods=["GET", "POST"])
def verify_otp():
    if "otp" not in session:
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        entered_otp = request.form.get("otp")

        if entered_otp == session.get("otp"):
            user_id = session.get("otp_user")

            db = get_db()
            cur = db.cursor(dictionary=True)
            cur.execute("SELECT * FROM users WHERE id=%s", (user_id,))
            user = cur.fetchone()

            session.clear()
            session["user_id"] = user["id"]
            session["role"] = user["role"]

            flash("Login successfull", "success")

            if user["role"] == "admin":
                return redirect("/admin/dashboard")
            else:
                return redirect("/user/dashboard")

        flash("Invalid OTP", "danger")

    return render_template("auth/verify_otp.html")


@auth_bp.route("/resend-otp")
def resend_otp():
    if "otp_user" not in session:
        return redirect(url_for("auth.login"))

    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT email FROM users WHERE id=%s", (session["otp_user"],))
    user = cur.fetchone()

    otp = generate_otp()
    session["otp"] = otp
    send_otp_email(user["email"], otp)

    flash("OTP resent successfully", "info")
    return redirect(url_for("auth.verify_otp"))


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")

        db = get_db()
        cur = db.cursor()
        cur.execute(
            "INSERT INTO users (username, password, email, role) VALUES (%s,%s,%s,'user')",
            (username, password, email)
        )
        db.commit()

        flash("Registration successful. Please login.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))
