locals {
  default_name       = "${var.project}-backend-${terraform.workspace}"
  celery_worker_name = "${var.project}-celery-worker-${terraform.workspace}"
}

# Docker image repository
resource "aws_ecr_repository" "ecr" {
  name = local.default_name

  tags = merge(
    var.common_tags,
    {
      Name : "Calories Backend: ${terraform.workspace}"
    }
  )
}

# Django
resource "aws_cloudwatch_log_group" "backend" {
  name              = local.default_name
  retention_in_days = var.log_retention

  tags = merge(
    var.common_tags,
    {
      Name : "Calories Backend: ${terraform.workspace}"
    }
  )
}

resource "aws_ecs_task_definition" "backend" {
  family = local.default_name
  container_definitions = templatefile("${path.module}/task_definition_template.json",
    {
      name      = "backend"
      image     = "${aws_ecr_repository.ecr.repository_url}:${terraform.workspace}"
      env       = terraform.workspace
      log_group = aws_cloudwatch_log_group.backend.name
      region    = var.region
    }
  )

  tags = merge(
    var.common_tags,
    {
      Name : "Calories Backend: ${terraform.workspace}"
    }
  )
}

# Celery Worker
resource "aws_cloudwatch_log_group" "celery_worker" {
  name              = local.celery_worker_name
  retention_in_days = var.log_retention

  tags = merge(
    var.common_tags,
    {
      Name : "Calories Backend: ${terraform.workspace}"
    }
  )
}

resource "aws_ecs_task_definition" "celery_worker" {
  family = local.celery_worker_name
  container_definitions = templatefile("${path.module}/celery_template.json",
    {
      name      = "celery"
      image     = "${aws_ecr_repository.ecr.repository_url}:${terraform.workspace}"
      env       = terraform.workspace
      log_group = aws_cloudwatch_log_group.celery_worker.name
      region    = var.region
      command   = ["celery", terraform.workspace]
    }
  )

  tags = merge(
    var.common_tags,
    {
      Name : "Calories Backend: ${terraform.workspace}"
    }
  )
}

# Cluster
data "aws_ami" "amazon_linux_ecs" {
  most_recent = true
  owners      = ["amazon"]
  filter {
    name   = "name"
    values = ["amzn-ami-*-amazon-ecs-optimized"]
  }
  filter {
    name   = "owner-alias"
    values = ["amazon"]
  }
}

resource "aws_ecs_cluster" "this" {
  name = local.default_name

  tags = merge(
    var.common_tags,
    {
      Name : "Calories Backend: ${terraform.workspace}"
    }
  )
}

# EC2 instance role and policies
data "aws_iam_policy_document" "ecs_instance_policy" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["ec2.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "ecs_instance_role" {
  name               = local.default_name
  path               = "/"
  assume_role_policy = data.aws_iam_policy_document.ecs_instance_policy.json

  tags = merge(
    var.common_tags,
    {
      Name : "Calories Backend: ${terraform.workspace}"
    }
  )
}

resource "aws_iam_role_policy_attachment" "ecs_instance_role_attachment" {
  role       = aws_iam_role.ecs_instance_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonEC2ContainerServiceforEC2Role"
}

resource "aws_iam_role_policy_attachment" "ecs_instance_role_attachment_S3_full_access" {
  role       = aws_iam_role.ecs_instance_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
}

resource "aws_iam_instance_profile" "ecs_instance_profile" {
  name = local.default_name
  role = aws_iam_role.ecs_instance_role.id
}

resource "aws_launch_configuration" "this" {
  name_prefix                 = local.default_name
  image_id                    = data.aws_ami.amazon_linux_ecs.id
  instance_type               = var.instance_type
  security_groups             = var.security_group_ids
  key_name                    = var.key_name
  user_data                   = "#!/bin/bash\necho ECS_CLUSTER='${aws_ecs_cluster.this.name}' > /etc/ecs/ecs.config"
  iam_instance_profile        = aws_iam_instance_profile.ecs_instance_profile.id
  associate_public_ip_address = true

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_autoscaling_group" "this" {
  name                 = local.default_name
  max_size             = var.max_instances
  min_size             = var.min_instances
  desired_capacity     = var.desired_instances
  vpc_zone_identifier  = var.subnet_ids
  launch_configuration = aws_launch_configuration.this.name
  health_check_type    = "ELB"

  lifecycle {
    create_before_destroy = true
  }

  tag {
    key                 = "Name"
    value               = "Calories Backend: ${terraform.workspace}"
    propagate_at_launch = true
  }

  dynamic "tag" {
    for_each = var.common_tags

    content {
      key                 = tag.key
      value               = tag.value
      propagate_at_launch = true
    }
  }
}

# Django service
resource "aws_ecs_service" "this" {
  name                               = local.default_name
  cluster                            = aws_ecs_cluster.this.id
  task_definition                    = aws_ecs_task_definition.backend.arn
  desired_count                      = var.desired_service_tasks
  deployment_maximum_percent         = var.deployment_maximum_percent
  deployment_minimum_healthy_percent = var.deployment_minimum_healthy_percent

  load_balancer {
    target_group_arn = var.lb_target_group_arn
    container_name   = "backend"
    container_port   = 8000
  }
}

# Celery Worker service
resource "aws_ecs_service" "celery_worker" {
  name                               = local.celery_worker_name
  cluster                            = aws_ecs_cluster.this.id
  task_definition                    = aws_ecs_task_definition.celery_worker.arn
  desired_count                      = var.celery_worker_desired_service_tasks
  deployment_maximum_percent         = var.celery_worker_deployment_maximum_percent
  deployment_minimum_healthy_percent = var.celery_worker_deployment_minimum_healthy_percent
}
