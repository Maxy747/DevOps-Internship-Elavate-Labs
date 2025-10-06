# Task 6: Host a Static Website with GitHub Pages

This repository contains the submission for Task 6 of the DevOps Internship at Elevate Labs. The objective of this task was to deploy a simple static HTML website using GitHub Pages.

## 🚀 Live Demo

The deployed website can be accessed at the following URL:

[https://maxy747.github.io/DevOps-Internship-Elavate-Labs/](https://maxy747.github.io/DevOps-Internship-Elavate-Labs/)

---

## 📝 Task Overview

-   **Objective:** Deploy a simple HTML website using GitHub Pages.
-   **Tools Used:** GitHub, GitHub Pages, GitHub Actions.
-   **Deliverables:** A live website link and the GitHub repository containing the source code.

---

## 🛠️ Steps Taken

1.  **Created the HTML File:** A basic `index.html` file was created to serve as the landing page for the website. CSS was included directly within the file for styling.

2.  **Set Up the Repository:** A new GitHub repository was initialized to host the project files.

3.  **Configured GitHub Actions for Deployment:**
    -   A GitHub Actions workflow was created at `.github/workflows/deploy.yml`.
    -   This workflow was configured to automatically build and deploy the contents of the `/Task 6` directory to GitHub Pages.
    -   The workflow is triggered on every push to the `main` branch.

4.  **Configured GitHub Pages Source:**
    -   In the repository settings, under **Settings > Pages**, the deployment source was set to **GitHub Actions**. This tells GitHub to use our custom workflow for deployments instead of a specific branch.

5.  **Pushed and Deployed:** The `index.html` file and the workflow file were pushed to the `main` branch, which triggered the deployment process and made the site live.