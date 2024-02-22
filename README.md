# Web Service Assignment2

---
This is a Flask-based web service that provides URL shortening 
functionality and user authentication using JSON Web Tokens (JWT)

## Feature
* ***User Management*** : 
Users can register, change their passwords, and log in securely.
* ***URL Shortening***: 
Users can shorten long URLs into shorter, more manageable ones.
* ***Authentication***: 
Secure authentication using JWT ensures that only registered users can access certain endpoints.

### JWT and authorization
JWT module provides functions for creating and verifying JSON Web Tokens (JWTs). 
It includes functions for encoding and decoding data to/from base64,
creating JWTs with HMAC-SHA256 signature, and verifying the integrity of JWTs

### Micro-service and Docker
Using Dockerfile to contianerize our application.
1. **Build the Docker** Image: Navigate to the directory containing Dockerfile
```bash
docker build -t web_service_assignment2 -f Dockerfile.
```
2. **Run the Docker Container**
```BASH
docker run -p 5000:5000 web_service_assignment2
```

## Set up

```bash
set FLASK_ENV=development
python auth_and_url_short.py
```



