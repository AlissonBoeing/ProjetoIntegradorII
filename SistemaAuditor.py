#!/user/bin/venv
import random
import socket
import sys
from threading import Thread

import zmq
from Public import Message, Commands

global user_input


########################################################################################################################

class Jogador:
    '''Classe Jogador: Representa um jogador
    contem sua pontuacao, socket(dealer), posicao, pontuacao e IP do SS
    '''

    def __init__(self, **kwargs):
        self.id = self._get(kwargs, Commands.ID, None)
        self._socket = self._get(kwargs, 'socket', None)
        self.pos = self._get(kwargs, Commands.INITIAL_POS, None)
        self.ip = self._get(kwargs, Commands.IP, None)
        self.score = 0

    def increase_score(self):
        '''Atualiza a pontuacao do jogador'''
        self.score = self.score + 1

    def _get(self, kwargs, key, defval):
        try:
            return kwargs[key]
        except:
            return defval

    def set_pos(self, coord):
        '''Atualiza/Define a posicao do jogador'''
        self.pos = coord

    def set_ip(self, ip):
        '''Atualiza/Define o IP do jogador'''
        self.ip = ip


########################################################################################################################


class Jogo:
    """
        Classe Responsavel pelo jogo, ou seja:
        >Sorteia as cacas
        >Verifica a validade das cacas
        >Controla
        >gerencia mapa
        >a posição atual onde está cada robô e aposição para a qual cada robô deverá se deslocar na sua primeira movimentação.
        atributo "manual": true se o jogo for manual, false se for automatico, vem por default true
    """

    DIMENSAO = 6  # dimensao do mapa, no NxN
    NUMERO_DE_CACAS = 3  # numero de cacas no mapa

    # jogadores_dict: Dict[zmq.Socket, Jogador]

    def __init__(self):
        # Supondo que o mapa e numero de cacas sejam estaticos.
        self.dimensao = Jogo.DIMENSAO
        self.numero_de_cacas = Jogo.NUMERO_DE_CACAS
        self.manual = True  # Modo de jogo, true se manual, false se automatico

        self.lista_de_cacas = []  # lista das cacas
        self._jogador_pos = dict()  # dicionario da posicao de cada jogador {socket : (coordX, coordY) }
        self.jogadores_dict = dict()

    def set_game_mode(self, mode):
        self.manual = mode

    def sorteia_cacas(self):
        """Sorteia as cacas, retorna uma lista com n cacas, dispostas em tuplas (coordX, coordY)"""
        self.lista_de_cacas = []
        i = 0
        while i != self.numero_de_cacas:
            x, y = random.randint(0, self.dimensao - 1), random.randint(0, self.dimensao - 1)
            if (x, y) not in self.lista_de_cacas:
                self.lista_de_cacas.append((x, y))
                i = i + 1

        return self.lista_de_cacas

    def registra_jogador(self, socket, kwargs):
        """Registra o jogador, caso a ID solicitada JA esteja em uso, retorna falso"""
        id = kwargs[Commands.ID]
        ip = kwargs[Commands.IP]
        pos = kwargs[Commands.INITIAL_POS]
        print("Registra_jogador, id = ", id, " ip= ", ip, "pos= ", pos)
        for player in self.jogadores_dict.values():
            if id == player.id:
                return False
        else:
            self.jogadores_dict[socket] = Jogador(socket=socket, id=id, ip=ip, pos=pos)
            self._jogador_pos[socket] = pos
            return True

    def remove_bandeira(self, cacas):
        """Retorna true e remove da lista de cacas quando a caca eh valida, false caso contrario
         """
        if cacas in self.lista_de_cacas:
            self.lista_de_cacas.remove(cacas)
            return True
        return False

    def move_jogador(self, socket_jogador, coord):
        """Atualiza a posicao do jogador"""
        coord = tuple(coord)
        if coord > (0, 0):
            if coord not in self._jogador_pos.values():
                self._jogador_pos[socket_jogador] = coord
                self.jogadores_dict[socket_jogador].set_pos(coord)
                print("Jogador: ", self.jogadores_dict[socket_jogador].id, " esta indo para ",
                      self.jogadores_dict[socket_jogador].pos)
                return True

        return False

    def stop(self):
        """"Para a partida porem mantem os jogadores cadastrados
            Zera o placar dos jogadores.
        """
        player_score_dict = dict()
        for jogador in self.jogadores_dict.values():
            player_score_dict[jogador.id] = jogador.score
            jogador.score = 0

        return player_score_dict

    def get_player_ip(self, id):
        """Retorna a pontuacao do jogador
        ID = nome do jogador"""
        for player in self.jogadores_dict.values():
            if player.id == id:
                return player.ip

    def update_map(self):
        """Retorna uma lista de posicao, com a posicao de cada jogador, ou seja, apenas as coord ocupadas"""
        pos_list = []
        for jogador in self.jogadores_dict.values(): pos_list.append(jogador.pos)
        return pos_list


