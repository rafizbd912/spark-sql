# -*- coding: utf-8 -*-
"""Spark_sql_project

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1KOn8WThHYhTkf1BgE0qLzhpqbWWlyaYb

PROJECT 3: SPARK SQL

### Step 0: Set up EMR

 [AWS Academy Getting Started](https://drive.google.com/file/d/1kWReqxb5hfEH3CA-dQYUKWsXsEOuRZGF/view)
"""

# Commented out IPython magic to ensure Python compatibility.
# %%capture
# !apt install libkrb5-dev
# !pip install sparkmagic
# !pip install -i https://test.pypi.org/simple/ penn-grader==0.5.0

# Commented out IPython magic to ensure Python compatibility.
# %load_ext sparkmagic.magics

"""### 0.2: The Sharp Spark

Connect your notebook to the EMR cluster you created. In the first cell, copy the link to the Master Public DNS specified in the setup document. You will need to add `http://` to the beginning of the address and the auth details to the end.

For example, if my DNS (directly from the AWS EMR console) is `ec2-3-15-237-211.us-east-2.compute.amazonaws.com` my address would be,

`http://ec2-3-15-237-211.us-east-2.compute.amazonaws.com -a cis545-livy -p password1 -t Basic_Access`

For our example, the cell would read,

```
%spark add -s spark_session -l python -u http://ec2-3-15-237-211.us-east-2.compute.amazonaws.com -a cis545-livy -p password1 -t Basic_Access
```
"""

# Commented out IPython magic to ensure Python compatibility.
# %spark add -s spark_session -l python -u http://ec2-34-203-236-28.compute-1.amazonaws.com/ -a cis545-livy -p Rafiz123 -t Basic_Access

# To restart:
#%spark delete -s spark_session
#OR just factory reset runtime under the runtime tab
# %spark delete -s spark_session

"""## Step 1: Data Wrangling, Cleaning, and Shaping [32 pts]

We will be working with two datasets - (1) LinkedIn data containing information on their users like education, experience, industry etc. (2) Stock price information of companies over a 10 year period (2000-2011) where these users have worked at.  


The data is stored in an S3 bucket, a cloud storage service. Below, with our help, you will download it onto the nodes of your [EMR cluster](https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-what-is-emr.html).

### 1.1: The Stupendous Schema



A schema is a description of the structure of data. In Spark, schemas are defined using a `StructType` object. This is a collection of data types, termed `StructField`'s, that specify the structure and variable type of each component of the dataset. For example, suppose we have the following simple JSON object,


```
{
 "student_name": "Alpha Beta",
 "GPA": 3.6,
 "courses": [
    {"department": "Computer and Information Science",
     "course_id": "CIS 5450",
     "semester": "Fall 2021"},
    {"department": "Computer and Information Science",
     "course_id": "CIS 5550",
     "semester": "Fall 2021"}
 ],
 "grad_year": 2023
 }
```

We would define its schema as follows,

```       
schema = StructType([
           StructField("student_name", StringType(), nullable=True),
           StructField("GPA", FloatType(), nullable=True),
           StructField("courses", ArrayType(
                StructType([
                  StructField("department", StringType(), nullable=True),
                  StructField("course_id", StringType(), nullable=True),
                  StructField("semester", StringType(), nullable=True)
                ])
           ), nullable=True),
           StructField("grad_year", IntegerType(), nullable=True)
         ])
```


Each `StructField` has the following structure: `(name, type, nullable)`. The `nullable` flag defines that the specified field may be empty. The first task is to define the `schema` of `linkedin_small_real.json`. A smaller version of the JSON dataset can be found [here](https://drive.google.com/a/seas.upenn.edu/file/d/1yZ_0xz6uSJ8lAxhGzn2BVjCpDOjagcqb/view?usp=sharing). 


We will now be defining an explicit schema for the `linkedin_small_real.json` dataset.   

Make sure to use `nullable=True` for all the fields as well as **store dates as a StringType()**.
"""

