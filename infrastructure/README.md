# Backend application infrastructure

# Requirements
- [Terraform](https://www.terraform.io/)
- [AWS Vault](https://github.com/99designs/aws-vault)

## Quick access

- [ALB](#alb)
- [ECS](#ecs)
- [RDS](#rds)
- [Redis](#redis)
- [Storage](#storage)
- [VPC](#vpc)

## Workspace env

In order to deploy a new workspace you need to create a file called `WORKSPACE.tfvars` with the following structure:
```tfvars
has_private_subnets                                  =
vpc_cidr_block                                       =
subnet_public_A_cidr_block                           =
subnet_public_B_cidr_block                           =
subnet_private_A_cidr_block                          = # This is optional if has_private_subnets=false
subnet_private_B_cidr_block                          = # This is optional if has_private_subnets=false
alb_certificate_arn                                  = # This can be ""
rds_backtrack_window                                 =
rds_backup_retention_period                          =
rds_username                                         =
rds_db_name                                          =
rds_delete_protection                                =
ecs_log_retention                                    =
ecs_instance_type                                    =
ecs_key_name                                         =
ecs_max_instances                                    =
ecs_min_instances                                    =
ecs_desired_instances                                =
ecs_desired_service_tasks                            =
ecs_deployment_maximum_percent                       =
ecs_deployment_minimum_healthy_percent               =
ecs_celery_worker_desired_service_tasks              =
ecs_celery_worker_deployment_maximum_percent         =
ecs_celery_worker_deployment_minimum_healthy_percent =
redis_engine_version                                 =
redis_node_type                                      =
redis_parameter_group_name                           =
```

## Deploying a new workspace

In order to create a new deploy, follow these steps:
1. Create a new workspace: `./terraform.sh workspace new WORKSPACE`
2. Enter the workspace: `./terraform.sh workspace select WORKSPACE`
3. Create a file called `WORKSPACE.tfvars` with the structure from the section [above](#workspace-env)
4. Run the script: `./apply.sh`

## Modules

### VPC

Created resources:

- VPC
- 2 public subnets
- 2 private subnets
- Internet Gateway
- Main route table for public subnets
- 2 NAT gateways (One placed on each public subnet)
- 2 Private route tables with traffic to each NAT gateway
- Security groups for:
  - ELB
  - Instances
  - RDS
  - Redis

### ALB

Created resources:

- ALB
- Backend target group
- HTTP listener
- HTTPS listener

### RDS

Created resources:

- DB subnet group
- RDS instance

### ECS

Created resources:

- ECR
- Cloudwatch log group
- Backend task definition
- Celery Worker task definition
- ECS Cluster
- IAM Role for ECS Instance
  - AmazonEC2ContainerServiceforEC2Role Policy
  - AmazonS3FullAccess Policy
- IAM Instance profile
- Launch Configuration
- Autoscaling group
- ECS service for django
- ECS service for celery worker

### Redis

Created resources:

- Elasticache subnet group
- Elasticache cluster

### Storage

Created resources:

- S3 bucket
