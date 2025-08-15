# Use pre-built web application image
resource "docker_image" "web" {
  name         = var.web_image_tag
  keep_locally = true
}

# Web application container
resource "docker_container" "web" {
  image = docker_image.web.image_id
  name  = "${var.project_name}_web"

  ports {
    internal = 8000
    external = var.web_port
  }

  env = [
    "DJANGO_SECRET_KEY=${var.django_secret_key}",
    "DJANGO_DEBUG=${var.django_debug}",
    "DJANGO_ALLOWED_HOSTS=${var.django_allowed_hosts}",
    "POSTGRES_DB=${var.postgres_db}",
    "POSTGRES_USER=${var.postgres_user}",
    "POSTGRES_PASSWORD=${var.postgres_password}",
    "POSTGRES_HOST=${docker_container.db.name}",
    "POSTGRES_PORT=5432",
    "MEDIA_ROOT=${var.media_root}"
  ]

  volumes {
    volume_name    = docker_volume.media.name
    container_path = "/app/media"
  }

  networks_advanced {
    name = docker_network.tweets_net.name
  }

  depends_on = [docker_container.db]

  restart = "unless-stopped"

  # Wait for database health check
  provisioner "local-exec" {
    command = "sleep 10"
  }
} 