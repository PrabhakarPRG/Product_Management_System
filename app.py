from flask import Flask, render_template, redirect, url_for, session, jsonify
from config import SECRET_KEY
from db import get_db

# Import modules
from modules.auth import auth_bp
from modules.products import products_bp
from modules.cart import cart_bp
from modules.categories import categories_bp
from modules.orders import orders_bp
from modules.payment import payment_bp

app = Flask(__name__)
app.secret_key = SECRET_KEY

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(products_bp)
app.register_blueprint(cart_bp)
app.register_blueprint(categories_bp)
app.register_blueprint(orders_bp)
app.register_blueprint(payment_bp)

# -------------------------
# HOME
# -------------------------
@app.route("/")
def home():
    return redirect(url_for("auth.login"))


# -------------------------
# ADMIN DASHBOARD
# -------------------------
@app.route("/admin/dashboard")
def admin_dashboard():
    if session.get("role") != "admin":
        return redirect("/login")

    db = get_db()
    cur = db.cursor()

    cur.execute("SELECT COUNT(*) FROM products")
    total_products = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM orders")
    total_orders = cur.fetchone()[0]

    cur.execute("SELECT IFNULL(SUM(total_amount),0) FROM orders")
    revenue = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM products WHERE stock < 5")
    low_stock = cur.fetchone()[0]

    return render_template(
        "admin/dashboard.html",
        total_products=total_products,
        total_orders=total_orders,
        revenue=revenue,
        low_stock=low_stock
    )


@app.route("/admin/dashboard")
def admin_stats():
    if session.get("role") != "admin":
        return redirect(url_for("auth.login"))

    db = get_db()
    cur = db.cursor()

    cur.execute("SELECT COUNT(*) FROM products")
    total_products = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM users")
    total_users = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM orders")
    total_orders = cur.fetchone()[0]

    cur.execute("SELECT IFNULL(SUM(total_amount),0) FROM orders")
    revenue = cur.fetchone()[0]

    return render_template(
        "admin/dashboard.html",
        total_products=total_products,
        total_users=total_users,
        total_orders=total_orders,
        revenue=revenue
    )

@app.route("/api/admin/sales")
def admin_sales():
    if session.get("role") != "admin":
        return jsonify({})

    # Demo data (replace with real query later)
    return jsonify({
        "months": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
        "sales": [12000, 18000, 15000, 22000, 30000, 35000]
    })


# -------------------------
# USER DASHBOARD
# -------------------------
@app.route("/user/dashboard")
def user_dashboard():
    if session.get("role") != "user":
        return redirect(url_for("auth.login"))
    return render_template("user/dashboard.html")


@app.route("/api/user/stats")
def user_stats():
    if "user_id" not in session:
        return jsonify({})

    user_id = session["user_id"]
    db = get_db()
    cur = db.cursor()

    cur.execute("SELECT COUNT(*) FROM orders WHERE user_id=%s", (user_id,))
    orders = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM cart WHERE user_id=%s", (user_id,))
    cart_items = cur.fetchone()[0]

    return jsonify({
        "orders": orders,
        "cart": cart_items
    })


# -------------------------
# COMMON ROUTES
# -------------------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))


# -------------------------
# RUN SERVER
# -------------------------
if __name__ == "__main__":
    app.run()
