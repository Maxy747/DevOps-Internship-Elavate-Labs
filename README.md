# DevOps Internship - Elavate Labs

A comprehensive portfolio demonstrating practical skills in various essential DevOps domains, focusing on establishing robust and automated Continuous Integration and Continuous Deployment (CI/CD) pipelines.

## 🎯 Internship Goal

The primary goal of this internship was to implement, automate, and manage infrastructure and application deployment using modern DevOps tools and practices. The tasks represent a structured journey from foundational scripting and infrastructure provisioning to complex application containerization, pipeline creation, and deployment.

---

## 📂 Repository Structure & Tasks

| Task | Core Focus | Description |
|:-----|:-----------|:------------|
| **Task 1** | **Linux & Scripting Fundamentals** | Automating routine administrative tasks using Bash/Python scripting to manage system resources and logs |
| **Task 2** | **Infrastructure as Code (IaC)** | Defining and provisioning cloud resources using Terraform (HCL) |
| **Task 3** | **Containerization with Docker** | Creating efficient, multi-stage Dockerfiles for applications and managing images locally |
| **Task 4** | **Source Control & Collaboration** | Demonstrating advanced Git workflows (branching, merging, rebasing) and GitHub integration |
| **Task 5** | **Continuous Integration (CI) Pipeline** | Implementing automated CI pipeline with GitHub Actions to build, test, and push Docker images |
| **Task 6** | **Continuous Deployment (CD) Setup** | Extending CI to full CD process, automatically deploying containerized applications to staging |
| **Task 7** | **Application Orchestration (Kubernetes)** | Defining and deploying applications using Kubernetes Manifests for high availability |
| **Task 8** | **Monitoring, Logging, and Observability** | Implementing centralized logging solutions (ELK Stack/Prometheus/Grafana) |

---

## 🚀 Featured Projects

### Project 1: Scalable Static Website with AWS S3 & GitHub Actions

Automated deployment pipeline for static websites using serverless architecture.

**Key Features:**
- Automated CI/CD with GitHub Actions
- Serverless hosting on AWS S3
- Public website access with bucket policies
- Auto-deployment on git push to main branch

**Tech Stack:** AWS S3, GitHub Actions, AWS IAM, HTML/CSS

**Live Demo:** [View Website](http://static-website-devops-project.s3-website.eu-north-1.amazonaws.com)

**Implementation:**
- Created S3 bucket with static website hosting enabled
- Configured IAM user for secure programmatic access
- Built GitHub Actions workflow (.github/workflows/deployS3.yml)
- Automated sync from project subfolder to S3 on push to main

---

### Project 2: CI/CD Pipeline with Docker & Kubernetes

Complete containerized application pipeline with automated testing and deployment.

**Key Features:**
- Automated testing with pytest
- Docker containerization
- Auto-build and push to Docker Hub
- Kubernetes deployment with Minikube
- Multi-replica deployment with NodePort service

**Tech Stack:** Python, Flask, Docker, GitHub Actions, Kubernetes, pytest

**Workflow:**
1. Code push triggers GitHub Actions
2. Automated tests run via pytest
3. Docker image built and pushed to Docker Hub
4. Kubernetes deployment via kubectl

**Implementation:**
- Developed Flask web application with automated tests
- Created Dockerfile for containerization
- Built CI/CD workflow (.github/workflows/project-4-docker-ci-workflow.yml)
- Configured Kubernetes deployment and service YAMLs
- Validated deployment on Minikube with 2 replicas

---

## 🛠️ Key Technologies & Tools

| Category | Tools |
|:---------|:------|
| **Cloud Provider** | AWS |
| **Infrastructure as Code** | Terraform (HCL) |
| **Containerization** | Docker, Docker Hub |
| **Orchestration** | Kubernetes, Minikube |
| **CI/CD & Automation** | GitHub Actions, Bash, Python |
| **Languages** | Python, JavaScript, Java, HTML/CSS |
| **Testing** | pytest |
| **Monitoring** | Prometheus, Grafana, ELK Stack |

---

## 🏃 Getting Started

### Prerequisites
- Git
- Docker & Docker Hub account
- Terraform (for IaC tasks)
- Minikube & kubectl
- AWS Account with configured credentials
- GitHub account with Actions enabled

### Quick Setup

#### Static Website Deployment
```bash
# Configure AWS credentials in GitHub Secrets
# AWS_ACCESS_KEY_ID
# AWS_SECRET_ACCESS_KEY

# Push to main branch triggers auto-deployment
git push origin main
```

#### Docker CI/CD Pipeline
```bash
# Configure Docker Hub credentials in GitHub Secrets
# DOCKER_USERNAME
# DOCKER_PASSWORD

# Start Minikube
minikube start

# Apply Kubernetes configs
kubectl apply -f deployment.yml
kubectl apply -f service.yml

# Access the service
minikube service python-app-service
```

### Exploring Individual Tasks

Navigate to the respective task folder. Each folder contains:
1. **README.md** - Detailed objectives, solution summary, and implementation steps
2. **Configuration Files** - Terraform `.tf`, Dockerfiles, Kubernetes YAMLs
3. **Scripts** - Bash or Python automation scripts

---

## 📚 Learning Outcomes

- Implemented serverless architecture with AWS S3
- Built automated CI/CD pipelines with GitHub Actions
- Containerized applications using Docker
- Orchestrated deployments with Kubernetes
- Configured secure IAM policies and access controls
- Automated testing and quality assurance
- Provisioned infrastructure as code with Terraform
- Implemented monitoring and logging solutions
- Mastered Git workflows and collaboration practices

---

## 👤 Author

**Mazin**

---

## 📄 License

This project is open source and available for educational purposes.
