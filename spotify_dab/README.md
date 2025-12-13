# spotify_dab — Databricks Bundle & Transformations

This `spotify_dab` repository contains Databricks resources, DLT transformations, and supporting artifacts for a Spotify-like ETL pipeline on Azure. The project includes Databricks notebooks and a DLT-based gold layer that reads silver Delta tables produced from bronze Parquet ingests.

## What's in this folder
- `src/` — Python source code and Databricks notebooks used by jobs and pipelines.
- `resources/` — Databricks resources (pipelines, jobs) used by the Databricks bundle.
- `pyproject.toml` / `requirements.txt` — Project dependencies for development.
- `databricks.yml` — The Databricks bundle configuration and targets.

## Purpose & Goal
This subproject is focused on the Databricks side of the end-to-end pipeline:
- Execute Databricks notebooks that transform bronze Parquet files into Delta `silver` tables.
- Deploy and run Delta Live Tables (DLT) flows that maintain `gold` SCD Type 2 tables.

## Quick Links
- Databricks bundle config: [spotify_dab/databricks.yml](spotify_dab/databricks.yml#L1)
- DLT transformations: [spotify_dab/src/gold/dlt/transformations](spotify_dab/src/gold/dlt/transformations)
- Silver processing notebook: [spotify_dab/src/silver/silver_dimensions.ipynb](spotify_dab/src/silver/silver_dimensions.ipynb#L1)

---

## Prerequisites
- An Azure subscription and a Databricks workspace.
- Azure Data Lake Storage Gen2 account with `bronze` and `silver` containers.
- Azure SQL Database with the sample data (seeded using `source_scripts/spotify_initial_load.sql`).
- Installed tools on your machine:
    - `databricks` CLI (https://docs.databricks.com/dev-tools/cli/index.html)
    - `uv` package manager (optional; used by the Databricks bundle)
    - Python 3.10+ / `databricks-connect` if using local runs (see `pyproject.toml`).

## Local Development Setup
1. Create a Python virtual environment and activate it.
2. Install `uv` and project dependencies (recommended):
```bash
# If you have uv installed
uv sync --dev
# or install using pip for test-only dependencies
pip install -r requirements.txt
```
3. Configure the Databricks CLI (personal token) and connect to your workspace:
```bash
databricks configure --token
```

4. Set Databricks host in `databricks.yml` to your workspace host and update `root_path` if required. Edit:
 - `spotify_dab/databricks.yml` — `workspace.host`, `root_path` and `permissions`.

## Deploying to Databricks (Dev)
Use the Databricks bundle support in the Databricks CLI to deploy the bundle.

```bash
# Authenticate first
databricks configure --token

# Deploy the bundle to the dev target
databricks bundle deploy --target dev

# Run the sample job/pipeline (created by the bundle)
databricks bundle run
```

Notes:
- The `resources` folder contains `spotify_dab_etl.pipeline.yml` and `sample_job.job.yml` that define the pipeline and job tasks.
- Deployment will import the resources to the configured Databricks workspace. `--target` `dev`/`prod` changes mode and default scheduling.

## Delta Live Tables (DLT) — Deploying Gold Layers
Deltal Live Tables are in `src/gold/dlt/transformations` and produce SCD Type 2 gold tables from `spotify_cata.silver.<table>`.
- DLT scripts expect silver tables to exist. Deploy the DLT pipeline via the Databricks Workspace UI or by bundling resources and running the associated pipeline.

### Creating a DLT Pipeline
1. In the Databricks UI, navigate to **Workflows -> Delta Live Tables**.
2. Create a pipeline and specify the Python file(s) or folder (e.g., `src/gold/dlt`).
3. Configure `catalog` and `schema` variables and runtime environment.

## Running the Databricks Notebooks (silver)
The `silver_dimensions.ipynb` notebook uses Autoloader to read Parquet files from ADLS bronze, transforms the data, deduplicates, and writes Delta tables in the `silver` layer.

To run interactively:
1. Open the notebook in your Databricks workspace or use the Databricks CLI.
2. Update storage paths in the notebook if your storage account differs (`abfss://bronze@storagespotifyazure...`).
3. Run the notebook cells to ingest bronze data to Delta `silver` tables (e.g., `spotify_cata.silver.DimUser`).

## Seeding the Azure SQL DB (Optional Test Data)
The repo contains `source_scripts/spotify_initial_load.sql` with a consistent, large seed dataset. To load it:
1. Connect to your Azure SQL Database using your preferred SQL client.
2. Run the SQL script to create tables and seed data.

## Running Tests
The bundle uses `pytest` for tests and `uv` for dependencies.
```bash
# Run tests
uv run pytest
```

## Important Configuration Tips
- Use Azure Key Vault or Databricks secrets to store database credentials and storage SAS keys. Avoid committing secrets in code.
- Update ADF and Databricks configs to match your environment:
    - Linked services: `linkedService/AzureSqlDatabase1.json`, `linkedService/AzureDataLakeStorage1.json`
    - Databricks `databricks.yml` and `resources` files
- Update the runtime images and cluster specs in the Databricks UI for production scale.

## Troubleshooting
- If Autoloader can't find files, verify the `abfss://` path and ADLS permissions.
- If ADF fails to connect, check firewall rules on the Azure SQL instance and ensure the ADF managed identity has network access.
- For DLT, check pipeline logs and look for schema changes that break SCD flows.

## Contribution
Contributions are welcome. See the main repo README for contribution guidance and where to find the ADF and Databricks artifacts.

## License
This repository uses the same license as the project root (see `LICENSE` for details).

