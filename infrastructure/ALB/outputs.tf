output "backend_target_group_arn" {
  description = "The arn of the load balancer target group"
  value       = aws_lb_target_group.backend.arn
}