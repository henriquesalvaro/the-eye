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

variable "security_group_ids" {
  description = "List of VPC security groups to associate"
  type        = list(string)
  default     = []
}

variable "public_subnet_ids" {
  description = "A list of VPC subnet IDs"
  type        = list(string)
  default     = []
}

variable "vpc_id" {
  description = "The VPC identifier"
  type        = string
}

variable "certificate_arn" {
  description = "Certificate ARN"
  type        = string
}

variable "igw_resource" {
  description = "Internet Gateway Resource"
  type        = any
  default     = null
}
