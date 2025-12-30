# test_user.py
import pytest
import sqlite3
import os
from unittest.mock import patch
import user
import time

# 使用临时数据库文件
TEST_DB = "test_market.db"
user.DB_FILE = TEST_DB

# --- 测试准备与清理 ---
@pytest.fixture(scope="module", autouse=True)
def setup_db():
    # 删除旧数据库（如果存在）
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)

    # 初始化用户表
    user.init_db()

    # 创建 products 表，避免 delete_user 报错
    conn = sqlite3.connect(TEST_DB)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS products(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            seller TEXT
        )
    """)
    conn.commit()
    conn.close()

    yield

    # teardown: 尝试删除文件（Windows 下可能被锁）
    for _ in range(5):
        try:
            if os.path.exists(TEST_DB):
                os.remove(TEST_DB)
            break
        except PermissionError:
            time.sleep(0.1)

# --- 测试注册功能 ---
def test_register_success():
    result = user.register("alice", "password123", "alice@example.com")
    assert result is True

def test_register_duplicate():
    user.register("bob", "pw", "bob@example.com")
    result = user.register("bob", "pw", "bob@example.com")
    assert result is False

# --- 测试登录功能 ---
def test_login_success():
    user.register("charlie", "secret", "charlie@example.com")
    assert user.login("charlie", "secret") is True

def test_login_wrong_password():
    assert user.login("charlie", "wrong") is False

def test_login_nonexistent():
    assert user.login("ghost", "nopw") is False

# --- 测试显示用户信息 ---
def test_show_user(capsys):
    user.register("dave", "pw", "dave@example.com")
    user.show_user("dave")
    captured = capsys.readouterr()
    assert "dave@example.com" in captured.out

# --- 测试更新密码 ---
def test_update_password(monkeypatch):
    user.register("eve", "oldpw", "eve@example.com")

    # 模拟 input() 返回旧密码、新密码两次
    inputs = iter(["oldpw", "newpw123", "newpw123"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    
    user.update_password("eve")
    # 验证密码是否更新
    assert user.login("eve", "newpw123") is True
    assert user.login("eve", "oldpw") is False

# --- 测试更新联系方式 ---
def test_update_contact(monkeypatch, capsys):
    user.register("frank", "pw", "old@example.com")
    monkeypatch.setattr('builtins.input', lambda _: "new@example.com")
    user.update_contact("frank")
    captured = capsys.readouterr()
    assert "已更新" in captured.out

# --- 测试删除用户 ---
def test_delete_user():
    user.register("grace", "pw", "g@example.com")
    # 在 products 表中插入一个商品，保证 delete_user 正常运行
    conn = sqlite3.connect(TEST_DB)
    c = conn.cursor()
    c.execute("INSERT INTO products(name, seller) VALUES(?, ?)", ("item1", "grace"))
    conn.commit()
    conn.close()

    user.delete_user("grace")
    # 删除后登录应失败
    assert user.login("grace", "pw") is False
