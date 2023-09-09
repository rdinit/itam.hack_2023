from flask import Blueprint, request
from .models import User
from . import db
from flask_login import login_user, login_required, logout_user


frontend = Blueprint('frontend', __name__)