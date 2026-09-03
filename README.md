# MDDS Address API 🇮🇳

A REST API for accessing and searching India's administrative address hierarchy using **MDDS (Metadata and Data Standards)** codes.

The project is designed to provide structured access to **States, Districts, Sub-Districts, and Villages**, making Indian administrative location data easier to integrate into applications such as address forms, logistics systems, government applications, delivery platforms, and location-based services.

> 🚧 **Project Status:** Work in Progress
> The data validation and initial backend/database setup are complete. Additional API functionality, authentication, rate limiting, and production features are being developed.

---

## 📌 Features

### Current

* Indian administrative hierarchy data model
* MDDS code-based identification
* State → District → Sub-District → Village hierarchy
* Dataset inspection and validation scripts
* Duplicate and missing-value validation
* Hierarchy consistency validation
* PostgreSQL database support
* Prisma ORM integration
* Neon PostgreSQL database support
* Express.js REST API foundation
* Health-check endpoint
* Address API route structure
* Raw datasets excluded from Git history/repository

### Planned

* [ ] Complete address search API
* [ ] State listing endpoint
* [ ] District-by-state endpoint
* [ ] Sub-district-by-district endpoint
* [ ] Village-by-sub-district endpoint
* [ ] Village autocomplete/search
* [ ] Pagination
* [ ] API authentication
* [ ] API key management
* [ ] Rate limiting
* [ ] API usage logging
* [ ] Swagger/OpenAPI documentation
* [ ] Production deployment
* [ ] Automated testing
* [ ] CI/CD pipeline

---

## 🏗️ Architecture

```text
                    ┌─────────────────────┐
                    │      Client         │
                    │ Web / Mobile / App  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    Express.js API   │
                    │      REST Layer     │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │       Prisma        │
                    │        ORM          │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ PostgreSQL / Neon   │
                    │    Database         │
                    └─────────────────────┘

Data Pipeline

MDDS Datasets
     │
     ▼
Python Import Scripts
     │
     ▼
Validation
     │
     ▼
Clean Structured Data
     │
     ▼
PostgreSQL / Neon
```

---

## 🗂️ Project Structure

```text
mdds-address-api/
│
├── backend/
│   ├── .agents/
│   ├── .claude/
│   ├── .cursor/
│   ├── .devin/
│   │
│   ├── prisma/
│   │   └── schema.prisma
│   │
│   ├── src/
│   │   ├── config/
│   │   │   └── prisma.js
│   │   │
│   │   ├── routes/
│   │   │   ├── address.routes.js
│   │   │   └── health.routes.js
│   │   │
│   │   ├── app.js
│   │   └── server.js
│   │
│   ├── package.json
│   ├── package-lock.json
│   ├── prisma.config.ts
│   └── test-prisma.js
│
├── data-import/
│   ├── data/                    # Local only - not committed
│   │
│   ├── import_to_neon.py
│   ├── inspect_datasets.py
│   ├── validate_datasets.py
│   ├── inspection_report.txt
│   │
│   └── reports/
│       ├── validation_summary.csv
│       └── validation_notes.md
│
├── schema.sql
├── test_db.py
├── .gitignore
└── README.md
```

---

## 🛠️ Technology Stack

| Technology     | Purpose                         |
| -------------- | ------------------------------- |
| **Node.js**    | Backend runtime                 |
| **Express.js** | REST API framework              |
| **Prisma**     | Database ORM                    |
| **PostgreSQL** | Relational database             |
| **Neon**       | Serverless PostgreSQL           |
| **Python**     | Data processing/import pipeline |
| **Pandas**     | Dataset processing              |
| **Git/GitHub** | Version control                 |

---

# 📊 Data Model

The core administrative hierarchy is:

```text
India
 │
 └── State
      │
      └── District
           │
           └── Sub-District
                │
                └── Village
```

Each level is associated with an MDDS identifier.

The source datasets use fields such as:

```text
MDDS STC
STATE NAME

MDDS DTC
DISTRICT NAME

MDDS Sub_DT
SUB-DISTRICT NAME

MDDS PLCN
Area Name
```

---

# 🔄 Data Import Pipeline

The project includes a Python-based pipeline for processing the original MDDS datasets.

```text
Raw Dataset
     │
     ▼
Dataset Inspection
     │
     ▼
Column Validation
     │
     ▼
Missing Value Check
     │
     ▼
Duplicate Check
     │
     ▼
Code Validation
     │
     ▼
Hierarchy Validation
     │
     ▼
Clean Dataset
     │
     ▼
Neon PostgreSQL
```

### Validation Checks

The validation pipeline checks for:

* Missing values
* Duplicate records
* Invalid state codes
* Invalid district codes
* Invalid sub-district codes
* Invalid village codes
* Hierarchy inconsistencies
* Expected column structure

Validation reports are stored under:

```text
data-import/reports/
```

---

# 🚀 Getting Started

## 1. Clone the repository

```bash
git clone https://github.com/VinayTodkar/MDDS-Address-API-project.git
cd MDDS-Address-API-project
```

