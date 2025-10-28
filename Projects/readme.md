# DevOps Projects Portfolio

A collection of hands-on DevOps projects demonstrating CI/CD pipelines, cloud infrastructure, and containerization.

## 📋 Projects Overview

### 1. Scalable Static Website with AWS S3 & GitHub Actions

Automated deployment pipeline for static websites using serverless architecture.

**Key Features:**
- Automated CI/CD with GitHub Actions
- Serverless hosting on AWS S3
- Public website access with bucket policies
- Auto-deployment on git push to main branch

**Tech Stack:**
- AWS S3 (Static Website Hosting)
- GitHub Actions (CI/CD)
- AWS IAM (Security & Access Control)
- HTML/CSS

**Live Demo:** [View Website](http://static-website-devops-project.s3-website.eu-north-1.amazonaws.com)

---

### 2. CI/CD Pipeline with Docker & Kubernetes

Complete containerized application pipeline with automated testing and deployment.

**Key Features:**
- Automated testing with pytest
- Docker containerization
- Auto-build and push to Docker Hub
- Kubernetes deployment with Minikube
- Multi-replica deployment with NodePort service

**Tech Stack:**
- Python & Flask
- Docker & Docker Hub
- GitHub Actions
- Kubernetes (Minikube)
- pytest (Testing)

**Workflow:**
1. Code push triggers GitHub Actions
2. Automated tests run via pytest
3. Docker image built and pushed to Docker Hub
4. Kubernetes deployment via kubectl

---

## 🚀 Getting Started

### Prerequisites
- AWS Account (Project 1)
- Docker installed (Project 2)
- Minikube & kubectl (Project 2)
- GitHub account with Actions enabled

### Setup Instructions

#### Project 1: Static Website
```bash
# Configure AWS credentials in GitHub Secrets
# AWS_ACCESS_KEY_ID
# AWS_SECRET_ACCESS_KEY

# Push to main branch triggers auto-deployment
git push origin main
```

#### Project 2: Docker CI/CD
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

---

## 📚 Learning Outcomes

- Implemented serverless architecture with AWS S3
- Built automated CI/CD pipelines with GitHub Actions
- Containerized applications using Docker
- Orchestrated deployments with Kubernetes
- Configured secure IAM policies and access controls
- Automated testing and quality assurance

---

## 👤 Author

**Mazin**

## 📄 License

This project is open source and available for educational purposes.
