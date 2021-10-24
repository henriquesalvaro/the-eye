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
