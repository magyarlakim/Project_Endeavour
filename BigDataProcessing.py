from pyspark.sql import SparkSession
from pyspark.sql.functions import *
import pandas as pd
from pyspark.sql.functions import pandas_udf

#Create a tailor made session
spark = SparkSession.builder.\
        appName("Mysession").\
        config("spark.sql.caseSensitive", "True").\
        getOrCreate()
spark
# Importing libraries
import requests
from io import BytesIO
from zipfile import ZipFile
# Downloading and Extracting Json File
jsonFilePath = 'proxylogon_ssrf_rce_poc_2021-03-14T01401970.json'

# Creating a Spark Dataframe
df = spark.read.json(jsonFilePath)

# 1 Data manipulation in standard spark.dataframe
df.printSchema()
df.columns
df.select("TargetUserName", "User", "Level").describe().show()
columnDiagnostics = df.dropDuplicates(["TargetUserName", "User"]).select("TargetUserName", "User").collect()
#modify columns
df_mod = df.\
    withColumnRenamed("CommandLine", "MyCommandline").\
    printSchema()

df_mod2 = df.\
    withColumn("MyServerName",col("TargetServerName")).\
    select(col("Company").alias("MyComp"), \
    col("Channel").alias("Channel_tunnel"), \
    col("DestinationIp").alias("DestIP")).\
    drop('TargetProcessId').\
    printSchema()

df_filtered = df.\
    filter( (df.Channel  == "Security")) \
    .show(truncate=False)  

#filtering

df_security = spark.createDataFrame([
    ['12345', 'Fixed income', 45, 75], ['31256', 'Fixed income', 2, 86], ['49271', 'Equity', 45, 45],
    ['13465', 'Equity', 4, 68], ['45689', 'Equity', 5, 75], ['65894', 'Investment fund', 26, 60],
    ['24675', 'Structured product', 15, 85], ['24586', 'Fixed income', 18, 80]], schema=['Security_ID', 'asset_class', 'price', 'bond'])
df_security.show()

df_security.groupby('asset_class').avg().show()

def plus_mean(pandas_df):
    return pandas_df.assign(price=pandas_df.price - pandas_df.price.mean())

df_security.groupby('asset_class').applyInPandas(plus_mean, schema=df_security.schema).show()

# Section 2: SQLlike behaviour
df.createOrReplaceTempView('mordorTable')

df_sqllike = spark.sql(
'''
SELECT Hostname,Channel,EventID, Count(*) as count
FROM mordorTable
GROUP BY Hostname,Channel,EventID
ORDER BY count DESC
'''
)
df_sqllike.show(truncate=False)