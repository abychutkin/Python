from socket import *
import subprocess

def auth(cliSocket):
    username = b'admin'
    passw = b'123'
    for i in range(3):
        cliSocket.send(b'Login:')
        login=cliSocket.recv(BUFFSIZE)[:-1]
        cliSocket.send(b'Password:')
        password=cliSocket.recv(BUFFSIZE)[:-1]
        if login == username and paassword == passw:
            return True
    return False

def clientWork(cliSocket):
    while True:
        cliSocket.send('cmd: ')
        command=cliSocket.recv(BUFFSIZE)
        if not command or command[:-1]==b'exit':
            break
        output = subprocess.getoutput(command)
        cliSocket.send(bytes(output+'\n','utf-8'))
    cliSocket.close()

HOST = ''
PORT = 4448
BUFFSIZE = 1024
ADDR = (HOST,PORT)

tcpServer = socket(AF_INET, SOCK_STREAM)
tcpServer.bind(ADDR)
tcpServer.listen(5)

while True:
    tcpConn = tcpServer.accept()[0]
    if auth(tcpConn):
        clientWork(tcpConn)
    else:
        tcpConn.close()
tcpServer.close()
