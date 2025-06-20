# HBnB API - Part 2

A RESTful API for the HBnB (Holberton School Airbnb Clone) application built with Flask and Flask-RESTx.

## Architecture

This application follows a layered architecture pattern:

- **Presentation Layer**: Flask-RESTx API endpoints
- **Business Logic Layer**: Facade pattern with service classes
- **Persistence Layer**: Repository pattern with in-memory storage

## Project Structure
hbnb/
├── app/
│ ├── api/v1/ # API endpoints (Presentation Layer)
│ │ ├── views/ # API route handlers
│ │ └── models.py # API schemas
│ ├── models/ # Data models
│ ├── services/ # Business logic (Facade)
│ └── persistence/ # Data access (Repository)
├── config.py # Configuration settings
├── run.py # Application entry point
├── init_data.py # Sample data initialization
├── test_api.py # API testing script
└── requirements.txt # Python dependencies

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

1. Start the Flask application:
   ```bash
   python run.py
   ```

2. The API will be available at:
   - Base URL: `http://localhost:5000`
   - API Documentation: `http://localhost:5000/api/v1/docs/`
   - Health Check: `http://localhost:5000/health`

## API Endpoints

### Users
- `GET /api/v1/users/` - List all users
- `POST /api/v1/users/` - Create a new user
- `GET /api/v1/users/<id>` - Get user by ID
- `PUT /api/v1/users/<id>` - Update user
- `DELETE /api/v1/users/<id>` - Delete user
- `POST /api/v1/users/login` - Authenticate user

### Places
- `GET /api/v1/places/` - List all places
- `POST /api/v1/places/` - Create a new place
- `GET /api/v1/places/<id>` - Get place by ID
- `PUT /api/v1/places/<id>` - Update place
- `DELETE /api/v1/places/<id>` - Delete place
- `GET /api/v1/places/search?name=<name>` - Search places
- `GET /api/v1/places/user/<user_id>` - Get user's places
- `POST /api/v1/places/<id>/amenities/<amenity_id>` - Add amenity to place
- `DELETE /api/v1/places/<id>/amenities/<amenity_id>` - Remove amenity from place

### Reviews
- `GET /api/v1/reviews/` - List all reviews
- `POST /api/v1/reviews/` - Create a new review
- `GET /api/v1/reviews/<id>` - Get review by ID
- `PUT /api/v1/reviews/<id>` - Update review
- `DELETE /api/v1/reviews/<id>` - Delete review
- `GET /api/v1/reviews/place/<place_id>` - Get place reviews
- `GET /api/v1/reviews/user/<user_id>` - Get user reviews

### Amenities
- `GET /api/v1/amenities/` - List all amenities
- `POST /api/v1/amenities/` - Create a new amenity
- `GET /api/v1/amenities/<id>` - Get amenity by ID
- `PUT /api/v1/amenities/<id>` - Update amenity
- `DELETE /api/v1/amenities/<id>` - Delete amenity
- `GET /api/v1/amenities/search?name=<name>` - Search amenities

## Testing

### Initialize Sample Data
```bash
python init_data.py
```

### Run API Tests
```bash
python test_api.py
```

### Manual Testing with curl

1. Create a user:
   ```bash
   curl -X POST http://localhost:5000/api/v1/users/ \
     -H "Content-Type: application/json" \
     -d '{"email": "test@example.com", "password": "password123", "first_name": "John", "last_name": "Doe"}'
   ```

2. Get all users:
   ```bash
   curl http://localhost:5000/api/v1/users/
   ```

3. Create a place:
   ```bash
   curl -X POST http://localhost:5000/api/v1/places/ \
     -H "Content-Type: application/json" \
     -d '{"name": "Test Place", "city_id": "city_001", "user_id": "USER_ID_HERE", "number_rooms": 2, "price_by_night": 100}'
   ```

## Features

- **RESTful API**: Complete CRUD operations for all entities
- **Input Validation**: Automatic validation of request data
- **Error Handling**: Proper HTTP status codes and error messages
- **Documentation**: Auto-generated API documentation with Swagger UI
- **Modular Architecture**: Clean separation of concerns
- **In-Memory Storage**: Fast development and testing
- **Extensible Design**: Easy to add new features and endpoints

## Design Patterns Used

- **Facade Pattern**: Simplifies complex subsystem interactions
- **Repository Pattern**: Abstracts data access layer
- **Factory Pattern**: Application factory for Flask
- **Strategy Pattern**: Configurable application settings

## Next Steps

This implementation provides a solid foundation for the HBnB application. Future enhancements could include:

- Database integration (SQLAlchemy, PostgreSQL)
- Authentication and authorization (JWT tokens)
- File upload for place images
- Advanced search and filtering
- Pagination for large datasets
- Rate limiting and caching
- Unit and integration tests

## License

This project is part of the Holberton School curriculum.