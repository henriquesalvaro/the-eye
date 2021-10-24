variable "project" {
  description = "The project name"
  type        = string
}

variable "region" {
  type = string
}

variable "common_tags" {
  type = map(string)
}

variable "log_retention" {
  description = "Cloudwatch log retention in days"
  type        = number
  default     = 14
}

variable "instance_type" {
  description = "Instance Type"
  type        = string
}

variable "security_group_ids" {
  description = "List of VPC security groups to associate"
  type        = list(string)
  default     = []
}

variable "key_name" {
  description = "The deployment key name"
  type        = string
}

variable "max_instances" {
  description = "The max number of allowed instances"
  type        = string
  default     = 1
}

variable "min_instances" {
  description = "The min number of allowed instances"
  type        = string
  default     = 1
}

variable "desired_instances" {
  description = "The desired number of instances"
  type        = string
  default     = 1
}

variable "subnet_ids" {
  description = "A list of VPC subnet IDs"
  type        = list(string)
  default     = []
}

variable "desired_service_tasks" {
  description = "Desired number of tasks running on service"
  type        = number
  default     = 1
}

variable "deployment_maximum_percent" {
  description = "Maximum health percentage on deployment"
  type        = number
  default     = 200
}

variable "deployment_minimum_healthy_percent" {
  description = "Minimum health percentage on deployment"
  type        = number
  default     = 100
}

variable "lb_target_group_arn" {
  description = "The target group arn of the load balancer"
  type        = string
}

variable "celery_worker_desired_service_tasks" {
  description = "Desired number of tasks running on service"
  type        = number
  default     = 1
}

variable "celery_worker_deployment_maximum_percent" {
  description = "Maximum health percentage on deployment"
  type        = number
  default     = 200
}

variable "celery_worker_deployment_minimum_healthy_percent" {
  description = "Minimum health percentage on deployment"
  type        = number
  default     = 100
}