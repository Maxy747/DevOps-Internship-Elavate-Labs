# Task 7: Monitor System Resources Using Netdata

This repository contains the submission for the Data Analyst Internship Task 7 at Elevate Labs.

## Objective

The goal of this task was to install Netdata, a system monitoring tool, and visualize system and application performance metrics in real-time.

## Steps Completed

1.  **Ran Netdata using Docker:** The official `netdata/netdata` Docker image was used to run the monitoring agent. The container was launched using the following command:
    ```bash
    docker run -d --name netdata -p 19999:19999 netdata/netdata
    ```
2.  **Accessed the Dashboard:** The real-time metrics dashboard was accessed at `http://localhost:19999`.
3.  **Captured Metrics:** A screenshot of the dashboard displaying live metrics for CPU, memory, and disk I/O was taken as the deliverable.

## Screenshot

[Netdata Dashboard]
![SharedScreenshot1](https://github.com/user-attachments/assets/584f9031-3145-41a4-9cfb-86ab7094a263)

![SharedScreenshot3](https://github.com/user-attachments/assets/19e49cba-9c57-47e6-af61-3d57f3d7fc5c)
