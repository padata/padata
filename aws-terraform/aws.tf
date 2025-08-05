provider "aws" {
  region = var.aws_region
}

resource "aws_s3_bucket" "databricks_root_bucket" {
  bucket = var.databricks_root_bucket
  force_destroy = true
}

resource "aws_iam_role" "databricks_cross_account_role" {
  name = "databricks-cross-account-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Principal = {
          AWS = "arn:aws:iam::414351767826:root" # Databricks account ID
        },
        Effect = "Allow",
        Sid    = ""
      }
    ]
  })
}
