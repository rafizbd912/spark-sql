# Stock Analysis with PySpark

This project analyzes stock price change and hiring trends of organizations using PySpark. The analysis consists of preprocessing LinkedIn data, preprocessing Stocks data, and merging the processed data into a final data frame for further analysis or model training. 

## Dataset

The datasets are based on the LinkedIn and Stocks data for multiple organizations across several years.

## Steps

### LinkedIn Data Processing 

The LinkedIn data contains hiring trends of multiple organizations. The goal is to format this data by aggregating on a monthly basis, creating a processed dataframe `hire_train_sdf` for each organization, year, and average number of hires for each month in that year.

### Stocks Data Processing 

Stocks data includes daily closing prices for various organizations. This information is processed to obtain the average monthly closing prices, and the percentage change in the closing stock price from the first month of a given year to the last month of the given year is computed. The processed dataframe `stocks_train_sdf` has the closing prices and computed `direction` (positive or negative change) for each organization and year.

### Combining LinkedIn and Stocks Data 

The preprocessed LinkedIn and Stocks dataframes are merged to form the final training dataframe `training_sdf`. This dataframe includes hiring data, stocks data, and the stock result (direction of stock percentage change in the following year).

## Code Structure

1. **LinkedIn Data Processing**
    - Filter and process raw LinkedIn data.
    - Create an intermediate dataframe `filter_3_linkedin_sdf` with aggregated hiring data.
    - Generate `hire_train_sdf` from `filter_3_linkedin_sdf` with average hiring for each month in a given year.

2. **Stocks Data Processing**
    - Process raw stocks data.
    - Create an intermediate dataframe `filter_2_stocks_sdf` with average monthly closing prices.
    - Generate `stocks_train_sdf` from `filter_3_stocks_sdf` with the direction of percentage change in the closing stock price for a given year.

3. **Combining LinkedIn and Stocks Data**
    - Create `training_sdf` by merging `hire_train_sdf` and `stocks_train_sdf`. This dataframe includes the stock result, i.e., the direction of stock percentage change in the following year.

## Potential Uses

The final processed dataframe `training_sdf` can be used for various data analysis tasks or predictive modeling, such as analyzing the relationship between hiring trends and stock market performance, or predicting future stock trends based on hiring data.

## Requirements

- Apache Spark
- PySpark

The project has been structured and documented such that anyone with Python and PySpark knowledge can understand the processing steps. The code has been modularized into different sections for better readability and understanding.
