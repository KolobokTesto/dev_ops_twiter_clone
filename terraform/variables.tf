variable "project_name" {
  description = "Name of the project used for resource naming"
  type        = string
  default     = "tweets"
}

variable "web_port" {
  description = "Port to expose for the web application"
  type        = number
  default     = 8000
}

variable "web_image_tag" {
  description = "Docker image tag for web application"
  type        = string
  default     = "tweets-web:dev"
}

variable "postgres_image_tag" {
  description = "Docker image tag for PostgreSQL"
  type        = string
  default     = "postgres:16-alpine"
}

# Database configuration
variable "postgres_db" {
  description = "PostgreSQL database name"
  type        = string
  default     = "tweets"
}

variable "postgres_user" {
  description = "PostgreSQL username"
  type        = string
  default     = "tweets"
}

variable "postgres_password" {
  description = "PostgreSQL password"
  type        = string
  default     = "tweets"
  sensitive   = true
}

# Django configuration
variable "django_secret_key" {
  description = "Django secret key"
  type        = string
  default     = "changeme"
  sensitive   = true
}

variable "django_debug" {
  description = "Django debug mode"
  type        = string
  default     = "1"
}

variable "django_allowed_hosts" {
  description = "Django allowed hosts"
  type        = string
  default     = "*"
}

variable "media_root" {
  description = "Media files root path"
  type        = string
  default     = "/app/media"
} 