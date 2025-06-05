from repositories.base_repository import BaseRepository
from config import Config

class TripRepository(BaseRepository):
    def __init__(self):
        super().__init__(Config.TRIPS_FILE)