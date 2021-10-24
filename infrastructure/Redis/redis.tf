resource "aws_elasticache_subnet_group" "this" {
  name       = "${var.project}-${terraform.workspace}"
  subnet_ids = var.subnet_ids
}

resource "aws_elasticache_cluster" "this" {
  cluster_id           = "${var.project}-${terraform.workspace}"
  engine               = "redis"
  engine_version       = var.engine_version
  node_type            = var.node_type
  num_cache_nodes      = 1
  parameter_group_name = var.parameter_group_name
  port                 = 6379
  subnet_group_name    = aws_elasticache_subnet_group.this.name
  security_group_ids   = var.security_group_ids
  apply_immediately    = true

  tags = merge(
    var.common_tags,
    {
      Name : "Calories Backend: ${terraform.workspace}"
    }
  )
}
