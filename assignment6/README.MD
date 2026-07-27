# Assignment 6 — Spark Architecture and Data Processing

## Tools Used
PySpark 4.2.0, Jupyter Notebook, Python

## Dataset
Sample - Superstore Dataset (9994 rows, 21 columns)

## File
- spark_assignment.ipynb → All 15 questions (theory + code)

## Topics Covered
- Q1:  Roles of Driver, Cluster Manager and Executor
- Q2:  Lazy Evaluation and performance optimization
- Q3:  Reading CSV with PySpark
- Q4:  CSV vs Parquet — row-based vs columnar storage
- Q5:  Filtering and selecting columns in PySpark
- Q6:  Renaming columns and casting data types
- Q7:  Lineage Graph (DAG) and fault tolerance
- Q8:  Filtering with multiple AND conditions
- Q9:  Predicate Pushdown in Parquet
- Q10: Adding derived columns with withColumn()
- Q11: Transformations vs Actions with examples
- Q12: Load Parquet, filter nulls, save as CSV
- Q13: Client Mode vs Cluster Mode
- Q14: Filtering with OR conditions
- Q15: Why show() is safer than collect()

## Note on Q12
Parquet read/write requires Hadoop winutils setup on Windows.
The concept and Spark commands are documented in the notebook.
In a real cloud environment like Databricks or EMR,
this would work directly without any additional setup.