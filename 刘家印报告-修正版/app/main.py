# -*- coding: utf-8 -*-
"""菜单式主程序：串联图书/读者/借阅/统计模块。"""
from mongodb_connect import get_db, close
import book_manager, reader_manager, borrow_manager, stat_manager

def show_status():
    db = get_db()
    print("=" * 40)
    print("数据库连接正常，各集合文档总数：")
    for name in ["books", "readers", "borrow_logs"]:
        print(f"  {name}: {db[name].count_documents()} 条")
    print("=" * 40)

def menu():
    print("""
===== 图书情报检索与统计平台 =====
1. 按条件检索图书
2. 评分排行 Top5
3. 新增图书
4. 修改图书库存
5. 删除图书
6. 读者学院统计
7. 借阅登记
8. 归还处理
9. 分类统计报表
10. 借阅趋势分析
11. 畅销榜
0. 退出
==================================""")

def main():
    show_status()
    while True:
        menu()
        choice = input("请选择功能：").strip()
        if choice == "1":
            kw = input("书名关键字（可空）：").strip() or None
            cat = input("类别（可空）：").strip() or None
            res = book_manager.search(category=cat, keyword=kw)
            if not res: print("无结果")
            for b in res: print(b.get("title"), b.get("price"))
        elif choice == "2":
            for b in book_manager.top_rating(5):
                print(b["title"], b["rating"])
        elif choice == "3":
            book_manager.add_book({
                "isbn": input("ISBN："), "title": input("书名："),
                "author": input("作者："), "category": input("类别："),
                "price": float(input("价格：")), "stock": int(input("库存：")),
                "rating": 0.0, "borrow_count": 0})
        elif choice == "4":
            book_manager.update_stock(input("ISBN："), int(input("增减量：")))
        elif choice == "5":
            book_manager.delete_book(input("要删除的 ISBN："))
        elif choice == "6":
            for r in reader_manager.count_by_college():
                print(r["_id"], r["count"])
        elif choice == "7":
            borrow_manager.borrow_book(input("借阅证号："), input("ISBN："))
        elif choice == "8":
            borrow_manager.return_book(input("借阅证号："), input("ISBN："))
        elif choice == "9":
            for r in stat_manager.category_stat():
                print(r)
        elif choice == "10":
            for r in stat_manager.borrow_trend():
                print(r)
        elif choice == "11":
            for b in stat_manager.best_sellers(5):
                print(b["title"], b["borrow_count"])
        elif choice == "0":
            break
        else:
            print("输入有误，请重选")
    close()
    print("已关闭数据库连接，再见。")

if __name__ == "__main__":
    main()
