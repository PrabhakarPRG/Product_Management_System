import os

UPLOAD_FOLDER = os.path.join("static", "uploads", "products")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}


SECRET_KEY = "final-year-secret-key"

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "ecommerce_db"
}

MAIL_SERVER = "smtp.gmail.com"
MAIL_PORT = 587
MAIL_USERNAME = "prabhakar9313@gmail.com"
MAIL_PASSWORD = "xqsx sabu mtkg lvdq"

RAZORPAY_KEY_ID = "rzp_test_SEststTLY6hPqb"
RAZORPAY_KEY_SECRET = "XJPJIQSytO5kkcA05qsGdt7Z"
