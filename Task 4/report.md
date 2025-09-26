# Task 4: Git Workflow Documentation

This document summarizes the steps taken to complete Task 4: "Build a Version-Controlled DevOps Project with Git," focusing on Git best practices and branching.

## 1. Project Initialization

- Initialized a new local Git repository with `git init`.
- Created the initial files, including a `README.md`.
- Made the first commit on the default `main` branch.
- Created a `.gitignore` file to exclude unnecessary files (like logs and temporary directories).
- Connected the local repository to a new GitHub remote and pushed the `main` branch.

## 2. Setting Up Branches

The core branching structure was set up to ensure development stability:

- Created the `dev` branch from `main` to serve as the integration and testing environment (`git checkout -b dev`).
- Pushed the new `dev` branch to the remote repository (`git push -u origin dev`).

## 3. Feature Development and Merge

A new feature was developed on its own isolated branch:

- Created a new feature branch from `dev` (`git checkout -b feature/add-script`).
- Added a new script file (`new_script.sh`) and committed the changes locally.
- Pushed the `feature/add-script` branch to GitHub.

## 4. Using Pull Requests (PRs)

All merges into protected branches were performed through Pull Requests on GitHub to facilitate code review:

- **Feature to Dev:** A PR was created to merge `feature/add-script` into `dev`. This step simulates a code review and testing phase before integration.
- **Dev to Main (Release):** Once all features were integrated and verified in `dev`, a final PR was created to merge `dev` into `main`. This simulates the preparation for a stable release.

## 5. Finalizing the Release

- On the `main` branch, a Git tag was created to permanently mark the stable release point in the project's history.
- The new tag was pushed to the remote repository.
- All project steps were fully documented in the main `README.md` file.
