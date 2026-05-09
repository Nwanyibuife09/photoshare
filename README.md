# PhotoShare

Welcome to PhotoShare! This application is a platform for sharing and viewing photos, consisting of a React frontend and a FastAPI backend with Redis.

## Features

- **Photo Management:** Upload, view, and share photos easily.
- **Fast and Responsive:** Built with React and Vite for a snappy frontend experience.
- **Robust API:** Powered by FastAPI for high-performance backend services.

## Tech Stack

- **Frontend:** React, Vite
- **Backend:** Python, FastAPI
- **Database/Cache:** Redis

## Prerequisites

To run this application easily and ensure it works perfectly on any system, it is highly recommended to use Docker.

- [Docker Desktop](https://www.docker.com/products/docker-desktop) installed and running.

## Running the Application (Recommended)

The easiest way to start the entire application (Frontend, Backend, and Redis) is using Docker Compose.

1. Open your terminal in this repository's root folder.
2. Run the following command:
   ```bash
   docker-compose up --build
   ```
   *(If you are using newer versions of Docker, use `docker compose up --build`)*

3. Once all containers are running, you can access the application at:
   - **Frontend:** http://localhost (or http://localhost:80)
   - **Backend API:** http://localhost:8000
   - **API Documentation (Swagger):** http://localhost:8000/docs

## Running Manually (Without Docker)

If you prefer to run the application manually, you will need Node.js and Python installed.

### 1. Environment Variables

Create a `.env` file in the `backend` directory to store your environment variables (you can copy from a `.env.example` if one exists). Ensure any necessary configuration values like database endpoints or API keys are set.

### 2. Start a Local Redis Server
You must have a Redis server running locally on port 6379, or update the `REDIS_URL` in `backend/.env` to point to your Redis instance.

### 3. Start the Backend (FastAPI)
1. Open a terminal in this root directory.
2. Create and activate a virtual environment:
   ```bash
   python -m venv backend/venv
   # Windows:
   backend\venv\Scripts\activate
   # Mac/Linux:
   source backend/venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r backend/requirements.txt
   ```
4. Run the server:
   ```bash
   uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
   ```

### 3. Start the Frontend (React + Vite)
1. Open a **new terminal window** and navigate to the `frontend` folder:
   ```bash
   cd frontend
   ```
2. Install Node dependencies:
   ```bash
   npm install
   ```
3. Start the Vite development server:
   ```bash
   npm run dev
   ```
4. Open the local URL provided in the terminal (usually http://localhost:5173).
