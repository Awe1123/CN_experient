# 服务端部分
# 导入GUI库
# TCP通信程序：接收到客户端的文字消息，服务器查询字典并自动回复。
import socket
from os.path import commonprefix
from struct import pack, unpack
from sys import exit

import PySimpleGUI as sg

# 设置缓冲区大小（一次能接收的最大字节数）
BUFFER_SIZE = 9012

words = {'how': 'Fine',
         'how old': '20',
         "name": 'LJS',
         "who": 'CSUer',
         'school': 'CSU',
         'where': 'CSU, Changsha',
         'number': '8207210306',
         'bye': 'Bye'}

HOST = ''
PORT = 50007

# 创建TCP套接字，绑定地址和端口号
sock_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 创建UDP Socket
# sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

# 将套接字绑定到地址
sock_server.bind((HOST, PORT))
# 开始监听TCP传入连接
sock_server.listen(1)

try:
    # 接受TCP连接并返回
    conn, addr = sock_server.accept()
except:
    exit()

while True:
    int_bytes = b''
    rest = 4
    while rest > 0:
        temp = conn.recv(rest)
        if not temp:
            break
        int_bytes = int_bytes + temp
        rest = rest - len(temp)
    if rest > 0:
        break

    rest = unpack('i', int_bytes)[0]
    data = b''
    while rest > 0:
        # 接受TCP套接字的数据
        temp = conn.recv(min(rest, BUFFER_SIZE))
        # 接受UDP套接字的数据
        # conn.recvfrom(min(rest, BUFFER_SIZE))
        data = data + temp
        rest = rest - len(temp)
    if rest > 0:
        break
    data = ' '.join(data.decode().split())
    m = 0
    key = ''
    for k in words.keys():
        if len(commonprefix([k, data])) > len(k) * 0.7:
            key = k
            break
        length = len(set(data.split()) & set(k.split()))
        if length > m:
            m = length
            key = k
    reply = words.get(key, "Sorry. I don't know.").encode()
    # 完整发送TCP数据
    conn.sendall(pack('i', len(reply)) + reply)
    # 发送UDP数据
    # conn.sendto(pack('i', len(reply)) + reply)

    # 定义布局，确定行数
    layout = [
        [sg.Text('Listening on port:'), sg.Text(PORT)],
        [sg.Text('Connected by:'), sg.Text(addr)],
        [sg.Text('Received message:'), sg.Text(data)],
    ]
    # 创建窗口
    window = sg.Window('Sever_Windows', layout)
    event, values = window.read()  # 窗口的读取，有两个返回值(1.事件2.值)

conn.close()
sock_server.close()

# 关闭窗口
window.close()
