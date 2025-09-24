# DevOps Task 2: Simple Jenkins CI/CD Pipeline

This project demonstrates a basic Continuous Integration and Continuous Deployment (CI/CD) pipeline built with Jenkins. The primary objective was to automate the process of building, testing, and deploying a simple Node.js web application using Docker.

## Tools and Technologies

* **Jenkins:** The automation server used to orchestrate the entire CI/CD workflow.
* **Docker:** Used for containerizing the application, ensuring a consistent and isolated deployment environment.
* **Git & GitHub:** The version control system and repository hosting service for the application source code and the `Jenkinsfile`.
* **Node.js (Express):** The runtime and framework for the simple "Hello, World!" web application.

## Project Structure

The repository contains the following key files:

* `app.js`: A simple Node.js Express server that responds with a "Hello World" message.
* `package.json`: Defines the Node.js project dependencies and scripts.
* `Dockerfile`: Contains the instructions for building a Docker image of the application.
* `Jenkinsfile`: The core of this project. It defines the pipeline stages and steps for Jenkins to execute.

## CI/CD Pipeline Workflow

The `Jenkinsfile` defines a declarative pipeline with three distinct stages:

1.  **Build:**
    * The pipeline checks out the latest code from the GitHub repository.
    * It then runs `npm install` inside the project directory (`Task 2`) to install all the required dependencies listed in `package.json`.

2.  **Test:**
    * A placeholder test script defined in `package.json` is executed to simulate a testing phase and ensure the application is stable.

3.  **Deploy:**
    * The pipeline uses the `Dockerfile` to build a new Docker image of the application.
    * It then gracefully stops and removes any container from a previous deployment.
    * Finally, it runs a new container from the newly built image, mapping port 8081 on the host to port 8080 in the container.

## How to Verify the Deployment

After a successful run of the Jenkins pipeline, the containerized application can be accessed by navigating to the following URL in a web browser:

[http://localhost:8081](http://localhost:8081)

## Learning Outcomes

This task provided hands-on experience in setting up a complete CI/CD pipeline from scratch. Key challenges included correctly configuring the Jenkins job with the proper repository URL and script path, as well as debugging `Jenkinsfile` syntax. The outcome is a functional, automated deployment process, which is a fundamental practice in modern DevOps.
