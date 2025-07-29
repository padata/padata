import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.context import SparkContext
from pyspark.sql.functions import col

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Read source data (e.g., from S3 or JDBC)
source_df = spark.read.format("csv").option("header", "true").load("s3://your-bucket/source-data/")

# Simple transformation
transformed_df = source_df.filter(col("some_column").isNotNull())

# Write to S3 in Parquet (Glue recommended)
output_path = "s3://your-bucket/glue-output/"
transformed_df.write.mode("overwrite").parquet(output_path)

job.commit()
