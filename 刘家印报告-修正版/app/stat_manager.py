# -*- coding: utf-8 -*-
"""统计：分类统计、借阅趋势、畅销榜（聚合管道）。"""
from mongodb_connect import get_db

def category_stat():
    """按类别分组：库存总量、平均价格、图书数量，按库存总量降序。"""
    db = get_db()
    return list(db["books"].aggregate([
        {"$group": {
            "_id": "$category",
            "total_stock": {"$sum": "$stock"},
            "avg_price": {"$avg": "$price"},
            "count": {"$sum": 1}
        }},
        {"$sort": {"total_stock": -1}}
    ]))

def borrow_trend():
    """按年份分组统计借阅量，格式化输出。"""
    db = get_db()
    return list(db["borrow_logs"].aggregate([
        {"$group": {
            "_id": {"$dateToString": {"format": "%Y年", "date": "$borrow_date"}},
            "count": {"$sum": 1}
        }},
        {"$sort": {"_id": 1}}
    ]))

def best_sellers(n=5):
    """借阅次数最多的图书。"""
    db = get_db()
    return list(db["books"].find().sort("borrow_count", -1).limit(n))
