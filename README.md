# 📦 Celery-based Data Processing Application

A Python application that periodically fetches random user data from external APIs, stores it in a PostgreSQL database, and enriches it with address and credit card details — all orchestrated with **Celery** and **Redis**.

---

## 🚀 Features

- ✅ Periodic background jobs with Celery
- 📥 Fetch users from [Random Data API](https://random-data-api.com/)
- 🏦 Store in PostgreSQL
- 🗺️ Enrich with address & credit card info
- ⚙️ Managed with Docker Compose
- ✅ Tested with `pytest` and `requests-mock`

---

## 🛠️ Project Structure

```bash
.
├── app/                    # Application source code
├── tests/                  # Unit and integration tests
├── Dockerfile              # Main Dockerfile
├── Dockerfile.test         # Dockerfile for tests
├── docker-compose.yml      # Compose file for services
├── docker-compose.test.yml # Compose file for running tests
├── requirements.txt        # Project dependencies
├── .env.example            # Environment variables template
└── README.md
```

---

## ⚙️ Setup

1. **Clone the repo**
   ```bash
   git clone https://github.com/yourusername/project-name.git
   cd project-name


2. **Create .env file and fill credentials**
    ```bash
    cp .env.sample .env
    ```

---

## ▶️ Run the Application
```bash
  docker compose up --build
```

---

## 🧪 Run Tests
```bash
  docker compose -f docker-compose.test.yml up --build
```

---

## 🔒 Stopping Services
```bash
  docker compose down
```

---

## 🌐 Access
#### pgAdmin: http://localhost:5050
#### Use credentials from .env.