#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações distribuídas - Projeto 1 - lock_client.py
Grupo:
Números de aluno:
"""
# Zona para fazer imports

import sys
import sock_utils

# Programa principal

if len(sys.argv) > 2:
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])

    while True:

        msg = raw_input("Comando: ")
        client_sock = sock_utils.create_tcp_client_socket(HOST, PORT)
        if msg == "exit":
            sys.exit()
        client_sock.sendall(msg)
        resposta = sock_utils.receive_all(client_sock, 1024)
        print 'Recebi ', resposta
        client_sock.close()

else:
    print "Sem argumentos ou argumentos incompletos"