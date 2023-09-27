from flask import Blueprint
from ..src.controllers.user_controller import test

user_route = Blueprint("user_route", __name__)

user_route.route("/", methods=['GET'])(test)
