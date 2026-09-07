# 🇮🇳 MDDS Address API

A full-stack India Administrative Address API built using official MDDS (Metadata and Data Standards) datasets.

The project provides structured access to India's administrative hierarchy:

**State → District → Sub-District → Village**

The system combines a validated MDDS data pipeline, Neon PostgreSQL database, Express.js REST APIs, and a React frontend for searching and exploring Indian administrative location data.

---

## 👥 Team Project

This project was developed collaboratively by **3 team members**, with responsibilities divided across the data, backend, and frontend layers.

### Team Contributions

| Team Member | Contribution |
|---|---|
| **Vinay Sunil Todkar** | MDDS dataset collection, inspection, validation, data cleaning, data-import pipeline, NeonDB integration, Prisma/database work and backend support |
| **Priya Singh** | Express.js backend development and REST API implementation |
| **Darshan** | React frontend, dashboard, search interface and user-facing features |

---

## 👨‍💻 My Contribution — Vinay Sunil Todkar

My primary responsibility in this project was the **data engineering and database layer**, along with backend support.

### Data Engineering

- Collected and organized MDDS state-wise datasets
- Inspected the structure of the datasets
- Validated required columns
- Checked missing values
- Checked duplicate records
- Validated MDDS state codes
- Validated district codes
- Validated sub-district codes
- Validated village codes
- Performed administrative hierarchy validation
- Investigated and documented data-quality issues
- Generated dataset validation reports
- Prepared validated datasets for database import

### Database / Backend Support

- Worked with Neon PostgreSQL
- Worked with Prisma ORM
- Prepared the database structure for administrative data
- Developed and maintained data-import scripts
- Supported integration between the database and Express backend
- Assisted with backend API development

---

# 🎯 Project Objective

## 📌 Overview

**MDDS Address API** is a full-stack application designed to provide structured and accessible administrative location data for India.

The project processes state-wise MDDS datasets and organizes them into a hierarchical structure:

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

This structure makes the data useful for applications that require reliable Indian location and address information.

---

# 🏗️ System Architecture

```text
┌──────────────────────────────┐
│        MDDS DATASETS         │
│    Government Location Data  │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│       VINAY TODKAR           │
│   Data Import & Validation   │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│           NEON DB            │
│      PostgreSQL Database     │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│        PRIYA SINGH           │
│      EXPRESS BACKEND         │
└──────────────┬───────────────┘
               │
               ├── /api/v1/states
               ├── /api/v1/districts
               ├── /api/v1/sub-districts
               ├── /api/v1/villages
               └── /api/v1/search
               │
               ▼
┌──────────────────────────────┐
│       REACT FRONTEND         │
│          DARSHAN             │
└──────────────┬───────────────┘
               │
               ├── Dashboard
               ├── Villages
               ├── Users
               ├── API Logs
               ├── Settings
               └── Search
```

---

# 🔄 Data Flow

```text
MDDS Raw Datasets
        ↓
Dataset Inspection
        ↓
Data Validation
        ↓
Data Cleaning
        ↓
Validation Reports
        ↓
Neon PostgreSQL
        ↓
Prisma ORM
        ↓
Express.js Backend
        ↓
REST API
        ↓
React Frontend
        ↓
Dashboard / Search / Village Explorer
```

---

# 📊 MDDS Dataset

The project uses state-wise MDDS administrative datasets.

### Main Fields

| Field               | Description           |
| ------------------- | --------------------- |
| `MDDS STC`          | State Code            |
| `STATE NAME`        | State Name            |
| `MDDS DTC`          | District Code         |
| `DISTRICT NAME`     | District Name         |
| `MDDS Sub_DT`       | Sub-District Code     |
| `SUB-DISTRICT NAME` | Sub-District Name     |
| `MDDS PLCN`         | Location/Village Code |
| `Area Name`         | Area/Village Name     |

These fields establish the administrative relationship:

```text
State Code
    ↓
District Code
    ↓
Sub-District Code
    ↓
Village Code
```

---

# 🧹 Dataset Validation

A dedicated Python validation pipeline was developed to check the quality and consistency of the MDDS datasets before database import.

## Validation Process

### 1. Dataset Structure Validation

