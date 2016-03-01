#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações distribuídas - Projeto 1 - lock_client.py
Grupo:
Números de aluno:
"""
# Zona para fazer imports

import sys
import net_client as n

# Programa principal

client_commands = ["LOCK", "RELEASE", "TEST", "STATS", "EXIT"]

if len(sys.argv) > 2:
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    ID = int(sys.argv[3])
    lserver=n.server(HOST,PORT)

    while True:
        msg = raw_input("Comando: ")
        if msg in client_commands:
            if msg == "EXIT":
                lserver.close()
                sys.exit()
            print 'Recebi ', lserver.send_receive(msg)
        else:
            "Strange command try again"

else:
    print "Sem argumentos ou argumentos incompletos"