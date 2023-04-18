from pyspark.sql import SparkSession
from pyspark.sql.functions import *

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
df_mod2.show()
df_filtered = df.\
    filter( (df.state  == "OH") & (df.gender  == "M") ) \
    .show(truncate=False)  
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