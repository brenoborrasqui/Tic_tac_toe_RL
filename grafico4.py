import pygame

def texto(msg, cor, tam, x, y):

    myfont = pygame.font.SysFont('Roboto', tam)

    texto1 = myfont.render(msg, True, cor)

    tela.blit(texto1, [x, y])

    return texto1


def atualiza_tela(vet_board):

    draw_back(board_bar, size_board_bar, tela)

    atualiza_board(vet_board, posicao, tela, size_p)

    pygame.display.update()


def draw_back(board_bar, size_board_bar, tela):
    global COLOR_WHITE, COLOR_BLACK, COLOR_BACKG, COLOR_LINE, COLOR_X, COLOR_O

    posi_board_bar = [0, 0]

    tela.fill(COLOR_WHITE)
    board_bar.fill(COLOR_BACKG)
    pygame.draw.line(board_bar, COLOR_LINE, (250, 75), (250, 375), 10)
    pygame.draw.line(board_bar, COLOR_LINE, (350, 75), (350, 375), 10)
    pygame.draw.line(board_bar, COLOR_LINE, (150, 175), (450, 175), 10)
    pygame.draw.line(board_bar, COLOR_LINE, (150, 275), (450, 275), 10)
    tela.blit(board_bar, posi_board_bar)

    texto("REINICIAR", COLOR_LINE, 30, 250, 400)


def draw_peca(pos, peca, tela, size_p):
    x, y = pos

    if peca == 1:
        img_o = pygame.image.load("O.jpg")
        img_o = pygame.transform.scale(img_o, (size_p[0] - 35, size_p[1] - 35))
        tela.blit(img_o, ((x - size_p[0] / 2 + 18), (y - size_p[1] / 2 + 18)))

    elif peca == -1:
        img_o = pygame.image.load("X.jpg")
        img_o = pygame.transform.scale(img_o, (size_p[0] - 35, size_p[1] - 35))
        tela.blit(img_o, ((x - size_p[0] / 2 + 18), (y - size_p[1] / 2 + 18)))

    elif peca == 0:
        pass


def atualiza_board(vet_board, posicao, tela, size_p):

    for i in range(9):

        peca = vet_board[i]

        draw_peca(posicao[i], peca, tela, size_p)


def mouse_posicao(rects):

    for event in pygame.event.get():

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_posi = pygame.mouse.get_pos()

        if event.type == pygame.QUIT:
            pygame.quit()

        else:
            for p in rects:
                if event.type == pygame.MOUSEBUTTONDOWN and p.collidepoint(mouse_posi):
                    if p == rect0:
                        return 0
                    if p == rect1:
                        return 1
                    if p == rect2:
                        return 2
                    if p == rect3:
                        return 3
                    if p == rect4:
                        return 4
                    if p == rect5:
                        return 5
                    if p == rect6:
                        return 6
                    if p == rect7:
                        return 7
                    if p == rect8:
                        return 8
                    if p == Butt_1:
                        return -1


def tela_gameover(winner):

    tela.fill(COLOR_BACKG)

    img_o = pygame.image.load("O.jpg")
    img_o = pygame.transform.scale(img_o, (250, 250))
    tela.blit(img_o, ((size_board_bar[0] / 2 - (250 / 2)), (size_board_bar[1] / 2 - (250 / 2))))


def select_player():

    flag = 0x00

    while not flag:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_posi = pygame.mouse.get_pos()
                for d in Bs:
                    if event.type == pygame.MOUSEBUTTONDOWN and d.collidepoint(mouse_posi):
                        if d == B1:
                            return 's'
                            flag = 0x01

                        elif d == B2:
                            return 'n'
                            flag = 0x01


# Variaveis globais
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_BACKG = (20, 189, 172)
COLOR_LINE = (13, 161, 146)

size_board_bar = (600, 450)

size_p = (100, 100)  # define o tamanho da colisão de cada posição
p0 = (200, 125)  # define a primeira posição o retante acompanha
p1 = ((p0[0] + size_p[0]), (p0[1]))
p2 = ((p1[0] + size_p[0]), (p0[1]))
p3 = ((p0[0]), (p0[1] + size_p[1]))
p4 = ((p0[0] + size_p[0]), (p0[1] + size_p[1]))
p5 = ((p1[0] + size_p[0]), (p0[1] + size_p[1]))
p6 = ((p0[0]), (p3[1] + size_p[1]))
p7 = ((p0[0] + size_p[0]), (p3[1] + size_p[1]))
p8 = ((p1[0] + size_p[0]), (p3[1] + size_p[1]))

posicao = [
    p0, p1, p2,
    p3, p4, p5,
    p6, p7, p8
]

# Definindo os objetos de cada posição
rect0 = pygame.Rect(((p0[0] - 50), (p0[1] - 50)), size_p)
rect1 = pygame.Rect(((p1[0] - 50), (p1[1] - 50)), size_p)
rect2 = pygame.Rect(((p2[0] - 50), (p2[1] - 50)), size_p)
rect3 = pygame.Rect(((p3[0] - 50), (p3[1] - 50)), size_p)
rect4 = pygame.Rect(((p4[0] - 50), (p4[1] - 50)), size_p)
rect5 = pygame.Rect(((p5[0] - 50), (p5[1] - 50)), size_p)
rect6 = pygame.Rect(((p6[0] - 50), (p6[1] - 50)), size_p)
rect7 = pygame.Rect(((p7[0] - 50), (p7[1] - 50)), size_p)
rect8 = pygame.Rect(((p8[0] - 50), (p8[1] - 50)), size_p)
Butt_1 = pygame.Rect((250, 400), (100, 20))

# define uma lista para facilitar a identificação do objeto clicado
rects = [
    rect0, rect1, rect2,
    rect3, rect4, rect5,
    rect6, rect7, rect8,
    Butt_1
]

pygame.init()
pygame.font.init()

tela = pygame.display.set_mode([600, 450])
pygame.display.set_caption("Jogo da Velha com IA")
board_bar = pygame.Surface(size_board_bar)

tela.fill(COLOR_BACKG)

texto("DESEJA COMEÇAR JOGANDO?", COLOR_WHITE, 50, 40, 50)

B1 = pygame.Rect((115, 250), (100, 80))
pygame.draw.rect(tela, COLOR_BACKG, (B1))
texto("SIM", COLOR_WHITE, 50, 130, 270)

B2 = pygame.Rect((400, 250), (100, 80))
pygame.draw.rect(tela, COLOR_BACKG, (B2))
texto("NÃO", COLOR_WHITE, 50, 410, 270)

Bs = [B1, B2]

pygame.display.update()