# Commented out IPython magic to ensure Python compatibility.
# %%spark
# 
# from pyspark.sql.types import *
# 
# schema = StructType([
#     StructField("_id", StringType(), nullable=True),
#     
#     StructField("education", ArrayType(
#         StructType([
#           StructField("start", StringType(), nullable=True),
#           StructField("major", StringType(), nullable=True),
#           StructField("end", StringType(), nullable=True),
#           StructField("name", StringType(), nullable=True),
#           StructField("degree", StringType(), nullable=True),
#           StructField("desc", StringType(), nullable=True)
#     ])), nullable=True), 
# 
#     StructField("group", StructType([
#           StructField("affilition", ArrayType(StringType()), nullable=True),
#           StructField("member", StringType(), nullable=True)
#     ]), nullable=True), 
# 
#     StructField("locality", StringType(), nullable=True),
#     StructField("skills", ArrayType(StringType()), nullable=True),
#     StructField("industry", StringType(), nullable=True),
#     StructField("interval", IntegerType(), nullable=True),
# 
#     StructField("summary", StringType(), nullable=True),
#     StructField("interests", StringType(), nullable=True),
#     StructField("overview_html", StringType(), nullable=True),
#     StructField("specilities", StringType(), nullable=True),
#     StructField("homepage", ArrayType(StringType()), nullable=True),
#     StructField("honors", ArrayType(StringType()), nullable=True),
#     StructField("url", StringType(), nullable=True),
#     StructField("also_view", ArrayType(
#       StructType([
#           StructField("id", StringType(), nullable=True),
#           StructField("url", StringType(), nullable=True)
#       ])
#     ), nullable=True),
# 
#     
#     # The schema for the 'name' field
#      StructField("name", StructType([
#           StructField("family_name", StringType(), nullable=True),
#           StructField("given_name", StringType(), nullable=True)
#     ]), nullable=True),
# 
#     # The schema for the 'experience' field
#     StructField("experience", ArrayType(
#         StructType([
#           StructField("title", StringType(), nullable=True),
#           StructField("end", StringType(), nullable=True),
#           StructField("org", StringType(), nullable=True),
#           StructField("start", StringType(), nullable=True),
#           StructField("desc", StringType(), nullable=True),
#         ])
#     ), nullable=True),
# 
#     # The schema for the 'events' field
#      StructField("events", ArrayType(
#         StructType([
#           StructField("from", StringType(), nullable=True),
#           StructField("to", StringType(), nullable=True),
#           StructField("title1", StringType(), nullable=True),
#           StructField("start", StringType(), nullable=True),
#           StructField("title2", StringType(), nullable=True),
#           StructField("end", StringType(), nullable=True)
#         ])
#     ), nullable=True)
# ])
#   
#

"""### 1.2: The Langorous Load

#### 1.2.1: Load LinkedIn Dataset 

In the following cell, we will load the `linkedin_small_real.json` dataset from the S3 bucket into a Spark dataframe (sdf) called `linkedin_data_sdf`.
"""

# Commented out IPython magic to ensure Python compatibility.
# %%spark
# 
# linkedin_data_sdf = spark.read.json("s3a://penn-cis545-files/linkedin_small_real.json", schema=schema)

# Commented out IPython magic to ensure Python compatibility.
# %%spark
# # Let's print out the first few rows to see how the data looks like in tabular form
# linkedin_data_sdf.show(5)

import pandas as pd

"""The cell below shows how to run SQL commands on Spark tables. """

# Commented out IPython magic to ensure Python compatibility.
# %%spark
# 
# 
# # Create SQL-accesible table
# linkedin_data_sdf.createOrReplaceTempView("linkedin_data")
# 
# # Declare SQL query to be excecuted
# query = '''SELECT * 
#            FROM linkedin_data 
#            ORDER BY _id
#            LIMIT 10'''
# 
# # Save the output sdf of spark.sql() as answer_sdf
# answer_sdf = spark.sql(query)
# answer_sdf.show()
#

"""We can then copy to 'answer_sdf' to colab"""

# Commented out IPython magic to ensure Python compatibility.
#Convert to Pandas
# %spark -o answer_sdf

"""#### 1.2.2: SQL refresher

In the next cell, we create `industry_family_name_df` to fetch the data from the `linkedin_data` table created above, returning rows with schema `(_id, industry, family_name)`. Remove all NULLs from the `family_name` and `industry` columns. Sort the columns by `_id, industry, family_name`, all ascending order.  Limit the sdf to 100 rows.
"""

# Commented out IPython magic to ensure Python compatibility.
# %%spark 
# 
# 
# 
# query = '''
#         SELECT 
#             _id,
#             industry,
#             name.family_name
#         FROM 
#             linkedin_data
#         WHERE 
#             name.family_name IS NOT NULL AND 
#             industry IS NOT NULL
#         ORDER BY 
#             _id ASC,
#             industry ASC,
#             name.family_name ASC
#         LIMIT 100
# '''
# 
# # Save the output sdf of spark.sql() as industry_family_name_df
# industry_family_name_df = spark.sql(query)
# industry_family_name_df.show(10)
#

