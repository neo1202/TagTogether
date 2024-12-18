# TagTogether

TagTogether is a cloud-based service designed to support a marketing campaign. The system includes essential modules and databases for user registration and login, event registration, post uploads, and dynamic leaderboard updates. The application provides a simple interface to display important information and functionalities, focusing on core features rather than aesthetics.

## Project Overview

This project consists of a backend service built with FastAPI and a frontend application using React and Vite. The backend handles user authentication, team management, and post uploads, while the frontend provides a user interface for interacting with these features.

## Frontend

### Setup

1. **Install Dependencies**: Run the following command to install the necessary packages.

   ```bash
   npm install
   ```

2. **Environment Configuration**: Create a `.env` file in the `frontend` directory with the following content:

   ```plaintext
   VITE_BACKEND_URL=<your_backend_url>
   ```

   Adjust the `VITE_BACKEND_URL` to point to your backend service URL.

3. **Run Development Server**: Start the development server with:

   ```bash
   npm run dev
   ```

## Backend

### Setup

1. **Environment Configuration**: Create a `.env` file in the `backend` directory with the following content:

   ```plaintext
   DATABASE_URL=<your_database_url>
   SECRET_KEY=<your_secret_key_here>
   ```

   Ensure the `DATABASE_URL` matches your PostgreSQL configuration and replace `your_secret_key_here` with a strong secret key.

2. **Run with Docker**: Use Docker Compose to build and run the backend services:

   ```bash
   docker-compose up --build
   ```

   This command will start the FastAPI application and a PostgreSQL database.

## Testing

### Load Testing

Use Locust to perform load testing and simulate user interactions:

1. **Start Locust**: Run the following command:

   ```bash
   locust -f test/load_test.py --host=<your_backend_url>
   ```

2. **Access Locust Web Interface**: Open a browser and go to `http://localhost:8089` to start the test and monitor the results.

## Additional Information

This project is designed to be a robust and scalable solution for managing marketing campaigns, with a focus on ease of use and extensibility.