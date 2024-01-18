
import findspark
findspark.init()
import pyspark
findspark.find()
from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession, SQLContext


if __name__== "__main__":
    ## CELL 1

    spark = SparkSession \
        .builder \
        .appName('test') \
        .master('local[*]') \
        .enableHiveSupport() \
        .config("spark.driver.extraClassPath", "C:\\Users\\junai\\Documents\\Projects\\mysql-connector-j-8.2.0\\mysql-connector-j-8.2.0.jar") \
        .getOrCreate()

    df = spark.read.format('jdbc'). \
        option('url', 'jdbc:myqsl://localhost:3306'). \
        option('driver', 'com.mysql.cj.jdbc.Driver'). \
        option('user','junaid'). \
        option('password', 'junaid'). \
        option('query', 'select count(*) from mydb.quotes'). \
        load()


