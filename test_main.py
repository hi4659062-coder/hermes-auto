from main import hello, add

def test_hello():
    assert hello("世界") == "你好，世界！"

def test_add():
    assert add(1, 2) == 3
