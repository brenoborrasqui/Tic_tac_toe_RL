"""
Curso de IA - Jogo da velha

Robo que aprende a jogar o Jogo da Velha por RL
"""
import numpy as np
import grafico4


def main():
    """Ambiente"""

    dim = 3  # Dimenssão do tabuleiro
    dim2 = dim * dim

    possibilidades = 3  # quantas formas eu tenho para preencher um espaço do tabuleiro
    empty = 0  # digito 0 na base ternária
    o = 1  # digito 1 na base ternária
    x = -1  # digito 2 na base ternária

    p1 = o
    p2 = x

    Q = 0.4 * np.ones((possibilidades**dim2, dim2))  # Inicializa Tabela Q

    # Parâmetros
    N_episodes = 30000  # Quantidade de vezes que o robo ira jogar

    alpha = 0.5
    gamma = 0.95

    max_epsilon = 1
    min_epsilon = 0
    decay_rate = 0.001
    epsilon = 1

    robo_começar = grafico4.select_player()

    if robo_começar == "s":

        quem_comeca = p2

    elif robo_começar == "n":

        quem_comeca = p1

    if quem_comeca == p2:

        try:
            arquivo = open("tabelaq2.txt", "r")
            Q = puxar_inteligencia(arquivo, possibilidades, dim2, quem_comeca)

        except Exception:
            for episode in range(N_episodes):
                Q = play_one_episode(Q, o, x, epsilon, dim2, empty, alpha, gamma, dim, quem_comeca)

                epsilon = min_epsilon + (max_epsilon - min_epsilon) * np.exp(-decay_rate * episode)

                if episode % 1000 == 0:
                    print(epsilon)

            guardar_inteligencia(Q, dim2, quem_comeca, p1, p2)

    elif quem_comeca == p1:

        try:
            arquivo = open("tabelaq1.txt", "r")
            Q = puxar_inteligencia(arquivo, possibilidades, dim2, quem_comeca)

        except Exception:
            for episode in range(N_episodes):
                Q = play_one_episode(Q, o, x, epsilon, dim2, empty, alpha, gamma, dim, quem_comeca)

                epsilon = min_epsilon + (max_epsilon - min_epsilon) * np.exp(-decay_rate * episode)

                if episode % 1000 == 0:
                    print(epsilon)

            guardar_inteligencia(Q, dim2, quem_comeca, p1, p2)

    while True:
        play_teste(Q, dim2, empty, x, o, dim, quem_comeca)


def play_one_episode(Q, o, x, epsilon, dim2, empty, alpha, gamma, dim, quem_comeca):
    """ Joga uma partida do jogo da velha"""

    vet_board = np.zeros(dim2)

    gameover = False
    p2 = x
    p1 = o
    current_player = []
    recorded_s_a_r = []
    quem_ncomeca = []

    if quem_comeca == p1:
        quem_ncomeca = p2
    elif quem_comeca == p2:
        quem_ncomeca = p1

    state = take_state(dim2, vet_board, empty, o, x)

    while not gameover:
        if current_player == quem_comeca:  # alterna entre os players

            current_player = quem_ncomeca

        else:
            current_player = quem_comeca

        # player atual faz uma jogada
        if current_player == p1:  # robo aprendiz
            action = take_action(Q, state, epsilon, dim2, vet_board, empty)

        else:  # robo com açoes totalmente aleatórias
            action = take_action(Q, state, 1, dim2, vet_board, empty)  # 1 no epsilon pq ele nunca vai pegar experiencias e sempre jogadas aleatorias

        # Preenchimento do tabuleiro
        vet_board[action] = current_player

        # A Partida terminou?
        gameover, winner = game_over(vet_board, dim, x, o)

        # Recebe a recompensa
        reward = get_reward(gameover, winner, p1)

        # Passo para o novo estado
        new_state = take_state(dim2, vet_board, empty, o, x)

        # Geralmente a atualização da tabela Q eh aqui, porem
        # como se trata de um problema de dois agentes, não pode ser aqui

        # Armazenamento da sequencia de state-action-reward do robo aprendiz
        if current_player == p1:
            recorded_s_a_r.append((state, action, reward))

        # Atualização estado
        state = new_state

    maximun = 0

    for s_a_r in reversed(recorded_s_a_r):

        s = s_a_r[0]
        a = s_a_r[1]
        r = s_a_r[2]

        Q[s, a] = (1 - alpha) * Q[s, a] + alpha * (r + gamma * maximun)

        maximun = np.max(Q[s, :])

    return Q


