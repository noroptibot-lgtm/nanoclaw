# Data Engineering (Senior Data Engineer)

## Overview

The Data Engineering skill provides comprehensive tools and frameworks for building scalable data pipelines, ETL processes, and data infrastructure using modern technologies like Apache Spark, Airflow, dbt, and Snowflake. This skill enables data engineers to design and implement robust data architectures, optimize data workflows, and ensure data quality and governance. It combines pipeline orchestration, data transformation, warehouse design, and streaming data processing with deep expertise in distributed systems and data modeling.

## Who Should Use This Skill

- **Data Engineers** building data pipelines and infrastructure
- **Senior Data Engineers** architecting data platforms
- **ETL Developers** creating data transformation workflows
- **Data Platform Engineers** managing data infrastructure
- **Analytics Engineers** building data models
- **Data Architects** designing data warehouses
- **ML Engineers** preparing data for ML pipelines
- **Tech Leads** establishing data engineering standards

## Purpose and Use Cases

Use this skill when you need to:
- Build ETL/ELT data pipelines
- Design data warehouse architectures
- Implement real-time streaming pipelines
- Create data quality frameworks
- Build data orchestration workflows
- Implement data lake architectures
- Create dimensional data models
- Build batch processing systems
- Implement CDC (Change Data Capture)
- Create data lineage tracking
- Build data catalog systems
- Implement data governance frameworks

**Keywords that trigger this skill:** data engineering, ETL, ELT, data pipeline, Airflow, Spark, dbt, Snowflake, data warehouse, data lake, streaming, Kafka, data modeling, dimensional modeling

## What's Included

### Pipeline Generator

**Pipeline Templates:**
- **Batch ETL Pipeline** - Scheduled data extraction and loading
- **Streaming Pipeline** - Real-time data processing with Kafka/Flink
- **ELT Pipeline** - Modern cloud data warehouse pattern
- **CDC Pipeline** - Change data capture and replication
- **Data Quality Pipeline** - Validation and monitoring
- **ML Feature Pipeline** - Feature engineering for ML
- **API Data Pipeline** - REST/GraphQL data ingestion
- **File Processing Pipeline** - CSV, Parquet, JSON processing

**Generation Features:**
```bash
# Generate Airflow DAG for batch ETL
python scripts/pipeline_generator.py batch-etl sales_pipeline \
  --source postgres \
  --destination snowflake \
  --schedule "0 2 * * *" \
  --with-quality-checks \
  --with-notifications

# Generate streaming pipeline
python scripts/pipeline_generator.py streaming orders_stream \
  --source kafka \
  --destination bigquery \
  --processing spark-structured-streaming \
  --with-schema-registry

# Generate dbt transformation project
python scripts/pipeline_generator.py dbt-project analytics \
  --warehouse snowflake \
  --models staging,intermediate,marts \
  --with-tests \
  --with-docs

# Generate data quality framework
python scripts/pipeline_generator.py data-quality \
  --tables users,orders,products \
  --checks completeness,accuracy,consistency \
  --framework great-expectations
```

