# Assignment 7 — Delta Lake Incremental Data Processing

## Tools Used
PySpark, Delta Lake, Databricks

## Dataset
Sample - Superstore Dataset (9994 rows, 21 columns)

## File
* `delta_incremental_assignment.ipynb` → All 6 steps (code + validation + summary)

## Objective
Perform incremental data processing using Delta Lake — load data into a Delta table, clean it, simulate new/incremental data, and apply a MERGE operation to update existing records and insert new ones.

## Steps Covered

* **Step 1:** Load Superstore dataset into a DataFrame from CSV
* **Step 2:** Basic cleaning — handle null values and remove duplicate rows
* **Step 3:** Fix column names (replace spaces with underscores) and save cleaned data as a Delta table (`superstore_delta`)
* **Step 4:** Create a simulated incremental dataset — one existing record with updated values (UPDATE scenario) and two new records (INSERT scenario)
* **Step 5:** Apply `MERGE INTO` operation on `Row_ID` — update matching records, insert non-matching records
* **Step 6:** Validate results (row count, duplicate check, null check) and display final dataset with a Region-wise summary

## Key Concepts Used
* Delta Lake `MERGE INTO` for UPSERT (update + insert) operations
* Data cleaning: null handling with `na.fill()`, duplicate removal with `dropDuplicates()`
* Safe type casting using `try_cast` / regex validation to handle malformed data
* Delta table transaction history (`DeltaTable.history()`) to verify MERGE operation metrics

## Output
* Final row count after MERGE
* Confirmation of 0 duplicate `Row_ID`s
* Updated record (`Row_ID = 1`) reflecting new Sales/Profit values
* Two newly inserted records visible in the final table
* Region-wise Sales and Profit summary
* Delta table history showing `numTargetRowsUpdated` and `numTargetRowsInserted` metrics
