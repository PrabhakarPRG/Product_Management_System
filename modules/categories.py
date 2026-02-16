from flask import Blueprint, render_template, request, jsonify, redirect, session
from db import get_db

categories_bp = Blueprint('categories', __name__)

@categories_bp.route('/admin/categories')
def admin_categories():
    if session.get('role') != 'admin':
        return redirect('/')

    db = get_db()
    cur = db.cursor(dictionary=True)

    cur.execute("""
        SELECT c.id, c.name, c.icon,
               COUNT(p.id) AS product_count
        FROM categories c
        LEFT JOIN products p ON p.category_id = c.id
        GROUP BY c.id
        ORDER BY c.name
    """)
    categories = cur.fetchall()

    return render_template(
        'admin/categories.html',
        categories=categories
    )


@categories_bp.route("/admin/categories/add", methods=["POST"])
def add_category():
    if session.get("role") != "admin":
        return {"error": "Unauthorized"}, 403

    name = request.form.get("name")
    icon = request.form.get("icon")

    if not name:
        return {"error": "Category name required"}, 400

    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO categories (name, icon) VALUES (%s, %s)",
        (name, icon)
    )

    conn.commit()
    cur.close()
    conn.close()

    return {"success": True}


@categories_bp.route('/admin/categories/edit/<int:id>', methods=['POST'])
def edit_category(id):
    name = request.form['name']
    icon = request.form['icon']

    db = get_db()
    cur = db.cursor()
    cur.execute(
        "UPDATE categories SET name=%s, icon=%s WHERE id=%s",
        (name, icon, id)
    )
    db.commit()

    return jsonify(success=True)


@categories_bp.route('/admin/categories/delete/<int:id>', methods=['DELETE'])
def delete_category(id):
    db = get_db()
    cur = db.cursor()
    cur.execute("DELETE FROM categories WHERE id=%s", (id,))
    db.commit()

    return jsonify(success=True)
