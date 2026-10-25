# -*- coding: utf-8 -*-
"""借阅管理：借阅登记、归还处理、逾期查询。"""
from datetime import datetime
from mongodb_connect import get_db

def get_col():
    return get_db()["borrow_logs"]

def borrow_book(reader_card, book_isbn):
    doc = {
        "borrow_date": datetime.now(),
        "reader_card": reader_card,
        "book_isbn": book_isbn,
        "status": "借出"
    }
    r = get_col().insert_one(doc)
    print(f"登记成功，_id={r.inserted_id}")

def return_book(reader_card, book_isbn):
    # borrow_logs 是时间序列集合，不支持对普通字段（status/return_date）做 update，
    # 因此采用：deleteMany 删除在借的"借出"记录 + insert_one 追加一条"已归还"流水。
    col = get_col()
    dr = col.delete_many(
        {"reader_card": reader_card, "book_isbn": book_isbn, "status": "借出"}
    )
    col.insert_one({
        "borrow_date": datetime.now(),
        "reader_card": reader_card,
        "book_isbn": book_isbn,
        "status": "已归还",
        "return_date": datetime.now()
    })
    print(f"归还处理完成，删除在借记录 {dr.deleted_count} 条，已追加归还流水")

def overdue_list():
    return list(get_col().find({"status": "逾期"}))
