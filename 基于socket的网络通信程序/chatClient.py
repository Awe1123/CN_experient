# 客户端部分
# 1) 导入库
import PySimpleGUI as sg

# 导入套接字库
import socket
from sys import exit
from struct import pack, unpack

# 主机IP为127.0.0.1
HOST = '127.0.0.1'

# 端口号为50007
PORT = 50007

# 创建TCP Socket
# 服务器之间网络通信，使用流式socket,for TCP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 创建UDP Socket
# sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

# 设置套接字操作的超时期为0.3s
sock.settimeout(0.3)

try:
    # 连接到address处的套接字
    sock.connect((HOST, PORT))
    sock.settimeout(None)

except Exception as e:
    print('Server not found or not open')
    exit()

while True:
    msg = input('Input the content you want to send:').encode()
    # 完整发送TCP数据
    sock.sendall(pack('i', len(msg)) + msg)
    length = unpack('i', sock.recv(4))[0]
    # 完整发送TCP数据
    data = sock.recv(length).decode()
    layout = [
        [sg.Text('Input the content you want to send:'), sg.InputText(msg)],
        [sg.Text('Received message:'), sg.Text(data)]
    ]
    # 3) 创建窗口
    window = sg.Window('Client _Windows', layout)
    event, values = window.read()  # 窗口的读取，有两个返回值(1.事件2.值)
    if msg.lower() == b'bye':
        break

sock.close()
