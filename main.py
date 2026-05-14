def hello(name: str) -> str:
    return f"你好，{name}！"

def add(a: int, b: int) -> int:
    return a + b

if __name__ == "__main__":
    print(hello("世界"))
    print(f"1+2={add(1,2)}")
