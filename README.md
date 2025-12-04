# 🚀 Social App API (Django + DRF)

A simple social media backend built with **Django**, **Django REST Framework**, and **JWT Authentication**.
Includes user registration/login, posts, likes, and comments.

---

## 📦 Features

- JWT Authentication (Login + Register)
- Create, Edit, Delete Posts
- Upload Images & Videos
- Like & Unlike Posts
- Comment on Posts
- Owner-based permissions
- Validation & Error Handling

---

# 📌 API Endpoints

## 🔐 Authentication

| Method | Endpoint | Description |
|--------|----------|--------------|
| **POST** | `/api/login/` | User login (email or username) |
| **POST** | `/api/register/` | User registration with profile upload |

---

## 📝 Posts

| Method | Endpoint | Description |
|--------|----------|--------------|
| **GET** | `/api/posts` | Get all posts |
| **POST** | `/api/posts/create` | Create a post (Auth required) |
| **PUT** | `/api/posts/<pk>/edit` | Edit a post (Owner only) |
| **DELETE** | `/api/posts/<pk>/delete` | Delete a post (Owner only) |

---

## ❤️ Likes

| Method | Endpoint | Description |
|--------|----------|--------------|
| **GET / POST** | `/api/like/<pk>` | Like or Unlike a post |

---

## 💬 Comments

| Method | Endpoint | Description |
|--------|----------|--------------|
| **POST** | `/api/comment/<pk>` | Add a comment to a post |

---

# 📌 Example Requests

## 🔐 Register User

**POST:** `/api/register/`  
Body (form-data):
```
username
email
password
confirm_password
profile (file)
```

---

## 🔐 Login

**POST:** `/api/login/`
```
{
  "username": "example",
  "password": "12345"
}
```

---

## 📝 Create Post

**POST:** `/api/posts/create`  
Headers:
```
Authorization: Bearer <token>
```
Body (multipart/form-data):
```
title
content
image (optional)
video (optional)
```

---

# ⚙️ Installation

```
python3 -m venv env or python -m venv env
source env/bin/activate(env\Scripts\activate on window)
git clone <repo-url>
cd project
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

---

# 🐳 Run Project by docker

```
docker pull khun90/social_app:v1
docker run --name webserver -dp 8000:8000 khun90/social_app:v1
```

---

# 🔒 Security Notes

- Passwords hashed securely
- JWT Authentication
- Permission checks
- Strict validation everywhere

---

# 📜 License

MIT License