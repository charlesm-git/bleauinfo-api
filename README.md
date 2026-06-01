# 🧠 Bleau.Info Statistics API

REST API providing statistical data and boulder recommendations for the Fontainebleau bouldering area. All data is sourced from [bleau.info](https://bleau.info). The API serves a React frontend and is optimized for read-only access in production.

## 🚀 Features

- Statistical bouldering data by area, grade, style, and time
- Boulder recommendation engine using precomputed similarity matrices (ascent, grade, style)
- Full-text search across boulders and areas
- Clean architecture with SQLAlchemy models and Pydantic schemas

## 📦 Tech Stack

| Component | Technology |
|-----------|-----------|
| Framework | FastAPI |
| ORM | SQLAlchemy |
| Database | SQLite (read-only) |
| ML/Recommendations | NumPy, SciPy (sparse matrices) |
| Deployment | Docker (Python 3.13 Alpine) → Google Cloud Run |
| Package Manager | Poetry |

## 🏗️ Project Structure

```
├── main.py              # App entrypoint & router registration
├── database.py          # DB session & recommendation matrix loading
├── crud/                # Database query logic
├── models/              # SQLAlchemy ORM models
├── routers/             # FastAPI route definitions
├── schemas/             # Pydantic request/response schemas
├── similarity_*.npz     # Precomputed recommendation matrices
└── Dockerfile           # Production container
```

## 🔌 API Endpoints

### 🧗‍♂️ Boulders
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/boulders` | List all boulders (pagination & filtering) |
| GET | `/boulders/{id}` | Get boulder details |

### 🗺️ Areas
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/areas` | List all areas |
| GET | `/areas/{id}` | Get area details |
| GET | `/areas/{id}/boulders` | List boulders in an area |
| GET | `/areas/{id}/stats` | Area stats (count, grade distribution, etc.) |

### 🌍 Regions
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/regions` | List all regions |
| GET | `/regions/{id}/areas` | List areas in a region |

### 👤 Users
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/users` | List all users |
| GET | `/users/{id}` | Get user details |
| GET | `/users/{id}/boulders/set` | Boulders set by user |
| GET | `/users/{id}/boulders/repeats` | Boulders repeated by user |
| GET | `/users/{id}/stats` | User stats |

### 🔍 Search
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/search/{text}` | Search boulders and areas |

### 🎯 Recommendation
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/recommendation` | Get boulder recommendations based on selected boulders, with configurable ascent/grade/style weights |

### 📊 Statistics
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/stats/boulders/top-rated/{grade}` | Top 10 rated boulders for a grade |
| GET | `/stats/boulders/most-ascents/{grade}` | Top 10 most repeated boulders |
| GET | `/stats/boulders/hardest` | Boulders graded 8c+ |
| GET | `/stats/boulders/styles/distribution` | Boulder count per style |
| GET | `/stats/boulders/ratings/distribution` | Boulder count per rating |
| GET | `/stats/areas/most-ascents` | Top 10 areas by repeats |
| GET | `/stats/grades/distribution` | Boulders per grade |
| GET | `/stats/users/top-setters` | Top 10 boulder setters |
| GET | `/stats/users/top-repeaters` | Top 10 repeaters |
| GET | `/stats/users/repeat-volume` | User repeat volume histogram |
| GET | `/stats/ascents/per-month` | Monthly ascent distribution |
| GET | `/stats/ascents/per-year` | Yearly ascent totals |
| GET | `/stats/ascents/per-grade` | Ascents per grade |

## 🚀 Getting Started

```bash
# Install dependencies
poetry install

# Run locally
uvicorn main:app --reload --port 8000
```

## 🐳 Docker

```bash
docker build -t bleauinfo-api .
docker run -p 8080:8080 bleauinfo-api
```
