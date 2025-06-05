from flask import Flask
import os

class Config:
    DEBUG = True
    JSON_SORT_KEYS = False
    # DATA_PATH = '/trip-planner-backend/data/'  # Path to the data directory
    # TRIPS_FILE = DATA_PATH + 'trips.json'  # Path to the trips JSON file
    # ITINERARIES_FILE = DATA_PATH + 'itineraries.json'  # Path to the itineraries JSON file
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR = os.path.join(BASE_DIR, 'data')
    TRIPS_FILE = os.path.join(DATA_DIR, 'trips.json')
    ITINERARIES_FILE = os.path.join(DATA_DIR, 'itineraries.json')


app = Flask(__name__)
app.config.from_object(Config)