**Generated Pipeline Structure (Airflow):**
```python
# dags/sales_etl_pipeline.py
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.snowflake.hooks.snowflake import SnowflakeHook
from airflow.operators.email import EmailOperator
import pandas as pd

default_args = {
    'owner': 'data-engineering',
    'depends_on_past': False,
    'email': ['data-team@company.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'sales_etl_pipeline',
    default_args=default_args,
    description='Daily sales data ETL pipeline',
    schedule_interval='0 2 * * *',  # Run at 2 AM daily
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['etl', 'sales', 'daily'],
)

def extract_sales_data(**context):
    """Extract sales data from PostgreSQL source"""
    execution_date = context['execution_date']
    start_date = execution_date.strftime('%Y-%m-%d')
    end_date = (execution_date + timedelta(days=1)).strftime('%Y-%m-%d')

    pg_hook = PostgresHook(postgres_conn_id='postgres_source')

    query = f"""
        SELECT
            order_id,
            customer_id,
            product_id,
            quantity,
            unit_price,
            total_amount,
            order_date,
            status
        FROM sales.orders
        WHERE order_date >= '{start_date}'
        AND order_date < '{end_date}'
    """

    df = pg_hook.get_pandas_df(query)

    # Save to XCom
    context['ti'].xcom_push(key='sales_data_count', value=len(df))

    # Save to staging
    staging_path = f'/tmp/sales_staging_{execution_date}.parquet'
    df.to_parquet(staging_path, index=False)

    return staging_path

def transform_sales_data(**context):
    """Transform and clean sales data"""
    ti = context['ti']
    staging_path = ti.xcom_pull(task_ids='extract_sales_data')

    df = pd.read_parquet(staging_path)

    # Data transformations
    # 1. Handle missing values
    df['customer_id'].fillna('UNKNOWN', inplace=True)

    # 2. Calculate derived fields
    df['discount_amount'] = (df['unit_price'] * df['quantity']) - df['total_amount']
    df['discount_percentage'] = (df['discount_amount'] / (df['unit_price'] * df['quantity'])) * 100

    # 3. Add metadata
    df['etl_timestamp'] = datetime.now()
    df['etl_date'] = context['execution_date'].date()

    # 4. Data type conversions
    df['order_date'] = pd.to_datetime(df['order_date'])
    df['total_amount'] = df['total_amount'].astype(float)

    # 5. Remove duplicates
    df.drop_duplicates(subset=['order_id'], keep='first', inplace=True)

    # Save transformed data
    transformed_path = f'/tmp/sales_transformed_{context["execution_date"]}.parquet'
    df.to_parquet(transformed_path, index=False)

    # Push metrics to XCom
    ti.xcom_push(key='transformed_count', value=len(df))
    ti.xcom_push(key='duplicate_count', value=len(df) - len(df.drop_duplicates()))

    return transformed_path

def validate_data_quality(**context):
    """Run data quality checks"""
    ti = context['ti']
    transformed_path = ti.xcom_pull(task_ids='transform_sales_data')

    df = pd.read_parquet(transformed_path)

    quality_checks = []

    # Check 1: No null values in critical columns
    critical_columns = ['order_id', 'product_id', 'quantity', 'total_amount']
    null_counts = df[critical_columns].isnull().sum()
    if null_counts.sum() > 0:
        quality_checks.append({
            'check': 'null_values',
            'status': 'FAILED',
            'details': null_counts.to_dict()
        })
    else:
        quality_checks.append({
            'check': 'null_values',
            'status': 'PASSED'
        })

    # Check 2: Valid value ranges
    if (df['quantity'] < 0).any():
        quality_checks.append({
            'check': 'quantity_range',
            'status': 'FAILED',
            'details': 'Negative quantities found'
        })
    else:
        quality_checks.append({
            'check': 'quantity_range',
            'status': 'PASSED'
        })

    # Check 3: Record count threshold
    min_expected_records = 100
    if len(df) < min_expected_records:
        quality_checks.append({
            'check': 'record_count',
            'status': 'WARNING',
            'details': f'Only {len(df)} records, expected at least {min_expected_records}'
        })
    else:
        quality_checks.append({
            'check': 'record_count',
            'status': 'PASSED'
        })

    # Check for failures
    failed_checks = [c for c in quality_checks if c['status'] == 'FAILED']
    if failed_checks:
        raise ValueError(f"Data quality checks failed: {failed_checks}")

    return quality_checks

def load_to_snowflake(**context):
    """Load data to Snowflake data warehouse"""
    ti = context['ti']
    transformed_path = ti.xcom_pull(task_ids='transform_sales_data')

    df = pd.read_parquet(transformed_path)

    snow_hook = SnowflakeHook(snowflake_conn_id='snowflake_dw')

    # Load to staging table
    snow_hook.insert_rows(
        table='STAGING.SALES_ORDERS',
        rows=df.values.tolist(),
        target_fields=df.columns.tolist(),
    )

    # Merge into production table
    merge_query = """
        MERGE INTO PRODUCTION.SALES_ORDERS AS target
        USING STAGING.SALES_ORDERS AS source
        ON target.order_id = source.order_id
        WHEN MATCHED THEN
            UPDATE SET
                customer_id = source.customer_id,
                product_id = source.product_id,
                quantity = source.quantity,
                total_amount = source.total_amount,
                updated_at = CURRENT_TIMESTAMP()
        WHEN NOT MATCHED THEN
            INSERT (
                order_id, customer_id, product_id, quantity,
                total_amount, order_date, etl_timestamp
            )
            VALUES (
                source.order_id, source.customer_id, source.product_id,
                source.quantity, source.total_amount, source.order_date,
                source.etl_timestamp
            )
    """

    snow_hook.run(merge_query)

    # Clean up staging
    snow_hook.run("TRUNCATE TABLE STAGING.SALES_ORDERS")

    return len(df)

# Define tasks
extract_task = PythonOperator(
    task_id='extract_sales_data',
    python_callable=extract_sales_data,
    dag=dag,
)

transform_task = PythonOperator(
    task_id='transform_sales_data',
    python_callable=transform_sales_data,
    dag=dag,
)

quality_task = PythonOperator(
    task_id='validate_data_quality',
    python_callable=validate_data_quality,
    dag=dag,
)

load_task = PythonOperator(
    task_id='load_to_snowflake',
    python_callable=load_to_snowflake,
    dag=dag,
)

success_email = EmailOperator(
    task_id='send_success_email',
    to='data-team@company.com',
    subject='Sales ETL Pipeline - Success',
    html_content="""
        <h3>Sales ETL Pipeline Completed Successfully</h3>
        <p>Execution Date: {{ execution_date }}</p>
        <p>Records Processed: {{ ti.xcom_pull(task_ids='transform_sales_data', key='transformed_count') }}</p>
    """,
    dag=dag,
)

# Set task dependencies
extract_task >> transform_task >> quality_task >> load_task >> success_email
```