# Commented out IPython magic to ensure Python compatibility.
#Convert to Pandas
# %spark -o industry_family_name_df

"""#### 1.2.3: Load Stock Prices Data 
Now we create a schema for the Stock Prices data. The schema should be relatively simple, compared to the LinkedIn schema. A tiny version of the data is [here](https://docs.google.com/spreadsheets/d/1TStiS-bwkCJR1w5rJ18QPlNe3SIK2Z8QS9gK6ltnjJQ/edit?usp=sharing) in csv format.We store the `Date` field as a String.

"""

# Commented out IPython magic to ensure Python compatibility.
# %%spark
# 
# from pyspark.sql.types import *
# 
# 
# 
# stocks_schema = StructType([
#     StructField("Date", StringType(), nullable=True),
#     StructField("Open", FloatType(), nullable=True),
#     StructField("High", FloatType(), nullable=True),
#     StructField("Low", FloatType(), nullable=True),
#     StructField("Close", FloatType(), nullable=True),
#     StructField("Volume", IntegerType(), nullable=True),
#     StructField("OpenInt", IntegerType(), nullable=True),
#     StructField("org", StringType(), nullable=True)
# ])

"""In the following cell, we will load the entire `stocks.csv` dataset from the S3 bucket into a Spark dataframe (sdf) called `stocks_sdf`. 


"""

# Commented out IPython magic to ensure Python compatibility.
# %%spark
# 
# # Load stock data
# 
# stocks_sdf = spark.read.format("csv") \
#               .option("header", "true") \
#               .schema(stocks_schema) \
#               .load("s3a://penn-cis545-files/stocks.csv")
# 
# # Creates SQL-accesible table
# stocks_sdf.createOrReplaceTempView('stocks')
# 
# # Display the first 10 rows
# query = '''SELECT *
#            FROM stocks'''
# answer_stocks_sdf = spark.sql(query)
# answer_stocks_sdf.show(10)

# Commented out IPython magic to ensure Python compatibility.
#Convert to Pandas
# %spark -o answer_stocks_sdf

"""#### 1.2.4: Calculate Percentage Change

In the next cell, we display the percentage change in the daily stock prices for each organization. In order to do so, we will need the data from the `stocks_sdf` table created above. We create a new column called `percentage_change` that uses the opening and closing stock prices for each organization, for each day, and calculates the percentage change in the stock price as follows: 

\begin{align}
percentage\_change = \frac{close-open}{open}*100.0
\end{align}

In order to avoid nulls, we calculate the percentage change for only for those organizations and days where the **opening price is NOT 0.0**. The percentage_change value is a float.
"""

# Commented out IPython magic to ensure Python compatibility.
# %%spark
# 
# from pyspark.sql.functions import when
# from pyspark.sql.functions import col
# 
# 
# answer_sdf = stocks_sdf.withColumn("percentage_change", 
#                                     when (col("Open") != 0, 
#                                          (col("Close")-col("Open"))/col("Open")*100.0)
#                                     .otherwise(None)) \
#                         .orderBy(["Date", "org"], ascending=[True, True])
# 
# answer_sdf.createOrReplaceTempView("test_1_2_4")
#

# Commented out IPython magic to ensure Python compatibility.
# 
# %%spark
# answer_sdf.createOrReplaceTempView("test_1_2_4")
# test_1_2_4_sdf = spark.sql("SELECT * FROM test_1_2_4 LIMIT 10")

# Commented out IPython magic to ensure Python compatibility.
#Convert to Pandas
# %spark -o test_1_2_4_sdf

