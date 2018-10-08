import argparse
from socket import *


def connection(host, ports):
    print('PORT\tSTATE\tSERVICE')
    try:
        targetIp = gethostbyname(host)
    except:
        print("[-] Cannot resolve '{0}': Unknown host".format(host))
    tcpSocket = socket(AF_INET, SOCK_STREAM)
    for port in ports:
        scanner(targetIp, port)


def scanner(host, port):
    try:
        targetSocket = socket(AF_INET, SOCK_STREAM)
        targetSocket.connect((host,int(port)))
        targetSocket.send(b'random_string')
        banner = targetSocket.recv(100)

        #Убираем "220 " из баннера
        banner = banner.decode('utf-8') # Декодируется объект bytes, чтобы стать строкой
        banner = banner.split(' ')
        banner = ' '.join(banner[1:])
        
        print('{0}/tcp\t{1}\t{2}'.format(port,'open',banner[:-1])) 
        targetSocket.close()
    except:
        print('{0}/tcp\tclosed'.format(port))


parser = argparse.ArgumentParser(description='Simple Banner Grabbing Script',usage='You should specify host and port/ports to scan')
group = parser.add_mutually_exclusive_group() # это добавлено чтобы сделать опции -p и -P взаимоисключающимися
parser.add_argument('-H',dest='targetHost',action='store',help='Remote host')
group.add_argument('-p',dest='targetPort',action='store',type=int,help='Port to scan')
group.add_argument('-P',dest='targetPorts',action='store',help='Ports to scan')
args = parser.parse_args()

targetHost = args.targetHost



if targetHost == None or (args.targetPort == None and args.targetPorts == None):
    print(parser.usage)
    exit(0)


if args.targetPort:
    targetPorts = [args.targetPort]

if args.targetPorts:
    args.targetPorts = args.targetPorts.split(',')
    targetPorts = []
    for i in args.targetPorts:
        if i == '-':
            targetPorts = [i for i in range(65536)]
        elif '-' in i:
            borders = [int(i) for i in i.split('-')]
            for j in range(borders[0],borders[1]+1):
                targetPorts.append(j)
        else:
            targetPorts.append(i)

connection(targetHost,targetPorts)
