from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from db import get_db
from werkzeug.utils import secure_filename
import os

products_bp = Blueprint('products', __name__)
UPLOAD_FOLDER = 'static/uploads/products'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@products_bp.route("/admin/products")
def admin_products():
    if session.get("role") != "admin":
        return redirect("/")

    db = get_db()
    cur = db.cursor(dictionary=True)

    # Fetch products
    cur.execute("""
        SELECT p.*, c.name AS category_name
        FROM products p
        LEFT JOIN categories c ON p.category_id = c.id
    """)
    products = cur.fetchall()

    # 🔥 FETCH CATEGORIES (THIS WAS MISSING)
    cur.execute("SELECT id, name FROM categories")
    categories = cur.fetchall()

    return render_template(
        "admin/products.html",
        products=products,
        categories=categories
    )


@products_bp.route('/admin/products/add', methods=['POST'])
def add_product():
    if session.get('role') != 'admin':
        return redirect('/')

    name = request.form['name']
    desc = request.form['description']
    price = request.form['price']
    stock = request.form['stock']
    image = request.files['image']
    category_id = request.form.get("category_id")
    
    if not category_id:
        category_id = None   # allow NULL


    filename = secure_filename(image.filename)
    image.save(os.path.join('static/uploads/products', filename))

    db = get_db()
    cur = db.cursor()
    cur.execute("""
      INSERT INTO products (name, description, price, stock, category_id, image)
      VALUES (%s,%s,%s,%s,%s,%s)
    """, (name, desc, price, stock, category_id, filename))
    
    db.commit()
    return redirect('/admin/products')

@products_bp.route('/admin/products/ajax/delete/<int:id>', methods=['DELETE'])
def ajax_delete_product(id):
    db = get_db()
    cur = db.cursor()
    cur.execute("DELETE FROM products WHERE id=%s", (id,))
    db.commit()

    return jsonify({'status': 'deleted'})


@products_bp.route("/shop")
def shop():
    if "user_id" not in session:
        return redirect("/login")

    db = get_db()
    cur = db.cursor(dictionary=True)

    cur.execute("""
        SELECT p.*, c.name AS category_name
        FROM products p
        LEFT JOIN categories c ON p.category_id = c.id
        ORDER BY p.created_at DESC
    """)

    products = cur.fetchall()

    cur.close()
    db.close()

    return render_template("user/shop.html", products=products)