"""### 1.3: Cleaning LinkedIn Data

#### 1.3.1: Adding Experience

In this part, we are interested in when individuals began working at a particular company.  

Here is an example of an `experience` field:

```
{
   "experience": [
     {
        "org": "The Walt Disney Company", 
        "title" : "Mickey Mouse",
        "end" : "Present",
        "start": "November 1928",
        "desc": "Sailed a boat."
     },
     {
        "org": "Walt Disney World Resort",
        "title": "Mickey Mouse Mascot",
        "start": "January 2005",
        "desc": "Took pictures with kids."
     }
   ]
}
```

The task here is to extract each pair of company and start date from these arrays. This is known as "exploding" a row in Spark. 

Create an sdf called `raw_start_dates_sdf` that contains the company and start date for every experience of every individual in `linkedin_data_sdf`. Drop any row that contains a `null` in either column. 

```
+--------------------------+---------------+
|org                       |start_date     |
+--------------------------+---------------+
|Walt Disney World Resort  |January 2005   | 
|The Walt Disney Company   |November 1928  |
|...                       |...            |
+--------------------------+---------------+
```
"""

# Commented out IPython magic to ensure Python compatibility.
# %%spark 
# 
# 
# 
# from pyspark.sql.functions import explode, col
# 
# raw_start_dates_sdf = (
#     linkedin_data_sdf
#     .select(explode("experience").alias("exp"))
#     .select(col("exp.org").alias("org"), col("exp.start").alias("start_date"))
#     .dropna()
# )

# Commented out IPython magic to ensure Python compatibility.
# %%spark
# raw_start_dates_sdf.createOrReplaceTempView("test_1_3_1")
# test_1_3_1_sdf = spark.sql("SELECT * FROM test_1_3_1 ORDER BY org ASC, start_date DESC LIMIT 20")

# Commented out IPython magic to ensure Python compatibility.
#Convert to Pandas
# %spark -o test_1_3_1_sdf

"""#### 1.3.2: Filtering on Date

There are two issues with the values in our `date` column. First, the values are saved as strings, not datetime types. This halts us from running functions such as `ORDER BY` or `GROUP BY` on common months or years. Second, some values do not have both month and year information or are in other languages. So, here the task is to filter out and clean the `date` column. We are interested in only those rows that have date in the following format `"(month_name) (year)"`, e.g. "October 2010".

Using `raw_start_dates_sdf`, create an sdf called `filtered_start_dates_sdf` with the `date` column filtered in the manner above. **Keep only those rows with a start date between January 2000 ('2000-01-01') to December 2011 ('2011-12-01'), inclusive**.  Ensure that any dates that are not in our desired format are omitted. Drop any row that contains a `null` in either column. The format of the sdf is shown below:
```
+--------------------------+---------------+
|org                       |start_date     |
+--------------------------+---------------+
|Walt Disney World Resort  |2005-01-01     | 
|...                       |...            |
+--------------------------+---------------+
```
_Hint_: Refer to the [function list](https://spark.apache.org/docs/2.3.0/api/sql/index.html) to format the `date` column. In Spark SQL the date format we are interested in is `"MMM y"`.
"""

# Commented out IPython magic to ensure Python compatibility.
# %%spark
# 
# 
# 
# 
# 
# spark.sql("set spark.sql.legacy.timeParserPolicy=LEGACY")
# 
# 
# 
# from pyspark.sql.functions import col, to_date, year, month, regexp_extract
# 
# filtered_start_dates_sdf = (
# raw_start_dates_sdf
# .select("org", "start_date")
# .filter(col("start_date").rlike("^\w+\s\d{4}$")) # filter out rows with invalid format
# .withColumn("start_date", to_date(col("start_date"), "MMM yyyy")) # convert string to date type
# .filter(col("start_date").between("2000-01-01", "2011-12-01")) # filter by date range
# .filter(col("org").isNotNull() & col("start_date").isNotNull()) # drop any null rows
# )

# Commented out IPython magic to ensure Python compatibility.
# %%spark
# filtered_start_dates_sdf.createOrReplaceTempView("test_1_3_2")
# test_1_3_2_sdf = spark.sql("SELECT * FROM ((SELECT org, DATE_FORMAT(start_date, 'yyyy-MM-dd') AS start_date FROM test_1_3_2 ORDER BY start_date DESC, org DESC LIMIT 10) UNION (SELECT org, DATE_FORMAT(start_date, 'yyyy-MM-dd') AS start_date FROM test_1_3_2 ORDER BY start_date ASC, org ASC LIMIT 10)) ORDER BY start_date ASC, org ASC")

# Commented out IPython magic to ensure Python compatibility.
#Convert to Pandas
# %spark -o test_1_3_2_sdf

