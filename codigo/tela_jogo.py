from constantes import *  # Você pode usar as constantes definidas em constantes.py, se achar útil
                          # Por exemplo, usar a constante CORACAO é o mesmo que colocar a string '❤'
                          # diretamente no código
import motor_grafico as motor  # Utilize as funções do arquivo motor_grafico.py para desenhar na tela
                               # Por exemplo: motor.preenche_fundo(janela, [0, 0, 0]) preenche o fundo de preto
import random

def desenha_parede(janela, estado, altura_tela, largura_tela):
    mapa = estado["mapa"]
    deltax = (largura_tela - len(mapa[0]))//2
    deltay = (altura_tela - len(mapa))//2
    for parede in estado["paredes"]:
        motor.desenha_string(janela, parede[0] + deltax, parede[1] + deltay, PAREDE, CINZA_ESCURO_AZULADO, CINZA_MUITO_ESCURO_AZULADO)

def desenha_mapa(janela, estado, altura_tela, largura_tela):
    mapa = estado["mapa"]
    deltax = (largura_tela - len(mapa[0]))//2
    deltay = (altura_tela - len(mapa))//2
    for i in range(len(mapa)):
        for j in range(len(mapa[0])):
            if (i + j) % 2 == 0:
                motor.desenha_string(janela, j + deltax, i + deltay, '▯', CINZA_MEDIO_AZULADO, CINZA_ESCURO_AZULADO)
            else:
                motor.desenha_string(janela, j + deltax, i + deltay, '▯', CINZA_CLARO_AZULADO, CINZA_ESCURO_AZULADO)

def desenha_portal(janela, estado, altura_tela, largura_tela):
    mapa = estado["mapa"]
    deltax = (largura_tela - len(mapa[0]))//2
    deltay = (altura_tela - len(mapa))//2
    motor.desenha_string(janela, 1 + deltax, deltay + 10, "░", ROXO2, ROXO)
    motor.desenha_string(janela, 1 + deltax, deltay + 9, "░", ROXO2, ROXO)
    motor.desenha_string(janela, 1 + deltax, deltay + 11, "░", ROXO2, ROXO)

def desenha_tela(janela, estado, altura_tela, largura_tela):
    motor.preenche_fundo(janela, PRETO)
    mapa = estado["mapa"]
    deltax = (largura_tela - len(mapa[0]))//2
    deltay = (altura_tela - len(mapa))//2
    desenha_mapa(janela, estado, altura_tela, largura_tela)
    motor.desenha_string(janela, estado["pos_jogador"][0] + deltax, estado["pos_jogador"][1]+ deltay, JOGADOR, CINZA_ESCURO_AZULADO, BRANCO)
    for objeto in estado["objetos"]:
        motor.desenha_string(janela, objeto["posicao"][0] + deltax, objeto["posicao"][1]+ deltay, objeto["tipo"], CINZA_MEDIO_AZULADO, objeto["cor"])  
    for monstros in estado["monstros"]:
        motor.desenha_string(janela, monstros["posicao"][0] + deltax, monstros["posicao"][1]+ deltay, monstros["tipo"], CINZA_MEDIO_AZULADO, monstros["cor"])
    motor.desenha_string(janela, 0+ deltax, deltay-1, estado["max_vidas"]*'🤍', PRETO, BRANCO)
    motor.desenha_string(janela, 0+ deltax, deltay-1, estado["vidas"]*'🧡', PRETO, VERMELHO)
    desenha_parede(janela, estado, altura_tela, largura_tela)
    motor.desenha_string(janela, 0+ deltax, deltay+len(mapa), estado["mensagem"], PRETO, BRANCO)
    desenha_portal(janela, estado, altura_tela, largura_tela)

def move_jogador(estado, tecla): #funcao feita para que a funcao def atualiza estado nao fique tao grande
    posicaofut = estado["pos_jogador"][:]
    if tecla == "CIMA":
        posicaofut[1] -= 1
    if tecla == "BAIXO":
        posicaofut[1] += 1     
    if tecla == "ESQUERDA":
        posicaofut[0] -= 1
    if tecla == "DIREITA":
        posicaofut[0] += 1
    if posicaofut not in estado["paredes"]:
        estado["pos_jogador"] = posicaofut
        estado['mensagem'] = ''
    else:
        estado["mensagem"] = "bateu na parede"

def colisoes(estado): #funcao feita para que a funcao def atualiza estado nao fique tao grande
    for objeto in estado["objetos"]:
        if estado["pos_jogador"] == objeto["posicao"]:
            if objeto["tipo"] == CORACAO and estado["vidas"]<=4:
                estado["vidas"] += 1
                estado['mensagem'] = 'Ganhou uma vida!'
            if objeto["tipo"] == ESPINHO:
                estado["vidas"] -= 1
                if estado["vidas"] <= 0:
                    #jogador morre e vai pra tela de fim de jogo
                    estado["vidas"] = 5
                    estado["tela_atual"] = TELA_GAMEOVER
                else:
                    estado['mensagem'] = 'Perdeu uma vida, cuidado...'
            estado["objetos"].remove(objeto)

def move_gosma(estado, tecla):
    for monstros in estado["monstros"]:
        posfutura = []
        if monstros["tipo"] == GOSMA:
            if tecla == "CIMA" or tecla == "BAIXO" or tecla == "ESQUERDA" or tecla == "DIREITA":
                x = random.randint(0,1)
                if x == 0:
                    posmonstros2 = monstros["posicao"][0] + random.randint(-1, 1)
                    posfutura.append(posmonstros2)
                    posfutura.append(monstros["posicao"][1])
                else:
                    posmonstros2 = monstros["posicao"][1] + random.randint(-1, 1)
                    posfutura.append(monstros["posicao"][0])
                    posfutura.append(posmonstros2)
                if posfutura not in estado["paredes"]:
                    monstros["posicao"] = posfutura
                            
def atualiza_estado(estado, tecla):
    move_jogador(estado, tecla)
    colisoes(estado)
    move_gosma(estado, tecla)
    portal = [[1,10],[1,11],[1,9]]
    if estado["pos_jogador"] in portal:
        estado["tela_atual"] = TELA_SALA_SECRETA
    if tecla == 'i':
        estado['tela_atual'] = TELA_INVENTARIO
    # Termina o jogo se o jogador apertar ESC ou 'q'
    elif tecla == motor.ESCAPE or tecla =='q':
        estado['tela_atual'] = SAIR
    
