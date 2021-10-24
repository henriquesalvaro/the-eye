terraform {
  backend "s3" {
    bucket  = "theeye-backend-terraform"
    key     = "terraform.tfstate"
    region  = "us-east-1"
    encrypt = true
  }
}