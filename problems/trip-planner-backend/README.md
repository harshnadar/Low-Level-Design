# Trip Planner Backend

This is a Flask-based backend application for a trip planner. It allows users to manage trips and their associated itineraries. The application provides a RESTful API for creating, retrieving, updating, and deleting trips and itineraries.

## Project Structure

```
trip-planner-backend
├── app.py
├── models
│   ├── __init__.py
│   ├── trip.py
│   └── itinerary.py
├── repositories
│   ├── __init__.py
│   ├── base_repository.py
│   ├── trip_repository.py
│   └── itinerary_repository.py
├── routes
│   ├── __init__.py
│   ├── trips.py
│   └── itineraries.py
├── data
│   ├── trips.json
│   └── itineraries.json
├── utils
│   ├── __init__.py
│   └── json_handler.py
├── requirements.txt
├── config.py
└── README.md
```

## Requirements

To run this application, you need to install the following dependencies:

- Flask

You can install the required packages using the following command:

```
pip install -r requirements.txt
```

## API Endpoints

### Trips

- **GET /trips**: Retrieve all trips
- **POST /trips**: Create a new trip
- **GET /trips/<id>**: Retrieve a specific trip
- **PUT /trips/<id>**: Update a specific trip
- **DELETE /trips/<id>**: Delete a specific trip

### Itineraries

- **GET /itineraries**: Retrieve all itineraries
- **POST /itineraries**: Create a new itinerary
- **GET /itineraries/<id>**: Retrieve a specific itinerary
- **PUT /itineraries/<id>**: Update a specific itinerary
- **DELETE /itineraries/<id>**: Delete a specific itinerary

## Usage

1. Clone the repository to your local machine.
2. Navigate to the project directory.
3. Install the required dependencies.
4. Run the application using the command:

```
python app.py
```

5. Use a tool like Postman or curl to interact with the API endpoints.

## Data Persistence

The application uses JSON files for data persistence. The trips are stored in `data/trips.json` and the itineraries are stored in `data/itineraries.json`. The repository layer handles the loading and saving of data to these files.

## License

This project is licensed under the MIT License.