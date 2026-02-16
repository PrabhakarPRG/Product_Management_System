from flask import Blueprint, session, request, redirect, url_for, render_template, jsonify, flash
from db import get_db

cart_bp = Blueprint('cart', __name__)

# =========================
# ADD TO CART
# =========================

@cart_bp.route("/cart/add", methods=["POST"])
def add_to_cart():

    if "user_id" not in session:
        return jsonify({"success": False, "message": "Login required"})

    data = request.get_json()

    product_id = data.get("product_id")
    quantity = data.get("quantity", 1)

    if not product_id:
        return jsonify({"success": False, "message": "Product ID missing"})

    user_id = session["user_id"]

    db = get_db()
    cur = db.cursor(dictionary=True)

    # Check existing cart item
    cur.execute("""
        SELECT * FROM cart 
        WHERE user_id=%s AND product_id=%s
    """, (user_id, product_id))

    existing = cur.fetchone()

    if existing:
        cur.execute("""
            UPDATE cart 
            SET quantity = quantity + %s
            WHERE user_id=%s AND product_id=%s
        """, (quantity, user_id, product_id))
    else:
        cur.execute("""
            INSERT INTO cart (user_id, product_id, quantity)
            VALUES (%s, %s, %s)
        """, (user_id, product_id, quantity))

    db.commit()
    cur.close()

    return jsonify({"success": True})


# =========================
# VIEW CART
# =========================
@cart_bp.route('/cart')
def view_cart():

    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    user_id = session['user_id']

    db = get_db()
    cur = db.cursor(dictionary=True)

    cur.execute("""
        SELECT c.id as cart_id, c.quantity,
               p.name, p.price, p.image
        FROM cart c
        JOIN products p ON c.product_id = p.id
        WHERE c.user_id = %s
    """, (user_id,))

    items = cur.fetchall()

    total = sum(item['price'] * item['quantity'] for item in items)

    cur.close()
    db.close()

    return render_template("user/cart.html", items=items, total=total)



# ---------------- CHECKOUT ----------------
@cart_bp.route('/checkout', methods=['POST'])
def checkout():
    if 'user_id' not in session:
        return redirect('/login')

    user_id = session['user_id']

    db = get_db()
    cur = db.cursor(dictionary=True)

    # Get cart items
    cur.execute("""
        SELECT c.product_id, c.quantity, p.price
        FROM cart c
        JOIN products p ON c.product_id = p.id
        WHERE c.user_id = %s
    """, (user_id,))
    cart_items = cur.fetchall()

    if not cart_items:
        flash("Cart is empty!")
        return redirect('/cart')

    # Calculate total
    total_amount = sum(item['price'] * item['quantity'] for item in cart_items)

    # Create order
    cur.execute("""
        INSERT INTO orders (user_id, total_amount, status)
        VALUES (%s, %s, 'Pending')
    """, (user_id, total_amount))
    db.commit()

    order_id = cur.lastrowid

    # Insert order items
    for item in cart_items:
        cur.execute("""
            INSERT INTO order_items (order_id, product_id, quantity, price)
            VALUES (%s, %s, %s, %s)
        """, (
            order_id,
            item['product_id'],
            item['quantity'],
            item['price']
        ))

    # Clear cart
    cur.execute("DELETE FROM cart WHERE user_id = %s", (user_id,))
    db.commit()

    cur.close()
    db.close()

    flash("Order placed successfully!")
    return redirect('/my_orders')
