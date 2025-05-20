from flask import Blueprint, render_template

home_bp = Blueprint('home', __name__)
store_warehouse_bp = Blueprint('warehouse', __name__)

@home_bp.route("/")
def home():
    return render_template("index.html")

@store_warehouse_bp.route('/store-warehouse')
def store_warehouse():
    return render_template('Progress.html')