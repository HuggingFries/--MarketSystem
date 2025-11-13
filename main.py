# main.py
from user import init_db as init_user_db, register as user_register, login as user_login, \
                 show_user, update_password as update_user_password, update_contact as update_user_contact
from product import init_db as init_product_db, add_product, list_products, show_product_detail, \
                    update_product, delete_product_user
import sqlite3

DB_FILE = "market.db"

def get_user_products(username):
    """获取当前用户发布的商品列表"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT id, title, price FROM products WHERE seller=?", (username,))
    rows = c.fetchall()
    conn.close()
    return rows

def init_all_db():
    init_user_db()
    init_product_db()

def user_menu(username):
    while True:
        print(f"\n=== 用户操作 ({username}) ===")
        print("1. 查看个人主页")
        print("2. 发布商品")
        print("3. 查看商品列表")
        print("4. 查看商品详情")
        print("5. 查看自己发布的商品")
        print("6. 退出用户系统")
        choice = input("请选择操作: ")

        if choice == "1":
            # 查看个人主页
            while True:
                print("\n--- 个人主页 ---")
                print("1. 查看个人信息")
                print("2. 修改密码")
                print("3. 修改联系方式")
                print("4. 返回上一级")
                sub_choice = input("请选择操作: ")
                if sub_choice == "1":
                    show_user(username)
                elif sub_choice == "2":
                    update_user_password(username)
                elif sub_choice == "3":
                    update_user_contact(username)
                elif sub_choice == "4":
                    break
                else:
                    print("无效选项，请重试。")

        elif choice == "2":
            title = input("商品标题: ")
            description = input("商品描述: ")
            price = input("商品价格: ")
            add_product(title, description, price, username)

        elif choice == "3":
            keyword = input("请输入关键字（留空显示所有商品）: ")
            if keyword.strip() == "":
                keyword = None
            list_products(keyword)

        elif choice == "4":
            try:
                pid = int(input("请输入商品ID: "))
                show_product_detail(pid)
            except ValueError:
                print("请输入正确的数字ID。")

        elif choice == "5":
            while True:
                products = get_user_products(username)
                if not products:
                    print("您还没有发布任何商品。")
                    break
                print("\n--- 我的商品列表 ---")
                for p in products:
                    print(f"ID: {p[0]}, 标题: {p[1]}, 价格: {p[2]}")
                print("1. 修改商品")
                print("2. 删除商品")
                print("3. 返回上一级")
                sub_choice = input("请选择操作: ")
                if sub_choice == "1":
                    try:
                        pid = int(input("请输入要修改的商品ID: "))
                        update_product(pid, username)
                    except ValueError:
                        print("请输入正确的数字ID。")
                elif sub_choice == "2":
                    try:
                        pid = int(input("请输入要删除的商品ID: "))
                        delete_product_user(pid, username)
                    except ValueError:
                        print("请输入正确的数字ID。")
                elif sub_choice == "3":
                    break
                else:
                    print("无效选项，请重试。")

        elif choice == "6":
            break

        else:
            print("无效选项，请重试。")

if __name__ == "__main__":
    init_all_db()
    while True:
        print("\n=== 网络商场系统 ===")
        print("1. 用户注册")
        print("2. 用户登录")
        print("3. 退出系统")
        choice = input("请选择操作: ")

        if choice == "1":
            username = input("用户名: ")
            contact = input("联系方式（手机号或微信号）: ")
            while True:
                password1 = input("请输入密码: ")
                password2 = input("请再次输入密码: ")
                if password1 != password2:
                    print("两次密码不一致，请重新输入。")
                else:
                    break
            user_register(username, password1, contact)

        elif choice == "2":
            username = input("用户名: ")
            password = input("密码: ")
            if user_login(username, password):
                user_menu(username)

        elif choice == "3":
            print("退出系统，感谢使用！")
            break

        else:
            print("无效选项，请重试。")
