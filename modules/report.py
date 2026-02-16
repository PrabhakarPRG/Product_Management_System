from flask import Blueprint, render_template, session, redirect
report_bp = Blueprint("report", __name__)

@report_bp.route("/admin/reports")
def reports():
    if session.get("role") != "admin":
        return redirect("/login")
    return render_template("admin/reports.html")
