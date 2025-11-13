# product.py
import json
import os

PRODUCT_FILE = "products.json"

# 初始化
if not os.path.exists(PRODUCT_FILE):
    with open(PRODUCT_FILE, "w", encoding="utf-8") as f:
        json.dump([], f, ensure_ascii=False, indent=2)

def load_products():
    with open(PRODUCT_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_products(products):
    with open(PRODUCT_FILE, "w", encoding="utf-8") as f:
        json.dump(products, f, ensure_ascii=False, indent=2)

def add_product(title, description, price, seller_username, contact):
    """发布新商品"""
    products = load_products()
    product_id = len(products) + 1
    product = {
        "id": product_id,
        "title": title,
        "description": description,
        "price": price,
        "seller": seller_username,
        "contact": contact
    }
    products.append(product)
    save_products(products)
    print(f"商品 '{title}' 发布成功，ID={product_id}")

def list_products(keyword=None):
    """列出商品列表"""
    products = load_products()
    filtered = products
    if keyword:
        filtered = [p for p in products if keyword.lower() in p["title"].lower()]
    if not filtered:
        print("未找到商品。")
        return
    for p in filtered:
        print(f"ID: {p['id']}, 标题: {p['title']}, 价格: {p['price']}, 卖家: {p['seller']}")

def show_product_detail(product_id):
    """显示商品详情"""
    products = load_products()
    for p in products:
        if p["id"] == product_id:
            print(f"\nID: {p['id']}")
            print(f"标题: {p['title']}")
            print(f"描述: {p['description']}")
            print(f"价格: {p['price']}")
            print(f"卖家: {p['seller']}")
            print(f"联系方式: {p['contact']}")
            return
    print("未找到该商品。")

# === 命令行测试 ===
if __name__ == "__main__":
    current_user = input("请输入已登录用户名: ")
    contact = input("请输入您的联系方式（手机号或微信号）: ")

    while True:
        print("\n=== 商品系统 ===")
        print("1. 发布商品")
        print("2. 查看商品列表")
        print("3. 查看商品详情")
        print("4. 退出")
        choice = input("请选择操作: ")

        if choice == "1":
            title = input("商品标题: ")
            description = input("商品描述: ")
            price = input("商品价格: ")
            add_product(title, description, price, current_user, contact)

        elif choice == "2":
            keyword = input("请输入关键字（留空显示所有商品）: ")
            if keyword.strip() == "":
                keyword = None
            list_products(keyword)

        elif choice == "3":
            try:
                pid = int(input("请输入商品ID: "))
                show_product_detail(pid)
            except ValueError:
                print("请输入正确的数字ID。")

        elif choice == "4":
            break

        else:
            print("无效选项，请重试。")
