output "web_url" {
  description = "URL to access the web application"
  value       = "http://localhost:${var.web_port}"
}

output "web_container_id" {
  description = "ID of the web container"
  value       = docker_container.web.id
}

output "db_container_id" {
  description = "ID of the database container"
  value       = docker_container.db.id
}

output "network_name" {
  description = "Name of the Docker network"
  value       = docker_network.tweets_net.name
}

output "volumes" {
  description = "Created Docker volumes"
  value = {
    pgdata = docker_volume.pgdata.name
    media  = docker_volume.media.name
  }
} 