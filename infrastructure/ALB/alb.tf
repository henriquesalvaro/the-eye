resource "aws_lb" "this" {
  name               = "${var.project}-backend-${terraform.workspace}"
  internal           = false
  load_balancer_type = "application"
  security_groups    = var.security_group_ids
  subnets            = var.public_subnet_ids
  ip_address_type    = "ipv4"
  idle_timeout       = 60

  depends_on = [
    var.igw_resource
  ]

  tags = merge(
    var.common_tags,
    {
      Name : "Calories Backend: ${terraform.workspace}"
    }
  )
}

resource "aws_lb_target_group" "backend" {
  name                 = "${var.project}-backend-${terraform.workspace}"
  port                 = 8000
  protocol             = "HTTP"
  vpc_id               = var.vpc_id
  deregistration_delay = 10
  depends_on = [
    aws_lb.this,
  ]

  health_check {
    path = "/health-check/"
  }

  tags = merge(
    var.common_tags,
    {
      Name : "Calories Backend: ${terraform.workspace}"
    }
  )
}

resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.this.arn
  port              = "80"
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.backend.arn
  }
}

resource "aws_lb_listener" "https" {
  count = length(var.certificate_arn) > 0 ? 1 : 0

  load_balancer_arn = aws_lb.this.arn
  port              = "443"
  protocol          = "HTTPS"
  ssl_policy        = "ELBSecurityPolicy-2016-08"
  certificate_arn   = var.certificate_arn

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.backend.arn
  }
}
