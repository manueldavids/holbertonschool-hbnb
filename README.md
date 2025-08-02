# Holberton School HBNB

A comprehensive Airbnb-like web application built with Flask and Flask-RESTX, featuring a RESTful API with Swagger documentation and a modern frontend.

## 🚀 Quick Start

### Option 1: Automatic Script (Recommended)
```bash
# Run both backend and frontend automatically
./run_part4.sh
```

### Option 2: Python Script
```bash
# Run both backend and frontend automatically
python3 run_app.py
```

### Option 3: Manual (Two Terminals)
```bash
# Terminal 1: Start Backend API (Part 3)
./start_backend.sh

# Terminal 2: Start Frontend (Part 4)
./start_frontend.sh
```

## 🌐 Application URLs

Once running, you can access:

- **Frontend**: http://localhost:8000 (or 8001 if 8000 is busy)
- **Backend API**: http://localhost:5000
- **API Documentation**: http://localhost:5000/api/v1/swagger

## 📁 Project Structure

```
holbertonschool-hbnb/
├── part1/                          # Project documentation and diagrams
├── part2/                          # Initial API implementation
├── part3/                          # Complete backend API with database
│   ├── app/                        # Flask application
│   ├── api/                        # REST API endpoints
│   ├── migrations/                 # Database migrations
│   └── run.py                      # Application entry point
├── part4/                          # Frontend web application
│   ├── index.html                  # Main page
│   ├── login.html                  # Login page
│   ├── place.html                  # Place details page
│   ├── add_review.html             # Add review page
│   ├── scripts.js                  # JavaScript functionality
│   ├── styles/                     # CSS styles
│   └── images/                     # Website images
├── run_app.py                      # Python script to run both services
├── run_part4.sh                    # Shell script to run both services
├── start_backend.sh                # Script to start backend only
├── start_frontend.sh               # Script to start frontend only
└── README.md                       # This file
```

## 🔧 Features

### Backend API (Part 3)
- **RESTful API** with comprehensive CRUD operations
- **JWT Authentication** for secure user sessions
- **SQLAlchemy ORM** with SQLite database
- **Swagger Documentation** for easy API exploration
- **CORS Configuration** for frontend integration
- **Input Validation** and error handling
- **Modular Architecture** with clear separation of concerns

### Frontend (Part 4)
- **Modern Web Interface** with responsive design
- **User Authentication** with JWT tokens
- **Place Browsing** with filtering capabilities
- **Interactive UI** with smooth navigation
- **Real-time API Integration** with backend
- **Demo Mode** for non-authenticated users

## 📋 API Endpoints

### Authentication
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/refresh` - Refresh JWT token
- `POST /api/v1/auth/logout` - User logout

### Users
- `POST /api/v1/users/register` - User registration
- `GET /api/v1/users/search` - Search users
- `GET /api/v1/users/admin/<status>` - Get users by admin status

### Places
- `GET /api/v1/places/` - Get all places
- `POST /api/v1/places/` - Create a new place
- `GET /api/v1/places/<id>` - Get place details
- `PUT /api/v1/places/<id>` - Update place
- `DELETE /api/v1/places/<id>` - Delete place

### Reviews
- `GET /api/v1/reviews/` - Get all reviews
- `POST /api/v1/reviews/` - Create a new review
- `GET /api/v1/reviews/<id>` - Get review details
- `PUT /api/v1/reviews/<id>` - Update review
- `DELETE /api/v1/reviews/<id>` - Delete review
- `GET /api/v1/reviews/place/<place_id>` - Get reviews for a place

### Admin (Admin users only)
- `POST /api/v1/admin/users` - Create user (admin)
- `GET /api/v1/admin/users` - Get all users (admin)
- `PUT /api/v1/admin/users/<id>` - Update user (admin)
- `DELETE /api/v1/admin/users/<id>` - Delete user (admin)
- `POST /api/v1/admin/amenities` - Create amenity (admin)
- `GET /api/v1/admin/amenities` - Get all amenities (admin)
- `PUT /api/v1/admin/amenities/<id>` - Update amenity (admin)
- `DELETE /api/v1/admin/amenities/<id>` - Delete amenity (admin)

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Setup Instructions

1. **Clone the repository**
```bash
git clone <repository-url>
cd holbertonschool-hbnb
```

2. **Install backend dependencies**
```bash
cd part3
pip install -r requirements.txt
pip install requests
cd ..
```

3. **Initialize database (optional)**
```bash
cd part3
python3 -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all()"
cd ..
```

## 🚀 Usage

### Running the Complete Application

The easiest way to run the complete application is using the automatic scripts:

```bash
# Option 1: Shell script
./run_part4.sh

# Option 2: Python script
python3 run_app.py
```

### Running Individual Components

If you want to run components separately:

```bash
# Backend API only
./start_backend.sh

# Frontend only (in another terminal)
./start_frontend.sh
```

### Manual Execution

```bash
# Terminal 1: Backend
cd part3
python3 run.py

# Terminal 2: Frontend
cd part4
python3 -m http.server 8000
```

## 🧪 Testing

### API Testing
You can test the API endpoints using the Swagger UI:
- Visit: http://localhost:5000/api/v1/swagger

### Frontend Testing
- Open http://localhost:8000 in your browser
- Try the login functionality
- Browse places and test filters

### Manual API Testing with cURL

```bash
# Test login
curl -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password123"}'

# Test getting places (with token)
curl -X GET http://localhost:5000/api/v1/places/ \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## 🔧 Configuration

### Backend Configuration
The backend uses a configuration system in `part3/app/config.py`:

- **Development Mode**: Debug enabled
- **Database**: SQLite by default (configurable)
- **JWT**: Configurable expiration times
- **CORS**: Configured for frontend integration

### Frontend Configuration
The frontend connects to the backend via:

- **API Base URL**: http://localhost:5000/api/v1
- **CORS**: Configured to allow frontend requests
- **Authentication**: JWT token-based

## 🐛 Troubleshooting

### Common Issues

1. **Port already in use**
   - Stop any existing services on ports 5000 and 8000
   - The scripts will automatically use alternative ports if needed

2. **Database errors**
   - Ensure the database is initialized: `python3 -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all()"`

3. **CORS errors**
   - Verify the backend is running on port 5000
   - Check that CORS is properly configured in the backend

4. **Authentication issues**
   - Ensure users exist in the database
   - Check JWT token expiration

### Debug Mode

To run in debug mode:

```bash
# Backend with debug
cd part3
FLASK_ENV=development python3 run.py

# Frontend with debug (check browser console)
cd part4
python3 -m http.server 8000
```

## 📊 Technologies Used

### Backend
- **Flask 2.3.3** - Web framework
- **Flask-RESTX** - API framework with Swagger
- **SQLAlchemy** - ORM for database operations
- **Flask-JWT-Extended** - JWT authentication
- **Flask-CORS** - Cross-origin resource sharing
- **Flask-Bcrypt** - Password hashing
- **Alembic** - Database migrations

### Frontend
- **HTML5** - Structure
- **CSS3** - Styling
- **JavaScript (ES6+)** - Interactivity
- **Fetch API** - HTTP requests
- **Local Storage/Cookies** - Session management

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test both backend and frontend
5. Submit a pull request

## 📄 License

This project is part of the Holberton School curriculum.

## 👨‍💻 Author

Created as part of Holberton School's software engineering program.

---

**Note**: This is an educational project demonstrating full-stack web development with Flask backend and modern frontend integration. 