**Generated dbt Project:**
```yaml
# dbt_project.yml
name: 'analytics'
version: '1.0.0'
config-version: 2

profile: 'snowflake'

model-paths: ["models"]
analysis-paths: ["analyses"]
test-paths: ["tests"]
seed-paths: ["seeds"]
macro-paths: ["macros"]
snapshot-paths: ["snapshots"]

target-path: "target"
clean-targets:
  - "target"
  - "dbt_packages"

models:
  analytics:
    staging:
      +materialized: view
      +schema: staging
    intermediate:
      +materialized: view
      +schema: intermediate
    marts:
      +materialized: table
      +schema: marts
```

```sql
-- models/staging/stg_orders.sql
{{
    config(
        materialized='view',
        tags=['staging', 'orders']
    )
}}

WITH source AS (
    SELECT * FROM {{ source('raw', 'orders') }}
),

renamed AS (
    SELECT
        order_id,
        customer_id,
        product_id,
        quantity,
        unit_price,
        total_amount,
        order_date,
        status,
        created_at,
        updated_at

    FROM source

    WHERE order_date >= '2020-01-01'
)

SELECT * FROM renamed

-- models/staging/stg_orders.yml
version: 2

models:
  - name: stg_orders
    description: "Staging table for orders from source system"
    columns:
      - name: order_id
        description: "Unique identifier for the order"
        tests:
          - unique
          - not_null

      - name: customer_id
        description: "Foreign key to customers table"
        tests:
          - not_null
          - relationships:
              to: ref('stg_customers')
              field: customer_id

      - name: total_amount
        description: "Total order amount"
        tests:
          - not_null
          - dbt_expectations.expect_column_values_to_be_between:
              min_value: 0
              max_value: 1000000

      - name: order_date
        description: "Date the order was placed"
        tests:
          - not_null

-- models/intermediate/int_order_items.sql
{{
    config(
        materialized='view',
        tags=['intermediate', 'orders']
    )
}}

WITH orders AS (
    SELECT * FROM {{ ref('stg_orders') }}
),

products AS (
    SELECT * FROM {{ ref('stg_products') }}
),

customers AS (
    SELECT * FROM {{ ref('stg_customers') }}
),

enriched AS (
    SELECT
        o.order_id,
        o.order_date,
        o.quantity,
        o.unit_price,
        o.total_amount,

        c.customer_id,
        c.customer_name,
        c.customer_segment,

        p.product_id,
        p.product_name,
        p.category,
        p.brand,

        -- Calculated fields
        o.quantity * o.unit_price AS gross_amount,
        o.total_amount - (o.quantity * o.unit_price) AS discount_amount,
        CASE
            WHEN o.total_amount > 0 THEN
                ((o.quantity * o.unit_price - o.total_amount) / (o.quantity * o.unit_price)) * 100
            ELSE 0
        END AS discount_percentage

    FROM orders o
    LEFT JOIN customers c ON o.customer_id = c.customer_id
    LEFT JOIN products p ON o.product_id = p.product_id
)

SELECT * FROM enriched

-- models/marts/fct_sales.sql
{{
    config(
        materialized='table',
        tags=['marts', 'sales']
    )
}}

WITH order_items AS (
    SELECT * FROM {{ ref('int_order_items') }}
),

aggregated AS (
    SELECT
        order_id,
        order_date,
        customer_id,
        customer_name,
        customer_segment,

        -- Aggregated metrics
        COUNT(DISTINCT product_id) AS num_products,
        SUM(quantity) AS total_quantity,
        SUM(gross_amount) AS total_gross_amount,
        SUM(discount_amount) AS total_discount_amount,
        SUM(total_amount) AS total_net_amount,

        -- Average metrics
        AVG(unit_price) AS avg_unit_price,
        AVG(discount_percentage) AS avg_discount_percentage

    FROM order_items

    GROUP BY 1, 2, 3, 4, 5
)

SELECT * FROM aggregated
```