########################################################################################################################

class Auditor:
    """
        Classe InterfaceAuditor, eh a classe responsavel pela comunicacao do arbitro com os SS
        Uma thread sera para coisas automaticas do sistema, como atualizacao de mapa e etc
        Publish:
        Socket para o broadcast
        {cmd='start',(x,y)} tamanho do mapa X por Y
        {cmd='cacas', lista de tuplas das cacas} envia a posicao de todas as cacas para os SS cadastrados
        {cmd=obteve_caca, (id_robo, [coorX,coordY]} informa a todos SS cadastrados que algum robo obteve alguma caca
         Router:
         Socket para atender soliticacoes individuais de cada SS, e atende, exclusivamente, a solicitacao de IP do SR.
    """

    def __init__(self, port):
        self.port = port

        # cria os sockets
        self._context = zmq.Context()
        self._publish_socket = self._context.socket(zmq.PUB)
        self._router_socket = self._context.socket(zmq.ROUTER)

        # coisa os sockets
        self._publish_socket.bind("tcp://*:%s" % str(self.port))  # apenas para o broadcast
        self._router_socket.bind("tcp://*:%s" % str(self.port + 1))  # apenas para solicitacoes individuais

        # poller
        self._poller = zmq.Poller()
        self._poller.register(self._router_socket, zmq.POLLIN)  # notifica cada mensagem recebida

        # Jogo
        self.jogo = Jogo()
        self.cacas = []
        self.jogo_started = False
        self.thread_run_flag = True

        self._blocked = True
        # imprime o ip do servidor para facilitar a vida
        print("O ip do servidor eh ", self._get_my_ip(), "\n")

    def _get_my_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        self.my_ip = s.getsockname()[0]
        try:
            s.close()
        except Exception as e:
            pass
        return self.my_ip

    # Processa as requisicoes individuais de cada S.S.
    def _process_request(self, msg):
        print("msg.cmd:  ", msg.cmd)
        # cadastra o S.S
        if msg.cmd == Commands.LOGIN:
            if self.jogo.registra_jogador(msg.address, msg.data):
                print(msg.data)
                info = {'status': 200, 'info': 'logado'}
                self._send_status(info, msg.address)
                print("Login de ", msg.data, " efetuado com sucesso")
            else:
                info = {'status': 400, 'info': 'nao foi possivel logar'}
                self._send_status(info, msg.address)

        # autoriza ou nao o movimento de um jogador
        elif msg.cmd == Commands.MOVE_TO:
            if self.jogo.move_jogador(msg.address, msg.data):
                # info = {'status': 200, 'info': 'OK'}
                # self._send_status(info, msg.address)
                self._update_map()
            else:
                info = {'status': 400, 'info': 'posicao invalida ou ja ocupada'}
                self._send_status(info, msg.address)

        # valida ou nao uma caca, caso seja validada, envia a todos a nova lista de cacas
        # atualiza placar tb
        elif msg.cmd == Commands.GET_FLAG:
            # self._process_flag(msg)
            self._process_flag_thread(msg)

        elif msg.cmd == Commands.GET_IP:
            ip = self.jogo.get_player_ip(msg.data)
            rep = Message(cmd=Commands.GET_IP, data=ip)
            self._router_socket.send_multipart([msg.address, rep.serialize()])
        else:
            pass

    def _process_flag_thread(self, msg):
        print("iniciou a thread pra processar bandeira\n")
        Thread(target=self._process_flag, args=[msg], daemon=False).start()

    def _process_flag(self, msg):
        self._blocked = True
        coord = tuple(msg.data)
        print("get_flag", coord)
        status = 400

        if coord in self.jogo.lista_de_cacas:
            print("a caca eh valida, digite ok pra continuar ")
            while user_input != 'ok': pass  # n faz nada ate o cabra digitar ok
            self.jogo.jogadores_dict[msg.address].increase_score()
            self.jogo.remove_bandeira(coord)
            self._update_flags()
            print("O jogador", self.jogo.jogadores_dict[msg.address].id, "obteve a caca em ", coord,
                  " sua pontuacao eh ", self.jogo.jogadores_dict[msg.address].score)
            status = 200
        else:
            print("caca invalida, digite ok pra continuar")
            while user_input != 'ok': pass

        self._router_socket.send_multipart(
            [msg.address, Message(cmd=Commands.STATUS_GET_FLAG, data=status).serialize()])
        #a = Message(cmd=Commands.STATUS_GET_FLAG, data=status)
        print("status de valida caca enviado")
        #self._publish_socket.send(a.serialize())
        self._blocked = False

    def is_blocked(self):
        return self._blocked


    def _update_map(self):
        msg = Message(cmd=Commands.UPDATE_MAP, data=self.jogo.update_map())
        self._publish_socket.send(msg.serialize())

    def _update_flags(self):
        # atualiza as cacas
        msg = Message(cmd=Commands.UPDATE_FLAGS, data=self.jogo.lista_de_cacas)
        self._publish_socket.send(msg.serialize())
        if self.jogo.lista_de_cacas: print("Bandeiras ", self.jogo.lista_de_cacas)
        else: print("\n\n\n FIM DE JOGO \n\n\n")

    def _send_status(self, info, address):
        resp = Message(cmd=Commands.STATUS, data=info)
        self._router_socket.send_multipart([address, resp.serialize()])

    def inicia_partida(self):
        """Sorteia cacas do jogo, envia a lista das cacas para todos os robos
           Sorteia posicao inicial de cada um, envia a posicao individualmente
           cmd=start
           """
        # self.set_mode(Commands.MANUAL)
        self._sorteia_cacas()
        self.jogo_started = True  # seta a flag de started pra true

    def set_mode(self, mode):
        """Manual = TRUE
           Automatico = False """
        self.jogo.manual = mode
        msg = Message(cmd=Commands.MODE, data=mode)
        self._publish_socket.send(msg.serialize())

        if mode: print("modo manual")
        else: print("modo automatico")

    def _sorteia_cacas(self):
        # Sorteia e envia as bandeiras
        self.cacas = self.jogo.sorteia_cacas()
        print(self.cacas)
        ##msg = Message(cmd=Commands.MODE, data=mode)
        #self._publish_socket.send(msg.serialize())
        #self.cacas = [(0,1),(1,2),(2,3),(3,4),(1,1)]
        msg = Message(cmd=Commands.START, data=self.cacas)
        print("Bandeiras: ", self.cacas)
        self._publish_socket.send(msg.serialize())

    def stop_game(self):
        """Termina a partida, imprime o placar, informa aos supervisores o fim da mesma """
        msg = Message(cmd=Commands.STOP)
        self._publish_socket.send(msg.serialize())
        placar = self.jogo.stop()
        print("o jogo terminou")
        for player in placar:
            print("o jogador ", player, " obteve ", placar[player])

        self.jogo_started = False

    def stop_thread(self):
        """Termina a thread responsavel por lidar com requisicoes dos supervisores"""
        self.thread_run_flag = False
        self.daemon.join(timeout=1)

    # lida com a recepcao de mensagens
    def _handle(self):
        while self.thread_run_flag:
            events = dict(self._poller.poll(timeout=None))  # dicionario = {SOCKET : EVENTO}
            for event in events:
                address, req = self._router_socket.recv_multipart()
                print(req)
                msg = Message(address, req)
                self._process_request(msg)

    def quit(self):
        msg = Message(cmd=Commands.QUIT)
        self._publish_socket.send(msg.serialize())

    def run(self):
        """Inicia a thread para lidar com requisicoes dos supervisores """
        self.daemon = Thread(target=self._handle, name="auditor run")
        self.daemon.daemon = True
        self.daemon.start()


