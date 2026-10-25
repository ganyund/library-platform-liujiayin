# -*- coding: utf-8 -*-
"""数据库连接模块：封装 library 库的获取，供其他模块统一调用。"""
from pymongo import MongoClient

# 连接参数统一定义在这里
# 使用读写账号 libWriter，密码中的 @ 需 URL 编码为 %40
MONGO_URI = "mongodb://libWriter:Writer%40123@localhost:27017/?authSource=admin"
DB_NAME = "library"

_client = None

def get_db():
    """获取 library 数据库连接（单例）。"""
    global _client
    if _client is None:
        _client = MongoClient(MONGO_URI)
    return _client[DB_NAME]

def close():
    """关闭连接。"""
    global _client
    if _client is not None:
        _client.close()
        _client = None

if __name__ == "__main__":
    db = get_db()
    print("数据库连接成功：", db.client.address)
    for name in db.list_collection_names():
        print(f"  集合 {name}: {db[name].count_documents()} 条")
    close()
