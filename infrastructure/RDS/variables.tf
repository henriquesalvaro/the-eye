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

variable "instance_class" {
  description = "The RDS instance type"
  type        = string
}

variable "allocated_storage" {
  description = "The allocated storage in gigabytes"
  type        = string
}

variable "db_name" {
  description = "The database name"
  type        = string
}

variable "username" {
  description = "Username for the master DB user"
  type        = string
}

variable "backup_retention_period" {
  description = "The days to retain backups for"
  type        = number
  default     = 1
}

variable "vpc_security_group_ids" {
  description = "List of VPC security groups to associate"
  type        = list(string)
  default     = []
}

variable "subnet_ids" {
  description = "A list of VPC subnet IDs"
  type        = list(string)
  default     = []
}

variable "delete_protection" {
  description = "Indicates if the database delete protection should be enabled"
  type        = bool
}
