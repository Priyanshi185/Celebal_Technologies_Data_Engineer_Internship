# Assignment 4 — Azure Cloud Fundamentals and Data Pipeline using ADF

## Tools Used
Microsoft Azure Portal, Azure Data Factory (V2), Azure Blob Storage

## Resources Created
- Resource Group: Resourse_1
- Storage Account: celebaldatastorage
- Blob Container: superstore-data
- Data Factory: cei-adf-pipeline

## Pipeline Overview
Source: Sample - Superstore.csv (Blob Storage)
Activities: Get Metadata → Copy Data
Destination: output/Superstore_output.csv (same container)

## Tasks Completed
- Task 1: Created Resource Group
- Task 2: Created Storage Account, Blob Container, uploaded CSV
- Task 3: Created ADF, Linked Service, Datasets, Get Metadata activity
- Task 4: Built pipeline with Copy Data activity
- Task 5: Executed pipeline successfully (Succeeded)
- Task 6: Assigned IAM roles (Reader, Contributor, Storage Blob Data Contributor)
- Mini Project: End-to-end pipeline — CSV from Blob → ADF → output folder

## Output
Pipeline executed successfully. Data copied to output/Superstore_output.csv (2.18 MiB)
Screenshots of all tasks available in the screenshots/ folder.