import sys,sock_utils
store={}
i=0
resposta=" "
if(len(sys.argv)>1):
    HOST = ''
    PORT = int(sys.argv[1])
    listerner_sock = sock_utils.create_tcp_server_socket(HOST,PORT,1)
    while True:
        (conn_sock, addr) = listerner_sock.accept()
        comando = sock_utils.receive_all(conn_sock, 1024)
        if(comando.split(" ")[0]== "GET"):
            resposta=store[int(comando.split(" ")[1])]
        if(comando.split(" ")[0]== "LIST"):
            resposta=str(store.items())
        if(comando.split(" ")[0]== "ADD"):
            store[i]=comando.split(" ")[1]
            i+=1
            resposta="Adicionado"
        if(comando.split(" ")[0]== "REMOVE"):
            store.pop(int(comando.split(" ")[1]))
            resposta="Removido"
        print 'recebi ',  comando
        conn_sock.sendall(resposta)
        conn_sock.close()
else:
    print "Sem argumentos"