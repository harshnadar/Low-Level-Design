from flask import Blueprint

trips_bp = Blueprint('trips', __name__)
itineraries_bp = Blueprint('itineraries', __name__)

from .trips import *
from .itineraries import *