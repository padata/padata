# CI/CD Workflow Script for Databricks Deployment with GitHub Actions and Databricks CLI

import os
import json
import subprocess

# Paths
NOTEBOOKS_DIR = "./notebooks"
JOBS_SPEC_FILE = "jobs.json"
DATABRICKS_REPO_PATH = "Repos/<your-username>/<repo-name>"

# Load jobs.json
def load_job_spec():
    with open(JOBS_SPEC_FILE) as f:
        return json.load(f)

# Sync local notebooks to Databricks Repo
def sync_notebooks():
    for root, _, files in os.walk(NOTEBOOKS_DIR):
        for file in files:
            if file.endswith(".py") or file.endswith(".ipynb"):
                local_path = os.path.join(root, file)
                relative_path = os.path.relpath(local_path, NOTEBOOKS_DIR)
                databricks_path = os.path.join(DATABRICKS_REPO_PATH, relative_path)
                cmd = ["databricks", "workspace", "import", "--overwrite", local_path, databricks_path]
                subprocess.run(cmd, check=True)
                print(f"Synced: {local_path} -> {databricks_path}")

# Deploy jobs defined in jobs.json
def deploy_jobs():
    job_spec = load_job_spec()
    for job in job_spec["jobs"]:
        cmd = ["databricks", "jobs", "create", "--json", json.dumps(job)]
        subprocess.run(cmd, shell=True)
        print(f"Deployed job: {job.get('name', '<Unnamed>')}")

# Run PyTest for notebook validation
def run_pytest():
    result = subprocess.run(["pytest", "--maxfail=1", "--disable-warnings", "-q"], capture_output=True)
    print(result.stdout.decode())
    if result.returncode != 0:
        raise Exception("Tests failed.")

if __name__ == "__main__":
    print("Running notebook tests...")
    run_pytest()
    print("Syncing notebooks to Databricks...")
    sync_notebooks()
    print("Deploying jobs...")
    deploy_jobs()
    print("CI/CD deployment complete.")