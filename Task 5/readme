# Task 5: Build a Kubernetes Cluster Locally with Minikube

## 1. Objective
The primary objective of this task was to gain hands-on experience in deploying and managing applications within a single-node Kubernetes cluster. This involved using **Minikube** to deploy a containerized application (Nginx) and exposing it via a Kubernetes Service.

## 2. Tools Used
* **Minikube:** Used to run a local, single-node Kubernetes cluster.
* **kubectl:** The command-line tool used to interact with and manage the Kubernetes cluster.
* **Docker:** Used as the container runtime and driver for the Minikube virtual machine.

## 3. Deliverables
This repository contains the following files and output evidence, as required by the task:

* **`deployment.yaml`**: The Kubernetes manifest file used to define the desired state of the Nginx application.
* **`service.yaml`**: The Kubernetes manifest file used to expose the Nginx deployment.
* **Screenshots**: Images demonstrating the status of pods, services, and the scaling operation.

## 4. Execution Steps

The following steps were executed to deploy and manage the application:

### A. Cluster Setup
1.  **Minikube Started:** The local Kubernetes cluster was initialized and started using the Docker driver.
    ```bash
    minikube start --driver=docker
    ```
2.  **Cluster Verified:** The readiness of the cluster node was verified using `kubectl get nodes`.

### B. Deployment and Service
1.  **Deployment Created:** A `deployment.yaml` file was created to define an Nginx deployment with **2 replicas**.
2.  **Deployment Applied:** The deployment was applied to the cluster.
    ```bash
    kubectl apply -f deployment.yaml
    ```
3.  **Service Created:** A `service.yaml` file was created to expose the Nginx deployment using a `NodePort` type.
4.  **Service Applied:** The service was applied to the cluster.
    ```bash
    kubectl apply -f service.yaml
    ```
5.  **Verification:** Pods and services were verified using:
    ```bash
    kubectl get pods
    kubectl get services
    ```
6.  **Application Accessed:** The application was accessed locally using the NodePort URL provided by Minikube.
    ```bash
    minikube service nginx-nodeport-service --url
    # Output: http://<MINIKUBE_IP>:<NODE_PORT>
    ```

### C. Scaling and Inspection
1.  **Deployment Scaled:** The number of replicas was scaled from 2 to **4** using the `kubectl scale` command.
    ```bash
    kubectl scale deployment nginx-deployment --replicas=4
    ```
2.  **Scaling Verified:** The increase in pod count was verified with `kubectl get pods`.
3.  **Pod Inspected:** Detailed information and logs for a running pod were retrieved for inspection.
    ```bash
    kubectl describe pod <POD_NAME>
    kubectl logs <POD_NAME> -c nginx-container
    ```

## 5. Outcome and Key Concepts Learned

This task provided hands-on experience with fundamental Kubernetes concepts, including:

* **Pods:** The smallest deployable unit, representing a single instance of a running process.
* **Deployments:** An object that manages the desired state of Pods and handles rolling updates and rollbacks.
* **Services:** An abstraction that defines a logical set of Pods and a policy for accessing them (e.g., Load Balancer, NodePort, ClusterIP).
* **Scaling:** Using `kubectl scale` to easily increase or decrease the number of application replicas to meet demand.
* **`kubectl` Usage:** Proficiency in key commands like `get`, `apply`, `describe`, and `logs`.
