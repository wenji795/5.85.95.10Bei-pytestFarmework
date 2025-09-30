import sys
import os
from jinja2 import Template
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import jsonpath
import pymysql
import pytest
import requests
from utils.excel_utils import read_excel



class TestRunner:


    # TODO:读取测试用例文件中的全部数据，用属性保存
    data = read_excel()

    # TODO:提取后的数据要初始化成一个全局的属性，可以用{}空字典存
    all = {}

    @pytest.mark.parametrize("case", data)
    def test_case(self, case):

            # 引用全局的all
            all = self.all

            #根据all的值，渲染case
            case = eval(Template(str(case)).render(all))
            # 渲染前：原本的数据源excel是列表，每一条用例是一个case是字典，先转成字符串str(case)，方便渲染
            # {"Authorization": "{{TOKEN}}"}     "{{TOKEN}}"：字典的 值，这里不是最终文本，而是 Jinja2 占位符（模板变量）
            # {{ ... }} 是 Jinja2 的语法，表示“把里面这个变量的值渲染进来”
            # 放在引号里是为了让渲染后的结果仍是一个“合法的字符串值”
            # 渲染时：render()是Template包的渲染函数
            # 渲染后：再用eval()转成字典
            # 外层花括号是字典，占位符要双大括；值是字符串要引号，渲染之后再反序列。



        # TODO:
            #核心步骤1: 解析请求数据
            method = case["method"]#case 是字典，字典要取某个键的值，必须用 方括号 []  意思是从字典里取指定键对应的值。
            url = "http://8.138.193.96:8888/api/private/v1" + case["path"]
            headers = eval(case["headers"]) if isinstance(case["headers"], str) else None
            params = eval(case["params"]) if isinstance(case["params"], str) else None
            data = eval(case["data"]) if isinstance(case["data"], str) else None
            json = eval(case["json"]) if isinstance(case["json"], str) else None
            files = eval(case["files"]) if isinstance(case["files"], str) else None

            request_data = {
                "method": method,
                "url": url,
                "headers": headers,
                "params": params,
                "data": data,
                "json": json,
                "files": files,
            }

            #核心步骤2: 发起请求，得到响应结果
            res = requests.request(**request_data)  # **字典 的意思是 参数解包，会把字典里的 key/value 当作函数的参数传进去。
            print("🔹核心步骤2json:",res.json())

            #核心步骤3: 处理断言
            #http响应断言
            # assert res.json()["meta"]["msg"] == case["expected"]#res.json() 会把返回的 JSON 字符串解析成 Python 字典。实际结果==预期结果
            print(res.json())
            if case ["check"]:
                # assert 实际结果 == 预期结果
                assert jsonpath.jsonpath(res.json(),case["check"])[0] == case["expected"]
                #case["check"] → 从字典里取出 JSONPath 表达式（例如 "$..msg"）case["expected"] → 从字典里取出预期结果（例如 "登录成功"）[0] → 因为 jsonpath() 返回列表，要取第一个元素
            else:
                # assert 预期结果 in 实际结果
                assert case["expected"] in res.text
                # assert case["expected"] in 实际结果

            #数据库断言
            # print(case ["sql_check"])
            # print(case ["sql_expected"])
            if case ["sql_check"] and case["sql_expected"]:
                #创建连接桥conn+游标驴cur，装货执行sql，卸货杀驴，拆桥
                conn = pymysql.Connect(  #pymysql.Connect() 是 PyMySQL 的连接方法，用来连接 MySQL 数据库
                    host="8.138.193.96",
                    port=3306,
                    database="mydb",
                    user="root",
                    password="beimeng2025",
                    charset="utf8mb4"
                )
                cur = conn.cursor()
                #执行语句
                cur.execute(case ["sql_check"])
                result = cur.fetchone()#从结果集中取一条数据（元组格式）

                cur.close()
                conn.close()
                assert result[0] == case["sql_expected"]

            #核心步骤4: 提取
            #JSON 提取
            if case["jsonExData"]:
                #首先把jsonExData的key和value拆开
                for key, value in eval(case["jsonExData"]).items():#这里case["jsonExData"]从excel拿出来是string，eval()转成字典
                   value = jsonpath.jsonpath(res.json(),value)[0] #value重新赋值！
                   # print(value)
                   #现在全局属性all在测试函数外面
                   all[key] = value
                   # print(all)

            #SQL提取
            if case["sqlExData"]:
                for key, value in eval(case["sqlExData"]).items():
                    print("🔹SQL 结果:", key)
                    print("🔹提取的数据value:", value)
                    conn = pymysql.Connect(  # pymysql.Connect() 是 PyMySQL 的连接方法，用来连接 MySQL 数据库
                        host="8.138.193.96",
                        port=3306,
                        database="mydb",
                        user="root",
                        password="beimeng2025",
                        charset="utf8mb4"
                    )
                    cur = conn.cursor()
                    cur.execute(value)
                    result = cur.fetchone()
                    cur.close()
                    conn.close()
                    value = result[0]
                    print("🔹value2结果:", value)
                    all[key] = value
                    print("🔹all结果:", all)

