import requests

login_data = {
    "method": "post",
    "url": "http://127.0.0.1:8888/api/private/v1/login",
    "data": {"username": "admin", "password": "123456"}
}

upload_data = {
    "method": "post",
    "url": "http://127.0.0.1:8888/api/private/v1/upload",
    "headers": None,
    "files": None
}

# === 获取 token ===
res1 = requests.request(**login_data)
token = res1.json()["data"]["token"]
print(token)

# === 文件上传 ===
upload_data["headers"] = {"Authorization": token}

# files 参数说明：
# 格式为 {参数名: 元组}
# 元组的结构为 (文件名, 文件对象, 文件类型)
# 例如: ("file", ("1.jpg", open("./file/1.jpg", "rb"), "jpg"))

upload_data["files"] = {"file": ("1.jpg", open("./file/1.jpg", "rb"), "jpg")}

res2 = requests.request(**upload_data)
print(res2.json())
