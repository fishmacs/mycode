package com.example

import org.apache.spark.SparkContext
import org.apache.spark.SparkContext._
import org.apache.spark.SparkConf
import org.apache.spark.sql.{SQLContext, DataFrame, Row}
import org.apache.spark.sql.types.{DataType, IntegerType, TimestampType, DateType, StringType, StructType, StructField}

object Hello {
  def main(args: Array[String]): Unit = {
    val conf = new SparkConf().setAppName("Simple Application")
    val sparkCxt = new SparkContext(conf)
    val sqlCxt = new SQLContext(sparkCxt)
    val columns = List(
      ("id", StringType),
      ("vendor", StringType),
      ("create_time", TimestampType),
      ("device_id", StringType),
      ("area", StringType),
      ("product", StringType)
    )
    val logData = sqlCxt.read
      .format("com.databricks.spark.csv")
      .option("header", "true")
      .option("inferSchema", "true")
      .schema(columnsToSchema(columns))
      .load("/Users/zw/work/lanzhou/bigdata/大数据上海数据样本/用户信息.csv")
    Println("Lines with data: %s".format(logData.count))
    saveDB(sqlCxt, logData, columns.updated(2, ("create_time", DateType)))
  }

  def saveDB(sqlCxt: SQLContext, df: DataFrame, columns: List[(String, DataType)]): Unit = {
    val df1 = sqlCxt.createDataFrame(
      df.map {
        case Row(id, vendor, time: java.sql.Timestamp, device, area, product) =>
          Row(id, vendor, new java.sql.Date(time.getTime), device, area, product)
      },
      columnsToSchema(columns))
    val url = "jdbc:sqlite:/Users/zw/Documents/mycode/learn/spark/spark-test/test.sqlite"
    df1.createJDBCTable(url, "user", true)
  }

  def columnsToSchema(columns: List[(String, DataType)]): StructType = {
    StructType(columns.map {case (n, t) => StructField(n, t)})
  }
}

object RddHelper {
  def showPartitions[T](rdd: org.apache.spark.rdd.RDD[T]): Seq[(Int, List[T])] = {
    rdd.mapPartitionsWithIndex {
      (i, iter) => {
        var map = scala.collection.mutable.Map[Int, List[T]]()
        while(iter.hasNext) {
          if (map.contains(i)) {
            map(i) = iter.next :: map(i)
          } else {
            map(i) = List[T](iter.next)
          }
        }
        map.iterator
      }
    }.collect
  }
}
