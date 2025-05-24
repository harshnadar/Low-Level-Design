from flask import Blueprint

api_bp = Blueprint('api', __name__)

from .ping import *
from .auth import *
from .tasks import *