Checks whether all required columns are available.

### 2. Missing Value Validation

Identifies missing values in important administrative fields.

### 3. Duplicate Validation

Detects duplicate records.

### 4. State Code Validation

Checks state-level MDDS codes.

### 5. District Code Validation

Checks district-level MDDS codes.

### 6. Sub-District Code Validation

Checks sub-district identifiers.

### 7. Village Code Validation

Checks village/location identifiers.

### 8. Hierarchy Validation

Verifies relationships between:

```text
State
 ↓
District
 ↓
Sub-District
 ↓
Village
```

---

# 🐍 Data Import & Validation Pipeline

The data processing scripts are located in:

```text
data-import/
```

### Important Files

```text
data-import/
│
├── import_to_neon.py
├── inspect_datasets.py
├── validate_datasets.py
├── inspection_report.txt
│
└── reports/
    ├── validation_summary.csv
    └── validation_notes.md
```

## Run Dataset Validation

From the project root:

```bash
cd data-import
python validate_datasets.py
```

The validation results are stored in:

```text
data-import/reports/
```

### Required Python Dependencies

The validation pipeline supports both `.xls` and `.ods` datasets.

```bash
pip install pandas xlrd odfpy
```

---

# 🗄️ Database

The project uses **PostgreSQL on Neon** as the cloud database and **Prisma** as the ORM.

### Database Hierarchy

```text
State
  ↓
District
  ↓
Sub-District
  ↓
Village
```

The Prisma schema is located at:

```text
backend/prisma/schema.prisma
```

---

# 🚀 REST API

The Express.js backend exposes endpoints for accessing the administrative hierarchy.

## States

```http
GET /api/v1/states
```

Returns state and union territory information.

## Districts

```http
GET /api/v1/districts
```

Returns district-level administrative data.

## Sub-Districts

```http
GET /api/v1/sub-districts
```

Returns sub-district-level information.

## Villages

```http
GET /api/v1/villages
```

Returns village-level administrative data.

## Search

```http
GET /api/v1/search
```

Provides location search functionality.

---

# 🔗 API Request Flow

```text
React Frontend
      ↓
Express.js API
      ↓
Prisma ORM
      ↓
Neon PostgreSQL
      ↓
JSON Response
      ↓
React Frontend
```

### Example

When a user selects a state:

```text
User selects a State
        ↓
Frontend requests Districts
        ↓
Express API
        ↓
Prisma Database Query
        ↓
Neon PostgreSQL
        ↓
District data returned
        ↓
Frontend displays Districts
```

---

# 🎨 React Frontend

The frontend provides a user interface for interacting with the API and exploring administrative data.

### Main Interface Areas

* Dashboard
* Villages
* Users
* API Logs
* Settings
* Search

The React application communicates with the Express API rather than directly accessing the database.

---

# 📁 Project Structure

```text
mdds-address-api/
│
├── backend/
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
│   │
│   ├── data/
│   │   └── MDDS datasets
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
├── frontend/
│
├── schema.sql
├── test_db.py
├── .gitignore
└── README.md
```

---

# 🛠️ Technology Stack

| Technology | Purpose                           |
| ---------- | --------------------------------- |
| Python     | Dataset processing and validation |
| Pandas     | Data analysis and validation      |
| xlrd       | `.xls` dataset support            |
| odfpy      | `.ods` dataset support            |
| Node.js    | Backend runtime                   |
| Express.js | REST API backend                  |
| Prisma     | ORM and database access           |
| PostgreSQL | Relational database               |
| Neon       | Cloud PostgreSQL                  |
| React      | Frontend                          |
| Git        | Version control                   |
| GitHub     | Source code management            |

---

# ⚙️ Backend Setup

## 1. Clone the Repository

```bash
git clone https://github.com/VinayTodkar/MDDS-Address-API-project.git
cd MDDS-Address-API-project
```

## 2. Install Backend Dependencies

```bash
cd backend
npm install
```

## 3. Configure Environment Variables

Create:

```text
backend/.env
```

Example:

```env
DATABASE_URL="your_neon_database_connection_string"
PORT=3000
```

> ⚠️ Never commit `.env` files or database credentials to GitHub.