########################################################################################################################

class InterfaceAuditora:
    """Uma interface em modo texto, cuja funcionalidade eh apenas iniciar partidas, terminar partidas e terminar a execucao
    deste mesmo sistema
    """

    def __init__(self, port):
        self.auditor = Auditor(port)
        self.auditor.run()

    def run(self):
        """le a entrada padrao
        start = inicia partida
        stop = termina partida, informa placar, resta placar e prepara-se para uma proxima
        q = finaliza partida (feito pra testes)
        """
        #atributos

        game = 1
        gameStatus = False
        modoAtual = -1


        global user_input
        user_input = ' '
        print("SISTEMA AUDITOR")
        print("Configurar partida " + str(game) + ":")
        print("manual: Para jogo manual")
        print("automatico: Para jogo no modo autônomo")
        print("start: Iniciar a partida")
        print("stop: Terminar a partida atual")
        print("q: Sair do jogo")

        while not user_input == Commands.QUIT:
            user_input = input("> ")
            if user_input == Commands.START:
                if(not gameStatus):
                    if(modoAtual != -1):
                        self.auditor.inicia_partida()
                        self.auditor._update_map()
                        print("Iniciou a partida: " + str(game))
                        gameStatus = True
                    else:
                        print("O modo nao foi configurado!!")
                else:
                    print("Partida " + str(game) + " ainda em andamento.")
            elif user_input == Commands.QUIT:
                self.auditor.stop_game()
                self.auditor.stop_thread()
                self.auditor.quit()
                sys.exit()
            elif user_input == Commands.STOP:
                if(gameStatus):
                    game = game + 1
                    gameStatus = False
                    modoAtual = -1
                    self.auditor.stop_game()
                    print("SISTEMA AUDITOR")
                    print("Configurar partida " + str(game) + ":")
                    print("manual: Para jogo manual")
                    print("automatico: Para jogo no modo autônomo")
                    print("start: Iniciar a partida")
                    print("stop: Terminar a partida atual")
                    print("q: Sair do jogo")
                else:
                    print("Nenhum jogo em andamento")
            elif user_input == "manual":
                if(not gameStatus):
                    modoAtual = True
                    self.auditor.set_mode(Commands.MANUAL)
                else:
                    print("Nao eh possivel alterar com o jogo em andamento")
            elif user_input == "automatico":
                if(not gameStatus):
                    modoAtual = False
                    self.auditor.set_mode(Commands.AUTOMATICO)
                else:
                    print("Nao eh possivel alterar com o jogo em andamento")
            elif user_input == "ok":
                while self.auditor.is_blocked(): pass
                user_input = "kandughojaknjf"
            else:
                pass

        print("Fim")


########################################################################################################################
if __name__ == "__main__":
    joguineo = InterfaceAuditora(Commands.PORT_SA)
    joguineo.run()

