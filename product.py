import sqlite3

DB_FILE = "market.db"

# === 数据库初始化 ===
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    # 商品表
    c.execute("""
        CREATE TABLE IF NOT EXISTS products(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            price TEXT,
            seller TEXT,
            contact TEXT,
            FOREIGN KEY(seller) REFERENCES users(username)
        )
    """)
    conn.commit()
    conn.close()

# === 输入校验 ===
def validate_title(title):
    if not title.strip():
        print("商品标题不能为空。")
        return False
    return True

def validate_price(price):
    if not price.strip():
        print("商品价格不能为空。")
        return False
    try:
        float(price)
        return True
    except ValueError:
        print("商品价格必须是数字。")
        return False

# === 用户相关辅助函数 ===
def get_user_contact(username):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT contact FROM users WHERE username=?", (username,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else None

# === 商品操作 ===
def add_product(title, description, price, seller_username):
    if not validate_title(title) or not validate_price(price):
        return
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT contact FROM users WHERE username=?", (seller_username,))
    row = c.fetchone()
    if not row:
        print("无法获取卖家联系方式，请检查用户名。")
        conn.close()
        return
    contact = row[0]
    c.execute("INSERT INTO products(title, description, price, seller, contact) VALUES(?,?,?,?,?)",
              (title, description, price, seller_username, contact))
    conn.commit()
    conn.close()
    print(f"商品 '{title}' 发布成功。")

def list_products(keyword=None):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    if keyword:
        c.execute("SELECT id, title, price, seller FROM products WHERE title LIKE ?", (f"%{keyword}%",))
    else:
        c.execute("SELECT id, title, price, seller FROM products")
    rows = c.fetchall()
    conn.close()
    if not rows:
        print("未找到商品。")
        return
    for row in rows:
        print(f"ID: {row[0]}, 标题: {row[1]}, 价格: {row[2]}, 卖家: {row[3]}")

def show_product_detail(product_id):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT id, title, description, price, seller, contact FROM products WHERE id=?", (product_id,))
    row = c.fetchone()
    conn.close()
    if not row:
        print("未找到该商品。")
        return
    print(f"\nID: {row[0]}")
    print(f"标题: {row[1]}")
    print(f"描述: {row[2]}")
    print(f"价格: {row[3]}")
    print(f"卖家: {row[4]}")
    print(f"联系方式: {row[5]}")

# === 修改自己商品 ===
def update_product(product_id, username):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT title, description, price FROM products WHERE id=? AND seller=?", (product_id, username))
    row = c.fetchone()
    if not row:
        print("未找到该商品，或您无权限修改。")
        conn.close()
        return
    print(f"当前标题: {row[0]}")
    print(f"当前描述: {row[1]}")
    print(f"当前价格: {row[2]}")

    new_title = input("请输入新的标题（回车保持不变）: ")
    new_description = input("请输入新的描述（回车保持不变）: ")
    new_price = input("请输入新的价格（回车保持不变）: ")

    new_title = new_title if new_title.strip() else row[0]
    new_description = new_description if new_description.strip() else row[1]
    new_price = new_price if new_price.strip() else row[2]

    if not validate_title(new_title) or not validate_price(new_price):
        print("修改失败，数据不符合要求。")
        conn.close()
        return

    c.execute("UPDATE products SET title=?, description=?, price=? WHERE id=? AND seller=?",
              (new_title, new_description, new_price, product_id, username))
    conn.commit()
    conn.close()
    print("商品信息已更新。")

# === 删除自己商品 ===
def delete_product_user(product_id, username):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT id FROM products WHERE id=? AND seller=?", (product_id, username))
    row = c.fetchone()
    if not row:
        print("未找到该商品，或您无权限删除。")
        conn.close()
        return
    c.execute("DELETE FROM products WHERE id=? AND seller=?", (product_id, username))
    conn.commit()
    conn.close()
    print(f"商品 ID {product_id} 已删除。")

# === 命令行测试 ===
if __name__ == "__main__":
    init_db()
    seller = input("请输入已登录用户名: ")
    while True:
        print("\n=== 商品系统 ===")
        print("1. 发布商品")
        print("2. 查看商品列表")
        print("3. 查看商品详情")
        print("4. 修改自己发布的商品")
        print("5. 删除自己发布的商品")
        print("6. 退出")
        choice = input("请选择操作: ")

        if choice == "1":
            title = input("商品标题: ")
            description = input("商品描述: ")
            price = input("商品价格: ")
            add_product(title, description, price, seller)

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
            try:
                pid = int(input("请输入要修改的商品ID: "))
                update_product(pid, seller)
            except ValueError:
                print("请输入正确的数字ID。")

        elif choice == "5":
            try:
                pid = int(input("请输入要删除的商品ID: "))
                delete_product_user(pid, seller)
            except ValueError:
                print("请输入正确的数字ID。")

        elif choice == "6":
            break

        else:
            print("无效选项，请重试。")
