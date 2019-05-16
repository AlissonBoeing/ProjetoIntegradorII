import socket

from pip._vendor.distlib.compat import raw_input

ip = raw_input('digite o ip de conexao: ')
port = 7000
addr = ((ip, port))
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(addr)
mensagem = raw_input("digite uma mensagem para enviar ao servidor")
client_socket.send(mensagem)
print
'mensagem enviada'
client_socket.close()