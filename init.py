import os 
import boto3
import sys
import pymysql

client=boto3.client("ssm",region_name="us-east-2")

def get_params(name):
    return client.get_parameters(
        Name=f"/application/banking/{name}",
        WithDecryption=True)["Parameters"]["Value"]

try:
    conn=pymysql.connect(
        host=get_params("DB_HOST"),
        user=get_params("DB_USER"),
        password=get_params("DB_PASSWORD"),
        port=int(get_params("DB_PORT")),
        connect_timeout=10,
    )


    cur=conn.cursor()

    base_dir=os.path.dirname(os.path.abspath(__file__))
    sql_file=os.path.join(base_dir,"init.sql")

    with open(sql_file,"r",encoding="utf-8") as f:
        sql=f.read()

    for statement in sql.split(";"):
        statement=statement.strip()
        if statement:
            cur.execute(statement)

    conn.commit()
    print("✅ Database initialized successfully")

except Exception as e:
    print("Error :",e)

finally:
    conn.close()