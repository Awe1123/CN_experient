import threading
import subprocess

def run_server():
    # 启动服务器
    subprocess.run(["python", "chatServer.py"])

def run_client():
    # 启动客户端
    subprocess.run(["python", "chatClient.py"])

if __name__ == "__main__":
    # 创建并启动服务器线程
    server_thread = threading.Thread(target=run_server)
    server_thread.start()

    # 创建并启动客户端线程
    client_thread = threading.Thread(target=run_client)
    client_thread.start()

    # 等待两个线程完成
    server_thread.join()
    client_thread.join()
