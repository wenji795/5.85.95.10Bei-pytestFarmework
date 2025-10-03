import jsonpath

from utils.send_request import send_jdbc_request


def json_extrator(case, all, res):
    if case["jsonExData"]:
        # 首先把jsonExData的key和path拆开
        for key, path in eval(case["jsonExData"]).items():  # 这里case["jsonExData"]从excel拿出来是string，eval()转成字典
            v = jsonpath.jsonpath(res.json(), path)[0]  # value重新赋值！
            print("🔹v:", v)
            # 现在全局属性all在测试函数外面
            all[key] = v
            print("🔹all", all)

def jdbc_extrator(case, all):
    if case["sqlExData"]:
        for key, quary in eval(case["sqlExData"]).items():
            v = send_jdbc_request(quary, index=0)
            all[key] = v
            # print("🔹all结果:", all)