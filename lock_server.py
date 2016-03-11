#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações distribuídas - Projeto 1 - lock_server.py
Grupo:
Números de aluno:
"""

# Zona para fazer importação
import time as t,pickle,sock_utils,sys


###############################################################################

class resource_lock:
    def __init__(self):
        """
        Define e inicializa as características de um LOCK num recurso.
        """
        self.lock_state = False
        self.lock_counter = 0
        self.resource_owner = 0
        self.time_expire = 0

    def lock(self, client_id, time_limit):
        """
        Bloqueia o recurso se este não estiver bloqueado ou mantém o bloqueio
        se o recurso estiver bloqueado pelo cliente client_id. Neste caso renova
        o bloqueio do recurso até time_limit.
        Retorna True se bloqueou o recurso ou False caso contrário.
        """
        if not self.lock_state or client_id==self.resource_owner:
            self.lock_counter += 1
            self.lock_state = True
            self.resource_owner = client_id
            self.time_expire= time_limit
            return True
        return False

    def urelease(self):
        """
        Liberta o recurso incondicionalmente, alterando os valores associados
        ao bloqueio.
        """
        self.lock_state=False
        self.resource_owner=0
        self.time_expire=0


    def release(self, client_id):
        if self.resource_owner==client_id:
            self.lock_state=False
            self.resource_owner=0
            self.time_expire=0
            return True
        return False

    def test(self):
        """
        Retorna o estado de bloqueio do recurso.
        """
        return self.lock_state

    def stat(self):
        """
        Retorna o número de vezes que este recurso já foi bloqueado.
        """
        return self.lock_counter

    def time(self):
        """
        Devolve o tempo limite do recurso
        """
        return self.time_expire

###############################################################################

class lock_pool:
    def __init__(self, N):
        """
        Define um array com um conjunto de locks para N recursos. Os locks podem
        ser manipulados pelos métodos desta classe.
        """
        self.lock_pool_array=[]
        for i in range(N):
            self.lock_pool_array.append(resource_lock())


    def clear_expired_locks(self):
        """
        Verifica se os recursos que estão bloqueados ainda estão dentro do tempo
        de concessão do bloqueio. Liberta os recursos caso o seu tempo de
        concessão tenha expirado.
        """
        for lock in self.lock_pool_array:
            if lock.time()<t.time():
                lock.urelease()


    def lock(self, resource_id, client_id, time_limit):
        """
        Tenta bloquear o recurso resource_id pelo cliente client_id, até ao
        instante time_limit. Retorna True em caso de sucesso e False caso
        contrário.
        """
        return self.lock_pool_array[resource_id].lock(client_id,time_limit)

    def release(self, resource_id, client_id):
        """
        Tenta libertar o recurso resource_id pelo cliente client_id. Retorna
        True em caso de sucesso e False caso contrário.
        """
        return self.lock_pool_array[resource_id].release(client_id)

    def test(self,resource_id):
        """
        Retorna True se o recurso resource_id estiver bloqueado e False caso
        contrário.
        """
        return self.lock_pool_array[resource_id].test()

    def stat(self,resource_id):
        """
        Retorna o número de vezes que o recurso resource_id já foi bloqueado.
        """
        return self.lock_pool_array[resource_id].stat()

    def __repr__(self):
        """
        Representação da classe para a saída standard. A string devolvida por
        esta função é usada, por exemplo, se uma instância da classe for
        passada à função print.
        """
        output=""
        counter=0
        for lock in self.lock_pool_array:
            output+="recurso " + str(counter) + " bloqueado pelo cliente " + str(lock.resource_owner) + "\n"
            counter+=1
        #
        # Acrecentar a output uma linha por cada recurso bloqueado, da forma:
        # recurso <número do recurso> bloqueado pelo cliente <id do cliente> até
        # <instante limite da concessão do bloqueio>
        #
        # Caso o recurso não esteja bloqueado a linha é simplesmente da forma:
        # recurso <número do recurso> desbloqueado
        #
        return output

###############################################################################

# código do programa principal


if(len(sys.argv)>3):
    HOST = ''
    PORT = int(sys.argv[1])
    resource_number=int(sys.argv[2])
    resource_time=int(sys.argv[3])
else:
    HOST = ''
    PORT = 9999
    resource_number=10
    resource_time=10
    print "A utiizar os parametros padrão"
print "Porta: " + str(PORT)
print "Recursos: " + str(resource_number) + " Tempo: " + str(resource_time)
lp = lock_pool(resource_number)
msgcliente = []
ret = []
sock=sock_utils.create_tcp_server_socket(HOST,PORT,1)
while True:
    (conn_sock, addr) = sock.accept()
    print 'ligado a %s', addr
    try:
        msg = sock_utils.receive_all(conn_sock,1024)
        msg_unp = pickle.loads(msg)
        print 'recebi %s' % msg_unp
        msg_unp[1]=int(msg_unp[1])
        if(len(msg_unp)>2):
            msg_unp[2]=int(msg_unp[2])
            msg_unp[1]=int(msg_unp[1])

        if msg_unp[1] > len(lp.lock_pool_array):
                msg_pronta_enviar = 'UNKNOWN RESOURCE'
        else:
            lp.clear_expired_locks()
            if(msg_unp[0] == 'LOCK'):
                if lp.lock(msg_unp[1], msg_unp[2], t.time() + resource_time):
                    msg_pronta_enviar = 'OK'
                else:
                    msg_pronta_enviar = 'NOK'

            elif(msg_unp[0] == 'RELEASE'):
                if lp.release(msg_unp[1], msg_unp[2]):
                    msg_pronta_enviar = 'OK'
                else:
                    msg_pronta_enviar = 'NOK'

            elif(msg_unp[0] == 'TEST'):
                if lp.test(msg_unp[1]):
                    msg_pronta_enviar = 'LOCKED'
                else:
                    msg_pronta_enviar = 'UNLOCKED'

            elif(msg_unp[0] == 'STATS'):
                msg_pronta_enviar = lp.stat(msg_unp[1])

            else:
                print "ERROR ERROR ERROR ABORT ABORT ABORT :D"
                msg_pronta_enviar = "cant do op"

        msg_pronta_enviar = pickle.dumps(msg_pronta_enviar,-1)
        conn_sock.sendall(msg_pronta_enviar)
        conn_sock.close()
    except:
        print "Unexpected error:", sys.exc_info()[0]
        conn_sock.close()
sock.close()
