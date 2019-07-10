#Projeto Integrador II - IFSC Campus São José
Alunos: Alisson Boeing, Rafael Teles.

Este trabalho foi desenvolvido com o objetivo de executar partidas de caça ao tesouro utilizando robôs Lego Mindstorm EV3. Os quais possuem um sistema operacional Linux. Para o desenvolvimento foi usado a linguagem Python3.

O sistema completo se divide em três, o sistema auditor é responsavel por gerir as partidas, o sistema supervisor faz a interface entre o auditor e o ultimo sistema, o Robô. Abaixo uma descrição de como estes foram desenvolvidos. Os códigos e diagramas de classes e casos de uso, se encontram neste repositório.

##Sistema Auditor
#####Classes:
- **Jogador**: Classe do jogador, contém sua pontuação, socket(dealer), posição, pontuação e IP do SS.
- **Jogo**: Sorteia as cacas, verifica a validade das caças, controla, gerencia o mapa, a posição atual onde está cada robô e a posição para a qual cada robô deverá se deslocar na sua primeira movimentação.
- **Auditor**: É a classe responsável pela comunicação do árbitro com os SS.

Detalhamento deste sistema no [repositório do Grupo 3](https://github.com/SuyKingsleigh/PJI-2.git "Grupo3"), responsável pelo desenvolvimento do Sistema Auditor.

##Sistema Supervisor
#####Classes:
- **Communication**: Classe dedicada a realizar a comunicação entre o SS e o SR, uma instância desta é um Thread que envia ou recebe dados para um dos sistemas, ou seja, cada sistema deve possuir uma instância para receber e outra para enviar. Quando uma mensagem chega, é tratada e enfileirada em uma lista específica daquele tipo de mensagem, para que possa ser lida no sistema da forma correta.
- **Comunica_SA**: Classe responsável pelo tratamento das mensagens entre o SS e o SA, uma instância envia e recebe mensagens e também insere as mensagens em uma fila específica para ser lida pelo sistema.

A interface é realizada pela Interface.py onde nela são instânciados as comunicações e feito a gerência do Sistema Robô, armazenando informações dele e da partida. 

##Sistema Robô
#####Classes:
- **Robô**: Classe do robô em si, possui as instâncias dos motores e dos sensores, possui os atributos dele como posição inicial, posição atual, sentido que está apontado, modo de operação, mover nas quatro direções, mover automático a partir de uma lista de caças. o Robô é uma Thread na qual está sempre aguardando comandos no modo manual ou procurando as caças da lista no modo automático.
- **Treasure**: Classe responsável por gerenciar a lista de caças, e ordená-la da melhor forma conforme a posição atual do robô.
- **Communication**: Mesma classe utilizada no SS.

O arquivo SistemaRobo.py gerencia o robô e as comunicações, ele faz a leitura das listas de mensagens e toma as decisões conforme os requisitos de projeto.


