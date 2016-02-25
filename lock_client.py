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
import pickle
import net_client as n

# Programa principal

if len(sys.argv) > 2:
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    ID = int(sys.argv[3])
    lserver=n.server(HOST,PORT)

    while True:
        msg = raw_input("Comando: ")
        if msg == "exit":
            sys.exit()
        lserver.connect()
        print 'Recebi ', lserver.send_receive(msg)



else:
    print "Sem argumentos ou argumentos incompletos"