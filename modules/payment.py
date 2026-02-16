# modules/payment.py

import razorpay
from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from config import RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET
from db import get_db

payment_bp = Blueprint("payment", __name__)

client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))


# =========================
# Create Razorpay Order
# =========================
@payment_bp.route("/create-payment", methods=["POST"])
def create_payment():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    amount = float(request.json["amount"]) * 100  # Convert to paise

    razorpay_order = client.order.create({
        "amount": int(amount),
        "currency": "INR",
        "payment_capture": 1
    })

    return jsonify({
        "order_id": razorpay_order["id"],
        "razorpay_key": RAZORPAY_KEY_ID
    })


# =========================
# Verify Payment
# =========================
@payment_bp.route("/verify-payment", methods=["POST"])
def verify_payment():

    data = request.json

    try:
        client.utility.verify_payment_signature({
            "razorpay_order_id": data["razorpay_order_id"],
            "razorpay_payment_id": data["razorpay_payment_id"],
            "razorpay_signature": data["razorpay_signature"]
        })

        conn = get_db()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO payments 
            (order_id, user_id, razorpay_payment_id, razorpay_order_id, razorpay_signature, amount, status)
            VALUES (%s,%s,%s,%s,%s,%s,%s)
        """, (
            data["order_id"],
            session["user_id"],
            data["razorpay_payment_id"],
            data["razorpay_order_id"],
            data["razorpay_signature"],
            data["amount"]/100,
            "Success"
        ))

        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"status": "success"})

    except:
        return jsonify({"status": "failed"})



#/------------admin payment history/-----------

@payment_bp.route("/admin/payment")
def admin_payment():
    conn = get_db()
    cur = conn.cursor(dictionary=True)

    cur.execute("""
        SELECT p.*, u.username 
        FROM payments p
        JOIN users u ON p.user_id = u.id
        ORDER BY p.created_at DESC
    """)

    payments = cur.fetchall()

    cur.close()
    conn.close()

    return render_template("admin/payment.html", payments=payments)
