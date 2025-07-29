# An end-to-end PySpark-based ETL pipeline built on Databricks
# Implements Medallion Architecture: Bronze → Silver → Gold
# Supports batch ingestion, transformation, and enrichment using Delta Lake

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, current_timestamp

# Initialize Spark Session with Delta support
spark = SparkSession.builder \
    .appName("ETL Pipeline - Medallion Architecture") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
    .getOrCreate()

# Define paths (replace with actual storage paths)
raw_path = "/mnt/data/raw/"
bronze_path = "/mnt/delta/bronze/"
silver_path = "/mnt/delta/silver/"
gold_path = "/mnt/delta/gold/"

# Ingest raw data into Bronze layer (e.g., JSON file)
def ingest_to_bronze():
    df_raw = spark.read.json(raw_path)
    df_bronze = df_raw.withColumn("ingested_at", current_timestamp())
    df_bronze.write.format("delta").mode("overwrite").save(bronze_path)

# Clean and transform Bronze data into Silver
def transform_to_silver():
    df_bronze = spark.read.format("delta").load(bronze_path)
    df_silver = df_bronze.filter(col("important_field").isNotNull())
    df_silver.write.format("delta").mode("overwrite").save(silver_path)

# Aggregate and enrich Silver data into Gold
def enrich_to_gold():
    df_silver = spark.read.format("delta").load(silver_path)
    df_gold = df_silver.groupBy("category").count()
    df_gold.write.format("delta").mode("overwrite").save(gold_path)

# Run pipeline
if __name__ == "__main__":
    print("Ingesting to Bronze...")
    ingest_to_bronze()
    print("Transforming to Silver...")
    transform_to_silver()
    print("Enriching to Gold...")
    enrich_to_gold()
    print("ETL Pipeline complete.")