"""### 1.4: Cleaning Stock Data

#### 1.4.1: Adding Company Names

Now, we have to merge the stocks and linkedin dataframes. This would be difficult to do directly, as the companies in our stock dataset are defined by their stock tickers instead of the full names. Thus, we would not be able to merge it with the `org` field in `hire_train_sdf`. We must convert them to that format. For this purpose, we can create a user-defined function (udf) to achieve the mentioned conversion.

A udf is defined as a normal Python function and then registered to be used as a Spark SQL function. The task is to create a udf, `TICKER_TO_NAME()` that will convert the ticker field in `raw_stocks` to the company's name. This will be done using the provided `ticker_to_name_dict` dictionary. We are only interested in the companies in that dictionary.
"""

# Commented out IPython magic to ensure Python compatibility.
# %%spark
# 
# # Dictionary linking stock ticker symbols to their names
# ticker_to_name_dict = {'NOK': 'Nokia',
#                        'UN': 'Unilever',
#                        'BP': 'BP',
#                        'JNJ': 'Johnson & Johnson',
#                        'TCS': 'Tata Consultancy Services',
#                        'SLB': 'Schlumberger',
#                        'NVS': 'Novartis',
#                        'CNY': 'Huawei',
#                        'PFE': 'Pfizer',
#                        'ACN': 'Accenture',
#                        'DELL': 'Dell',
#                        'MS': 'Morgan Stanley',
#                        'ORCL': 'Oracle',
#                        'BAC': 'Bank of America',
#                        'PG': 'Procter & Gamble',
#                        'CGEMY': 'Capgemini',
#                        'GS': 'Goldman Sachs',
#                        'C': 'Citi',
#                        'IBM': 'IBM',
#                        'CS': 'Credit Suisse',
#                        'MDLZ': 'Kraft Foods',
#                        'WIT': 'Wipro Technologies',
#                        'CSCO': 'Cisco Systems',
#                        'PWC': 'PwC',
#                        'GOOGL': 'Google',
#                        'CTSH': 'Cognizant Technology Solutions',
#                        'HSBC': 'HSBC',
#                        'DB': 'Deutsche Bank',
#                        'MSFT': 'Microsoft',
#                        'HPE': 'Hewlett-Packard',
#                        'ERIC': 'Ericsson',
#                        'BCS': 'Barclays Capital',
#                        'GSK': 'GlaxoSmithKline'}
# 
# 
# from pyspark.sql.functions import udf
# from pyspark.sql.types import StringType
# 
# def ticker_to_name(ticker):
#     try:
#         return ticker_to_name_dict[ticker]
#     except KeyError:
#         return None
#         
# # Register udf as a SQL function. 
# spark.udf.register("TICKER_TO_NAME", ticker_to_name, StringType())
#

# Commented out IPython magic to ensure Python compatibility.
# %%spark
# 
# ticker_to_name = [((str(ticker_to_name("GOOGL")),str(ticker_to_name("TSLA"))))]
# columns = ['A', 'B']
# dataframe = spark.createDataFrame(ticker_to_name, columns)

# Commented out IPython magic to ensure Python compatibility.
#Convert to Pandas
# %spark -o dataframe

"""#### 1.4.2: Wrangling stocks data

We can now begin to wrangle `stocks_sdf` with our new `TICKER_TO_NAME()` function.

Create an sdf called `filter_1_stocks_sdf` as follows. Convert all the ticker names in `stocks_sdf` to the company names and save it as `org`. Next, convert the `date` field to a datetime type. As explained before this will help order and group the rows in future steps. 

Drop any company names that do not appear in `ticker_to_name_dict`. **Keep any date between January 1st 2001 ('2001-01-01') and December 4th 2012 ('2012-12-04') inclusive**, in the format shown below (note this is a datetime object not a string):

```
+----+------------+--------------+
|org |date        |Close         |
+----+------------+--------------+
|IBM |2000-01-03  |...           |
|... |...         |...           |
+----+------------+--------------+
```
"""

# Commented out IPython magic to ensure Python compatibility.
# %%spark
# 
# from pyspark.sql.functions import to_date, col, expr
# 
# filter_1_stocks_sdf = stocks_sdf.select(
#     col("Close"),
#     to_date(col("Date"), "yyyy-MM-dd").alias("date"),
#     expr("TICKER_TO_NAME(org)").alias("org")
# ).filter(
#     col("org").isNotNull() &
#     col("date").between("2001-01-01", "2012-12-04")
# )

