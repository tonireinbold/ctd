import os
import psutil
import socket
import threading
import time

HOST = "localhost"
PORT = 10012

username = input("Nome de usuário: ")
password = input("Senha: ")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(f"{username}:{password}".encode())
    response = s.recv(1024)

    if response.decode() == "INVALIDO":
        print("Nome de usuário ou senha inválidos.")
    else:
        blacklist = response.decode().split("\n")
        print("Conectado e Operando - Não Feche essa Janela.")


        def shutdown():
            print("Encerrando o programa...")
            os._exit(0)

        shutdown_thread = threading.Timer(3 * 60 * 60, shutdown)
        shutdown_thread.start()

        while True:
            for root, dirs, files in os.walk(os.path.join(os.environ['LOCALAPPDATA'], "Temp")):
                for file in files:
                    file_path = os.path.join(root, file)
                    if file_path in blacklist:
                        s.sendall(b"DETECTADO")
                        time.sleep(1)  # espera um pouco para evitar spam

            for proc in psutil.process_iter():
                if proc.name() in blacklist:
                    s.sendall(b"DETECTADO")
                    time.sleep(1)  # espera um pouco para evitar spam

            time.sleep(60)
