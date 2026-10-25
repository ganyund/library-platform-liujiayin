# -*- coding: utf-8 -*-
"""读者管理：信息管理、学院统计、等级分布。"""
from mongodb_connect import get_db

def get_col():
    return get_db()["readers"]

def list_readers():
    return list(get_col().find())

def count_by_college():
    return list(get_col().aggregate([
        {"$group": {"_id": "$college", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}
    ]))

def level_distribution():
    return list(get_col().aggregate([
        {"$group": {"_id": "$level", "count": {"$sum": 1}}}
    ]))

def colleges():
    return get_col().distinct("college")
