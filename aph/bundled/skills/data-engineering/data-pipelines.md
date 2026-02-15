---
name: data-pipelines
description: "Expert in building robust and scalable data pipelines using Python, SQL, and dbt. Covers ELT, modularity, and data quality patterns."
---

# Skill: Data Engineering Pipelines (Python / SQL / dbt)

## Objectifs
- Construire des pipelines de données robustes, scalables et maintenables.
- Assurer la qualité et l'intégrité des données.
- Optimiser les performances des transformations et des requêtes.

## Stack Ciblée
- **Langage**: Python 3.9+, SQL (Dialecte spécifique: BigQuery, Snowflake, Postgres, DuckDB)
- **Transformation**: dbt (data build tool)
- **Orchestration**: Airflow, Dagster, ou Prefect
- **Data Quality**: Great Expectations, dbt tests

## Patterns Recommandés
- **ELT over ETL**: Charger les données brutes (Load) avant de les transformer (Transform) dans l'entrepôt.
- **Modularité dbt**: Modèles atomiques, staging layers, intermediate layers, marts.
- **Idempotence**: Les pipelines doivent pouvoir être relancés sans dupliquer les données (MERGE, DELETE/INSERT).
- **Schema Enforcement**: Typage strict des DataFrames (Pandas/Polars) et contraintes SQL.
- **Logging & Monitoring**: Tracer chaque étape du pipeline.

## Exemples de Prompts Recommandés
- "Génère un modèle dbt pour nettoyer les données utilisateurs brutes et calculer le revenu par cohorte."
- "Écris un script Python pour extraire des données d'une API REST avec pagination et gestion des erreurs (backoff)."
- "Optimise cette requête SQL pour réduire le scan de données dans BigQuery."

## Anti-patterns à Éviter
- **Hardcoded Credentials**: Utiliser des variables d'environnement ou un gestionnaire de secrets.
- **Select ***: Toujours expliciter les colonnes pour éviter les casses de schéma en aval.
- **Boucles en SQL**: Utiliser des opérations vectorielles ou des CTEs.
- **Manque de Tests**: Chaque transformation critique doit avoir un test (unique, not_null, accepted_values).

## Ressources Externes
- [dbt Docs](https://docs.getdbt.com/)
- [Airflow Docs](https://airflow.apache.org/)
- [Pandas Docs](https://pandas.pydata.org/)
