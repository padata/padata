# unity_catalog_demo.py

from pyspark.sql import SparkSession

# Initialize SparkSession with Unity Catalog support
spark = SparkSession.builder \
    .appName("Unity Catalog Demo") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.databricks.sql.initial.catalog", "main") \
    .getOrCreate()

# Configure Unity Catalog: catalog, schema, table creation with permissions
def setup_unity_catalog_demo():
    print("Setting up Unity Catalog demo...")

    # Create catalog, schema, and table
    spark.sql("""
        CREATE CATALOG IF NOT EXISTS demo_catalog;
        CREATE SCHEMA IF NOT EXISTS demo_catalog.sales_data;
        CREATE TABLE IF NOT EXISTS demo_catalog.sales_data.orders (
            order_id STRING,
            customer_id STRING,
            product_id STRING,
            quantity INT,
            order_date DATE
        ) USING DELTA;
    """)

    # Grant permissions (role must exist in Databricks/AD/AWS IAM)
    spark.sql("GRANT SELECT, INSERT ON TABLE demo_catalog.sales_data.orders TO `data_engineer_role`;")
    spark.sql("GRANT ALL PRIVILEGES ON SCHEMA demo_catalog.sales_data TO `data_admin_role`;")

    print("Unity Catalog resources and permissions configured.")

# Optionally demonstrate audit log or lineage query (placeholder)
def show_lineage_example():
    print("For lineage, use the Databricks UI under 'Data > Lineage' tab or Azure Purview integration.")

if __name__ == "__main__":
    setup_unity_catalog_demo()
    show_lineage_example()
