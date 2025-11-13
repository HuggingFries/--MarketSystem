import sqlite3
import bcrypt

DB_FILE = "market.db"

# === 数据库初始化 ===
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    # 用户表
    c.execute("""
        CREATE TABLE IF NOT EXISTS users(
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            contact TEXT
        )
    """)
    conn.commit()
    conn.close()

# === 密码加密与校验 ===
def hash_password(plain_password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(plain_password.encode('utf-8'), salt)
    return hashed.decode('utf-8')  # 存为字符串

def check_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

# === 用户操作 ===
def register(username, password, contact):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT username FROM users WHERE username=?", (username,))
    if c.fetchone():
        print("用户名已存在，请选择其他用户名。")
        conn.close()
        return False
    hashed_pw = hash_password(password)
    c.execute("INSERT INTO users(username, password, contact) VALUES(?,?,?)",
              (username, hashed_pw, contact))
    conn.commit()
    conn.close()
    print(f"用户 '{username}' 注册成功。")
    return True

def login(username, password):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT password FROM users WHERE username=?", (username,))
    row = c.fetchone()
    conn.close()
    if not row:
        print("用户名不存在。")
        return False
    if check_password(password, row[0]):
        print("登录成功。")
        return True
    else:
        print("密码错误。")
        return False

def show_user(username):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT username, contact FROM users WHERE username=?", (username,))
    row = c.fetchone()
    conn.close()
    if row:
        print(f"用户名: {row[0]}")
        print(f"联系方式: {row[1]}")
    else:
        print("未找到用户信息。")

def update_password(username):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    old_pw = input("请输入当前密码: ")
    c.execute("SELECT password FROM users WHERE username=?", (username,))
    row = c.fetchone()
    if not row:
        print("用户不存在。")
        conn.close()
        return
    if not check_password(old_pw, row[0]):
        print("当前密码错误。")
        conn.close()
        return
    while True:
        new_pw1 = input("请输入新密码: ")
        new_pw2 = input("请再次输入新密码: ")
        if new_pw1 != new_pw2:
            print("两次密码不一致，请重新输入。")
        else:
            break
    hashed_pw = hash_password(new_pw1)
    c.execute("UPDATE users SET password=? WHERE username=?", (hashed_pw, username))
    conn.commit()
    conn.close()
    print("密码已更新。")

def update_contact(username):
    new_contact = input("请输入新的联系方式: ")
    if not new_contact.strip():
        print("联系方式不能为空。")
        return
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("UPDATE users SET contact=? WHERE username=?", (new_contact, username))
    conn.commit()
    conn.close()
    print("联系方式已更新。")

def delete_user(username):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    # 级联删除用户发布的商品
    c.execute("DELETE FROM products WHERE seller=?", (username,))
    # 删除用户自身
    c.execute("DELETE FROM users WHERE username=?", (username,))
    conn.commit()
    conn.close()
    print(f"用户 '{username}' 及其所有商品已删除。")