# Commented out IPython magic to ensure Python compatibility.
# #################     DO NOT EDIT      ##################
# %%spark
# filter_1_stocks_sdf.createOrReplaceTempView("test_1_4_2")
# test_1_4_2_sdf = spark.sql("SELECT * FROM ((SELECT org, DATE_FORMAT(date, 'yyyy-MM-dd') as date, Close FROM test_1_4_2 ORDER BY date DESC, org DESC LIMIT 10) UNION (SELECT org, DATE_FORMAT(date, 'yyyy-MM-dd') as date, Close FROM test_1_4_2 ORDER BY date ASC, org ASC LIMIT 10)) ORDER BY date ASC, org DESC")

# Commented out IPython magic to ensure Python compatibility.
#Convert to Pandas
# %spark -o test_1_4_2_sdf

"""## Step 2: Analysis on LinkedIn Data

### 2.1: Counting Employees [2 Pts]

Now we would like to find for each company, the number of individuals who started in the same month and year. Use `filtered_start_dates_sdf` and create a new sdf called `start_dates_sdf` which will contain the total number of employees who began working at the same company on the same start date (name the new column as `num_employees`). The format of the sdf is shown below:

```
+--------------------------+---------------+---------------+
|org                       |start_date     |num_employees  |
+--------------------------+---------------+---------------+
|Walt Disney World Resort  |2005-01-01     |1              |
|...                       |...            |...            |
+--------------------------+---------------+---------------+
```
"""

# Commented out IPython magic to ensure Python compatibility.
# %%spark
# 
# 
# from pyspark.sql.functions import count
# 
# start_dates_sdf = filtered_start_dates_sdf.groupBy("org", "start_date").agg(
#     count("*").alias("num_employees")
# )
#

# Commented out IPython magic to ensure Python compatibility.
# %%spark
# 
# start_dates_sdf.createOrReplaceTempView("test_2_1")
# test_2_1_sdf = spark.sql("SELECT org, DATE_FORMAT(start_date, 'yyyy-MM-dd') as start_date, num_employees FROM test_2_1 ORDER BY num_employees DESC, org DESC, start_date ASC LIMIT 10")

# Commented out IPython magic to ensure Python compatibility.
#Convert to Pandas
# %spark -o test_2_1_sdf

"""### 2.2: Reshape DataFrame

Our next step is to use `start_dates_sdf` and create a new sdf called `raw_hire_train_sdf` that has for a single company and a single year, the number of hires in Jan through Dec, as well as the total number of hires that year (name it `total_num`). Note that for each company we will have several rows corresponding to years between 2000 and 2011. It is alright if for a given company you don't have a given year. However, ensure that for a given company and given year, each month column has an entry, i.e. if no one was hired the value should be `0`.  

_Note_: We will use the first three letters of each month in naming, i.e. `jan, feb, mar, apr, may, jun, jul, aug, sep, oct, nov, dec`.

The format of the `raw_hire_train_sdf` is shown below:

```
+----+-----+----------+---------+----------+----------+
|org |year |jan_hired |   ...   |dec_hired |total_num |
+----+-----+----------+---------+----------+----------+
|IBM |2008 |...       |   ...   |...       |...       |
|IBM |2009 |...       |   ...   |...       |...       |
|... |...  |...       |   ...   |...       |...       |
+----+-----+----------+---------+----------+----------+
```
"""

# Commented out IPython magic to ensure Python compatibility.
# %%spark
# 
# 
# 
# from pyspark.sql.functions import year, month, sum, col
# from functools import reduce
# 
# # Extract year and month from the start_date column
# start_dates_with_year_month_sdf = start_dates_sdf.withColumn(
#     "year", year("start_date")
# ).withColumn(
#     "month", month("start_date")
# )
# 
# # Pivot the DataFrame and calculate the number of hires for each month
# pivot_hire_sdf = start_dates_with_year_month_sdf.groupBy("org", "year").pivot(
#     "month"
# ).agg(
#     sum("num_employees").alias("num_employees")
# ).na.fill(0)
# 
# # Rename month columns
# month_columns = [
#     "jan_hired", "feb_hired", "mar_hired", "apr_hired", "may_hired", "jun_hired",
#     "jul_hired", "aug_hired", "sep_hired", "oct_hired", "nov_hired", "dec_hired"
# ]
# renamed_pivot_hire_sdf = pivot_hire_sdf.select(
#     col("org"),
#     col("year"),
#     *[col(str(i + 1)).alias(month_columns[i]) for i in range(12)]
# )
# 
# # Calculate the total number of hires for each org and year
# raw_hire_train_sdf = renamed_pivot_hire_sdf.withColumn(
#     "total_num", reduce(lambda a, b: a + b, [col(month) for month in month_columns])
# )

