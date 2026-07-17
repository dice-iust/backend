# TripTide – Travel Companion Platform

TripTide is a collaborative travel planning platform that enables users to organize trips, manage itineraries, communicate with travel companions, and coordinate travel activities.

This project was developed as part of a university software engineering course using **Django REST Framework** for the backend. The platform follows a RESTful architecture and supports secure authentication, real-time communication, and cloud deployment.

## Features

- User registration and authentication using JWT
- User profile management
- Profile editing
- Travel creation and management
- Trip planning
- Participant management
- Real-time chat functionality
- Media upload and management
- Filtering support for API endpoints
- RESTful API architecture
- Cloud deployment on Liara

## Tech Stack

### Backend

- Python
- Django
- Django REST Framework
- Django Channels
- Daphne (ASGI)
- Gunicorn

### Database

- MySQL

### Authentication

- JWT Authentication (SimpleJWT)

### Real-Time Communication

- Django Channels
- Redis

### Deployment

- Liara Cloud
- WhiteNoise

### Tools

- Git
- GitHub
- Postman

## Project Structure

```text
BackEnd_TravelPlanning/
│
├── Landing/
├── Travels/
├── planner/
├── signup/
├── profilepage/
├── editprofile/
├── chat/
├── media/
│
├── manage.py
├── requirements.txt
└── BackEnd_TravelPlanning/
```

## Installation

Clone the repository:

```bash
git clone https://github.com/dice-iust/backend.git
```

Navigate to the project directory:

```bash
cd backend
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment.

**Windows**

```bash
venv\Scripts\activate
```

**Linux / macOS**

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Apply database migrations:

```bash
python manage.py migrate
```

Run the development server:

```bash
python manage.py runserver
```

## Authentication

The project uses **JWT Authentication** via Django REST Framework SimpleJWT.

Authenticated API endpoints require a valid JWT access token.

## Real-Time Communication

Real-time messaging is implemented using:

- Django Channels
- Redis Channel Layer
- Daphne (ASGI Server)

This enables instant communication between travel participants.

## Deployment

The backend application is configured for deployment on **Liara Cloud** using:

- Gunicorn
- WhiteNoise
- Liara Build Configuration

## Development Team

This project was developed by a **six-member Agile software development team**.

- 4 Frontend Developers
- 2 Backend Developers

Development was managed through a GitHub Organization with separate repositories for frontend and backend services, enabling collaborative development and version control.

## Future Improvements

Potential future enhancements include:

- Push notifications
- Trip recommendation system
- Expense management
- Google Maps integration
- Email verification
- Social login
- API documentation (Swagger/OpenAPI)
- Docker support
- CI/CD pipeline

## License

This project was developed for educational purposes as part of a university software engineering course.
