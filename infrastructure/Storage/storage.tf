locals {
  default_name = "${var.project}-backend-${terraform.workspace}"
}

resource "aws_s3_bucket" "bucket" {
  bucket = local.default_name
  acl    = "private"

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }

  tags = merge(
    var.common_tags,
    {
      Name : "Calories Backend: ${terraform.workspace}"
    }
  )
}
