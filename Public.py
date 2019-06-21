import json

class Message:
    """Exemplos de uso:
    ENVIANDO UMA MENSAGEM:

    msg = Message(cmd=Commands.ALGUM_COMANDO, data=ALGUMA_COISA)
    msg_serializada = msg.serialize()
    socket.envia(msg_serializada)

    RECEBENDO UMA MENSAGEM:
    resposta = socket.recebe()
    resposta = Message(0, resposta)

    ATRIBUTOS
    cmd=Comando enviado, todos estao descritos na classe Commands
    data=Lista, String, Tabela Hash, Boolean, Inteiro, etc
    """
    def __init__(self, address='' ,raw_data='', **kwargs):

        # raw_data: mensagem em json vinda do cliente
        # kwargs: dicionario para nova mensagem
        self.address = address

        if raw_data:
            raw_data = raw_data.decode('ascii')
            j = json.loads(raw_data)

            self.cmd = j[0]
            self.data = j[1]

        else:
            # se existir a chave solicitada  (cmd, data)
            # retorna seu valor, caso contrario retorna o valor padrao
            self.cmd = self._get(kwargs, 'cmd', '')
            self.data = self._get(kwargs, 'data', [])


    def _get(self, kwargs, key, defval):
        try:
            return kwargs[key]
        except:
            return defval


    def __bytes__(self):
        return self.serialize()


    def get(self, key):
        return self.data[key]


    def serialize(self):
        # converte em json e codifica em ascii
        return json.dumps((self.cmd, self.data)).encode('ascii')



class Commands:
    """Essa classe tem apenas como funcao ser um dicionario das mensagens
    |       COMANDO    |                   FUNCAO                          |
    |  LOGIN           |  Efetuar o login do SS no SA                      |
    |  START           |  Iniciar a partida e informar as cacas aos SS     |
    |  GET_FLAG        |  Informar que achou uma bandeira                  |
    |  GO_GET_FLAG     |  Ordenar que o Robo va atras de tal bandeira      |
    |  STOP            |  Acabar a partida                                 |
    |  UPDATE_FLAGS    |  Atualizar lista de bandeiras                     |
    |  GET_IP          |  Obter o IP do SS                                 |
    |  CONECT_TO_SS    |  Conectar ao SS                                   |
    |  STATUS          |  Retornar o Status de uma solicitacao             |
    """

    LOGIN = "login"
    MOVE_TO = "move_to"
    START = "start"
    GET_FLAG = "get_flag"
    GO_GET_FLAG = "go_get_flag"
    STOP = "stop"
    CHECK = "check"
    POS = "pos"
    UPDATE_FLAGS = "update"
    UPDATE_MAP = "updatemap"
    INITIAL_POS = "initial"
    QUIT = "q"
    GET_IP = "get_player_ip"
    STATUS = "status"
    STATUS_GET_FLAG = "sgf"
    MASTER = "master"
    PORT_SA = 8888
    PORT_SS = 9999
    CONNECT_TO_SS = "sup"
    GET_ROBOT_POS = "robot_pos"

    ID = "id"
    IP = "ip"

    MODE = "mode"
    MANUAL = True
    AUTOMATICO = False
    DIRECTION = "dir"