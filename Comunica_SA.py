import socket
from threading import Thread
from Public import *
import zmq
# from src.Public import Commands

class Comunica_SA:
    def __init__(self, port, ip):
        super().__init__()
        self.daemon = True

        #self.receiveList = list()
        self.map_list = list() #mapa de jogadores
        self.flags_list = list() #mapa de cacas
        self.commands_list = list() # comandos start stop e mode

        self.port = port
        self.servers_ip = ip
        self.my_ip = self._get_my_ip()
        self.id = id
        self._thread_run_flag = True  # flag que permite a execucao da thread

        # criacao dos sockets, dealer_socket manda mensagens para o servidor
        # sub_socket recebe mensagens do servidor (mensagens as quais sao enviadas para todos os clientes)
        self.context = zmq.Context()
        self.dealer_socket = self.context.socket(zmq.DEALER)
        self._sub_socket = self.context.socket(zmq.SUB)


        # inscreve para todos os topicos
        self._sub_socket.setsockopt(zmq.SUBSCRIBE, b"")
        self._sub_socket.setsockopt(zmq.LINGER, 0)

        # conecta os sockets
        self._sub_socket.connect("tcp://%s:%d" % (self.servers_ip, port))
        self.dealer_socket.connect("tcp://%s:%d" % (self.servers_ip, self.port + 1))


    def _get_my_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        self.my_ip = s.getsockname()[0]
        print("IP do Supervisor", self.my_ip)
        try:
            s.close()
        except Exception as e:
            pass
        return self.my_ip

    def login(self, id, posicao):
        '''Metodo  para o Login no jogo, envia a ID do robo
            id = nome do robo, STRING
            posicao = posicao do robo, (coordX, coordY)
        '''
        dados = {
            Commands.ID: id,
            Commands.IP: self.my_ip,
            Commands.INITIAL_POS: posicao
        }
        req = Message(cmd=Commands.LOGIN, data=dados)
        self.dealer_socket.send(req.serialize())
        self._read_rep()

    def _read_rep(self):
        resp = self.dealer_socket.recv()
        resp = Message(0, resp)
        print("status: ", resp.data[Commands.STATUS], "\ninfo: ", resp.data['info'])
        return resp.data[Commands.STATUS]

    def try_move(self, coord):
        """
        informa ao supervisor que ta indo pra coord
        coord = (coordX, coordY)
        """
        req = Message(cmd=Commands.MOVE_TO, data=coord)
        self.dealer_socket.send(req.serialize())

    def get_flag(self, coord):
        """
        Envia mensagem que obteve uma bandeira
        coord = (coordX, coordY) tupla de inteiros"""
        req = Message(cmd=Commands.GET_FLAG, data=coord)
        self.dealer_socket.send(req.serialize())

    def _recv(self):
        print("iniciou a thread")
        while True:
            ans = self._sub_socket.recv()
            rep = Message(0, ans)
            self._process_broadcast_messages(rep)



    def _process_broadcast_messages(self, msg):
        print("Comando recebido : ", msg.cmd, "\nDados: ", msg.data)
        # Processa Mensagens vindas do socket subscribe
        # nem todas as mensagens terao resposta
        #self.receiveList.append(msg)

        if msg.cmd == Commands.START:
            # recebe a lista de cacas
            # so recebe essa mensagem uma vez, que eh no inicio da partida
           # self.receiveList.append(msg)

            self.commands_list.append(msg.cmd)
            self.flags_list.append(msg.data)

            lista_de_cacas = msg.data
            print("lista de cacas ", lista_de_cacas)

        elif msg.cmd == Commands.UPDATE_MAP:
            # recebe uma lista com a posicao de cada jogador
            # toda vez q um jogador se mexer, essa lista sera atualizada
            self.map_list.append(msg.data)
            mapa_atualizado = msg.data
            print("mapa atualizado", mapa_atualizado)

        elif msg.cmd == Commands.UPDATE_FLAGS:
            # recebe a lista de bandeiras atualizadas
            # toda vez que alguem obter uma bandeira, essa lista sera atualizada
            self.flags_list.append(msg.data)
            self.lista_de_cacas = msg.data
            print("lista de cacas ", self.lista_de_cacas)

        elif msg.cmd == Commands.MODE:
            # recebe o modo de jogo
            # modo_de_jogo eh true se for manual
            # modo_de_jogo eh false se for automatico
            # quem define o modo de jogo eh o arbitro
            #self.commands_list.append(msg.data)
            modo_de_jogo = msg.data
            if modo_de_jogo:
                print("manual\n")
                self.commands_list.append("manual")
            else:
                print("automatico\n")
                self.commands_list.append("automatico")

        elif msg.cmd == Commands.STOP:
            # metodo para parar a partida
            # nao tem dados
            self.commands_list.append(msg.cmd)
            print("PARAR O JOGO")
            pass
        else:
            pass

    def run(self):
        '''Inicia a Thread, a qual ira tratar todas as mensagens Broadcast  do servidor '''
        self.daemon = Thread(target=self._recv, name="recebe_mensagens")
        self.daemon.daemon = False
        self.daemon.start()

    def get_map_list(self):
        return self.map_list# mapa de jogadores
    def get_flags_list(self): # mapa de cacas
        return self.flags_list
    def get_commands_list(self):
        return self.commands_list

    def pop_map_list(self):
        return self.map_list.pop()
    def pop_flags_list(self):
        return self.flags_list.pop()
    def pop_commands_list(self):
        return self.commands_list.pop()


# if __name__ == "__main__":
#
#     # cria objeto e inicia thread
#     com = Comunica_SA(Commands.PORT_SA, "localhost")
#     com.run()
#
#
#     # testa login
#     com.login("ID de teste", (-1,-1)) # id do robo e posicao inicial
#     # tem que da o start no auditor para que ele envie a lista de cacas
#     # dai eh so digitar uma caca da lista pra testar
#     # vai ficar meio bugado pq vai ter duas threads escrevendo no mesmo terminal
#     coord = int(input("\nX: ")), int(input("Y: "))
#     com.get_flag(coord)
#
#     # testa mover
#     com.try_move((0,2))
