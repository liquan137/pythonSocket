from flask import Blueprint

kf = Blueprint("kf", __name__)

from . import views
