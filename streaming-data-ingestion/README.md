# Streaming Data Ingestion

## Purpose
Real-time data ingestion framework using Kafka or Kinesis and Databricks Structured Streaming to enable low-latency processing of operational events.

## Tech Stack
- Databricks (Structured Streaming, Delta Lake)
- Kafka or Kinesis (configurable)
- PySpark
- Auto Loader
- Delta Live Tables (optional)

## Features
- Streaming ingestion with checkpointing and watermarking
- Dynamic schema inference
- Time-based windowed aggregations
- Storage into Silver and Gold Delta tables
- Monitoring and metrics for observability

## Architecture