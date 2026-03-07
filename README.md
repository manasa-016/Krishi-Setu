# Krishi-Setu Backend

An agricultural technology (AgriTech) platform that connects farmers with vendors (buyers). It serves as a marketplace enabling farmers to sell their harvests directly to vendors, with features for location-based discovery, demand tracking, and price history analysis.

---

## Tech Stack

| Component | Technology |
|-----------|------------|
| **Framework** | FastAPI (Python) |
| **Database** | PostgreSQL with SQLAlchemy ORM |
| **Authentication** | JWT (JSON Web Tokens) with bcrypt password hashing |
| **Migration Tool** | Alembic |
| **Server** | Uvicorn (ASGI) |
| **Validation** | Pydantic |
| **Frontend Server** | Flask (for file uploads only) |
| **Email** | SMTP with environment variable configuration |
| **Push Notifications** | FCM (Firebase Cloud Messaging) support |

---

## Project Structure

```
Krishi-Setu_backend/
├── app/                          # Main FastAPI application
│   ├── main.py                  # FastAPI app initialization with CORS
│   ├── core/
│   │   ├── config.py            # Settings from .env
│   │   ├── database.py          # SQLAlchemy engine & session
│   │   └── security.py          # JWT, password hashing, auth guards
│   ├── models/                  # SQLAlchemy ORM models
│   │   ├── user.py              # User (farmer/vendor)
│   │   ├── farm.py              # Farm with GPS coordinates
│   │   ├── harvest.py           # Harvest listings
│   │   ├── demand.py            # Vendor demands
│   │   ├── transaction.py       # Purchase transactions
│   │   └── price_history.py     # Crop price tracking
│   ├── schemas/                 # Pydantic request/response models
│   ├── api/routes/              # API endpoints
│   │   ├── auth.py              # Register, login, profile
│   │   ├── harvest.py           # Harvest CRUD, nearby search
│   │   ├── demand.py            # Demand management
│   │   ├── transactions.py      # Transaction handling
│   │   └── prices.py            # Price history
│   └── services/
│       ├── distance_service.py  # Haversine formula for GPS
│       └── price_service.py     # Price change calculation
├── alembic/                     # Database migrations
├── app.py                       # Flask app for file uploads
├── main.py                      # Legacy FastAPI app (older version)
├── models.py                    # Legacy SQLAlchemy models
├── schemas.py                   # Legacy Pydantic schemas
├── config.py                    # Legacy config (root level)
├── database.py                  # Legacy database setup
├── requirements.txt             # Python dependencies
└── Dockerfile                   # Docker configuration
```

---

## Key Features

### 1. User Authentication
- JWT-based authentication with `OAuth2PasswordBearer`
- Password hashing using bcrypt
- Role-based access control (farmer/vendor)
- Register with email/phone and password
- Login with credentials

### 2. Farm Management
- Farmers can have multiple farms
- GPS coordinates (latitude/longitude) for each farm
- Used for distance-based harvest discovery

### 3. Harvest Management
- Farmers create harvest listings with:
  - Crop type, category (vegetables/fruits/flowers)
  - Quantity (kg), price per kg
  - Description
- Status tracking (available/sold)
- Location-based nearby harvest search (within 10km radius)

### 4. Demand System
- Vendors can post demand requirements
- Specify crop type, category, required quantity, offered price

### 5. Transactions
- Track purchases between vendors and farmers
- Status: pending/completed/cancelled

### 6. Price History
- Track historical prices for different crop types
- Calculate price changes (percentage)

### 7. Location Services
- Haversine formula for calculating distance between coordinates
- Find nearby harvests within 10km radius

---

## API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login
- `GET /auth/profile` - Get current user profile

### Harvests
- `POST /harvest/` - Create harvest (farmer only)
- `GET /harvest/` - List available harvests
- `GET /harvest/nearby/{lat}/{lng}` - Find nearby harvests

### Demands
- Managed via demand router

### Transactions
- Managed via transaction router

### Prices
- Price history endpoints

---

## Database Models

1. **User** - id (UUID), name, email, phone, password_hash, role, verified, created_at
2. **Farm** - id (UUID), farmer_id, name, location_lat, location_lng
3. **Harvest** - id (UUID), farmer_id, crop_type, category, quantity, price_per_kg, description, status, created_at
4. **Demand** - id (UUID), vendor_id, crop_type, category, required_quantity, offered_price, status, created_at
5. **Transaction** - id (UUID), harvest_id, vendor_id, status, created_at
6. **PriceHistory** - id (UUID), crop_type, price, created_at

---

## Configuration

Create a `.env` file in the root directory with the following variables:

```env
# Database
DATABASE_URL=postgresql://username:password@localhost:5432/krishi_setu

# JWT Settings
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Email (SMTP)
SENDER_EMAIL=your-email@gmail.com
APP_PASSWORD=your-app-password

# Firebase Cloud Messaging
FCM_SERVER_KEY=your-fcm-server-key
```

---

## Run Commands

### Prerequisites
- Python 3.11+
- PostgreSQL database

### Local Development

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Set up environment variables:**
Create a `.env` file (see Configuration section above)

3. **Run database migrations:**
```bash
alembic upgrade head
```

4. **Start the FastAPI server:**
```bash
uvicorn app.main:app --reload
```

The API will be available at: `http://localhost:8000`

5. **API Documentation:**
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Using Docker

1. **Build the Docker image:**
```bash
docker build -t krishi-setu-backend .
```

2. **Run the container:**
```bash
docker run -p 8000:8000 --env-file .env krishi-setu-backend
```

### Using Docker Compose

1. **Start all services:**
```bash
docker-compose up -d
```

---

## Testing

Run tests with pytest:
```bash
pytest
```

---

## License

This project is proprietary software developed for Krishi-Setu.
