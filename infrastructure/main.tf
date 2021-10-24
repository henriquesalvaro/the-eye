module "vpc" {
  source                      = "./VPC"
  project                     = local.project
  region                      = local.region
  common_tags                 = local.common_tags
  vpn                         = local.vpn
  has_private_subnets         = var.has_private_subnets
  vpc_cidr_block              = var.vpc_cidr_block
  subnet_public_A_cidr_block  = var.subnet_public_A_cidr_block
  subnet_public_B_cidr_block  = var.subnet_public_B_cidr_block
  subnet_private_A_cidr_block = var.subnet_private_A_cidr_block
  subnet_private_B_cidr_block = var.subnet_private_B_cidr_block
}

module "alb" {
  source             = "./ALB"
  project            = local.project
  region             = local.region
  common_tags        = local.common_tags
  vpc_id             = module.vpc.vpc_id
  igw_resource       = module.vpc.igw_resource
  security_group_ids = [module.vpc.elb_security_group_id]
  public_subnet_ids  = module.vpc.public_subnet_ids
  certificate_arn    = var.alb_certificate_arn
}

module "rds" {
  source                  = "./RDS"
  project                 = local.project
  region                  = local.region
  common_tags             = local.common_tags
  instance_class          = var.rds_instance_class
  allocated_storage       = var.rds_allocated_storage
  subnet_ids              = var.has_private_subnets ? module.vpc.private_subnet_ids : module.vpc.public_subnet_ids
  backup_retention_period = var.rds_backup_retention_period
  vpc_security_group_ids  = [module.vpc.rds_security_group_id]
  username                = var.rds_username
  db_name                 = var.rds_db_name
  delete_protection       = var.rds_delete_protection
}

module "ecs" {
  source                                           = "./ECS"
  project                                          = local.project
  region                                           = local.region
  common_tags                                      = local.common_tags
  log_retention                                    = var.ecs_log_retention
  instance_type                                    = var.ecs_instance_type
  security_group_ids                               = [module.vpc.instances_security_group_id]
  key_name                                         = var.ecs_key_name
  max_instances                                    = var.ecs_max_instances
  min_instances                                    = var.ecs_min_instances
  desired_instances                                = var.ecs_desired_instances
  subnet_ids                                       = var.has_private_subnets ? module.vpc.private_subnet_ids : module.vpc.public_subnet_ids
  desired_service_tasks                            = var.ecs_desired_service_tasks
  deployment_maximum_percent                       = var.ecs_deployment_maximum_percent
  deployment_minimum_healthy_percent               = var.ecs_deployment_minimum_healthy_percent
  lb_target_group_arn                              = module.alb.backend_target_group_arn
  celery_worker_desired_service_tasks              = var.ecs_celery_worker_desired_service_tasks
  celery_worker_deployment_maximum_percent         = var.ecs_celery_worker_deployment_maximum_percent
  celery_worker_deployment_minimum_healthy_percent = var.ecs_celery_worker_deployment_minimum_healthy_percent
}

module "storage" {
  source          = "./Storage"
  project         = local.project
  region          = local.region
  common_tags     = local.common_tags
}

module "redis" {
  source               = "./Redis"
  project              = local.project
  region               = local.region
  common_tags          = local.common_tags
  subnet_ids           = var.has_private_subnets ? module.vpc.private_subnet_ids : module.vpc.public_subnet_ids
  engine_version       = var.redis_engine_version
  node_type            = var.redis_node_type
  parameter_group_name = var.redis_parameter_group_name
  security_group_ids   = [module.vpc.redis_security_group_id]
}
