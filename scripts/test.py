import os
def testmethod():
    # 创建多级目录
    path = "222"
    os.makedirs(path,exist_ok=True)
    print("路径被创建")

if __name__ == "__main__":
    testmethod()