# -*- coding: utf-8 -*-
"""图书管理：增删改查、条件检索、评分排行。"""
from mongodb_connect import get_db

def get_col():
    return get_db()["books"]

def add_book(book):
    r = get_col().insert_one(book)
    print(f"新增成功，_id={r.inserted_id}")

def add_books(books):
    r = get_col().insert_many(books)
    print(f"批量新增 {len(r.inserted_ids)} 条")

def find_by_isbn(isbn):
    return get_col().find_one({"isbn": isbn})

def search(price_min=None, category=None, keyword=None):
    q = {}
    if price_min is not None:
        q["price"] = {"$gte": price_min}
    if category:
        q["category"] = category
    if keyword:
        q["title"] = {"$regex": keyword}
    return list(get_col().find(q))

def update_stock(isbn, delta):
    r = get_col().update_one({"isbn": isbn}, {"$inc": {"stock": delta}})
    print(f"受影响 {r.modified_count} 条")

def delete_book(isbn):
    r = get_col().delete_one({"isbn": isbn})
    print(f"删除 {r.deleted_count} 条")

def top_rating(n=5):
    return list(get_col().find().sort("rating", -1).limit(n))
