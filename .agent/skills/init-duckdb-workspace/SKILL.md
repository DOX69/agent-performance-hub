---
name: init-duckdb-workspace
description: Scaffolds a standardized DuckDB analytical workspace including folders for multiple data formats (CSV, Parquet, JSON), persistent databases, and a query editor with a workflow guide.
---

# Workflow

1.  **Scaffold Directories**: Create the following structure in the project root:
    -   `duckdb/data/csv/`
    -   `duckdb/data/parquet/`
    -   `duckdb/data/json/`
    -   `duckdb/db/public/`
    -   `duckdb/query_editor/_template/`

2.  **Deploy README**: Copy the standardized `assets/README.md` to `duckdb/README.md`.

3.  **Deploy Guide**: Create `duckdb/query_editor/_template/guide.sql` with the following content:
    ```sql
    -- 1. Query files directly (In-memory)
    SELECT * FROM read_csv_auto('duckdb/data/csv/*.csv') LIMIT 10;
    SELECT * FROM read_parquet('duckdb/data/parquet/*.parquet') LIMIT 10;
    SELECT * FROM read_json_auto('duckdb/data/json/*.json') LIMIT 10;

    -- 2. Create/Open persistent DB
    -- Command: duckdb duckdb/db/public/my_data.db

    -- 3. Create tables in persistent DB
    CREATE TABLE my_table AS SELECT * FROM read_csv_auto('duckdb/data/csv/my_file.csv');

    -- 4. List existing tables
    SHOW TABLES;
    ```

## Instructions for the Agent

- Use the `assets/README.md` file provided in this skill as the source of truth for the workspace documentation.
- Ensure all directory paths are relative to the workspace root.
- If the `duckdb/` directory already exists, ask the user for confirmation before overwriting or appending.
