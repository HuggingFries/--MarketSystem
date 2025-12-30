# test_product.py
import pytest
import sqlite3
import os
from unittest.mock import patch
import user
import product
import time

# 使用临时数据库
TEST_DB = "test_market.db"
user.DB_FILE = TEST_DB
product.DB_FILE = TEST_DB

# --- 测试准备与清理 ---
@pytest.fixture(scope="module", autouse=True)
def setup_db():
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)
    # 初始化用户表和商品表
    user.init_db()
    product.init_db()

    # 创建一个测试用户
    user.register("seller1", "pw", "seller1@example.com")
    yield

    # teardown 删除数据库文件
    for _ in range(5):
        try:
            if os.path.exists(TEST_DB):
                os.remove(TEST_DB)
            break
        except PermissionError:
            time.sleep(0.1)

# --- 测试商品添加 ---
def test_add_product_success(capsys):
    product.add_product("商品1", "描述1", "10.5", "seller1")
    captured = capsys.readouterr()
    assert "发布成功" in captured.out

def test_add_product_invalid_title(capsys):
    product.add_product("", "描述2", "15", "seller1")
    captured = capsys.readouterr()
    assert "标题不能为空" in captured.out

def test_add_product_invalid_price(capsys):
    product.add_product("商品3", "描述3", "abc", "seller1")
    captured = capsys.readouterr()
    assert "必须是数字" in captured.out

def test_add_product_nonexistent_seller(capsys):
    product.add_product("商品4", "描述4", "20", "ghost")
    captured = capsys.readouterr()
    assert "无法获取卖家联系方式" in captured.out

# --- 边界和辅助函数测试 ---
def test_validate_title_and_price():
    assert product.validate_title("") is False
    assert product.validate_title("有效标题") is True
    assert product.validate_price("") is False
    assert product.validate_price("abc") is False
    assert product.validate_price("12.5") is True

def test_get_user_contact():
    assert product.get_user_contact("seller1") == "seller1@example.com"
    assert product.get_user_contact("不存在用户") is None

# --- 测试商品列表和详情 ---
def test_list_products(capsys):
    product.list_products()
    captured = capsys.readouterr()
    assert "商品1" in captured.out

def test_list_products_keyword_not_found(capsys):
    product.list_products("不存在")
    captured = capsys.readouterr()
    assert "未找到商品" in captured.out

def test_show_product_detail(capsys):
    # 获取商品ID
    conn = sqlite3.connect(TEST_DB)
    c = conn.cursor()
    c.execute("SELECT id FROM products WHERE title=?", ("商品1",))
    pid = c.fetchone()[0]
    conn.close()

    product.show_product_detail(pid)
    captured = capsys.readouterr()
    assert "描述1" in captured.out

# --- 测试修改商品 ---
def test_update_product(monkeypatch, capsys):
    conn = sqlite3.connect(TEST_DB)
    c = conn.cursor()
    c.execute("SELECT id FROM products WHERE title=?", ("商品1",))
    pid = c.fetchone()[0]
    conn.close()

    # 模拟 input() 返回新标题、新描述、新价格
    inputs = iter(["新标题", "新描述", "15.5"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    product.update_product(pid, "seller1")
    captured = capsys.readouterr()
    assert "已更新" in captured.out or "修改失败" not in captured.out

def test_update_product_invalid(monkeypatch, capsys):
    conn = sqlite3.connect(TEST_DB)
    c = conn.cursor()
    c.execute("SELECT id FROM products WHERE title=?", ("新标题",))
    pid = c.fetchone()[0]
    conn.close()

    # 模拟输入空标题和非数字价格，触发修改失败
    inputs = iter(["", "desc", "abc"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    product.update_product(pid, "seller1")
    captured = capsys.readouterr()
    assert "修改失败" in captured.out

# --- 测试删除商品 ---
def test_delete_product_user(capsys):
    conn = sqlite3.connect(TEST_DB)
    c = conn.cursor()
    c.execute("SELECT id FROM products WHERE title=?", ("新标题",))
    pid = c.fetchone()[0]
    conn.close()

    product.delete_product_user(pid, "seller1")
    captured = capsys.readouterr()
    assert "已删除" in captured.out
