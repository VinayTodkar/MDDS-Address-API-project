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
| **Frontend Developer** | React frontend, dashboard, search interface and user-facing features |

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

The objective of MDDS Address API is to provide a centralized and structured way to access Indian administrative location data through APIs.

The platform follows the hierarchy:

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

This makes the data useful for applications that require reliable Indian location and address information.

🏗️ System Architecture
┌──────────────────────────────┐
│       MDDS DATASETS          │
│   Government Location Data   │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│       VINAY TODKAR           │
│  Data Import & Validation    │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│           NEONDB             │
│      PostgreSQL Database     │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│       PRIYA SINGH            │
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
│           Darshan            |
|        REACT FRONTEND        │
└──────────────┬───────────────┘
               │
               ├── Dashboard
               ├── Villages
               ├── Users
               ├── API Logs
               ├── Settings
               └── Search
🔄 Data Flow
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
📊 MDDS Dataset

The project uses state-wise MDDS administrative datasets.

The main fields include:

MDDS STC
STATE NAME
MDDS DTC
DISTRICT NAME
MDDS Sub_DT
SUB-DISTRICT NAME
MDDS PLCN
Area Name

These fields establish the administrative relationship:

State Code
    ↓
District Code
    ↓
Sub-District Code
    ↓
Village Code
🧹 Dataset Validation

A dedicated Python validation pipeline was developed to check the quality and consistency of the MDDS datasets before database import.

## The validation process includes:

Dataset Structure Validation

Checks whether all required columns are available.

Missing Value Validation

Identifies missing values in important administrative fields.

Duplicate Validation

Detects duplicate records.

State Code Validation

Checks state-level MDDS codes.

District Code Validation

Checks district-level MDDS codes.

Sub-District Code Validation

Checks sub-district identifiers.

Village Code Validation

Checks village/location identifiers.

Hierarchy Validation

Verifies relationships between:

State
 ↓
District
 ↓
Sub-District
 ↓
Village
🐍 Data Import Pipeline

The data processing scripts are located in:

data-import/

Important files:

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
Run Dataset Validation
cd data-import
python validate_datasets.py

The validation results are stored in:

data-import/reports/
🗄️ Database

The project uses PostgreSQL on Neon as the cloud database and Prisma as the ORM.

Database hierarchy
State
  ↓
District
  ↓
Sub-District
  ↓
Village

The Prisma schema is located at:

backend/prisma/schema.prisma
🚀 REST API

The Express backend exposes endpoints for accessing the administrative hierarchy.

States
GET /api/v1/states

Returns state and union territory information.

Districts
GET /api/v1/districts

Returns district-level administrative data.

Sub-Districts
GET /api/v1/sub-districts

Returns sub-district-level information.

Villages
GET /api/v1/villages

Returns village-level administrative data.

Search
GET /api/v1/search

Provides location search functionality.

🔗 API Request Flow
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

Example:

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
🎨 React Frontend

The frontend provides a user interface for interacting with the API and exploring administrative data.

Main interface areas include:

Dashboard
Villages
Users
API Logs
Settings
Search

The React application communicates with the Express API rather than directly accessing the database.

📁 Project Structure
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
🛠️ Technology Stack
Technology	Purpose
Python	Dataset processing and validation
Pandas	Data analysis and validation
Node.js	Backend runtime
Express.js	REST API
Prisma	ORM and database access
PostgreSQL	Relational database
Neon	Cloud PostgreSQL
React	Frontend
Git	Version control
GitHub	Source code management
⚙️ Backend Setup
1. Clone the Repository
git clone https://github.com/VinayTodkar/MDDS-Address-API-project.git
cd MDDS-Address-API-project
2. Install Backend Dependencies
cd backend
npm install
3. Configure Environment Variables

Create:

backend/.env

Example:

DATABASE_URL="your_neon_database_connection_string"
PORT=3000

Do not commit .env or database credentials to GitHub.

4. Start the Backend
npm start

For development:

npm run dev
🧪 Database Testing

Database connectivity can be tested using:

backend/test-prisma.js

Additional database testing utilities are available in:

test_db.py
💡 Use Cases

The API can be used in applications that require Indian administrative location data, including:

Address forms
E-commerce applications
Delivery and logistics platforms
Government applications
Location-based services
Customer registration systems
Address verification systems
KYC workflows
Business applications
Location autocomplete
Data analysis applications
🌟 Key Project Highlights
Data Engineering
State-wise MDDS dataset processing
Automated dataset validation
Missing-value detection
Duplicate detection
Administrative code validation
Hierarchy validation
Validation reporting
Database-ready data preparation
Backend
Express.js REST API
Prisma ORM
PostgreSQL database
Neon cloud database
Administrative hierarchy endpoints
Frontend
React-based interface
Dashboard
Location search
Village exploration
API-related management screens
📈 Project Status
Component	Status
MDDS Dataset Collection	✅ Completed
Dataset Inspection	✅ Completed
Dataset Validation	✅ Completed
Validation Reports	✅ Completed
Data Import Pipeline	✅ Completed
NeonDB Integration	✅ Completed
Prisma Database Layer	✅ Completed
Backend Foundation	✅ Completed
REST API	🚧 Team Development
React Frontend	🚧 Team Development
Dashboard	🚧 Team Development
Search	🚧 Team Development
API Logs	🚧 Team Development
Authentication	🚧 Future Enhancement
Production Deployment	🚧 Future Enhancement
🤝 Team Architecture

The project is divided into three major layers:

┌─────────────────────────────────────┐
│           DATA LAYER                │
│                                     │
│      Vinay Sunil Todkar             │
│      MDDS Data + Database           │
└──────────────────┬──────────────────┘
                   │
                   ▼
┌─────────────────────────────────────┐
│          BACKEND LAYER              │
│                                     │
│          Priya Singh                │
│       Express.js REST API           │
└──────────────────┬──────────────────┘
                   │
                   ▼
┌─────────────────────────────────────┐
│         FRONTEND LAYER              │
│                                     │
│       React Application              │
│ Dashboard / Villages / Search       │
└─────────────────────────────────────┘
📚 What I Learned

Through this project, I gained practical experience in:

Data engineering
Data cleaning
Dataset validation
ETL pipelines
Python and Pandas
PostgreSQL
Neon cloud databases
Prisma ORM
Backend integration
REST APIs
Git and GitHub
Team collaboration
Full-stack application architecture
🔗 Repository

GitHub Repository:

https://github.com/VinayTodkar/MDDS-Address-API-project

👨‍💻 Contributors
Vinay Sunil Todkar

Data Engineering | Database | Backend Support

Main responsibilities:

MDDS datasets
Data inspection
Data validation
Data cleaning
Data import
NeonDB
Prisma
Database integration
Backend support
Priya Singh

Backend Developer

Main responsibilities:

Express.js
REST API
Backend architecture
API integration
Frontend Developer

Frontend Developer

Main responsibilities:

React
Dashboard
Search
Village interface
User-facing application
📄 License

This project was developed as a collaborative academic/software development project.

🚀 MDDS Address API
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

Building a structured and accessible administrative location platform for India.
