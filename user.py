# user.py
import json
import os

USER_FILE = "users.json"

# 初始化：若文件不存在则创建空文件
if not os.path.exists(USER_FILE):
    with open(USER_FILE, "w", encoding="utf-8") as f:
        json.dump({}, f)

def load_users():
    """读取用户数据"""
    with open(USER_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_users(users):
    """保存用户数据"""
    with open(USER_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)

def register(username, password):
    """注册新用户"""
    users = load_users()
    if username in users:
        print(f"用户 '{username}' 已存在！")
        return False
    users[username] = {"password": password}
    save_users(users)
    print(f"注册成功，欢迎 {username}！")
    return True

def login(username, password):
    """登录验证"""
    users = load_users()
    if username not in users:
        print("用户不存在！")
        return False
    if users[username]["password"] != password:
        print("密码错误！")
        return False
    print(f"登录成功，欢迎回来 {username}！")
    return True

def show_user(username):
    """显示用户信息"""
    users = load_users()
    if username not in users:
        print("未找到用户。")
        return
    info = users[username]
    print(f"用户名: {username}")
    print(f"密码: {info['password']}")  # 实际项目中不应显示密码，仅为演示

# === 以下为命令行交互测试 ===
if __name__ == "__main__":
    while True:
        print("\n=== 用户系统 ===")
        print("1. 注册")
        print("2. 登录")
        print("3. 查看用户信息")
        print("4. 退出")
        choice = input("请选择操作: ")

        if choice == "1":
            username = input("请输入用户名: ")
            password = input("请输入密码: ")
            register(username, password)

        elif choice == "2":
            username = input("用户名: ")
            password = input("密码: ")
            login(username, password)

        elif choice == "3":
            username = input("要查看的用户名: ")
            show_user(username)

        elif choice == "4":
            break

        else:
            print("无效选项，请重试。")
