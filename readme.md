Projeto de Aplicações Distribuidas do grupo 025

------------------ Primeira Entrega ------------------

Só temos uma nota em questão a esta parte do projeto.

No enunciado, na lista de comandos, no comando LOCK e RELEASE o argumento client_id vêm em primeiro lugar em relação à
ordem da mensagem. Nós decidimos alterar isto para simplificar a implementação do LOCK_SERVER.
Passou a ser:

LOCK resource_id client_id
RELEASE resource_id client_id
TEST resource_id
STATS resource_id