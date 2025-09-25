# This block configures the required providers for this project.
# We need the Docker provider to interact with the Docker API.
terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0.1"
    }
  }
}

# This block defines the Docker provider configuration.
# By leaving it empty, we tell Terraform to connect to the local Docker daemon.
provider "docker" {}

# This resource block tells Terraform to pull a Docker image.
# We are pulling the latest version of the "nginx" image from Docker Hub.
resource "docker_image" "nginx" {
  name = "nginx:latest"
}

# This resource block defines the Docker container we want to create.
# It depends on the 'docker_image' resource to ensure the image is pulled first.
resource "docker_container" "nginx_server" {
  image = docker_image.nginx.image_id
  name  = "devops-task-3-nginx"

  # This maps port 80 inside the container to port 8080 on your host machine.
  ports {
    internal = 80
    external = 8888
  }
}
