# admin.py
import sqlite3
from product import list_products as user_list_products, show_product_detail
from user import show_user

DB_FILE = "market.db"

# === 数据库操作 ===
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    # 管理员表
    c.execute("""
        CREATE TABLE IF NOT EXISTS admins(
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            contact TEXT
        )
    """)
    conn.commit()
    conn.close()

# --- 管理员操作 ---
def register_admin(username, password, contact):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO admins(username, password, contact) VALUES(?, ?, ?)",
                  (username, password, contact))
        conn.commit()
        print(f"管理员 '{username}' 注册成功。")
        return True
    except sqlite3.IntegrityError:
        print(f"管理员 '{username}' 已存在。")
        return False
    finally:
        conn.close()

def login_admin(username, password):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT password FROM admins WHERE username=?", (username,))
    row = c.fetchone()
    conn.close()
    if not row:
        print("管理员不存在！")
        return False
    if row[0] != password:
        print("密码错误！")
        return False
    print(f"管理员登录成功，欢迎 {username}！")
    return True

def update_admin_password(username):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT password FROM admins WHERE username=?", (username,))
    row = c.fetchone()
    if not row:
        print("未找到管理员。")
        conn.close()
        return
    old_password = input("请输入旧密码: ")
    if old_password != row[0]:
        print("旧密码错误！")
        conn.close()
        return
    while True:
        new_password1 = input("请输入新密码: ")
        new_password2 = input("请再次输入新密码: ")
        if new_password1 != new_password2:
            print("两次密码不一致，请重新输入。")
        else:
            break
    c.execute("UPDATE admins SET password=? WHERE username=?", (new_password1, username))
    conn.commit()
    conn.close()
    print("密码已更新。")

def update_admin_contact(username):
    new_contact = input("请输入新的联系方式: ")
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("UPDATE admins SET contact=? WHERE username=?", (new_contact, username))
    conn.commit()
    conn.close()
    print("联系方式已更新。")

# --- 用户管理 ---
def list_users():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT username, password, contact FROM users")
    rows = c.fetchall()
    conn.close()
    if not rows:
        print("当前没有用户。")
        return
    for row in rows:
        print(f"用户名: {row[0]}, 密码: {row[1]}, 联系方式: {row[2]}")

def delete_user(username):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    # 先删除用户发布的商品
    c.execute("DELETE FROM products WHERE seller=?", (username,))
    
    # 再删除用户自身
    c.execute("DELETE FROM users WHERE username=?", (username,))
    
    conn.commit()
    conn.close()
    print(f"用户 '{username}' 及其所有商品已删除。")

# --- 商品管理 ---
def list_products():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT id, title, price, seller, contact FROM products")
    rows = c.fetchall()
    conn.close()
    if not rows:
        print("当前没有商品。")
        return
    for row in rows:
        print(f"ID: {row[0]}, 标题: {row[1]}, 价格: {row[2]}, 卖家: {row[3]}, 联系方式: {row[4]}")

def delete_product(product_id):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("DELETE FROM products WHERE id=?", (product_id,))
    conn.commit()
    conn.close()
    print(f"商品 ID {product_id} 已删除。")

# === 命令行交互 ===
if __name__ == "__main__":
    init_db()
    while True:
        print("\n=== 管理员系统 ===")
        print("1. 管理员注册")
        print("2. 管理员登录")
        print("3. 修改管理员密码")
        print("4. 修改管理员联系方式")
        print("5. 查看所有用户")
        print("6. 删除用户")
        print("7. 查看所有商品")
        print("8. 删除商品")
        print("9. 退出")
        choice = input("请选择操作: ")

        if choice == "1":
            username = input("管理员用户名: ")
            contact = input("联系方式: ")
            while True:
                password1 = input("请输入密码: ")
                password2 = input("请再次输入密码: ")
                if password1 != password2:
                    print("两次密码不一致，请重新输入。")
                else:
                    break
            register_admin(username, password1, contact)

        elif choice == "2":
            username = input("管理员用户名: ")
            password = input("密码: ")
            login_admin(username, password)

        elif choice == "3":
            username = input("管理员用户名: ")
            update_admin_password(username)

        elif choice == "4":
            username = input("管理员用户名: ")
            update_admin_contact(username)

        elif choice == "5":
            list_users()

        elif choice == "6":
            username = input("请输入要删除的用户名: ")
            delete_user(username)

        elif choice == "7":
            list_products()

        elif choice == "8":
            try:
                pid = int(input("请输入要删除的商品ID: "))
                delete_product(pid)
            except ValueError:
                print("请输入正确的数字ID。")

        elif choice == "9":
            break

        else:
            print("无效选项，请重试。")
