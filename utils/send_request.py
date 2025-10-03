import pymysql
import requests


def send_http_request(**request_data):
    res = requests.request(**request_data)  # **字典 的意思是 参数解包，会把字典里的 key/value 当作函数的参数传进去。
    print("🔹核心步骤2json:", res.json())
    return res

def send_jdbc_request(sql, index=0):
    # 创建连接桥conn+游标驴cur，装货执行sql，卸货杀驴，拆桥
    conn = pymysql.Connect(  # pymysql.Connect() 是 PyMySQL 的连接方法，用来连接 MySQL 数据库
        host="8.138.193.96",
        port=3306,
        database="mydb",
        user="root",
        password="beimeng2025",
        charset="utf8mb4"
    )
    cur = conn.cursor()
    # 执行语句
    cur.execute(sql)
    # cur.execute(case["sql_check"])
    result = cur.fetchone()  # 从结果集中取一条数据（元组格式）

    cur.close()
    conn.close()
    return result[index]


