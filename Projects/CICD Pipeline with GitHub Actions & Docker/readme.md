# Project 4: CI/CD Pipeline with GitHub Actions & Docker

This project implements **Project 4: CI/CD Pipeline with GitHub Actions & Docker (No Cloud Needed)** from the Elevate Labs internship program.

The goal is to build a complete Continuous Integration (CI) pipeline that automatically tests a Python web application, builds it into a Docker image, and pushes the image to Docker Hub. It also includes steps for simulating Continuous Deployment (CD) by running the container locally using Minikube.

[![Project 4 Docker CI Pipeline](https://github.com/Maxy747/DevOps-Internship-Elavate-Labs/actions/workflows/project-4-docker-ci-workflow.yml/badge.svg)](https://github.com/Maxy747/DevOps-Internship-Elavate-Labs/actions/workflows/project-4-docker-ci-workflow.yml)

---

## Project Architecture & Workflow

This project uses Docker for containerization and GitHub Actions for CI automation. The local deployment simulation uses Minikube (Kubernetes).

1. **Code & Push:** Developer writes/updates Python Flask application code (`app.py`, `app_test.py`, `requirements.txt`) and pushes changes to the `main` branch of the GitHub repository.
2. **CI Trigger (GitHub Actions):** The push triggers the workflow defined in `.github/workflows/project-4-docker-ci-workflow.yml`.
3. **Test:** The workflow installs dependencies and runs `pytest` to execute automated tests. If tests fail, the pipeline stops.
4. **Build:** If tests pass, the workflow uses the `Dockerfile` to build a Docker image containing the application and its dependencies.
5. **Push:** The workflow logs into Docker Hub (using secrets) and pushes the newly built image (e.g., `mazinmazy/devops-internship-elavate-labs:latest`).
6. **(Manual CD Simulation):** Developer uses Minikube and `kubectl` on their local machine to apply Kubernetes configurations (`deployment.yml`, `service.yml`). Kubernetes pulls the image from Docker Hub and runs the application pods.
7. **Access:** Developer uses `minikube service` to access the running application in their browser.

---

## Technology Stack

- **Language/Framework:** Python / Flask
- **Testing:** pytest
- **Containerization:** Docker
- **Image Registry:** Docker Hub
- **CI/CD Platform:** GitHub Actions
- **Local Deployment:** Minikube / Kubernetes (kubectl)

---

## Implementation Details

### 1. Python Application

A simple Flask web application (`app.py`) serves a "Hello World" message. Dependencies are managed in `requirements.txt`, and tests are defined in `app_test.py`.

### 2. Dockerfile

The `Dockerfile` defines the image build process:

```dockerfile
# Start from a Python base image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose the application port
EXPOSE 5000

# Run the application
CMD ["flask", "run", "--host=0.0.0.0"]
```

### 3. GitHub Actions Workflow

The workflow (`.github/workflows/project-4-docker-ci-workflow.yml`) automates testing, building, and pushing the Docker image:

```yaml
name: Project 4 - Docker CI Pipeline

on:
  push:
    branches: [ "main", "master" ]
    paths:
      # Only run if files in this specific project folder change
      - 'Projects/CICD Pipeline with GitHub Actions & Docker/**'

jobs:
  build_and_push:
    runs-on: ubuntu-latest

    steps:
      - name: Check out code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'

      # Use quotes because the path has spaces
      - name: Install dependencies and run tests
        run: |
          pip install -r "Projects/CICD Pipeline with GitHub Actions & Docker/requirements.txt"
          pytest "Projects/CICD Pipeline with GitHub Actions & Docker/app_test.py"

      - name: Log in to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}

      # Use quotes because the path has spaces
      - name: Build and push Docker image
        uses: docker/build-push-action@v5
        with:
          context: "./Projects/CICD Pipeline with GitHub Actions & Docker"
          push: true
          tags: ${{ secrets.DOCKER_USERNAME }}/${{ github.event.repository.name }}:latest
```

### 4. Kubernetes Configuration (for Minikube)

- **`deployment.yml`:** Defines how Kubernetes should run the application, specifying the Docker image (`mazinmazy/devops-internship-elavate-labs:latest`) and the number of replicas.
- **`service.yml`:** Defines how to expose the application running in the pods, using a `NodePort` service type for easy local access via Minikube.

---

## Project Validation (Screenshots)

### 1. Local Docker Build & Run
![Local Docker Run](path/to/your/local_docker_run.jpg)

### 2. Successful GitHub Actions Workflow
![GitHub Actions Success](path/to/your/github_actions_success.jpg)

### 3. Image Pushed to Docker Hub
![Docker Hub Image](path/to/your/docker_hub_image.jpg)

### 4. Minikube Pods Running
![Minikube Pods Running](path/to/your/minikube_pods.jpg)

### 5. Application Accessed via Minikube Service
![Minikube Service Access](path/to/your/minikube_service_access.jpg)

---

## How to Run Locally (Using Minikube)

### Prerequisites
- Docker Desktop
- Minikube
- kubectl

### Steps

1. **Clone Repository:**
   ```bash
   git clone <your-repo-url>
   ```

2. **Start Minikube:**
   ```bash
   minikube start
   ```

3. **Navigate to Project Folder:**
   ```bash
   cd "DevOps-Internship-Elavate-Labs/Projects/CICD Pipeline with GitHub Actions & Docker"
   ```

4. **Apply Kubernetes Configs:**
   ```bash
   kubectl apply -f deployment.yml
   kubectl apply -f service.yml
   ```

5. **Wait for Pods:**
   Check status with:
   ```bash
   kubectl get pods
   ```
   Wait until status shows `Running`.

6. **Access Service:**
   ```bash
   minikube service python-app-service
   ```
   This will open the app in your browser.

---

## License

This project is part of the Elevate Labs DevOps internship program.

---

**Author:** Mazin