# Commented out IPython magic to ensure Python compatibility.
# %%spark
# raw_hire_train_sdf.createOrReplaceTempView("test_2_2")
# test_2_2_sdf = spark.sql("SELECT * FROM test_2_2 ORDER BY total_num DESC, org DESC, year ASC LIMIT 20")

# Commented out IPython magic to ensure Python compatibility.
#Convert to Pandas
# %spark -o test_2_2_sdf

"""### 2.3: Filtering on Company Size

# Create an sdf called `hire_train_sdf` that contains all the observations in `raw_hire_train_sdf` with `total_num` greater than or equal to 20.
"""

# Commented out IPython magic to ensure Python compatibility.
# %%spark
# 
# # Keep all rows where total_num >= 20
# 
# from pyspark.sql.functions import col
# 
# hire_train_sdf = raw_hire_train_sdf.filter(col("total_num") >= 20)

# Commented out IPython magic to ensure Python compatibility.
# 
# %%spark
# hire_train_sdf.createOrReplaceTempView("test_2_3")
# test_2_3_sdf = spark.sql("SELECT * FROM test_2_3 ORDER BY org ASC, year ASC LIMIT 10")

# Commented out IPython magic to ensure Python compatibility.
#Convert to Pandas
# %spark -o test_2_3_sdf

"""## Step 3: Analyzing Stock Data

### 3.1: Average Closing Price

The data in `filter_1_stocks_sdf` gives closing prices on a daily basis. Since we are interested in monthly trends, we will only keep the **average of the closing price of each month per year for each org**. 

Create an sdf `filter_2_stocks_sdf` that contains only the average of closing prices for each month-year pair sorted by the org alphabetically and then month, year from earliest to latest with the closing price rounded off to 3 decimal places. The format of the sdf is shown below:

```
+----+------------+--------------+--------------+
|org |month       |year          |close         |
+----+------------+--------------+--------------+
|IBM |01          |2000          |...           |
|... |...         |...           |...           |
+----+------------+--------------+--------------+
```
"""

# Commented out IPython magic to ensure Python compatibility.
# %%spark
# 
# 
# from pyspark.sql.functions import year, month, avg, round
# 
# filter_2_stocks_sdf = (
#     filter_1_stocks_sdf
#     .withColumn("year", year("date"))
#     .withColumn("month", month("date"))
#     .groupBy("org", "year", "month")
#     .agg(round(avg("Close"), 3).alias("close"))
#     .orderBy("org", "year", "month")
# )
#

# Commented out IPython magic to ensure Python compatibility.
# %%spark
# filter_2_stocks_sdf.createOrReplaceTempView("test_3_1")
# test_3_1_sdf = spark.sql("SELECT * FROM test_3_1 LIMIT 10")

# Commented out IPython magic to ensure Python compatibility.
#Convert to Pandas
# %spark -o test_3_1_sdf

"""### 3.2: Reshape DataFrame Again!

Now, we will begin to shape our dataframe into the format of the final training sdf.

Create an sdf `filter_3_stocks_sdf` that has for a single company and a single year, the average stock price for each month in that year. This is similar to the table created in Step 3.1. If the data is not avaliable, drop any rows containing any `null` values, in any column. The format of the sdf is shown below:

```
+----+-----+----------+---------+----------+
|org |year |jan_stock |   ...   |dec_stock |
+----+-----+----------+---------+----------+
|IBM |2008 |...       |   ...   |...       |
|IBM |2009 |...       |   ...   |...       |
|... |...  |...       |   ...   |...       |
+----+-----+----------+---------+----------+
```
"""

# Commented out IPython magic to ensure Python compatibility.
# %%spark
# 
# #ToDo
# 
# from pyspark.sql.functions import col
# 
# filter_3_stocks_sdf = (
#     filter_2_stocks_sdf
#     .groupBy("org", "year")
#     .pivot("month")
#     .agg(avg("close"))
#     .dropna()
# )
# 
# # Rename columns
# month_names = [
#     "jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"
# ]
# new_column_names = ["org", "year"] + [f"{month}_stock" for month in month_names]
# filter_3_stocks_sdf = filter_3_stocks_sdf.toDF(*new_column_names)

