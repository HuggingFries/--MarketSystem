# main.py
from user import register, login
from product import add_product, list_products, show_product_detail
from admin import list_users, list_products as admin_list_products, delete_user, delete_product

def main_menu():
    while True:
        print("\n=== 网络商场系统 ===")
        print("1. 用户注册")
        print("2. 用户登录")
        print("3. 管理员登录")
        print("4. 退出")
        choice = input("请选择操作: ")

        if choice == "1":
            username = input("请输入用户名: ")
            password = input("请输入密码: ")
            register(username, password)

        elif choice == "2":
            username = input("用户名: ")
            password = input("密码: ")
            if login(username, password):
                user_menu(username)

        elif choice == "3":
            admin_password = input("请输入管理员密码: ")
            if admin_password == "admin123":  # 简单演示
                admin_menu()
            else:
                print("管理员密码错误！")

        elif choice == "4":
            print("退出系统。")
            break

        else:
            print("无效选项，请重试。")

def user_menu(username):
    contact = input("请输入您的联系方式（手机号或微信号）: ")
    while True:
        print(f"\n=== 用户菜单 ({username}) ===")
        print("1. 发布商品")
        print("2. 查看商品列表")
        print("3. 查看商品详情")
        print("4. 退出登录")
        choice = input("请选择操作: ")

        if choice == "1":
            title = input("商品标题: ")
            description = input("商品描述: ")
            price = input("商品价格: ")
            add_product(title, description, price, username, contact)

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
            print(f"{username} 已退出登录。")
            break

        else:
            print("无效选项，请重试。")

def admin_menu():
    while True:
        print("\n=== 后台管理菜单 ===")
        print("1. 查看所有用户")
        print("2. 删除用户")
        print("3. 查看所有商品")
        print("4. 删除商品")
        print("5. 返回主菜单")
        choice = input("请选择操作: ")

        if choice == "1":
            list_users()
        elif choice == "2":
            username = input("请输入要删除的用户名: ")
            delete_user(username)
        elif choice == "3":
            admin_list_products()
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

if __name__ == "__main__":
    main_menu()
