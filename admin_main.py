# admin_main.py
from admin import init_db as init_admin_db, register_admin, login_admin, update_admin_password, \
                  update_admin_contact, list_users, delete_user, delete_product
from product import list_products

def admin_menu(username):
    while True:
        print(f"\n=== 管理员操作 ({username}) ===")
        print("1. 修改管理员密码")
        print("2. 修改管理员联系方式")
        print("3. 查看所有用户")
        print("4. 删除用户")
        print("5. 查看所有商品")
        print("6. 删除商品")
        print("7. 退出管理员系统")
        choice = input("请选择操作: ")

        if choice == "1":
            update_admin_password(username)
        elif choice == "2":
            update_admin_contact(username)
        elif choice == "3":
            list_users()
        elif choice == "4":
            uname = input("请输入要删除的用户名: ")
            delete_user(uname)
        elif choice == "5":
            list_products()
        elif choice == "6":
            try:
                pid = int(input("请输入要删除的商品ID: "))
                delete_product(pid)
            except ValueError:
                print("请输入正确的数字ID。")
        elif choice == "7":
            break
        else:
            print("无效选项，请重试。")

if __name__ == "__main__":
    init_admin_db()
    while True:
        print("\n=== 管理员系统 ===")
        print("1. 注册管理员")
        print("2. 管理员登录")
        print("3. 退出后台")
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
            from admin import login_admin
            if login_admin(username, password):
                admin_menu(username)

        elif choice == "3":
            print("退出后台管理系统。")
            break

        else:
            print("无效选项，请重试。")
