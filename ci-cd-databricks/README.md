# CI/CD for Databricks

## Purpose
Demonstrates CI/CD workflows for deploying Databricks jobs, workflows, and notebooks using GitHub Actions and Databricks CLI.

## Tech Stack
- GitHub Actions
- Databricks CLI
- Databricks Repos
- JSON Job API

## Features
- Automatically sync local notebooks to Databricks Repos
- Job deployment using `jobs.json` specification
- GitHub Secrets for token-based authentication
- Notebook testing with `pytest`
- Approval workflow for production deployments