### Streaming Pipeline Framework

**Streaming Technologies:**
- Kafka with Kafka Streams
- Apache Flink
- Spark Structured Streaming
- AWS Kinesis
- Google Dataflow
- Apache Beam

**Streaming Features:**
```python
# Spark Structured Streaming pipeline
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

spark = SparkSession.builder \
    .appName("OrderStreamProcessing") \
    .getOrCreate()

# Define schema
order_schema = StructType([
    StructField("order_id", StringType(), False),
    StructField("customer_id", StringType(), False),
    StructField("product_id", StringType(), False),
    StructField("quantity", IntegerType(), False),
    StructField("price", DoubleType(), False),
    StructField("timestamp", TimestampType(), False),
])

# Read from Kafka
orders_stream = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "orders") \
    .option("startingOffsets", "latest") \
    .load()

# Parse JSON
parsed_orders = orders_stream \
    .select(from_json(col("value").cast("string"), order_schema).alias("data")) \
    .select("data.*")

# Transformations
enriched_orders = parsed_orders \
    .withColumn("total_amount", col("quantity") * col("price")) \
    .withColumn("processing_time", current_timestamp()) \
    .withWatermark("timestamp", "10 minutes")

# Aggregations with windowing
order_metrics = enriched_orders \
    .groupBy(
        window(col("timestamp"), "5 minutes"),
        col("product_id")
    ) \
    .agg(
        count("*").alias("order_count"),
        sum("quantity").alias("total_quantity"),
        sum("total_amount").alias("revenue"),
        avg("price").alias("avg_price")
    )

# Write to sink
query = order_metrics \
    .writeStream \
    .format("console") \
    .outputMode("update") \
    .option("truncate", False) \
    .start()

query.awaitTermination()
```

### Data Quality Framework

**Quality Check Types:**
- Completeness checks (null values, missing data)
- Accuracy checks (value ranges, formats)
- Consistency checks (referential integrity)
- Timeliness checks (data freshness)
- Uniqueness checks (duplicate detection)
- Schema validation
- Statistical validation

