from flask import Blueprint, render_template
from web_app.src.food_options import FoodOptions
from datetime import datetime

home_routes = Blueprint("home_routes", __name__)


@home_routes.route("/")
@home_routes.route("/home")
def index():
    now = datetime.now()
    current_time = now.strftime("%H%M")
    return render_template("index.html", data=FoodOptions(), time=current_time)
