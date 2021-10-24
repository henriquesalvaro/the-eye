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

variable "subnet_ids" {
  description = "A list of VPC subnet IDs"
  type        = list(string)
  default     = []
}

variable "engine_version" {
  description = "Engine version"
  type        = string
  default     = "5.0.5"
}

variable "node_type" {
  description = "Redis node type"
  type        = string
  default     = "cache.t2.micro"
}

variable "parameter_group_name" {
  description = "Parameter group name"
  type        = string
  default     = "default.redis5.0"
}

variable "security_group_ids" {
  description = "List of VPC security groups to associate"
  type        = list(string)
  default     = []
}
