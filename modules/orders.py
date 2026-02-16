from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for  
from db import get_db

orders_bp = Blueprint("orders", __name__)

# ================= ADMIN =================
@orders_bp.route("/admin/orders")
def admin_orders():
    db = get_db()
    cur = db.cursor(dictionary=True)

    cur.execute("""
        SELECT 
            o.id,
            u.username AS customer_name,
            u.email,
            o.status,
            o.created_at
        FROM orders o
        JOIN users u ON o.user_id = u.id
        ORDER BY o.created_at DESC
""")
    orders = cur.fetchall()

    for order in orders:
        cur.execute("""
            SELECT p.name, oi.quantity, oi.price
            FROM order_items oi
            JOIN products p ON p.id = oi.product_id
            WHERE oi.order_id = %s
        """, (order["id"],))
        order["items"] = cur.fetchall()

    return render_template("admin/orders.html", orders=orders)


@orders_bp.route("/admin/orders/update-status", methods=["POST"])
def update_order_status():
    data = request.json
    db = get_db()
    cur = db.cursor()

    cur.execute(
        "UPDATE orders SET status=%s WHERE id=%s",
        (data["status"], data["order_id"])
    )
    db.commit()
    return jsonify({"success": True})


# ================= USER =================

@orders_bp.route("/my_orders")
def user_orders():
    if "user_id" not in session:
        return redirect("/login")

    db = get_db()
    cur = db.cursor(dictionary=True)

    cur.execute("""
        SELECT o.id, o.total_amount, o.status, o.created_at
        FROM orders o
        WHERE o.user_id = %s
        ORDER BY o.created_at DESC
    """, (session["user_id"],))

    orders = cur.fetchall()

    cur.close()
    db.close()

    return render_template("user/my_orders.html", orders=orders)
