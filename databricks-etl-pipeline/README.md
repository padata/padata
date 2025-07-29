## Purpose
An end-to-end PySpark-based ETL pipeline built on Databricks, implementing the Medallion Architecture using Delta Lake to support batch ingestion, transformation, and data enrichment.

## Tech Stack
- Databricks (Jobs, Workflows, Repos)
- Delta Lake
- PySpark
- Azure Data Lake Gen2 / Amazon S3
- Unity Catalog (for governance)

## Features
- Ingestion from PostgreSQL, APIs, and JSON files
- Bronze → Silver → Gold transformation logic
- Schema evolution and versioning
- Performance optimizations: Partitioning and Z-Ordering
- CI/CD deployment via GitHub Actions and Databricks CLI

## Architecture