**Implementation (Great Expectations):**
```python
# great_expectations/expectations/orders_suite.py
import great_expectations as ge
from great_expectations.dataset import PandasDataset

def create_expectations_suite():
    """Create comprehensive expectations suite for orders data"""

    suite = ge.core.ExpectationSuite(expectation_suite_name="orders_suite")

    # Completeness checks
    suite.add_expectation(
        ge.core.ExpectationConfiguration(
            expectation_type="expect_column_values_to_not_be_null",
            kwargs={"column": "order_id"}
        )
    )

    suite.add_expectation(
        ge.core.ExpectationConfiguration(
            expectation_type="expect_column_values_to_not_be_null",
            kwargs={"column": "customer_id"}
        )
    )

    # Uniqueness checks
    suite.add_expectation(
        ge.core.ExpectationConfiguration(
            expectation_type="expect_column_values_to_be_unique",
            kwargs={"column": "order_id"}
        )
    )

    # Value range checks
    suite.add_expectation(
        ge.core.ExpectationConfiguration(
            expectation_type="expect_column_values_to_be_between",
            kwargs={
                "column": "quantity",
                "min_value": 1,
                "max_value": 1000
            }
        )
    )

    suite.add_expectation(
        ge.core.ExpectationConfiguration(
            expectation_type="expect_column_values_to_be_between",
            kwargs={
                "column": "total_amount",
                "min_value": 0,
                "max_value": 1000000
            }
        )
    )

    # Format checks
    suite.add_expectation(
        ge.core.ExpectationConfiguration(
            expectation_type="expect_column_values_to_match_regex",
            kwargs={
                "column": "order_id",
                "regex": "^ORD[0-9]{10}$"
            }
        )
    )

    # Statistical checks
    suite.add_expectation(
        ge.core.ExpectationConfiguration(
            expectation_type="expect_column_mean_to_be_between",
            kwargs={
                "column": "total_amount",
                "min_value": 50,
                "max_value": 500
            }
        )
    )

    # Referential integrity
    suite.add_expectation(
        ge.core.ExpectationConfiguration(
            expectation_type="expect_column_values_to_be_in_set",
            kwargs={
                "column": "status",
                "value_set": ["pending", "processing", "completed", "cancelled"]
            }
        )
    )

    return suite

# Validate data
def validate_orders_data(df):
    """Validate orders dataframe against expectations"""
    ge_df = ge.from_pandas(df)

    results = ge_df.validate(expectation_suite=create_expectations_suite())

    if not results.success:
        failed_expectations = [
            exp for exp in results.results
            if not exp.success
        ]
        raise ValueError(f"Data quality validation failed: {failed_expectations}")

    return results
```

### Data Warehouse Designer

**Design Features:**
- Dimensional modeling (star/snowflake schemas)
- Slowly Changing Dimensions (SCD Type 1, 2, 3)
- Fact table design
- Aggregate tables
- Data mart creation
- Partitioning strategies
- Index optimization

**Dimensional Model Example:**
```sql
-- Dimension Tables

-- DIM_CUSTOMER (SCD Type 2)
CREATE TABLE DIM_CUSTOMER (
    customer_key BIGINT PRIMARY KEY,
    customer_id VARCHAR(50) NOT NULL,
    customer_name VARCHAR(200) NOT NULL,
    email VARCHAR(200),
    segment VARCHAR(50),
    country VARCHAR(50),

    -- SCD Type 2 fields
    valid_from DATE NOT NULL,
    valid_to DATE,
    is_current BOOLEAN DEFAULT TRUE,

    -- Audit fields
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- DIM_PRODUCT
CREATE TABLE DIM_PRODUCT (
    product_key BIGINT PRIMARY KEY,
    product_id VARCHAR(50) NOT NULL,
    product_name VARCHAR(200) NOT NULL,
    category VARCHAR(100),
    subcategory VARCHAR(100),
    brand VARCHAR(100),
    unit_price DECIMAL(10, 2),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- DIM_DATE
CREATE TABLE DIM_DATE (
    date_key INT PRIMARY KEY,
    date DATE NOT NULL,
    year INT,
    quarter INT,
    month INT,
    month_name VARCHAR(20),
    week INT,
    day_of_month INT,
    day_of_week INT,
    day_name VARCHAR(20),
    is_weekend BOOLEAN,
    is_holiday BOOLEAN,
    fiscal_year INT,
    fiscal_quarter INT
);

-- Fact Table

-- FCT_SALES
CREATE TABLE FCT_SALES (
    sales_key BIGINT PRIMARY KEY,
    order_id VARCHAR(50) NOT NULL,

    -- Foreign keys to dimensions
    customer_key BIGINT REFERENCES DIM_CUSTOMER(customer_key),
    product_key BIGINT REFERENCES DIM_PRODUCT(product_key),
    order_date_key INT REFERENCES DIM_DATE(date_key),

    -- Measures
    quantity INT NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL,
    discount_amount DECIMAL(10, 2) DEFAULT 0,
    tax_amount DECIMAL(10, 2) DEFAULT 0,
    total_amount DECIMAL(10, 2) NOT NULL,

    -- Degenerate dimensions
    order_status VARCHAR(50),

    -- Audit
    etl_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
PARTITION BY RANGE (order_date_key);
```

