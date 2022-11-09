from flask import Blueprint, render_template
from web_app.src.food_options import FoodOptions

home_routes = Blueprint("home_routes", __name__)


@home_routes.route("/")
@home_routes.route("/home")
def index():
    return render_template("index.html", data=FoodOptions())
