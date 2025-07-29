from pyspark.sql import SparkSession
from pyspark.sql.functions import col, current_timestamp, window
import mlflow
import mlflow.sklearn
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Initialize Spark Session
spark = SparkSession.builder \
    .appName("Streaming ETL + MLflow Pipeline") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
    .getOrCreate()

# Define Delta Lake paths
bronze_path = "/mnt/delta/bronze/streaming/"
silver_path = "/mnt/delta/silver/streaming/"
gold_path = "/mnt/delta/gold/streaming/"
checkpoint_path = "/mnt/checkpoints/streaming/"

# Streaming source config (Kafka)
kafka_bootstrap_servers = "localhost:9092"
topic_name = "events-topic"

# Ingest from Kafka to Bronze
def stream_to_bronze():
    df_kafka = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
        .option("subscribe", topic_name) \
        .option("startingOffsets", "latest") \
        .load()

    df_bronze = df_kafka.selectExpr("CAST(value AS STRING)") \
        .withColumn("ingested_at", current_timestamp())

    query = df_bronze.writeStream \
        .format("delta") \
        .outputMode("append") \
        .option("checkpointLocation", checkpoint_path + "bronze") \
        .start(bronze_path)

    return query

# Transform Bronze to Silver with schema inference and filtering
def stream_to_silver():
    df_bronze = spark.readStream.format("delta").load(bronze_path)
    df_silver = df_bronze.filter("value IS NOT NULL")

    query = df_silver.writeStream \
        .format("delta") \
        .outputMode("append") \
        .option("checkpointLocation", checkpoint_path + "silver") \
        .start(silver_path)

    return query

# Aggregate Silver to Gold with time-windowed counts
def stream_to_gold():
    df_silver = spark.readStream.format("delta").load(silver_path)
    df_gold = df_silver.withColumn("ts", current_timestamp()) \
        .groupBy(window("ts", "5 minutes")).count()

    query = df_gold.writeStream \
        .format("delta") \
        .outputMode("complete") \
        .option("checkpointLocation", checkpoint_path + "gold") \
        .start(gold_path)

    return query

# Train and log a model using MLflow
def train_and_log_model():
    iris = load_iris()
    X_train, X_test, y_train, y_test = train_test_split(iris.data, iris.target, random_state=42)
    model = LogisticRegression(max_iter=200)

    with mlflow.start_run():
        model.fit(X_train, y_train)
        predictions = model.predict(X_test)
        acc = accuracy_score(y_test, predictions)

        mlflow.log_param("model_type", "LogisticRegression")
        mlflow.log_metric("accuracy", acc)
        mlflow.sklearn.log_model(model, "model")
        print(f"Logged model with accuracy: {acc}")

if __name__ == "__main__":
    bronze_q = stream_to_bronze()
    silver_q = stream_to_silver()
    gold_q = stream_to_gold()

    print("Streaming pipeline started. Training and logging model...")
    train_and_log_model()

    bronze_q.awaitTermination()
    silver_q.awaitTermination()
    gold_q.awaitTermination()