## Technical Details

### Data Modeling Best Practices

**Dimensional Modeling:**
- Star schema for simplicity and performance
- Snowflake schema for normalized dimensions
- Slowly Changing Dimensions for historical tracking
- Conformed dimensions across data marts
- Role-playing dimensions for multiple relationships

**Data Vault Modeling:**
- Hubs for business entities
- Links for relationships
- Satellites for descriptive attributes
- Suitable for enterprise data warehouses

### Performance Optimization

**Partitioning:**
```sql
-- Time-based partitioning (Snowflake)
CREATE TABLE sales (
    order_id VARCHAR,
    order_date DATE,
    amount DECIMAL
)
PARTITION BY DATE_TRUNC('MONTH', order_date);

-- Range partitioning (PostgreSQL)
CREATE TABLE sales (
    order_id VARCHAR,
    order_date DATE,
    amount DECIMAL
) PARTITION BY RANGE (order_date);
```

**Clustering:**
```sql
-- Clustering (Snowflake)
CREATE TABLE sales (
    order_id VARCHAR,
    customer_id VARCHAR,
    order_date DATE
)
CLUSTER BY (customer_id, order_date);
```

## Best Practices

**Do:**
- Implement data quality checks at every stage
- Use incremental processing when possible
- Implement idempotent pipelines
- Version control all pipeline code
- Monitor pipeline performance and failures
- Document data lineage
- Use orchestration tools (Airflow, Prefect)
- Implement proper error handling and retries
- Use appropriate data formats (Parquet, Avro)
- Implement data governance

**Don't:**
- Process all data in single large batches
- Ignore data quality issues
- Skip testing pipelines
- Hard-code configuration values
- Ignore pipeline monitoring
- Skip documentation
- Use inefficient data formats (CSV for large data)
- Ignore data security and privacy
- Skip backup and recovery procedures

## Integration Points

This skill integrates with:
- **Orchestration:** Apache Airflow, Prefect, Dagster, AWS Step Functions
- **Processing:** Apache Spark, Flink, Beam, dbt
- **Storage:** Snowflake, BigQuery, Redshift, Databricks, S3, GCS
- **Streaming:** Kafka, Kinesis, Pub/Sub, Event Hubs
- **Quality:** Great Expectations, Soda, Monte Carlo
- **Monitoring:** Datadog, Prometheus, CloudWatch
- **Catalog:** Amundsen, DataHub, Alation

## Common Challenges and Solutions

### Challenge: Pipeline Failures
**Solution:** Implement retries with exponential backoff, add comprehensive error handling, monitor pipeline health, implement alerting, use checkpointing for long-running jobs

### Challenge: Data Quality Issues
**Solution:** Implement automated data quality checks, use schema validation, add data profiling, implement anomaly detection, create data quality dashboards

### Challenge: Slow Pipeline Performance
**Solution:** Optimize queries, use appropriate partitioning, implement incremental processing, use caching, parallelize operations, optimize file formats

### Challenge: Data Freshness
**Solution:** Implement streaming pipelines for real-time data, optimize batch schedules, use CDC for efficient updates, implement monitoring for data lag

### Challenge: Schema Evolution
**Solution:** Use schema registry, implement backward compatibility, version schemas, use flexible data formats (JSON, Avro), implement schema validation

### Challenge: Cost Management
**Solution:** Optimize query performance, use appropriate data retention policies, implement partitioning and clustering, monitor resource usage, use spot instances for batch jobs
