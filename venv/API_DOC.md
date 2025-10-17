# Backend API Documentation

This document describes all backend endpoints for the Django project.

---

## 1. Account App

### 1.1 Register
- **URL:** `/api/account/register/`
- **Method:** POST
- **Body (JSON):**
```json
{
  "username": "your_username",
  "email": "your_email@example.com",
  "password": "your_password"
}

{
  "id": 1,
  "username": "your_username",
  "email": "your_email@example.com"
}

 ### 1.2 Login
- **URL:** `/api/account/login/`
- **Method:** POST
- **Body (JSON):**
```json
{
  "username": "your_username",
  "password": "your_password"
}
   {
  "refresh": "<refresh_token>",
  "access": "<access_token>",
  "last_login": "2025-10-16T17:30:00Z"
}

 ---

## 2. Varse App

### 2.1 Get Data
- **URL:** `/api/varse/data/`
- **Method:** GET
- **Headers:**
```text
Authorization: Bearer <access_token>

{
  "data": [
    {
      "id": 1,
      "name": "Sample Data",
      "value": "123"
    }
  ]
}

---

## 3. Running Backend Locally (if not hosted)

If the backend is not hosted online, the developer can run it locally:

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Apply database migrations
python manage.py migrate

# 3. Start the server
python manage.py runserver

http://127.0.0.1:8000/api/...

---

## 4. Notes and Tips

- All **account endpoints** are under `/api/account/`
- All **varse endpoints** are under `/api/varse/`
- JWT token is required for **protected endpoints**
- Include the token in headers as:  

- Replace `<access_token>` with the token returned from login.
- Make sure to run migrations before starting the server if running locally.
- The developer can test endpoints using tools like **Thunder Client** or **Postman**.
