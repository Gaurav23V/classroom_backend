# Classroom Backend Application

## Overview

This is a Flask-based backend application for managing users, principals, students, teachers, and assignments in a classroom setting.

## Features

- **Students**:
  - Create and edit draft assignments.
  - List all created assignments.
  - Submit assignments to teachers.

- **Teachers**:
  - List all assignments submitted to them.
  - Grade submitted assignments.

- **Principals**:
  - View all teachers.
  - View all submitted and graded assignments.
  - Re-grade assignments already graded by teachers.

## Setup Instructions

### Prerequisites

- **Docker** and **Docker Compose** installed on your machine.

### Clone the Repository

```bash
git clone https://github.com/yourusername/classroom_backend.git
cd classroom_backend
```

### Build and Run the Application

#### Using Docker Compose

1. **Build the Docker images and start the containers and also run the tests:**

   ```bash
   docker-compose up --build
   ```

2. **Access the Application:**

   - Open a web browser and navigate to `http://localhost:5000`.

3. **Run Tests:**

   ```bash
   docker-compose run test
   ```

4. **Stop the Application:**

   ```bash
   docker-compose down
   ```

### Application Configuration

- **Environment Variables:**

  - `DATABASE_URL`: Database connection string. Defaults to `sqlite:////app/data/store.sqlite3` if not provided.
  - `FLASK_APP`: Entry point of the Flask application (set to `core/server.py`).
  - `FLASK_ENV`: Environment configuration (set to `production`).

- **Database:**

  - The application uses PostgreSQL by default when running with Docker.

### API Endpoints

#### Auth

- **Header:** `X-Principal`
- **Value Example:** `{"user_id":1, "student_id":1}`

#### Student APIs

- **GET `/student/assignments`**: List all assignments for the authenticated student.
- **POST `/student/assignments`**: Create or edit a draft assignment.
- **POST `/student/assignments/submit`**: Submit a draft assignment to a teacher.

#### Teacher APIs

- **GET `/teacher/assignments`**: List all assignments submitted to the authenticated teacher.
- **POST `/teacher/assignments/grade`**: Grade a submitted assignment.

#### Principal APIs

- **GET `/principal/teachers`**: List all teachers.
- **GET `/principal/assignments`**: List all submitted and graded assignments.
- **POST `/principal/assignments/grade`**: Grade or re-grade an assignment.

### Testing

- **Test Coverage:** The application has a test coverage of 97%.

### Project Structure

- **`core/`**: Main application code.
- **`tests/`**: Test cases and SQL tests.
- **`Dockerfile`**: Instructions to build the Docker image.
- **`docker-compose.yml`**: Docker Compose configurations.
- **`requirements.txt`**: Python dependencies.

### Notes

- Ensure Docker is installed and running before starting the application.
- Adjust the database settings in `docker-compose.yml` and your application code if you use a different database.
- The default credentials and configurations are for development and testing purposes.

### Contact

For any questions or clarifications, feel free to reach out at [gaurav2301v@gmail.com](mailto:gaurav2301v@gmail.com).