# Commented out IPython magic to ensure Python compatibility.
# %%spark
# filter_3_stocks_sdf.createOrReplaceTempView("test_3_2")
# test_3_2_sdf = spark.sql("SELECT * FROM test_3_2 ORDER BY org, year ASC LIMIT 10")

# Commented out IPython magic to ensure Python compatibility.
#Convert to Pandas
# %spark -o test_3_2_sdf

"""### 3.3: Direction of Change

The final element in our training set is the binary output for each case, i.e. the `y` label. 

Create an sdf `stocks_train_sdf` from `filter_3_stocks_sdf` with an additional column `direction`. This should be the direction of percentage change in the closing stock price, i.e. `1` for positive or `-1` for negative, from the first month of a given year to the last month of the given year. Make this an **integer**.  The year begins in January and ends in December, inclusive. The format of the sdf is shown below:

```
+----+-----+----------+---------+----------+-------------+
|org |year |jan_stock |   ...   |dec_stock |direction    |
+----+-----+----------+---------+----------+-------------+
|IBM |2008 |...       |   ...   |...       |1            |
|IBM |2009 |...       |   ...   |...       |-1           |
|... |...  |...       |   ...   |...       |...          |
+----+-----+----------+---------+----------+-------------+
```
"""

# Commented out IPython magic to ensure Python compatibility.
# %%spark
# 
# from pyspark.sql.functions import when, signum
# 
# stocks_train_sdf = filter_3_stocks_sdf.withColumn(
#     "direction",
#     when(
#         ((col("dec_stock") - col("jan_stock")) / col("jan_stock")) > 0, 1
#     ).otherwise(-1).cast("integer")
# )

# Commented out IPython magic to ensure Python compatibility.
# %%spark
# stocks_train_sdf.createOrReplaceTempView("test_3_3")
# test_3_3_sdf = spark.sql("SELECT * FROM test_3_3 ORDER BY org, year ASC LIMIT 10")

# Commented out IPython magic to ensure Python compatibility.
#Convert to Pandas
# %spark -o test_3_3_sdf

"""## Step 4: Combining LinkedIn and Stocks Data

### 4.1: The CRAZY Combination

Now that we have individually created the two halves of our training data we will merge them together to create the combined final training sdf.

Create an sdf called `training_sdf` in the format of the one shown at the beginning of Step 3. Note that in our definition for the `stock_result` column, the `stock_result` value for a particular year corresponds to the direction of the stock percentage change in the **following** year. For example, the stock_result in the `2008` row for `IBM` will contain the direction of IBM's stock in the year 2009. For the final training dataframe, we only need the entries for the companies where both hiring and stock data are available for the particular year.
The format of the sdf is shown below:
```
+----+-----+----------+---------+----------+----------+---------+----------+-------------+
|org |year |jan_hired |   ...   |dec_hired |jan_stock |   ...   |dec_stock |stock_result |
+----+-----+----------+---------+----------+----------+---------+----------+-------------+
|IBM |2008 |...       |   ...   |...       |...       |   ...   |...       |-1           |
|IBM |2009 |...       |   ...   |...       |...       |   ...   |...       |1            |
|... |...  |...       |   ...   |...       |...       |   ...   |...       |...          |
+----+-----+----------+---------+----------+----------+---------+----------+-------------+
```
"""

# Commented out IPython magic to ensure Python compatibility.
# %%spark
# 
# from pyspark.sql.functions import lead
# from pyspark.sql.window import Window
# 
# # First, we create a new DataFrame with the stock_result column
# # Shift the years by subtracting 1 to match with the following year's stock
# stocks_shifted = stocks_train_sdf.withColumn("year", filter_3_stocks_sdf["year"] - 1).select("org", "year", "direction").withColumnRenamed("direction", "stock_result")
# 
# # Now, join hire_train_sdf with stocks_shifted on both "org" and "year"
# training_sdf = hire_train_sdf.join(stocks_shifted, ["org", "year"], "inner").join(filter_3_stocks_sdf, ["org", "year"], "inner")
# 
#

# Commented out IPython magic to ensure Python compatibility.
# %%spark
# training_sdf.createOrReplaceTempView("test_4")
# test_4_sdf = spark.sql("SELECT * FROM test_4 ORDER BY org, year ASC LIMIT 10")

# Commented out IPython magic to ensure Python compatibility.
#Convert to Pandas
# %spark -o test_4_sdf