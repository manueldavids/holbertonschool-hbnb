# Holberton School HBNB

A comprehensive Airbnb-like web application built with Flask and Flask-RESTX, featuring a RESTful API with Swagger documentation.

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [API Documentation](#api-documentation)
- [Installation](#installation)
- [Usage](#usage)
- [Testing](#testing)
- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)

## Project Overview

HBNB is a web application that provides a RESTful API for managing users, places, amenities, and reviews. The application follows a layered architecture pattern with a Facade design pattern for simplified data access.

### Key Features:
- **RESTful API** with comprehensive CRUD operations
- **Swagger Documentation** for easy API exploration
- **In-Memory Data Storage** with UUID-based identification
- **Input Validation** and error handling
- **Modular Architecture** with clear separation of concerns

## Features

### Core Functionality
- **User Management**: Create, read, update users with email validation
- **Place Management**: Manage rental properties with location and pricing
- **Amenity Management**: Handle property amenities and features
- **Review System**: User reviews and ratings for places
- **Relationship Management**: Connect users, places, amenities, and reviews

### Technical Features
- **UUID-based IDs**: Secure and unique identifier generation
- **Data Validation**: Input validation with proper error responses
- **HTTP Status Codes**: Proper REST API status code implementation
- **JSON Responses**: Consistent JSON response format
- **Error Handling**: Comprehensive error handling and user feedback

## API Documentation

### Base URL
```
http://127.0.0.1:5000/api/v1
```

### Available Endpoints

#### Users (`/users`)
- `GET /users/` - Get all users
- `POST /users/` - Create a new user
- `GET /users/<user_id>` - Get user by ID
- `PUT /users/<user_id>` - Update user

#### Amenities (`/amenities`)
- `GET /amenities/` - Get all amenities
- `POST /amenities/` - Create a new amenity
- `GET /amenities/<amenity_id>` - Get amenity by ID
- `PUT /amenities/<amenity_id>` - Update amenity

#### Places (`/places`)
- `GET /places/` - Get all places
- `POST /places/` - Create a new place
- `GET /places/<place_id>` - Get place by ID with details
- `PUT /places/<place_id>` - Update place
- `GET /places/<place_id>/reviews` - Get reviews for a place

#### Reviews (`/reviews`)
- `GET /reviews/` - Get all reviews
- `POST /reviews/` - Create a new review
- `GET /reviews/<review_id>` - Get review by ID
- `PUT /reviews/<review_id>` - Update review
- `DELETE /reviews/<review_id>` - Delete review
- `GET /reviews/places/<place_id>/reviews` - Get reviews for a place

### Interactive API Documentation
Access the Swagger UI at: `http://127.0.0.1:5000/api/v1/`

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Setup Instructions

1. **Clone the repository**
```bash
git clone <repository-url>
cd holbertonschool-hbnb
```

2. **Navigate to the project directory**
```bash
cd part2/hbnb
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the application**
```bash
python run.py
```

The application will start on `http://127.0.0.1:5000`

## Usage

### Starting the Server
```bash
python run.py
```

### Example API Calls

#### Create a User
```bash
curl -X POST http://127.0.0.1:5000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -d '{"first_name": "John", "last_name": "Doe", "email": "john@example.com"}'
```

#### Create an Amenity
```bash
curl -X POST http://127.0.0.1:5000/api/v1/amenities/ \
  -H "Content-Type: application/json" \
  -d '{"name": "WiFi"}'
```

#### Create a Place
```bash
curl -X POST http://127.0.0.1:5000/api/v1/places/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Beautiful Apartment",
    "description": "Cozy place in downtown",
    "price": 150.0,
    "latitude": 40.7128,
    "longitude": -74.0060,
    "owner_id": "user-uuid-here",
    "amenities": ["amenity-uuid-here"]
  }'
```

#### Create a Review
```bash
curl -X POST http://127.0.0.1:5000/api/v1/reviews/ \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Great place to stay!",
    "rating": 5,
    "user_id": "user-uuid-here",
    "place_id": "place-uuid-here"
  }'
```

## Testing

### Manual Testing with cURL

The project includes comprehensive testing capabilities. You can test all endpoints using the provided curl commands:

1. **Test User Endpoints**
```bash
# Get all users
curl -X GET http://127.0.0.1:5000/api/v1/users/

# Create a user
curl -X POST http://127.0.0.1:5000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -d '{"first_name": "Test", "last_name": "User", "email": "test@example.com"}'
```

2. **Test Place Endpoints**
```bash
# Get all places
curl -X GET http://127.0.0.1:5000/api/v1/places/

# Get place details
curl -X GET http://127.0.0.1:5000/api/v1/places/<place-id>
```

### Automated Testing
Refer to `TESTING_REPORT.md` for detailed testing documentation and results.

## Project Structure

```
holbertonschool-hbnb/
├── part1/                          # Project documentation and diagrams
│   ├── BusinessLogicLayer.png
│   ├── High-LevelPackageDiagram.png
│   ├── PlaceCreation.png
│   ├── RetrievePlacesbyCity.png
│   ├── SummitAReview.png
│   ├── UserRegristation.png
│   └── README.md
├── part2/                          # Main application
│   └── hbnb/
│       ├── app/                    # Application core
│       │   ├── __init__.py         # Flask app initialization
│       │   ├── api/                # API endpoints
│       │   │   └── v1/
│       │   │       ├── users.py    # User endpoints
│       │   │       ├── places.py   # Place endpoints
│       │   │       ├── amenities.py # Amenity endpoints
│       │   │       └── reviews.py  # Review endpoints
│       │   ├── models/             # Data models
│       │   │   ├── base_model.py   # Base model class
│       │   │   ├── user.py         # User model
│       │   │   ├── place.py        # Place model
│       │   │   ├── amenity.py      # Amenity model
│       │   │   └── review.py       # Review model
│       │   ├── services/           # Business logic
│       │   │   └── facade.py       # Facade pattern implementation
│       │   └── persistence/        # Data persistence
│       │       └── repository.py   # In-memory repository
│       ├── config.py               # Configuration settings
│       ├── run.py                  # Application entry point
│       ├── requirements.txt        # Python dependencies
│       ├── README.md               # Project documentation
│       └── TESTING_REPORT.md       # Testing documentation
└── README.md                       # Main project README
```

## Technologies Used

- **Backend Framework**: Flask 2.3.3
- **API Framework**: Flask-RESTX 1.1.0
- **Documentation**: Swagger/OpenAPI
- **Data Storage**: In-Memory Repository
- **Language**: Python 3.12
- **Architecture**: Facade Pattern, Layered Architecture

## API Response Format

### Success Response
```json
{
  "id": "uuid-string",
  "field1": "value1",
  "field2": "value2"
}
```

### Error Response
```json
{
  "error": "Error message description"
}
```

## Configuration

The application uses a simple configuration system in `config.py`:

- **Development Mode**: Debug enabled
- **Secret Key**: Configurable via environment variable
- **Host**: 127.0.0.1 (localhost)
- **Port**: 5000

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is part of the Holberton School curriculum.

## Author

Created as part of Holberton School's software engineering program.

---

**Note**: This is an educational project demonstrating RESTful API development with Flask and proper software architecture patterns. 