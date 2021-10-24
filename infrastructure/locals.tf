locals {
  project = "theeye"
  region  = "us-east-1"
  common_tags = {
    Environment = terraform.workspace
    Project     = "Calories"
  }
  vpn = "vpn-ip"
}
