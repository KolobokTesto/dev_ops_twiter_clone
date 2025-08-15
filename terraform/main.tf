terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0"
    }
  }
  required_version = ">= 1.7"
}

provider "docker" {
  host = "unix:///var/run/docker.sock"
}

# Docker network for services
resource "docker_network" "tweets_net" {
  name = "${var.project_name}_net"
}

# Docker volumes
resource "docker_volume" "pgdata" {
  name = "${var.project_name}_pgdata"
}

resource "docker_volume" "media" {
  name = "${var.project_name}_media"
} 