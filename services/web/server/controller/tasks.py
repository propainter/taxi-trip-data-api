import time
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from flask import   current_app
import datetime as dt

app = current_app
DATE_FORMAT_ISO = "%Y-%m-%d"
class SparkTasks:
        
    def loadSpark(self, spark_master):
        if len(spark_master) == 0:
            spark_master = "local[1]"
        try:
            if self.spark is not None:
                app.logger.warn("====ALREADY HAVE SPARK INSTANCE=======> {}".format(spark_master))
                return self.spark
        except:
            app.logger.warn("=====MAKING NEW SPARK INSTANCE======> {}".format(spark_master))
            self.spark = SparkSession.builder.master(spark_master).appName("gojek.test").getOrCreate()
        return self.spark
    
    def loadFile(self, spark_master, file_path):
        if len(file_path)>0:
            spark = self.loadSpark(spark_master)
            self.gojekDF = spark.read.parquet(file_path)
            return self.gojekDF

    def average_fare_heatmap_by_date(self, input_date):
        '''
        get avg fare by S2ID location per day
        '''
        input_date_start_string = "{} 00:00:00".format(dt.datetime.strftime(input_date, DATE_FORMAT_ISO))
        input_date_end_string = "{} 12:59:59".format(dt.datetime.strftime(input_date, DATE_FORMAT_ISO))
        inputDF = self.loadFile(current_app.config.get('SPARK_MASTER', ''), current_app.config.get('INPUT_DATA_FILE', ''))
        sol02DF = inputDF.filter(F.col("trip_start_timestamp").between(input_date_start_string, input_date_end_string)).groupby(F.col("pickup_location")).agg({"fare":"avg"})
        return sol02DF.collect()
    
    def average_speed_24hrs(self, input_date):
        '''
        get average speed in last 24 hrs
        '''
        kmInUnitMile = current_app.config.get('KM_IN_UNIT_MILE', 1.609344)
        input_date_start_string = "{} 00:00:00".format(dt.datetime.strftime(input_date, DATE_FORMAT_ISO))
        input_date_end_string = "{} 12:59:59".format(dt.datetime.strftime(input_date, DATE_FORMAT_ISO))
        inputDF = self.loadFile(current_app.config.get('SPARK_MASTER', ''), current_app.config.get('INPUT_DATA_FILE', ''))
        sol03DF = inputDF.filter(F.col("trip_end_timestamp").between(input_date_start_string, input_date_end_string)).withColumn("trip_km_per_hr", (F.col("trip_miles")*kmInUnitMile)/(F.col("trip_seconds")/3600)).agg({"trip_km_per_hr":"avg"})
        return sol03DF.collect()


    def total_trips_counts_between_dates(self, start_date, end_date):
        '''
        get total trips count 
        '''
        start_date_string = dt.datetime.strftime(start_date, DATE_FORMAT_ISO)
        end_date_string = dt.datetime.strftime(end_date, DATE_FORMAT_ISO)
        inputDF = self.loadFile(current_app.config.get('SPARK_MASTER', ''),current_app.config.get('INPUT_DATA_FILE', ''))
        # app.logger.warn([current_app.config.get('SPARK_MASTER', ''),current_app.config.get('INPUT_DATA_FILE', '')])
        # app.logger.warn(inputDF.printSchema())
        newDF = inputDF.withColumn("start_date", F.to_date("trip_start_timestamp")).filter(F.col("start_date").between(start_date_string,end_date_string)).groupby("start_date").count().orderBy("start_date")
        return newDF.collect()
        
    
    def sample_work(self):
        '''
        just a sample task to check if spark jobs running okay or not
        '''
        spark = self.loadSpark(current_app.config.get('SPARK_MASTER', ''))
        app.logger.warn(" here inside sample_work ")
        app.logger.warn(app.config.get('CONFIG_NAME'))
        rdd=spark.sparkContext.parallelize([1,2,3,4,5])
        countVal = rdd.count()
        return countVal

    def __del__(self):
        try:
            self.spark.stop()
        except:
            pass

sparkTasks = SparkTasks()
