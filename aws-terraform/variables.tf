variable "aws_region" {
  type        = string
  description = "AWS region"
}

variable "databricks_account_id" {
  type        = string
  description = "Databricks account ID from https://accounts.cloud.databricks.com"
}

variable "databricks_username" {
  type        = string
  description = "Databricks account username"
}

variable "databricks_password" {
  type        = string
  description = "Databricks account password"
  sensitive   = true
}

variable "workspace_name" {
  type        = string
  description = "Name of the Databricks workspace"
}

variable "databricks_root_bucket" {
  type        = string
  description = "Name of the S3 bucket to use for Databricks workspace root storage"
}

variable "vpc_id" {
  type        = string
  description = "VPC ID for Databricks workspace networking"
}

variable "subnet_ids" {
  type        = list(string)
  description = "List of subnet IDs for Databricks workspace"
}

variable "security_group_ids" {
  type        = list(string)
  description = "List of security group IDs for Databricks workspace"
}
