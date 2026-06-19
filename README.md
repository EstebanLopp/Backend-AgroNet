# AgroNet — Agricultural E-Commerce Platform

A multi-role web platform for agricultural commerce built as a capstone
project during my Software Development program at SENA (Colombia).

---

## Overview

AgroNet connects agricultural producers with buyers through a structured
marketplace. The system supports three distinct user roles — customer,
seller, and administrator — each with its own interface and set of
features.

The project was developed as a formative exercise. The architecture
reflects decisions made by a team of students learning full-stack
development under real project constraints.

---

## Tech Stack

**Backend**
- Node.js + Express.js
- MySQL (relational database)
- REST API (JSON responses)

**Frontend**
- HTML5 + CSS3 + Vanilla JavaScript
- Component-based structure (no framework)

---

## Features by Role

**Guest (unauthenticated)**
- Browse product catalog by category
- View product details and seller profiles
- Account registration and login
- Password recovery via token

**Customer**
- Full product catalog with filtering
- Shopping cart management
- Order placement and purchase history
- Profile management and address book
- Messaging with sellers

**Seller**
- Product creation, editing, and deletion
- Inventory management (active/disabled products)
- Order management and history
- Store profile customization
- Sales reporting

**Admin**
- User management (create, edit, disable)
- Product moderation
- Category management
- Banner and homepage content control
- Order oversight
- Platform-level reports

---

## Project Structure

```
agronet/
├── backend/
│   ├── config/         # Database connection pool (MySQL)
│   ├── controllers/    # Route handlers
│   ├── routes/         # API route definitions
│   ├── models/         # Database query layer
│   ├── services/       # Business logic
│   ├── validations/    # Input validation
│   └── server.js       # Express server entry point
├── frontend/
│   └── public/
│       ├── views/
│       │   ├── pages-general/    # Public pages (login, catalog, register)
│       │   ├── customer-pages/   # Customer dashboard and flows
│       │   ├── seller-pages/     # Seller dashboard and flows
│       │   └── admin-pages/      # Admin panel
│       ├── js/
│       │   └── components/       # Per-view JavaScript modules
│       └── css/
│           └── components/       # Per-component stylesheets
└── database/
    ├── esquema.sql       # Database schema
    └── datos_prueba.sql  # Sample data for local setup
```

---

## Local Setup

### Prerequisites

- Node.js v18+
- MySQL 8.0
- npm

### Installation

```bash
# Clone the repository
git clone https://github.com/EstebanLopp/Backend-AgroNet.git
cd Backend-AgroNet

# Install backend dependencies
cd backend
npm install

# Configure environment variables
cp .env.example .env
# Edit .env with your local database credentials
```

### Environment Variables

```env
DB_HOST=localhost
DB_USER=your_mysql_user
DB_PASSWORD=your_mysql_password
DB_NAME=agronet
DB_PORT=3306
PORT=3000
```

### Database Setup

```bash
# Import the schema into MySQL
mysql -u root -p < database/esquema.sql

# (Optional) Load sample data
mysql -u root -p agronet < database/datos_prueba.sql
```

### Run the Server

```bash
cd backend
node server.js
# Server running at http://localhost:3000
```

Open `frontend/public/views/pages-general/index.html` in your browser,
or access the app at `http://localhost:3000` if serving static files
through Express.

---

## Known Limitations

This project was built for educational purposes and has known areas for
improvement:

- Passwords are stored without hashing (bcrypt not implemented)
- No JWT-based authentication; session management is handled client-side
- Most backend routes beyond user registration are not yet implemented;
  data operations rely on localStorage and JSON files in the current state
- No input sanitization against SQL injection on incomplete routes
- No test suite

These are documented here intentionally — understanding what to improve
is part of the learning process.

---

## Status

**Academic project — not production-ready.**
Active development concluded in November 2025 as part of the SENA
formative program.

---

## Author

**Esteban Lopez**
Software Development Student — SENA, Colombia
[GitHub](https://github.com/EstebanLopp) · [LinkedIn](https://linkedin.com/in/TU-URL-AQUI)
