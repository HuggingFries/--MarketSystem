# user.py
import sqlite3

DB_FILE = "market.db"

# === 初始化数据库 ===
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users(
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            contact TEXT
        )
    """)
    conn.commit()
    conn.close()

# === 用户操作 ===
def register(username, password, contact):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users(username, password, contact) VALUES(?, ?, ?)", 
                  (username, password, contact))
        conn.commit()
        print(f"注册成功，欢迎 {username}！")
        return True
    except sqlite3.IntegrityError:
        print(f"用户 '{username}' 已存在！")
        return False
    finally:
        conn.close()

def login(username, password):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT password FROM users WHERE username=?", (username,))
    row = c.fetchone()
    conn.close()
    if not row:
        print("用户不存在！")
        return False
    if row[0] != password:
        print("密码错误！")
        return False
    print(f"登录成功，欢迎回来 {username}！")
    return True

def show_user(username):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT username, password, contact FROM users WHERE username=?", (username,))
    row = c.fetchone()
    conn.close()
    if not row:
        print("未找到用户。")
        return
    print(f"用户名: {row[0]}")
    print(f"密码: {row[1]}")
    print(f"联系方式: {row[2]}")

def update_password(username):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT password FROM users WHERE username=?", (username,))
    row = c.fetchone()
    if not row:
        print("未找到用户。")
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
    c.execute("UPDATE users SET password=? WHERE username=?", (new_password1, username))
    conn.commit()
    conn.close()
    print("密码已更新。")

def update_contact(username):
    new_contact = input("请输入新的联系方式: ")
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("UPDATE users SET contact=? WHERE username=?", (new_contact, username))
    conn.commit()
    conn.close()
    print("联系方式已更新。")

# === 命令行交互 ===
if __name__ == "__main__":
    init_db()
    while True:
        print("\n=== 用户系统 ===")
        print("1. 注册")
        print("2. 登录")
        print("3. 查看用户信息")
        print("4. 修改密码")
        print("5. 修改联系方式")
        print("6. 退出")
        choice = input("请选择操作: ")

        if choice == "1":
            username = input("请输入用户名: ")
            contact = input("请输入联系方式（手机号或微信号）: ")
            while True:
                password1 = input("请输入密码: ")
                password2 = input("请再次输入密码: ")
                if password1 != password2:
                    print("两次密码不一致，请重新输入。")
                else:
                    break
            register(username, password1, contact)

        elif choice == "2":
            username = input("用户名: ")
            password = input("密码: ")
            login(username, password)

        elif choice == "3":
            username = input("要查看的用户名: ")
            show_user(username)

        elif choice == "4":
            username = input("请输入用户名: ")
            update_password(username)

        elif choice == "5":
            username = input("请输入用户名: ")
            update_contact(username)

        elif choice == "6":
            break

        else:
            print("无效选项，请重试。")