## 4. Start the Backend

```bash
npm start
```

For development:

```bash
npm run dev
```

---

# 🧪 Database Testing

Database connectivity can be tested using:

```text
backend/test-prisma.js
```

Additional database testing utilities are available in:

```text
test_db.py
```

---

# 💡 Use Cases

The API can be used in applications that require Indian administrative location data, including:

* Address forms
* E-commerce applications
* Delivery and logistics platforms
* Government applications
* Location-based services
* Customer registration systems
* Address verification systems
* KYC workflows
* Business applications
* Location autocomplete
* Data analysis applications

---

# 🌟 Key Project Highlights

## Data Engineering

* State-wise MDDS dataset processing
* Automated dataset validation
* Missing-value detection
* Duplicate detection
* Administrative code validation
* Hierarchy validation
* Validation reporting
* Database-ready data preparation

## Backend

* Express.js REST API
* Prisma ORM
* PostgreSQL database
* Neon cloud database
* Administrative hierarchy endpoints
* Backend integration

## Frontend

* React-based interface
* Dashboard
* Location search
* Village exploration
* API-related management screens

---

# 📈 Project Status

| Component               | Status                |
| ----------------------- | --------------------- |
| MDDS Dataset Collection | ✅ Completed           |
| Dataset Inspection      | ✅ Completed           |
| Dataset Validation      | ✅ Completed           |
| Validation Reports      | ✅ Completed           |
| Data Import Pipeline    | ✅ Completed           |
| NeonDB Integration      | ✅ Completed           |
| Prisma Database Layer   | ✅ Completed           |
| Backend Foundation      | ✅ Completed           |
| REST API                | 🚧 Team Development   |
| React Frontend          | 🚧 Team Development   |
| Dashboard               | 🚧 Team Development   |
| Search                  | 🚧 Team Development   |
| API Logs                | 🚧 Team Development   |
| Authentication          | 🚧 Future Enhancement |
| Production Deployment   | 🚧 Future Enhancement |

---

# 🤝 Team Architecture

The project is divided into three major layers:

```text
┌─────────────────────────────────────┐
│             DATA LAYER              │
│                                     │
│       Vinay Sunil Todkar            │
│       MDDS Data + Database          │
└──────────────────┬──────────────────┘
                   │
                   ▼
┌─────────────────────────────────────┐
│           BACKEND LAYER             │
│                                     │
│           Priya Singh               │
│       Express.js REST API           │
└──────────────────┬──────────────────┘
                   │
                   ▼
┌─────────────────────────────────────┐
│          FRONTEND LAYER             │
│                                     │
│             Darshan                 │
│       React Application             │
│    Dashboard / Search / Villages    │
└─────────────────────────────────────┘
```

---

# 👨‍💻 Contributors

## Vinay Sunil Todkar

**Data Engineering | Database | Backend Support**

### Main Responsibilities

* MDDS datasets
* Data inspection
* Data validation
* Data cleaning
* Data import
* NeonDB integration
* Prisma
* Database integration
* Backend support

---

## Priya Singh

**Backend Developer**

### Main Responsibilities

* Express.js
* REST API
* Backend architecture
* API integration

---

## Darshan

**Frontend Developer**

### Main Responsibilities

* React
* Dashboard
* Search
* Village interface
* User-facing application

---

# 📚 What I Learned

Through this project, I gained practical experience in:

* Data engineering
* Data cleaning
* Dataset validation
* ETL pipelines
* Python and Pandas
* PostgreSQL
* Neon cloud databases
* Prisma ORM
* Backend integration
* REST APIs
* Git and GitHub
* Team collaboration
* Full-stack application architecture

---

# 🔗 Repository

**GitHub Repository**

https://github.com/VinayTodkar/MDDS-Address-API-project

---

# 📄 License

This project was developed as a collaborative academic/software development project.

---

# 🚀 MDDS Address API

```text
MDDS DATA
    ↓
DATA VALIDATION
    ↓
NEONDB
    ↓
EXPRESS.JS
    ↓
REST APIs
    ↓
REACT
    ↓
DASHBOARD + SEARCH + VILLAGES
```

> **Building a structured and accessible administrative location platform for India.**
