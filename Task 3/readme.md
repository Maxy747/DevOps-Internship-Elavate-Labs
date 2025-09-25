# Task 3: Provision a Docker Container with Terraform

This project demonstrates the use of **Terraform** as an Infrastructure as Code (IaC) tool to provision a local Docker container. The goal is to define the desired state of the infrastructure in a configuration file (`main.tf`) and use Terraform to create, manage, and destroy the resources.

## Tools Used
* **Terraform**: To manage the infrastructure lifecycle.
* **Docker**: To run the containerized application.

## Process Overview
1.  **Configuration**: The `main.tf` file is written to define a Docker image and a Docker container resource.
2.  **Initialization**: `terraform init` is run to initialize the working directory and download the necessary Docker provider.
3.  **Planning**: `terraform plan` is used to preview the changes that will be made to the infrastructure.
4.  **Application**: `terraform apply` executes the plan, pulling the Docker image and starting the container.
5.  **Destruction**: `terraform destroy` is run to tear down all managed infrastructure.

---

## Execution Logs 📜
Here are the complete logs from the terminal, showing the entire Terraform workflow.

### `terraform init`
```
PS C:\Users\MoeLustHer\Documents\GitHub\DevOps-Internship-Elavate-Labs\Task 3> terraform init
Initializing the backend...
Initializing provider plugins...
- Reusing previous version of kreuzwerker/docker from the dependency lock file
- Installing kreuzwerker/docker v3.0.2...
- Installed kreuzwerker/docker v3.0.2 (self-signed, key ID BD080C4571C6104C)

Terraform has been successfully initialized!
```

### `terraform plan`
```
PS C:\Users\MoeLustHer\Documents\GitHub\DevOps-Internship-Elavate-Labs\Task 3> terraform plan
docker_image.nginx: Refreshing state...
docker_container.nginx_server: Refreshing state...

Terraform will perform the following actions:

  # docker_container.nginx_server must be replaced
-/+ resource "docker_container" "nginx_server" {
      ~ id               = "5d61cd807960..." -> (known after apply)
      - network_mode     = "bridge" -> null # forces replacement
        # (48 attributes unchanged)
    }

Plan: 1 to add, 0 to change, 1 to destroy.
```

### `terraform apply`
```
PS C:\Users\MoeLustHer\Documents\GitHub\DevOps-Internship-Elavate-Labs\Task 3> terraform apply
docker_image.nginx: Refreshing state...
docker_container.nginx_server: Refreshing state...

Plan: 1 to add, 0 to change, 1 to destroy.

Do you want to perform these actions?
  Only 'yes' will be accepted to approve.

  Enter a value: yes

docker_container.nginx_server: Destroying... [id=5d61cd807960...]
docker_container.nginx_server: Destruction complete after 1s
docker_container.nginx_server: Creating...
docker_container.nginx_server: Creation complete after 0s [id=d51e782fe8ec...]

Apply complete! Resources: 1 added, 0 changed, 1 destroyed.
```
