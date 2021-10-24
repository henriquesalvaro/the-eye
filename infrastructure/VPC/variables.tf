variable "project" {
  description = "The project name"
  type        = string
}

variable "region" {
  type = string
}

variable "vpn" {
  type = string
}

variable "common_tags" {
  type = map(string)
}

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
}

variable "subnet_private_B_cidr_block" {
  type        = string
  description = "CIDR block to use on the Private Subnet B"
}