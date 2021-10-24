output "vpc_id" {
  description = "The VPC ID"
  value       = aws_vpc.main.id
}

output "public_subnet_ids" {
  description = "All the public subnet ids"
  value = [
    aws_subnet.public_A.id,
    aws_subnet.public_B.id
  ]
}

output "private_subnet_ids" {
  description = "All the private subnet ids"
  value = [
    join("", aws_subnet.private_A.*.id),
    join("", aws_subnet.private_B.*.id)
  ]
}

output "igw_resource" {
  description = "Internet gateway resource"
  value       = aws_internet_gateway.igw
}

output "elb_security_group_id" {
  description = "The ELB security group ID"
  value       = aws_security_group.elb_security_group.id
}

output "instances_security_group_id" {
  description = "The instances security group ID"
  value       = aws_security_group.instances_security_group.id
}

output "rds_security_group_id" {
  description = "The RDS security group ID"
  value       = aws_security_group.rds_security_group.id
}

output "redis_security_group_id" {
  description = "The Redis security group ID"
  value       = aws_security_group.redis_security_group.id
}
