# Job Tracker API

A REST API to track job applications. Built with Python FastAPI 
and PostgreSQL, containerized with Docker, deployed on AWS EC2 
with automated CI/CD via GitHub Actions.

## Live API
http://18.220.170.40:8001/docs

## Features
- Create, read, update, delete job applications
- Filter applications by status (applied, interview, rejected, offer)
- Input validation with Pydantic
- PostgreSQL database
- Dockerized with Docker Compose
- Auto-deploys on every push via GitHub Actions

## Tech Stack
- Python + FastAPI
- PostgreSQL
- Docker + Docker Compose
- AWS EC2
- GitHub Actions

## API Routes
- GET /jobs — get all applications
- POST /jobs — add new application
- GET /jobs/{id} — get one application
- PUT /jobs/{id} — update status or notes
- DELETE /jobs/{id} — remove application
- GET /jobs/status/{status} — filter by status (applied/interview/rejected/offer)

## How to Run Locally
1. Clone the repo
2. Create .env file:
   DB_HOST=db
   DB_NAME=jobtracker
   DB_USER=postgres
   DB_PASSWORD=yourpassword
3. Run: docker compose up --build
4. Open: http://localhost:8001/docs
