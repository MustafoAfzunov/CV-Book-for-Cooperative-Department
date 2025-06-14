# CVBOOK - Django Authentication API

Welcome to **CVBOOK**, a Django-based REST API for user authentication. This project provides a secure authentication system using JWT (JSON Web Tokens) with endpoints for user signup, signin, token refresh, and password management. This README provides an overview, setup instructions, API endpoints, and testing guidelines.

## Overview
CVBOOK is a Django application designed to handle user authentication with a custom user model. It leverages the `rest_framework_simplejwt` package for JWT-based authentication and includes email-based password reset functionality using Gmail's SMTP server.

## Features
- User signup with email and password.
- User signin with JWT token generation.
- Token refresh for extended sessions.
- Password reset via email link.
- Password reset confirmation with token validation.

## Prerequisites
- Python 3.10 or higher
- PostgreSQL (for the database)
- pip and virtualenv
- Postman (for manual API testing)
- Git (for version control)

## Installation
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/cvbook.git
   cd cvbook

   Set Up a Virtual Environment:
bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install Dependencies:
bash
pip install -r requirements.txt
Configure Environment Variables:

    Create a .env file in the project root:
    text

    SECRET_KEY=your_secret_key
    DB_NAME=cvbook
    DB_USER=cvbook_user
    DB_PASSWORD=secure_cvbook_password
    DB_HOST=localhost
    DB_PORT=5432
    EMAIL_HOST_USER=afzunov12@gmail.com
    EMAIL_HOST_PASSWORD=your_app_password  # 16-character App Password from Google
    DEFAULT_FROM_EMAIL=afzunov12@gmail.com
    Add .env to .gitignore to prevent committing sensitive data.

Apply Migrations:
bash
python manage.py migrate


Run the Development Server:
bash

    python manage.py runserver

Configuration

    Database: Uses PostgreSQL with a custom user model (authentication.CustomUser).
    Email: Configured to send password reset emails via Gmail’s SMTP server (smtp.gmail.com).
    JWT: Tokens are valid for 60 minutes (access) and 1 day (refresh).

API Endpoints

Below are the available authentication endpoints:
1. User Signup

    Endpoint: POST /api/auth/signup/
    Description: Registers a new user with email, password, first name, and last name.
    Request Body:
    json

{
    "username": "newuser",
    "email": "new@example.com",
    "password": "newpass123",
    "first_name": "New",
    "last_name": "User"
}
Response (200 OK):
json

    {
        "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
        "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    }
    Error (400 Bad Request): Duplicate email or invalid data.

2. User Signin

    Endpoint: POST /api/auth/signin/
    Description: Authenticates a user and returns JWT tokens.
    Request Body:
    json

{
    "username": "afzunov12@gmail.com",
    "password": "testpass123"
}
Response (200 OK):
json

    {
        "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
        "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    }
    Error (401 Unauthorized): Invalid credentials.

3. Token Refresh

    Endpoint: POST /api/auth/token/refresh/
    Description: Refreshes the access token using a refresh token.
    Request Body:
    json

{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
Response (200 OK):
json

    {
        "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    }
    Error (400 Bad Request): Invalid or expired refresh token.

4. Password Reset

    Endpoint: POST /api/auth/password/reset/
    Description: Sends a password reset email to the user.
    Request Body:
    json

{
    "email": "afzunov12@gmail.com"
}
Response (200 OK):
json

    {
        "message": "Password reset link sent."
    }
    Error (400 Bad Request): Invalid email.

5. Password Reset Confirm

    Endpoint: POST /api/auth/password/reset/confirm/<uidb64>/<token>/
    Description: Confirms the password reset with a new password.
    Request Body:
    json

{
    "new_password": "newpass123"
}
Response (200 OK):
json
{
    "message": "Password has been reset successfully."
}
Error (400 Bad Request): Invalid token or password.
