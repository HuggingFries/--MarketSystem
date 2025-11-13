# admin.py
import json
import os

USER_FILE = "users.json"
PRODUCT_FILE = "products.json"

# 初始化文件
for file in [USER_FILE, PRODUCT_FILE]:
    if not os.path.exists(file):
        if file == USER_FILE:
            with open(file, "w", encoding="utf-8") as f:
                json.dump({}, f, ensure_ascii=False, indent=2)
        else:
            with open(file, "w", encoding="utf-8") as f:
                json.dump([], f, ensure_ascii=False, indent=2)

# --- 用户管理 ---
def load_users():
    with open(USER_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_users(users):
    with open(USER_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)

def list_users():
    users = load_users()
    if not users:
        print("当前没有用户。")
        return
    for username in users:
        print(f"用户名: {username}, 密码: {users[username]['password']}")

def delete_user(username):
    users = load_users()
    if username in users:
        del users[username]
        save_users(users)
        print(f"用户 {username} 已删除。")
    else:
        print("未找到该用户。")

# --- 商品管理 ---
def load_products():
    with open(PRODUCT_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_products(products):
    with open(PRODUCT_FILE, "w", encoding="utf-8") as f:
        json.dump(products, f, ensure_ascii=False, indent=2)

def list_products():
    products = load_products()
    if not products:
        print("当前没有商品。")
        return
    for p in products:
        print(f"ID: {p['id']}, 标题: {p['title']}, 价格: {p['price']}, 卖家: {p['seller']}, 联系方式: {p['contact']}")

def delete_product(product_id):
    products = load_products()
    for p in products:
        if p["id"] == product_id:
            products.remove(p)
            save_products(products)
            print(f"商品 ID {product_id} 已删除。")
            return
    print("未找到该商品。")

# === 命令行后台管理 ===
if __name__ == "__main__":
    while True:
        print("\n=== 后台管理 ===")
        print("1. 查看所有用户")
        print("2. 删除用户")
        print("3. 查看所有商品")
        print("4. 删除商品")
        print("5. 退出")
        choice = input("请选择操作: ")

        if choice == "1":
            list_users()
        elif choice == "2":
            username = input("请输入要删除的用户名: ")
            delete_user(username)
        elif choice == "3":
            list_products()
        elif choice == "4":
            try:
                pid = int(input("请输入要删除的商品ID: "))
                delete_product(pid)
            except ValueError:
                print("请输入正确的数字ID。")
        elif choice == "5":
            break
        else:
            print("无效选项，请重试。")
