import sys
import os

import allure
from jinja2 import Template

from utils.allure_utils import allure_init
from utils.analyse_case import analyse_case
from utils.send_request import send_http_request, send_jdbc_request

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

            #allure报告初始化
            allure_init(case)

            #核心步骤1: 解析请求数据
            request_data = analyse_case(case)

            #核心步骤2: 发起请求，得到响应结果
            res = send_http_request(**request_data)

            #核心步骤3: 处理断言
            #http响应断言
            # assert res.json()["meta"]["msg"] == case["expected"]#res.json() 会把返回的 JSON 字符串解析成 Python 字典。实际结果==预期结果
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
                assert send_jdbc_request(case["sql_check"], index=0) == case["sql_expected"]

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
                    value = send_jdbc_request(value, index=0)
                    all[key] = value
                    print("🔹all结果:", all)