---

## 2. Backend Setup

Move into the backend directory:

```bash
cd backend
```

Install dependencies:

```bash
npm install
```

---

## 3. Configure Environment Variables

Create a `.env` file inside `backend/`.

Example:

```env
DATABASE_URL="your_neon_database_connection_string"
PORT=3000
```

> ⚠️ Never commit your `.env` file or database credentials to GitHub.

A `.env.example` file will be added as the project develops.

---

## 4. Configure Prisma

After configuring the database connection:

```bash
npx prisma generate
```

Run migrations when migrations are configured:

```bash
npx prisma migrate dev
```

---

## 5. Start the Development Server

```bash
npm start
```

or, if a development script is configured:

```bash
npm run dev
```

The local API will be available at:

```text
http://localhost:3000
```

---

# ❤️ Health Check

The project contains a health-check route for verifying that the API server is running.

Example:

```http
GET /health
```

Expected response will depend on the current implementation.

---

# 🔌 API Design

The planned API follows a hierarchy-based structure.

### Get all states

```http
GET /states
```

### Get districts for a state

```http
GET /states/{id}/districts
```

### Get sub-districts for a district

```http
GET /districts/{id}/subdistricts
```

### Get villages for a sub-district

```http
GET /subdistricts/{id}/villages
```

### Search villages

```http
GET /search?q={query}
```

### Autocomplete

```http
GET /autocomplete?q={query}
```

> These endpoints represent the project's API design/roadmap. Endpoints should only be considered production-ready once their implementation and tests are completed.

---

# 🔎 Example Address Hierarchy

A location can be represented as:

```json
{
  "village": "Manibeli",
  "subDistrict": "Akkalkuwa",
  "district": "Nandurbar",
  "state": "Maharashtra",
  "country": "India"
}
```

This structure is intended to make the API convenient for applications that need dependent address selection.

For example:

```text
Select State
     ↓
Select District
     ↓
Select Sub-District
     ↓
Select Village
```

---

# 🔐 Security

Security features are planned for future development.

Planned security mechanisms include:

* API key authentication
* Secure API secrets
* Rate limiting
* Input validation
* Request logging
* Secure HTTP headers
* Environment-based secrets
* Database credential protection

---

# 📈 Future Roadmap

## Phase 1 — Data Foundation

* [x] Collect MDDS datasets
* [x] Inspect datasets
* [x] Validate datasets
* [x] Create database schema
* [x] Configure Prisma
* [x] Configure Neon PostgreSQL
* [x] Create import pipeline

## Phase 2 — API Development

* [x] Express application foundation
* [x] Health endpoint
* [x] Address routes foundation
* [ ] State API
* [ ] District API
* [ ] Sub-district API
* [ ] Village API
* [ ] Search API
* [ ] Autocomplete API
* [ ] Pagination

## Phase 3 — Security & API Management

* [ ] API authentication
* [ ] API key management
* [ ] Rate limiting
* [ ] Usage tracking
* [ ] Request logging

## Phase 4 — Production

* [ ] Automated tests
* [ ] Swagger/OpenAPI
* [ ] CI/CD
* [ ] Production deployment
* [ ] Monitoring
* [ ] Performance optimization

---

# 🧪 Testing

Testing is currently under development.

The project contains database testing utilities:

```text
test_db.py
backend/test-prisma.js
```

Future testing will include:

* API endpoint tests
* Database integration tests
* Validation tests
* Error handling tests
* Search tests
* Pagination tests
* Performance tests

---

# 📦 Dataset Notice

The original MDDS datasets are **not included in this GitHub repository**.

They are intentionally excluded using:

```gitignore
data-import/data/
```

This keeps the repository lightweight and avoids redistributing source datasets without confirming their applicable licensing/usage terms.

To run the import pipeline locally, place the required datasets inside:

```text
data-import/data/
```

---

# 🤝 Contributing

This project is currently under active development.

If you would like to contribute:

```bash
git fork
git clone <your-fork>
git checkout -b feature/your-feature
```

Make your changes, test them, and submit a pull request.

---

# 📄 License

License information will be added once the project's source-data and software licensing requirements have been finalized.

---

# 👨‍💻 Author

**Vinay Sunil Todkar**

B.Tech — Artificial Intelligence & Data Science

GitHub:
https://github.com/VinayTodkar

---

# ⭐ Project Status

```text
MDDS Address API
────────────────────────────────

Data Pipeline       ████████████████████ 100%
Data Validation     ████████████████████ 100%
Database Setup      ███████████████░░░░░  75%
API Development     ████████░░░░░░░░░░░░  40%
Authentication      ██░░░░░░░░░░░░░░░░░░  10%
Testing             ███░░░░░░░░░░░░░░░░░  15%
Production          ░░░░░░░░░░░░░░░░░░░░   0%

Overall: 🚧 Work in Progress
```

> **Goal:** Build a reliable, scalable API for structured Indian administrative address data.
