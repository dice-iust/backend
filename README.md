# TripTide – Travel Companion Platform

TripTide is a collaborative travel planning platform that enables users to organize trips, manage itineraries, communicate with travel companions, and coordinate travel activities.

---

## Features

-  User registration and authentication using JWT
-  User profile management
-  Profile editing
-  Travel creation and management
-  Trip planning
-  Participant management
-  Real-time chat functionality
-  Media upload and management
-  Filtering support for API endpoints
-  RESTful API architecture
-  Cloud deployment on Liara

---

## Tech Stack

### Backend

- Python
- Django
- Django REST Framework
- Django Channels
- ASGI (Daphne)
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

---

## Project Structure

```
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

---

## Installation

Clone the repository

```bash
git clone https://github.com/dice-iust/backend.git
```

Move into the project directory

```bash
cd backend
```

Create a virtual environment

```bash
python -m venv venv
```

Activate the environment

Windows

```bash
venv\Scripts\activate
```

Linux / macOS

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run database migrations

```bash
python manage.py migrate
```

Start the development server

```bash
python manage.py runserver
```

---

## Authentication

The project uses **JWT Authentication** through Django REST Framework SimpleJWT.

Authenticated endpoints require a valid JWT access token.

---

## Real-Time Communication

The chat system is implemented using:

- Django Channels
- Redis Channel Layer
- ASGI Server (Daphne)

This enables real-time communication between users.


## Team

This project was developed by a **six-member Agile software development team**.

- 4 Frontend Developers
- 2 Backend Developers

Development was organized through a **GitHub Organization**, with separate repositories for frontend and backend development.

---

## Deployment

The backend was deployed on **Liara Cloud** using:

- Gunicorn
- WhiteNoise
- Liara Build Configuration

---

## Future Improvements

Potential future enhancements include:

- Push notifications
- Trip recommendation system
- Expense management
- Google Maps integration
- Email verification
- Social login
- API documentation with Swagger
- Docker support
- CI/CD pipeline

---

## License

This project was developed for educational purposes as part of a university software engineering project.

---
