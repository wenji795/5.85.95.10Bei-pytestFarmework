import allure


@allure.step("1.解析请求数据")
def analyse_case(case):
    method = case["method"]  # case 是字典，字典要取某个键的值，必须用 方括号 []  意思是从字典里取指定键对应的值。
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
    return request_data