def play_teste(Q, dim2, empty, x, o, dim, quem_comeca):
    """ Função para testar nosso robo"""

    vet_board = np.zeros(dim2)

    gameover = False
    p2 = x
    p1 = o
    current_player = []
    quem_ncomeca = []

    if quem_comeca == p1:
        quem_ncomeca = p2
    elif quem_comeca == p2:
        quem_ncomeca = p1

    state = take_state(dim2, vet_board, empty, o, x)

    draw_board(vet_board)  # desenha o tabuleiro inicial

    while not gameover:
        if current_player == quem_comeca:  # alterna entre os players

            current_player = quem_ncomeca

        else:
            current_player = quem_comeca

        # player atual faz uma jogada
        if current_player == p1:  # robo aprendiz
            action = take_action(Q, state, 0, dim2, vet_board, empty)  # robo utiliza somente das suas experiencias

        else:  # Humano

            nao_liberado = True

            while nao_liberado:

                action = None

                print("Faça sua jogada")

                while action == None:

                    action = grafico4.mouse_posicao(grafico4.rects)

                if action == -1:
                    vet_board = [-1, -1, -1, -1, -1, -1, -1, -1, -1]
                    break

                elif vet_board[action] == empty:
                    nao_liberado = False

        # Preenchimento do tabuleiro
        if action != -1:
            vet_board[action] = current_player
        else:
            pass

        # desenha o novo tabuleiro
        draw_board(vet_board)

        # A Partida terminou?
        gameover, winner = game_over(vet_board, dim, x, o)

        if gameover:
            while action != -1:
                action = grafico4.mouse_posicao(grafico4.rects)

        # Passo para o novo estado
        new_state = take_state(dim2, vet_board, empty, o, x)

        # Atualização estado
        state = new_state


def take_action(Q, state, epsilon, dim2, vet_board, empty):
    """Tomada de decição"""
    r = np.random.rand()  # numero aleatorio entre 0 e 1
    possible_actions = []

    for i in range(dim2):

        if vet_board[i] == empty:

            possible_actions.append(i)

    if r <= epsilon:  # ação aleatória

        n = len(possible_actions)
        index = np.random.choice(n)
        action = possible_actions[index]

        return action

    else:  # uso da experiencias
        Q_vals = Q[state, :]
        Q_possible = [Q_vals[i] for i in possible_actions]  # valores de Q das açoes possiveis
        max_Q_possible = np.max(Q_possible)  # maximo valor de Q dentro das açoes possiveis
        actions_max = [i for i in possible_actions if Q_vals[i] == max_Q_possible]
        action = np.random.choice(actions_max)
        return action


def take_state(dim2, vet_board, empty, o, x):
    """Representação dos Estados possíveis do tabuleiro"""

    somatorio = 0

    for i in range(dim2):
        if vet_board[i] == empty:
            digit = 0
        elif vet_board[i] == o:
            digit = 1
        else:
            digit = 2

        somatorio = somatorio + digit * (3**i)

    state = somatorio
    return state


def get_reward(gameover, winner, p1):
    """Estratégia de Recompensa"""

    if gameover and winner == p1:
        reward = 1
        return reward
    elif gameover and winner == "tie":
        reward = 0.5
        return reward
    else:
        reward = 0
        return reward


def game_over(vet_board, dim, x, o):

    mat_board = np.reshape(vet_board, (dim, dim))

    if np.all((mat_board == -1) == True):  # todos os campos não estão vazios?
        winner = 'desistencia'
        return True, winner

    # verifica linhas e colunas
    for player in (x, o):
        for i in range(dim):
            if mat_board[i, :].sum() == player * dim:  # verifica linhas
                winner = player
                return True, winner

            elif mat_board[:, i].sum() == player * dim:  # verifica colunas
                winner = player
                return True, winner

    # verifica diagonais
    for player in (x, o):
        if np.sum(np.diag(mat_board)) == player * dim:  # diagonal principal
            winner = player
            return True, winner

        elif np.sum(np.diag(np.fliplr(mat_board))) == player * dim:  # diagonal oposta
            winner = player
            return True, winner

    # verifica se deu empate
    if np.all((mat_board == 0) == False):  # todos os campos não estão vazios?
        winner = 'tie'
        return True, winner

    # Jogo ainda não terminou
    winner = None
    return False, winner


def draw_board(vet_board):

    grafico4.atualiza_tela(vet_board)


def guardar_inteligencia(Q, dim2, quem_comeca, p1, p2):
    """Grava um arquivo .txt com a tabela Q e as informações obtidas no treinamento """

    if quem_comeca == p2:

        arquivo = open("tabelaq2.txt", "w")

    elif quem_comeca == p1:

        arquivo = open("tabelaq1.txt", "w")

    for i in Q:

        lista = ""

        for j in range(dim2):

            valor = i[j]

            valor = str(valor)

            if j == (dim2 - 1):
                valor = valor + "\n"
            else:
                valor = valor + " "

            lista = lista + valor

        arquivo.write(lista)

    arquivo.close()


def puxar_inteligencia(arquivo, possibilidades, dim2, quem_comeca):
    """Pega as informações para preencher a tabela Q a partir de um arquivo .txt """

    Q = 0.4 * np.ones((possibilidades**dim2, dim2))

    for i in range(possibilidades**dim2):

        linha_str = arquivo.readline()

        linha_str = linha_str.strip()

        linha_str = linha_str.split()

        for j in range(dim2):

            valor = linha_str[j]

            valor = np.float(valor)

            Q[i, j] = valor

    arquivo.close()

    return Q


main()
