# DevOps-Internship-Elavate-Labs
Continuous Integration/Continuous Deployment

# DevOps-Internship-Elavate-Labs

This repository contains a simple Node.js application with a CI/CD pipeline configured using GitHub Actions. The pipeline automates the process of testing the application, building a Docker image, and pushing it to Docker Hub.

## How to Run Locally

To run this application on your local machine, you'll need to have Node.js and npm installed.

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/DevOps-Internship-Elavate-Labs.git](https://github.com/your-username/DevOps-Internship-Elavate-Labs.git)
    ```
2.  **Navigate to the project directory:**
    ```bash
    cd DevOps-Internship-Elavate-Labs
    ```
3.  **Install the dependencies:**
    ```bash
    npm install
    ```
4.  **Start the server:**
    ```bash
    npm start
    ```
    The application will be running at `http://localhost:8080`.

## CI/CD Pipeline

The CI/CD pipeline is defined in the `.github/workflows/main.yml` file and consists of two jobs:

* **`test`:** This job runs on every push to the `main` branch. It checks out the code, installs the dependencies, and runs the tests using `npm test`.
* **`build-and-push`:** This job runs after the `test` job has completed successfully. It builds a Docker image of the application and pushes it to Docker Hub.

## Technologies Used

* **Node.js:** A JavaScript runtime built on Chrome's V8 JavaScript engine.
* **Express.js:** A minimal and flexible Node.js web application framework.
* **Docker:** A platform for developing, shipping, and running applications in containers.
* **GitHub Actions:** A CI/CD platform that allows you to automate your build, test, and deployment pipeline.
