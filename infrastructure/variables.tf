variable "has_private_subnets" {
  type = bool
}

variable "vpc_cidr_block" {
  type        = string
  description = "CIDR block to use on the VPC"
}

variable "subnet_public_A_cidr_block" {
  type        = string
  description = "CIDR block to use on the Public Subnet A"
}

variable "subnet_public_B_cidr_block" {
  type        = string
  description = "CIDR block to use on the Public Subnet B"
}

variable "subnet_private_A_cidr_block" {
  type        = string
  description = "CIDR block to use on the Private Subnet A"
  default     = ""
}

variable "subnet_private_B_cidr_block" {
  type        = string
  description = "CIDR block to use on the Private Subnet B"
  default     = ""
}

variable "alb_certificate_arn" {
  type        = string
  description = "Certificate ARN to use on ALB HTTPS"
  default     = ""
}

variable "rds_backup_retention_period" {
  type        = number
  description = "Backup retention for aurora cluster in days"
}

variable "rds_username" {
  type        = string
  description = "Database master username"
}

variable "rds_db_name" {
  type        = string
  description = "Database name"
}

variable "rds_delete_protection" {
  type        = bool
  description = "Database deletion protection"
}

variable "rds_instance_class" {
  type        = string
  description = "Database Instance Type"
}

variable "rds_allocated_storage" {
  type        = number
  description = "Database storage allocation"
}

variable "ecs_log_retention" {
  type        = number
  description = "ECS Cloudwatch log retention in days"
}

variable "ecs_instance_type" {
  type        = string
  description = "ECS instance type"
}

variable "ecs_key_name" {
  type        = string
  description = "Keypair name to be used on ECS Instances"
}

variable "ecs_max_instances" {
  type        = number
  description = "ECS max number of instances"
}

variable "ecs_min_instances" {
  type        = number
  description = "ECS min number of instances"
}

variable "ecs_desired_instances" {
  type        = number
  description = "ECS desired number of instances"
}

variable "ecs_desired_service_tasks" {
  type        = number
  description = "ECS desired number of tasks for the application"
}

variable "ecs_deployment_maximum_percent" {
  type        = number
  description = "ECS deployment maximum health percentage"
}

variable "ecs_deployment_minimum_healthy_percent" {
  type        = number
  description = "ECS deployment minimum health percentage"
}

variable "ecs_celery_worker_desired_service_tasks" {
  description = "Desired number of tasks running on service"
  type        = number
  default     = 1
}

variable "ecs_celery_worker_deployment_maximum_percent" {
  description = "Maximum health percentage on deployment"
  type        = number
  default     = 200
}

variable "ecs_celery_worker_deployment_minimum_healthy_percent" {
  description = "Minimum health percentage on deployment"
  type        = number
  default     = 100
}

variable "redis_engine_version" {
  type        = string
  description = "Redis engine version"
}

variable "redis_node_type" {
  type        = string
  description = "Redis node type"
}

variable "redis_parameter_group_name" {
  type        = string
  description = "Redis default parameter group name"
}
