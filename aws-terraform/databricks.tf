provider "databricks" {
  alias   = "mws"
  host    = "https://accounts.cloud.databricks.com"
  account_id = var.databricks_account_id
  username   = var.databricks_username
  password   = var.databricks_password
}

resource "databricks_mws_workspaces" "workspace" {
  provider        = databricks.mws
  account_id      = var.databricks_account_id
  aws_region      = var.aws_region
  workspace_name  = var.workspace_name
  deployment_name = var.workspace_name
  credentials_id  = databricks_mws_credentials.creds.credentials_id
  storage_configuration_id = databricks_mws_storage_config.storage.storage_configuration_id
  network_id = databricks_mws_networks.network.network_id
}

resource "databricks_mws_credentials" "creds" {
  provider    = databricks.mws
  account_id  = var.databricks_account_id
  role_arn    = aws_iam_role.databricks_cross_account_role.arn
  credentials_name = "cross-account-creds"
}

resource "databricks_mws_storage_config" "storage" {
  provider    = databricks.mws
  account_id  = var.databricks_account_id
  storage_configuration_name = "s3-root-bucket"
  bucket_name = aws_s3_bucket.databricks_root_bucket.bucket
}

resource "databricks_mws_networks" "network" {
  provider      = databricks.mws
  account_id    = var.databricks_account_id
  network_name  = "databricks-network"
  vpc_id        = var.vpc_id
  subnet_ids    = var.subnet_ids
  security_group_ids = var.security_group_ids
}
