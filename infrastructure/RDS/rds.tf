resource "random_string" "password" {
  length  = 16
  special = false
}

resource "aws_db_subnet_group" "this" {
  name = "${var.project}-${terraform.workspace}-db-subnet-group"

  subnet_ids = var.subnet_ids
  tags = {
    Project     = var.project
    Name        = "DB Subnet Group"
    Environment = terraform.workspace
  }
}

resource "aws_db_instance" "this" {
  identifier = "${var.project}-${terraform.workspace}"

  engine         = "postgres"
  engine_version = "10.6"

  instance_class              = var.instance_class
  allocated_storage           = var.allocated_storage
  storage_type                = "gp2"
  storage_encrypted           = true
  allow_major_version_upgrade = false
  apply_immediately           = true
  multi_az                    = false

  name     = var.db_name
  username = var.username
  port     = "5432"
  password = random_string.password.result
  lifecycle {
    ignore_changes = [password]
  }

  maintenance_window        = "Mon:00:00-Mon:02:00"
  backup_window             = "02:00-03:00"
  backup_retention_period   = var.backup_retention_period
  deletion_protection       = var.delete_protection
  final_snapshot_identifier = "${var.project}-${terraform.workspace}-final-snapshot"
  skip_final_snapshot       = true

  vpc_security_group_ids = var.vpc_security_group_ids
  db_subnet_group_name   = aws_db_subnet_group.this.name

  copy_tags_to_snapshot = true
  tags = merge(
    var.common_tags,
    {
      Name : "Calories Backend: ${terraform.workspace}"
    }
  )
}