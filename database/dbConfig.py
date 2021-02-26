# from influxdb import InfluxDBClient
#
# client=InfluxDBClient(host="localhost",port="8086")
# print(client.get_list_database())
# import "influxdata/influxdb/schema"





from datetime import datetime
import os
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# You can generate a Token from the "Tokens Tab" in the UI
token = os.environ['INFLUX_TOKEN']
org = "glanceapp2020@gmail.com"
bucket = "glanceapp2020's Bucket"

client = InfluxDBClient(url="https://eu-central-1-1.aws.cloud2.influxdata.com", token=token)
client.query_api()