# CoreFlow – Mini ERP Backend

A lightweight ERP backend built with FastAPI and PostgreSQL, designed to manage customers, products, quotations, orders, invoices, and users with role-based access control.

---

## 🚀 Features

- JWT-based authentication and authorization
- Role management (`admin`, `employee`, `viewer`)
- Endpoints for full CRUD operations:
  - Users
  - Customers
  - Products
  - Quotations and items
  - Orders and items
  - Invoices and items
- Swagger UI auto-generated docs
- PostgreSQL integration with Docker
- Password hashing using `passlib`
- Strict PEP8-style Python code with full docstring coverage

---

## 🧱 Tech Stack

- Python 3.11+ (compatible up to 3.12 due to SQLAlchemy)
- FastAPI
- SQLAlchemy 2.x
- PostgreSQL 17
- Docker + Docker Compose
- JWT (via `jose`)
- Pydantic
- passlib
- python-dotenv

---

## 📦 Project Structure

```
coreflow/
├── app/
│   ├── database/
│   ├── models/
│   ├── routes/
│   ├── schemas/
│   ├── scripts/
│   ├── security/
│   └── services/
├── .env               # must be created manually
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## 🛠️ Getting Started

### 1. Create `.env` file

This file is **not included** in version control.  
Create it manually in the root directory:

```env
DATABASE_URL=postgresql+psycopg2://myuser:mypassword@db:5432/mydatabase
SECRET_KEY=your-super-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

### 2. Build and run with Docker Compose

```bash
docker-compose up --build
```

The API will be available at:  
👉 [http://localhost:8001/docs](http://localhost:8001/docs)

---

## 🔐 Authentication

All routes (except `/auth/login`) require a valid JWT token.

- Get token by posting to `/auth/login` with email & password (form).
- Use `"Bearer <your_token>"` in the `Authorization` header for all requests.

---

## 👤 Creating Your First Admin

On a fresh database, no users exist.  
To create the first admin:

- **Temporarily remove the `require_admin` dependency** from the `create_user` route
- Restart the backend
- POST to `/users/` with:

```json
{
  "name": "admin",
  "email": "admin@example.com",
  "password": "StrongPassword123!",
  "role": "admin"
}
```

Then re-activate the admin requirement in the route.

---

## 📈 API Documentation

- Swagger UI: [http://localhost:8001/docs](http://localhost:8001/docs)
- Redoc: [http://localhost:8001/redoc](http://localhost:8001/redoc)

---

## ✏️ Planned Features (v2 or v3)

- Frontend integration (React or similar)
- PDF generation for orders & invoices
- Email notifications
- Filtering, pagination
- Audit logging

---

## ✅ Status

This project is currently in **active backend development (v1)**.  
All backend services and routes are tested via Swagger.

---

## 🧪 Testing (planned)

Add tests using `pytest` in a future version.  
Structure will follow `tests/` folder with `pytest` fixtures and coverage reports.

---

## 📄 License

MIT License (or change to your preferred license)

---

## 🙌 Contributing

Coming soon. Feel free to fork and explore.
